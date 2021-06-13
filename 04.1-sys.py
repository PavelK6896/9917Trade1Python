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


class ShowBarPriceVolume(bt.Strategy):
    """Простейшая система без торговли. При приходе нового бара отображает его цены/объем"""

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[0].datetime[0]).date() if dt is None else dt  # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y")}, {txt}')  # Выводим дату с заданным текстом на консоль

    def __init__(self):
        """Инициализация торговой системы"""
        self.DataOpen = self.datas[0].open
        self.DataHigh = self.datas[0].high
        self.DataLow = self.datas[0].low
        self.DataClose = self.datas[0].close
        self.DataVolume = self.datas[0].volume

    def next(self):
        """Получение следующего бара"""
        self.log(
            f'Open={self.DataOpen[0]:.2f}, High={self.DataHigh[0]:.2f}, Low={self.DataLow[0]:.2f}, Close={self.DataClose[0]:.2f}, Volume={self.DataVolume[0]:.0f}')


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(ShowBarPriceVolume)  # Привязываем торговую систему
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
