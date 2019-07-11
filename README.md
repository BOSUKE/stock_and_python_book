# 「株とPython ─ 自作プログラムでお金儲けを目指す本」 サンプルコードなど

インプレスR&Dより出版されている[「株とPython ─ 自作プログラムでお金儲けを目指す本」](https://nextpublishing.jp/book/10319.html)に登場するサンプルソースコードや訂正・補足内容を記載しています。

## サンプルコード一覧

| 章・節番号  | サンプルコード内容 | GitHubでのファイルパス | 備考 |
|------------|-------------------|----------------------|---------|
| 2.3.2 | 2. PyQueryの使い方 | [chapter2/pyquery_sample.py](chapter2/pyquery_sample.py) | [株探のHTMLファイル変更に対応](#株探のHTMLファイル変更)  |
| 2.3.3.| 2. seleniumの使い方 | [chapter2/selenium_sample.py](chapter2/selenium_sample.py) | |
| 2.3.4 | リスト2.1 | [chapter2/get_brands.py](chapter2/get_brands.py )|[株探のHTMLファイル変更に対応](#株探のHTMLファイル変更)  |
| 2.4.1 | リスト2.2 | [chapter2/yahoo_csv_download.py](chapter2/yahoo_csv_download.py) | |
| 2.4.1 | リスト2.3 | [chapter2/csv_to_db.py](chapter2/csv_to_db.py) ||
| 2.5.2 | リスト2.4 | [chapter2/get_new_brands.py](chapter2/get_new_brands.py)| |
| 2.6.2 | リスト2.5 | [chapter2/csv_to_divide_union_data.py](chapter2/csv_to_divide_union_data.py) | |
| 2.6.2 | リスト2.6 | [chapter2/apply_divide_union_data.py](chapter2/apply_divide_union_data.py) | |
| 3.1 | リスト3.1 | [chapter3/get_price_dataframe.py](chapter3/get_price_dataframe.py)| |
| 3.2 | リスト3.2 ～ リスト3.4 | [chapter3/simulator.py](chapter3/simulator.py)| |
| 3.3 | リスト3.5 | [chapter3/golden_core30.py](chapter3/golden_core30.py) ||
| 3.3 | リスト3.6 | [chapter3/buy_and_hold.py](chapter3/buy_and_hold.py) ||
| 3.4 | リスト3.7 | [chapter3/rating_trade.py](chapter3/rating_trade.py) ||
| 3.4 | リスト3.8 | [chapter3/nikkei_tsumitate_trade.py](chapter3/nikkei_tsumitate_trade.py)||
| 4章 | リスト4.1 ～ リスト4.2 | [chapter4_5/simulator.py](chapter4_5/simulator.py) | 3章のsimulater.pyに指標関数を追加 |
| 5.4 | リスト5.1 | [chapter4_5/opincome_trade.py](chapter4_5/opincome_trade.py) | |

## 訂正と補足

### 株探のHTMLファイル変更
株探(Kabutan.jp)のページ内容（HTMLデータ内容)が本書執筆時から変更されたため、本書内の一部のコードがそのままでは動作しません。動作しないコードの一覧は [サンプルコード一覧](#サンプルコード一覧)を参照してください。
GitHub上のコードは本README.mdコミット時点で動作することを確認していますので、そちらを参考にしてください。

### JupyterLabの利用を推奨
本書内ではプログラムの実行環境として Jupyter Notebook を紹介していますが、 少なくとも
Python 3.6.5 + Jupyter Notebook 5.7.0 + pandas-highcharts 0.5.2の環境にて、pandas-highchartsのdisplay_chartsにてグラフがNotebook上に表示されない現象を確認しています。

Jupyter notebookの変わりにJupyterLab(0.35.4)上でプログラムを実行するとこの現象が発生しないことを確認しています(原因不明)。

JupyterLabはJupyter Notebookの後継となるソフトウエアで、同じような操作感で利用できます。

### 受渡日が1日短縮 (2019年7月16日約定分より)

本書の 1.4 権利確定日・権利落ち日・権利付き最終日 では、
買った日（約定日）を含め4日後に株は受け渡されると記載していますが、
2019年7月16日約定分より受け渡しが1日短く、3日後に変更されます。

2019年7月16日より前

| 25日(木)  | 26日(金) | 27日(土) | 28(日) | 29日(月) | 30日(火) |
|----------|----------|----------|--------|--------|--------|
|権利付き最終日|権利落ち日| (休日) | (休日) | | 権利確定日 |


2019年7月16日以降

| 25日(木)  | 26日(金) | 27日(土) | 28(日) | 29日(月) | 30日(火) |
|----------|----------|----------|--------|--------|--------|
| |権利付き最終日| (休日) | (休日) | 権利落ち日| 権利確定日 |
