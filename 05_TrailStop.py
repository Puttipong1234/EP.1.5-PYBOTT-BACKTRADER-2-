import backtrader as bt
from datetime import datetime

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

        #check 1
        if not self.position:
            if self.cross > 0: # cross over?
                self.buy()
                self.long_tr_order = None
            
            elif self.cross < 0:
                self.sell()
                self.short_tr_order = None
        
        elif self.position:
            if self.position.size > 0 and self.cross < 0: # force close long > open short
                self.close()
                self.cancel(self.long_tr_order)
                self.sell()
                self.short_tr_order = None
            
            elif self.position.size < 0 and self.cross > 0: # force close short > open long
                self.close()
                self.cancel(self.short_tr_order)
                self.buy()
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

cerebro.addstrategy(TrailStrategy)

cerebro.broker.setcash(100000)

if __name__ == '__main__':

    cerebro.run()
    cerebro.plot()