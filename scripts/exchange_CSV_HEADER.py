#!/usr/bin/env python

import csv
import sys
import os

if __name__ == '__main__':

    # 入力CSVファイルヘッダー
    IMPORT_CSVHEADER = ["A", "B", "C", "D", "E"]
    # 出力CSVファイルヘッダー
    OUTPUT_CSVHEADER = ["F", "B", "C", "A", "D", "E"]

    # 引数取得
    args = sys.argv

    # 引数判定
    if len(args) != 3:
        print(
            'Usage: python3 ./exchange.py CSVFILE_PATH START_ID')
        quit()

    # CSVファイル存在チェック
    csvfilepath = args[1]
    if not (os.path.exists(csvfilepath)):
        print('Invalid csv file path.')
        quit()

    # START_ID
    start_id = args[2]

    with open(csvfilepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['A'], row['D'])
