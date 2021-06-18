import backtrader as bt
from datetime import datetime

class ENGULFStrategy(bt.Strategy):

    params = (
        ("TP",20),
        ("SL",10)
    )

    def __init__(self):
        self.ENGULF = bt.talib.CDLENGULFING(
            self.data.open , self.data.high , self.data.low , self.data.close
        )

        self.startcash = self.broker.getvalue()

        self.long = list()
        self.short = list()
    
    def stop(self):
        pnl = round(self.broker.getvalue() - self.startcash,2)
        print("FINAL PnL : {}".format(pnl))
    
    def next(self):

        long_tp = self.data.close[0] * (1 + self.p.TP/100)
        long_sl = self.data.close[0] * (1 - self.p.SL/100)

        short_tp = self.data.close[0] * (1 - self.p.TP/100)
        short_sl = self.data.close[0] * (1 + self.p.SL/100)

        if not self.position:
            if self.ENGULF == 100: # bullish
                self.long = self.buy_bracket(
                    limitprice=long_tp,
                    stopprice=long_sl,
                    exectype=bt.Order.Market
                )
                print("OPEN LONG POSITION WITH TP SL")
            
            elif self.ENGULF == -100: # bearish
                self.short = self.sell_bracket(
                    limitprice=short_tp,
                    stopprice=short_sl,
                    exectype=bt.Order.Market
                )
                print("OPEN SHORT POSITION WITH TP SL")

        elif self.long and self.ENGULF == -100: # bearish
            self.close()
            print("CLOSE LONG POSITION")
            for o in self.long:
                self.cancel(o)
            print("CLOSE EXIST ORDER")
            self.long = []
            print("CLEAR LONG POSITION")
        
        elif self.short and self.ENGULF == 100: # bullish
            self.close()
            print("CLOSE SHORT POSITION")
            for o in self.short:
                self.cancel(o)
            print("CLOSE EXIST ORDER")
            self.short = []
            print("CLEAR SHORT POSITION")

cerebro = bt.Cerebro()

fromdate = datetime.strptime('2018-02-01','%Y-%m-%d')
todate = datetime.strptime('2021-06-01','%Y-%m-%d')
data = bt.feeds.GenericCSVData(dataname='data.csv',
                                dtformat=2,
                                compression=1,
                                timeframe=bt.TimeFrame.Days,
                                fromdate=fromdate,
                                todate = todate)

cerebro.adddata(data)

cerebro.addstrategy(ENGULFStrategy , TP = 40 , SL = 20)

cerebro.broker.setcash(100000)

if __name__ == '__main__':

    cerebro.run()
    cerebro.plot()