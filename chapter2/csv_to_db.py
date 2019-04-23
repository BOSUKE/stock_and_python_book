# -*- coding: utf-8 -*-
import csv
import glob
import datetime
import os
import sqlite3


def generate_price_from_csv_file(csv_file_name, code):
    with open(csv_file_name, encoding="shift_jis") as f:
        reader = csv.reader(f)
        next(reader)  # 先頭行を飛ばす
        for row in reader:
            d = datetime.datetime.strptime(row[0], '%Y/%m/%d').date() #日付
            o = float(row[1])  # 初値
            h = float(row[2])  # 高値
            l = float(row[3])  # 安値
            c = float(row[4])  # 終値
            v = int(row[5])    # 出来高
            yield code, d, o, h, l, c, v


def generate_from_csv_dir(csv_dir, generate_func):
    for path in glob.glob(os.path.join(csv_dir, "*.T.csv")):
        file_name = os.path.basename(path)
        code = file_name.split('.')[0]
        for d in generate_func(path, code):
            yield d


def all_csv_file_to_db(db_file_name, csv_file_dir):
    price_generator = generate_from_csv_dir(csv_file_dir,
                                            generate_price_from_csv_file)
    conn = sqlite3.connect(db_file_name)
    with conn:
        sql = """
        INSERT INTO raw_prices(code,date,open,high,low,close,volume)
        VALUES(?,?,?,?,?,?,?)
        """
        conn.executemany(sql, price_generator)
