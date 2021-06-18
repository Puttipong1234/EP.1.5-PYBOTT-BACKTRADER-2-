from __future__ import (absolute_import ,
                        division , 
                        print_function , 
                        unicode_literals)

import argparse
import backtrader as bt
from datetime import datetime

import config , csv , os
from binance.client import Client

#initialize 
client = Client(config.BINANCE_API_KEY , config.BINANCE_API_SECRET)

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Welcome To Backtesting App'
        )
    )

    # integer
    parser.add_argument("--maFast",default='20',required=False,
                        help='Please Define maFast recommend(10 ~ 30) ',
                        metavar='integer')
    
    parser.add_argument("--maSlow",default='45',required=False,
                        help='Please Define maFast recommend(20 ~ 50) ',
                        metavar='integer')
    
    parser.add_argument("--PT",default='10',required=True,
                        help='Please Define Trailstop Percentage recommend(2 ~ 30) ',
                        metavar='integer')
    
    # boolean args
    parser.add_argument("--plot",default='',required=False,
                        help='If you want to Plot ',
                        metavar='kwargs',
                        nargs='?',
                        const="{}")
    
    # string args
    parser.add_argument("--symbol",default='',required=True,
                        help='Please Define pair - symbol ',
                        metavar='string')
    
    
    return parser.parse_args(pargs)


def get_symbol_data(symbol):
    #Collect Data from Binance
    print("Collecting {} Data From Binance".format(symbol))
    candlesticks = client.get_historical_klines(symbol,
                                                Client.KLINE_INTERVAL_1DAY,
                                                "1 Feb, 2018",
                                                "1 Jun, 2021")

    print("Writing {} Data to CSV".format(symbol))

    if os.path.isfile("data.csv"):
        os.remove("data.csv")

    csvfile = open("data.csv","w",newline='')
    writer = csv.writer(csvfile,delimiter=',')

    for candlestick in candlesticks:
        candlestick[0] = str(float(candlestick[0])/1000) # change time stamp format 
        writer.writerow(candlestick)

    csvfile.close()
    return True


class TrailStrategy(bt.Strategy):

    params = (
        ("maFast",20),
        ("maSlow",45),
        ("percTrail",20),
    )

    def __init__(self):
        ma1 = bt.ind.EMA(period=self.p.maFast)
        ma2 = bt.ind.EMA(period=self.p.maSlow)
        self.cross = bt.ind.CrossOver(ma1,ma2) # 1 , -1

        self.long_tr_order = None
        self.short_tr_order = None

        self.startcash = self.broker.getvalue()
    
    def stop(self):
        pnl = round(self.broker.getvalue() - self.startcash,2)
        print("FINAL PnL : {}".format(pnl))

    def next(self):
        amount = self.broker.getvalue()/self.data.close[0]
        #check 1
        if not self.position:
            if self.cross > 0: # cross over?
                self.buy(size=amount)
                self.long_tr_order = None
            
            elif self.cross < 0:
                self.sell(size=amount)
                self.short_tr_order = None
        
        elif self.position:
            if self.position.size > 0 and self.cross < 0: # force close long > open short
                self.close()
                self.cancel(self.long_tr_order)
                self.sell(size=amount)
                self.short_tr_order = None
            
            elif self.position.size < 0 and self.cross > 0: # force close short > open long
                self.close()
                self.cancel(self.short_tr_order)
                self.buy(size=amount)
                self.long_tr_order = None

        
        #check2 has position but no order yet
        if self.long_tr_order is None and self.position.size > 0:
           self.long_tr_order = self.sell(
               exectype=bt.Order.StopTrail,
               trailpercent= self.p.percTrail/100
            )
        
        elif self.short_tr_order is None and self.position.size < 0:
            self.short_tr_order = self.buy(
                exectype=bt.Order.StopTrail,
                trailpercent= self.p.percTrail/100
            )


def run(args=None):

    args = parse_args(args)

    cerebro = bt.Cerebro()

    finish = get_symbol_data(symbol=args.symbol)

    if not finish:
        print("Unable to get symbol {} data".format(args.symbol))
        return

    fromdate = datetime.strptime('2018-02-01','%Y-%m-%d')
    todate = datetime.strptime('2021-06-01','%Y-%m-%d')
    data = bt.feeds.GenericCSVData(dataname='data.csv',
                                    dtformat=2,
                                    compression=1,
                                    timeframe=bt.TimeFrame.Days,
                                    fromdate=fromdate,
                                    todate = todate)

    cerebro.adddata(data)

    cerebro.addstrategy(TrailStrategy , maFast = int(args.maFast) ,
                                        maSlow = int(args.maSlow) ,
                                        percTrail = float(args.PT))
    # add analyzers
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name="AnnualReturn")
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="DrawDown")
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="TradeAnalyzer")
    cerebro.addanalyzer(bt.analyzers.Calmar, _name="Calmar")

    cerebro.broker.setcash(100000)

    result = cerebro.run()
    stat = result[0]

    import pprint

    print("===== Your AnnualReturn =====")
    pprint.pprint(stat.analyzers.AnnualReturn.get_analysis())
    print("============================= \n")

    print("===== Your DrawDown =====")
    pprint.pprint(stat.analyzers.DrawDown.get_analysis())
    print("============================= \n")

    print("===== Your TradeAnalyzer =====")
    pprint.pprint(stat.analyzers.TradeAnalyzer.get_analysis())
    print("============================= \n")

    # print("===== Your Calmar =====")
    # pprint.pprint(stat.analyzers.Calmar.get_analysis())
    # print("=============================")

    if args.plot:
        cerebro.plot()

if __name__ == '__main__':
    run()