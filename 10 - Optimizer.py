import datetime

import backtrader as bt


class PriceMACross(bt.Strategy):
    """Пересечение цены и SMA"""
    params = (
        ('SMAPeriod', 26),
        ('PrintLog', False),
    )

    def log(self, txt, dt=None, doprint=False):
        """Вывод строки с датой на консоль"""
        if self.params.PrintLog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')

    def __init__(self):
        """Инициализация торговой системы"""
        self.DataClose = self.datas[0].close
        self.Order = None  # Заявка
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.SMAPeriod)

    def notify_order(self, order):
        """Изменение статуса заявки"""
        if order.status in [order.Submitted,
                            order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'Bought @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
            elif order.issell():
                self.log(
                    f'Sold @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
        elif order.status in [order.Canceled, order.Margin,
                              order.Rejected]:
            self.log('Canceled/Margin/Rejected')
        self.Order = None

    def notify_trade(self, trade):
        """Изменение статуса позиции"""
        if not trade.isclosed:
            return

        self.log(f'Trade Profit, Gross={trade.pnl:.2f}, NET={trade.pnlcomm:.2f}')

    def next(self):
        """Получение следующего бара"""
        self.log(f'Close={self.DataClose[0]:.2f}')
        if self.Order:
            return

        if not self.position:
            isSignalBuy = self.DataClose[0] > self.sma[0]
            if isSignalBuy:
                self.log('Buy Market')
                self.Order = self.buy()
        else:  # Если позиция есть
            isSignalSell = self.DataClose[0] < self.sma[0]
            if isSignalSell:
                self.log('Sell Market')
                self.Order = self.sell()

    def stop(self):
        """Окончание запуска торговой системы"""
        self.log(f'SMA({self.params.SMAPeriod}), Конечный капитал: {self.broker.getvalue():.2f}', doprint=True)


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.optstrategy(PriceMACross, SMAPeriod=range(8, 65))
    # Торговая система на оптимизацию с параметрами. Первое значение входит, последнее - нет
    data = bt.feeds.YahooFinanceCSVData(
        dataname='AAPL.csv',
        fromdate=datetime.datetime(2020, 4, 1),
        todate=datetime.datetime(2021, 3, 1))

    cerebro.adddata(data)
    cerebro.broker.setcash(1000000)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)  # Кол-во акций для покупки/продажи
    cerebro.broker.setcommission(commission=0.001)  # Комиссия брокера 0.1% от суммы каждой исполненной заявки
    cerebro.run()  # Запуск торговой системы. Можно указать кол-во ядер процессора, которые будут загружены. Например, maxcpus=2
