import sqlite3
from dateutil.relativedelta import relativedelta
import simulator as sim

def simulate_rating_trade(db_file_name, start_date, 
                          end_date, deposit, reserve):
    conn = sqlite3.connect(db_file_name)

    def get_open_price_func(date, code):
        r = conn.execute('SELECT open FROM prices '
                         'WHERE code = ? AND date <= ? '
                         'ORDER BY date DESC LIMIT 1',
                         (code, date)).fetchone()
        return r[0]

    def get_close_price_func(date, code):
        r = conn.execute('SELECT close FROM prices '
                         'WHERE code = ? AND date <= ? '
                         'ORDER BY date DESC LIMIT 1',
                         (code, date)).fetchone()
        return r[0]

    def get_prospective_brand(date):
        """購入する銘柄を物色  購入すべき銘柄の(コード, 単元株数, 比率)を返す
        """
        prev_month_day = date - relativedelta(months=1)
        sql = """
        WITH last_date_t AS (
            SELECT
                MAX(date) AS max_date,
                code,
                think_tank
            FROM
                ratings
            WHERE
                date BETWEEN :prev_month_day AND :day
            GROUP BY
                code,
                think_tank
        ),  avg_t AS (
            SELECT
                ratings.code,
                AVG(ratings.target) AS target_avg
            FROM
                ratings,
                last_date_t
            WHERE
                ratings.date = last_date_t.max_date
                AND ratings.code = last_date_t.code
                AND ratings.think_tank = last_date_t.think_tank
            GROUP BY
                ratings.code
        )
        SELECT
            avg_t.code,
            brands.unit,
            (avg_t.target_avg / prices.close) AS rate
        FROM
            avg_t,
            prices,
            brands
        WHERE
            avg_t.code = prices.code
            AND prices.date = :day
            AND rate > 1.2
            AND prices.code = brands.code
        ORDER BY
            rate DESC
        LIMIT 
            1
        """
        return conn.execute(sql, 
                           {'day': date,
                            'prev_month_day': prev_month_day}).fetchone()

    current_month = start_date.month - 1

    def trade_func(date, portfolio):
        nonlocal current_month
        if date.month != current_month:
            # 月初め => 入金
            portfolio.add_deposit(reserve)
            current_month = date.month

        order_list = []

        # ±20パーセントで利確/損切り
        for code, stock in portfolio.stocks.items():
            current = get_close_price_func(date, code)
            rate = (current / stock.average_cost) - 1
            if abs(rate) > 0.2:
                order_list.append(
                    sim.SellMarketOrder(code, stock.current_count))

        # 月の入金額以上持っていたら新しい株を物色
        if portfolio.deposit >= reserve:
            r = get_prospective_brand(date)
            if r:
                code, unit, _= r
                order_list.append(sim.BuyMarketOrderAsPossible(code, unit))

        return order_list

    return sim.simulate(start_date, end_date, deposit,
                        trade_func,
                        get_open_price_func, get_close_price_func)
