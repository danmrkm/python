#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import pandas


def convert_xlsx_to_csv(excelfile, csvfile, sheetname, char_code):
    '''
    エクセルをCSVに変換
    '''

    # ファイル存在チェック
    if not os.path.exists(excelfile):
        print("Not found %s" % excelfile)
        return 1

    if os.path.exists(csvfile):
        print("Already exist %s" % csvfile)
        return 1

    # エクセルを読み込み
    data = pandas.read_excel(excelfile, sheetname, index_col=None)

    # CSVで出力
    data.to_csv(csvfile, encoding=char_code, index=None)

    print("Success to convert: %s => %s" % (excelfile, csvfile))
    return 0


if __name__ == '__main__':
    # 直接起動のみ実行

    # 引数のパーサー
    parser = argparse.ArgumentParser(description='エクセルの指定した列また行を読み込み出力する')
    # 引数の追加

    parser.add_argument('--input', '-i', type=str, required=True,
                        help='path of excel file')

    parser.add_argument('--output', '-o', type=str, required=True,
                        help='path of csv file')

    parser.add_argument('--sheetname', '-s', type=str,
                        default='Sheet1', help='sheet name to convert csv')

    parser.add_argument('--charcode', '-c', type=str, choices=['utf-8', 'shift_jis', 'cp932'],
                        default='utf-8', help='charactor code of output csv')

    # パースして結果をargsに格納
    args = parser.parse_args()

    result = convert_xlsx_to_csv(args.input, args.output, args.sheetname, args.charcode)

    print(result)
