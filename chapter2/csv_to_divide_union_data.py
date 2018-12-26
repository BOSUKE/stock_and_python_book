# -*- coding: utf-8 -*-
import csv
import glob
import datetime
import os
import sqlite3


def generater_devide_union_from_csv_file(csv_file_name, code):
    with open(csv_file_name) as f:
        reader = csv.reader(f)
        next(reader)  # 先頭行を飛ばす

        def parse_recode(row):
            d = datetime.datetime.strptime(row[0], '%Y/%m/%d').date() #日付
            r = float(row[4])  # 調整前終値
            a = float(row[6])  # 調整後終値
            return d, r, a

        _, r_n, a_n = parse_recode(next(reader))
        for row in reader:
            d, r, a = parse_recode(row)
            rate = (a_n * r) / (a * r_n)
            if abs(rate - 1) > 0.005:
                if rate < 1:
                    before = round(1 / rate, 2)
                    after = 1
                else:
                    before = 1
                    after = round(rate, 2)
                yield code, d, before, after
            r_n = r
            a_n = a


def generate_from_csv_dir(csv_dir, generate_func):
    for path in glob.glob(os.path.join(csv_dir, "*.T.csv")):
        file_name = os.path.basename(path)
        code = file_name.split('.')[0]
        for d in generate_func(path, code):
            yield d


def all_csv_file_to_divide_union_table(db_file_name, csv_file_dir):
    divide_union_generator = generate_from_csv_dir(csv_file_dir,
                                generater_devide_union_from_csv_file)
    conn = sqlite3.connect(db_file_name)
    with conn:
        sql = """
        INSERT INTO 
        divide_union_data (code, date_of_right_allotment,before, after)
        VALUES(?,?,?,?)
        """
        conn.executemany(sql, divide_union_generator)
