import backtrader as bt
from datetime import datetime

class firstStrategy(bt.Strategy):

    params = (
        ("OB",70),
        ("OS",30)
    )
    
    def __init__(self):
        self.startcash = self.broker.getvalue()
        self.rsi = bt.indicators.RSI_SMA(self.data.close , period=21)
    
    def next(self):

        amount = float(self.broker.getvalue()/self.data.close)

        if not self.position:
            if self.rsi < self.p.OS:
                self.buy(size=amount)
            
        else:
            if self.rsi > self.p.OB:
                self.close() # self.position.size
    
    def stop(self):
        pnl = round(self.broker.getvalue() - self.startcash,2)
        print("@OB{} @OS{} FINAL PnL : {}".format(self.p.OB,self.p.OS,pnl))


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

cerebro.addstrategy(firstStrategy , OB = 85 , OS = 40)
# cerebro.optstrategy(firstStrategy,OB = range(60,90,5),OS = range(20,50,5))

cerebro.broker.setcash(100000)

if __name__ == '__main__':

    cerebro.run()
    cerebro.plot()