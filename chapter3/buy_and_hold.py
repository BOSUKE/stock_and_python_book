# -*- coding: utf-8 -*-
import simulator as sim
from golden_core30 import create_stock_data

def simulate_buy_and_hold(db_file_name, start_date, end_date, code, deposit):

    stocks = create_stock_data(db_file_name, (code,),
                               start_date, end_date)

    def get_open_price_func(date, code):
        return stocks[code]['prices']['open'][date]

    def get_close_price_func(date, code):
        return stocks[code]['prices']['close'][date]

    def trade_func(date, portfolio):
        if date == start_date:
            return [sim.BuyMarketOrderAsPossible(
                code, stocks[code]['unit'])]
        return []

    return sim.simulate(start_date, end_date, deposit,
                        trade_func,
                        get_open_price_func, get_close_price_func)