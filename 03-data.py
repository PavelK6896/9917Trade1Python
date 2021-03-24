import datetime

import backtrader as bt

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    data = bt.feeds.YahooFinanceCSVData(
        dataname='AAPL.csv',
        fromdate=datetime.datetime(2020, 4, 1),
        todate=datetime.datetime(2021, 3, 1))
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
