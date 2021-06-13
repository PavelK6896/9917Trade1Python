import datetime

import backtrader as bt


class BuyAndHoldPullback(bt.Strategy):
    """Покупка и удержание на откате"""

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[0].datetime[0]).date() if dt is None else dt  # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y")}, {txt}')  # Выводим дату с заданным текстом на консоль

    def __init__(self):
        """Инициализация торговой системы"""
        self.DataClose = self.datas[0].close

    def next(self):
        """Получение следующего бара"""
        self.log(f'Close={self.DataClose[0]:.2f}')
        isSignalBuy = self.DataClose[0] < self.DataClose[-1] < self.DataClose[-2]  # Цена падает 2 сессии подряд
        if isSignalBuy:  # Если пришла заявка на покупку
            self.log('Buy Market')
            self.buy()  # Заявка на покупку одной акции по рыночной цене


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(BuyAndHoldPullback)  # Привязываем торговую систему
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
