# -*- coding: utf-8 -*-

from time import sleep
import easytrader
import easytrader.exceptions
from pywinauto.application import Application
from easytrader import refresh_strategies
from easytrader import grid_strategies



class Ths:
    def __init__(self):
        self.appName = r'C:\ths\thsmn\xiadan.exe'


    def startApp(self):
        self.user = easytrader.use('ths')

        self.user.enable_type_keys_for_editor()
        self.user.connect(self.appName)
        # self.app = Application().start(self.appName)
        # self.user.grid_strategy = grid_strategies.Xls


    def buy(self, id, price, count):
        try:
            code = str(id)
            if len(code) != 6:
                raise Exception
        except:
            print('股票代码错误!')
            return 0

        try:
            result = self.user.buy(code, price, count)
            print(result)
        except easytrader.exceptions.TradeError as e:
            print('\n\n 错误：', e)


    def sell(self, id, price, count):
        try:
            code = str(id)
            if len(code) != 6:
                raise Exception
        except:
            print('股票代码错误!')
            return 0

        try:
            result = self.user.sell(code, price, count)

            print(result)
        except easytrader.exceptions.TradeError as e:
            print('\n\n 错误：', e)


    # 获取资金状况
    def getBalance(self):
        return self.user.balance


    #  获取持仓
    def getPosition(self):
        return self.user.position


    # 查询当日成交
    def getTodayTrades(self):
        return self.user.today_trades


    # 查询当日委托
    def getTodayEntrusts(self):
        return self.user.today_entrusts


    # 刷新数据
    def refresh(self):
        self.user.refresh()


if __name__ == '__main__':
    id = 600028
    buyPrice = 4.07
    amount = 100
    sellPrice = 4.06

    ths = Ths()
    ths.startApp()

    for i in range(50):
        ths.buy(id, buyPrice, amount)
        # ths.sell(id, sellPrice, amount)
        print('-'*10,i+1,'-'*10,'\n')

    exit()
    for i in range(5):
        refresh_strategies.Toolbar(refresh_btn_index = 4)
        if len(ths.getTodayTrades()) == 0:
            # ths.refresh()
            # ths.user.refresh_strategy = refresh_strategies.Toolbar(refresh_btn_index = 4)
            sleep(.5)
        else:
            print(ths.getTodayEntrusts())
            break


    # print(ths.getBalance())
    # print('-'*10)
    # print(ths.getPosition())
    # print(ths.getTodayTrades())

    # sell id : self._config.CANCEL_ENTRUST_ENTRUST_FIELD