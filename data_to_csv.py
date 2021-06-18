import config , csv , os
from binance.client import Client

#initialize 
client = Client(config.BINANCE_API_KEY , config.BINANCE_API_SECRET)

#Collect Data from Binance
print("Collecting Data From Binance")
candlesticks = client.get_historical_klines("BTCUSDT",
                                            Client.KLINE_INTERVAL_1DAY,
                                            "1 Feb, 2018",
                                            "1 Jun, 2021")

print("Writing Data to CSV")
csvfile = open("data.csv","w",newline='')
writer = csv.writer(csvfile,delimiter=',')

for candlestick in candlesticks:
    candlestick[0] = str(float(candlestick[0])/1000) # change time stamp format 
    writer.writerow(candlestick)

csvfile.close()