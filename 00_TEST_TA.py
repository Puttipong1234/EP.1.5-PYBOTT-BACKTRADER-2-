import numpy
import talib
import matplotlib
import matplotlib.pyplot as plt
from numpy import genfromtxt

data = genfromtxt("data.csv",delimiter=",")

# DATA NORMALIZATION
_open = data[:,1]
_high = data[:,2]
_low = data[:,3]
_close = data[:,4]

# CREATE SOME TECHNICAL PATTERN ANALYSIS
res = talib.CDLENGULFING(_open, _high, _low, _close)

bullishEngulfing = []
bearishEngulfing = []

for index , i in enumerate(list(res)):
    if i == 100:
        bullishEngulfing.append(index)
    
    elif i == -100:
        bearishEngulfing.append(index)

print(bullishEngulfing)
print(bearishEngulfing)

# Create plot
fig = plt.figure()
axes = fig.add_axes([0.1,0.1,0.8,0.8])
axes.set_xlabel("1 Day - Timeframe")
axes.set_ylabel("PRICE")
axes.set_title("BTCUSDT")

# plot close price
plt.plot(_close,color="blue")

#plot bullEng , BearEng
plt.plot( bullishEngulfing , _close[bullishEngulfing] , "." , color="green" )
plt.plot(bearishEngulfing , _close[bearishEngulfing] , "." , color = "red")

# add legend
plt.legend(loc="upper left")
plt.show()