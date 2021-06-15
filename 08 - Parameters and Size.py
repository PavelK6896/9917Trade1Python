import datetime

import backtrader as bt


class PullbackBaySellParam(bt.Strategy):
    """Покупка на откате, удержание N баров с комиссией"""
    params = (
        ('ExitBars', 5),
    )

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[0].datetime[0]).date() if dt is None else dt
        print(f'{dt.strftime("%d.%m.%Y")}, {txt}')

    def __init__(self):
        """Инициализация торговой системы"""
        self.DataClose = self.datas[0].close
        self.Order = None  # Заявка
        self.BarExecuted = None

    def notify_order(self, order):
        """Изменение статуса заявки"""
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'Bought @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
            elif order.issell():
                self.log(
                    f'Sold @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
            self.BarExecuted = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
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
            isSignalBuy = self.DataClose[0] < self.DataClose[-1] < self.DataClose[-2]
            if isSignalBuy:
                self.log('Buy Market')
                self.Order = self.buy()
        else:
            isSignalSell = len(self) - self.BarExecuted >= self.params.ExitBars
            if isSignalSell:
                self.log('Sell Market')
                self.Order = self.sell()


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(PullbackBaySellParam, ExitBars=3)
    data = bt.feeds.YahooFinanceCSVData(
        dataname='AAPL.csv',
        fromdate=datetime.datetime(2020, 4, 1),
        todate=datetime.datetime(2021, 3, 1))

    cerebro.adddata(data)
    cerebro.broker.setcash(1000000)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.001)
    print(f'Старовый капитал: {cerebro.broker.getvalue():.2f}')
    cerebro.run()
    print(f'Конечный капитал: {cerebro.broker.getvalue():.2f}')
    cerebro.plot()
