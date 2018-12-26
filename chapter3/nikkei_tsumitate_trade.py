# -*- coding: utf-8 -*-
import simulator as sim
from golden_core30 import create_stock_data

def simulate_nikkei_tsumitate(db_file_name, start_date,
                              end_date, deposit, reserve):

    code = 1321
    stocks = create_stock_data(db_file_name, (code,),
                               start_date, end_date)
    def get_open_price_func(date, code):
        return stocks[code]['prices']['open'][date]

    def get_close_price_func(date, code):
        return stocks[code]['prices']['close'][date]

    current_month = start_date.month - 1
    def trade_func(date, portfolio):
        nonlocal  current_month
        if date.month != current_month:
            # åéèâÇﬂ => ì¸ã‡ => çwì¸
            portfolio.add_deposit(reserve)
            current_month = date.month
            return [sim.BuyMarketOrderAsPossible(code,
                                                 stocks[code]['unit'])]
        return []

    return sim.simulate(start_date, end_date,
                        deposit,
                        trade_func,
                        get_open_price_func,
                        get_close_price_func)

