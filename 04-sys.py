import datetime

import backtrader as bt


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
