# -*- coding: utf-8 -*-
import sqlite3
import datetime
from collections import defaultdict
import pandas as pd
import simulator as sim


def create_stock_data(db_file_name, code_list, start_date, end_date):
    """指定した銘柄(code_list)それぞれの単元株数と日足(始値・終値）を含む辞書を作成
    """
    stocks = {}
    tse_index = sim.tse_date_range(start_date, end_date)
    conn = sqlite3.connect(db_file_name)
    for code in code_list:
        unit = conn.execute('SELECT unit from brands WHERE code = ?',
                            (code,)).fetchone()[0]
        prices = pd.read_sql('SELECT date, open, close '
                             'FROM prices '
                             'WHERE code = ? AND date BETWEEN ? AND ?'
                             'ORDER BY date',
                             conn,
                             params=(code, start_date, end_date),
                             parse_dates=('date',),
                             index_col='date')
        stocks[code] = {'unit': unit,
                        'prices': prices.reindex(tse_index, method='ffill')}
    return stocks

def generate_cross_date_list(prices):
    """指定した日足データよりゴールデンクロス・デッドクロスが生じた日のリストを生成
    """
    # 移動平均を求める
    sma_5 = prices.rolling(window=5).mean()
    sma_25 = prices.rolling(window=25).mean()

    # ゴールデンクロス・デッドクロスが発生した場所を得る
    sma_5_over_25 = sma_5 > sma_25
    cross = sma_5_over_25 != sma_5_over_25.shift(1)
    golden_cross = cross & (sma_5_over_25 == True)
    dead_cross = cross & (sma_5_over_25 == False)
    golden_cross.drop(golden_cross.head(25).index, inplace=True)
    dead_cross.drop(dead_cross.head(25).index, inplace=True)

    # 日付のリストに変換
    golden_list = [x.date()
                   for x
                   in golden_cross[golden_cross].index.to_pydatetime()]
    dead_list = [x.date()
                 for x
                 in dead_cross[dead_cross].index.to_pydatetime()]
    return golden_list, dead_list


def simulate_golden_dead_cross(db_file_name,
                               start_date, end_date,
                               code_list,
                               deposit,
                               order_under_limit):
    """deposit: 初期の所持金
    　 order_order_under_limit: ゴールデンクロス時の最小購入金額 
    """
    
    stocks = create_stock_data(db_file_name, code_list, start_date, end_date)

    # {ゴールデンクロス・デッドクロスが発生した日 : 発生した銘柄のリスト}
    # の辞書を作成
    golden_dict = defaultdict(list)
    dead_dict = defaultdict(list)
    for code in code_list:
        prices = stocks[code]['prices']['close']
        golden, dead = generate_cross_date_list(prices)
        for l, d in zip((golden, dead), (golden_dict, dead_dict)):
            for date in l:
                d[date].append(code)

    def get_open_price_func(date, code):
        return stocks[code]['prices']['open'][date]

    def get_close_price_func(date, code):
        return stocks[code]['prices']['close'][date]

    def trade_func(date, portfolio):
        order_list = []
        # Dead crossが発生していて持っている株があれば売る
        if date in dead_dict:
            for code in dead_dict[date]:
                if code in portfolio.stocks:
                    order_list.append(
                        sim.SellMarketOrder(code,
                                            portfolio.stocks[code].current_count))
        # 保有していない株でgolden crossが発生していたら買う
        if date in golden_dict:
            for code in golden_dict[date]:
                if code not in portfolio.stocks:
                    order_list.append(
                        sim.BuyMarketOrderMoreThan(code,
                                                   stocks[code]['unit'],
                                                   order_under_limit))
        return order_list

    return sim.simulate(start_date, end_date,
                        deposit,
                        trade_func,
                        get_open_price_func, get_close_price_func)
                        

