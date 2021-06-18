import backtrader as bt
from datetime import datetime

class ENGULFStrategy(bt.Strategy):

    def __init__(self):
        self.ENGULF = bt.talib.CDLENGULFING(
            self.data.open , self.data.high , self.data.low , self.data.close
        )

        self.startcash = self.broker.getvalue()

        self.long = None
        self.short = None
    
    def stop(self):
        pnl = round(self.broker.getvalue() - self.startcash,2)
        print("FINAL PnL : {}".format(pnl))
    
    def next(self):

        if not self.position:
            if self.ENGULF == 100: # bullish
                self.buy(size=1)
                self.long = True
            
            elif self.ENGULF == -100: # bearish
                self.sell(size=1)
                self.short = True

        elif self.long and self.ENGULF == -100: # bearish
            self.close()
            self.long = False
            self.sell(size=1)
            self.short = True
        
        elif self.short and self.ENGULF == +100: # bullish
            self.close()
            self.short = False
            self.buy(size=1)
            self.long = True

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

cerebro.addstrategy(ENGULFStrategy)

cerebro.broker.setcash(100000)

if __name__ == '__main__':

    cerebro.run()
    cerebro.plot()