import datetime

import backtrader as bt


class MyCSVData(bt.feeds.GenericCSVData):
    def _loadline(self, linetokens):
        itoken = iter(linetokens)
        dttxt = next(itoken)
        y = int(dttxt[0:4])
        m = int(dttxt[4:6])
        d = int(dttxt[6:8])
        timee = next(itoken)
        h = int(timee[0:2])
        mi = int(timee[2:4])
        se = int(timee[4:6])

        dt = datetime.datetime(y, m, d, hour=h, minute=mi, second=se)
        dtnum = bt.date2num(dt)

        self.lines.datetime[0] = dtnum
        self.lines.open[0] = float(next(itoken))
        self.lines.high[0] = float(next(itoken))
        self.lines.low[0] = float(next(itoken))
        self.lines.close[0] = float(next(itoken))
        self.lines.volume[0] = float(next(itoken))
        self.lines.openinterest[0] = 0
        return True


class Test(bt.Strategy):
    def next(self):
        print(bt.num2date(self.data.datetime[0]), self.data.close[0])


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(Test)
    data0 = MyCSVData(
        dataname='BSN.txt',
        timeframe=bt.TimeFrame.Minutes,
        compression=10,
        separator=',',
    )

    cerebro.adddata(data0)
    cerebro.broker.setcash(100000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
