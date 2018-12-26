# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import numpy as np
import simulator as sim

def simulate_op_income_trade(db_file_name,
                             start_date,
                             end_date,
                             deposit,
                             growth_rate_threshold,
                             minimum_buy_threshold,
                             trading_value_threshold,
                             profit_taking_threshold,
                             stop_loss_threshold):
    """
    営業利益が拡大している銘柄を買う戦略のシミュレーション
    Args:
        db_file_name: DB(SQLite)のファイル名
        start_date:   シミュレーション開始日
        end_date:     シミュレーション終了日
        deposit:      シミュレーション開始時点での所持金
        growth_rate_threshold : 購入対象とする銘柄の四半期成長率の閾値
        minimum_buy_threshold : 購入時の最低価格
        trading_value_threshold: 購入対象とする銘柄の出来高閾値
        profit_taking_threshold: 利確を行う閾値
        stop_loss_threshold:   : 損切りを行う閾値
    """
    conn = sqlite3.connect(db_file_name)

    def get_open_price_func(date, code):
        """date日におけるcodeの銘柄の初値の取得"""
        r = conn.execute('SELECT open FROM prices '
                         'WHERE code = ? AND date <= ? ORDER BY date DESC LIMIT 1',
                         (code, date)).fetchone()
        return r[0]

    def get_close_price_func(date, code):
        """date日におけるcodeの銘柄の終値の取得"""
        r = conn.execute('SELECT close FROM prices '
                         'WHERE code = ? AND date <= ? ORDER BY date DESC LIMIT 1',
                         (code, date)).fetchone()
        return r[0]

    def get_op_income_df(date):
        """date日の出来高が閾値以上であるに四半期決算を公開した銘柄の銘柄コード、
        単元株、date日以前の四半期営業利益の情報、date日以前の四半期決算公表日を
        取得する
        """
        return pd.read_sql("""
                            WITH target AS (
                                SELECT
                                    code,
                                    unit,
                                    term
                                FROM
                                    quarterly_results
                                    JOIN prices
                                    USING(code, date)
                                    JOIN brands
                                    USING(code)
                                WHERE
                                    date = :date
                                    AND close * volume > :threshold
                                    AND op_income IS NOT NULL
                            )
                            SELECT
                                code,
                                unit,
                                op_income,
                                results.term as term
                            FROM
                                target
                                JOIN quarterly_results AS results
                                USING(code)
                            WHERE
                                results.term <= target.term
                            """,
                           conn,
                           params={"date": date,
                                   "threshold": trading_value_threshold})


    def check_income_increasing(income):
        """3期分の利益の前年同期比が閾値以上かつ単調増加であるかを判断。
        閾値以上単調増加である場合は3期分の前年同期比の平均値を返す。
        条件を満たさない場合は0を返す
        """
        if len(income) < 7 or any(income <= 0):
            return 0

        t1 = (income.iat[0] - income.iat[4]) / income.iat[4]
        t2 = (income.iat[1] - income.iat[5]) / income.iat[5]
        t3 = (income.iat[2] - income.iat[6]) / income.iat[6]

        if (t1 > t2) and (t2 > t3) and (t3 > growth_rate_threshold):
            return np.average((t1, t2, t3))
        else:
            return 0

    def choose_best_stock_to_buy(date):
        """date日の購入対象銘柄の銘柄情報・単位株を返す"""
        df = get_op_income_df(date)
        found_code = None
        found_unit = None
        max_rate = 0
        for code, f in df.groupby("code"):
            income = f.sort_values("term", ascending=False)[:7]
            rate = check_income_increasing(income["op_income"])
            if rate > max_rate:
                max_rate = rate
                found_code = code
                found_unit = income["unit"].iat[0]

        return found_code, found_unit

    def trade_func(date, portfolio):
        """date日の次の営業日の売買内容を決定する関数"""
        order_list = []

        # 売却する銘柄の決定
        for code, stock in portfolio.stocks.items():
            current = get_close_price_func(date, code)
            rate = (current / stock.average_cost) - 1
            if rate >= profit_taking_threshold or rate <= -stop_loss_threshold:
                order_list.append(
                    sim.SellMarketOrder(code, stock.current_count))

        # 購入する銘柄の決定
        code, unit, = choose_best_stock_to_buy(date)
        if code:
            order_list.append(sim.BuyMarketOrderMoreThan(code,
                                                         unit,
                                                         minimum_buy_threshold))

        return order_list

    # シミュレータの呼び出し
    return sim.simulate(start_date, end_date, deposit,
                        trade_func, get_open_price_func, get_close_price_func)
