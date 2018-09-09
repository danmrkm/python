#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import traceback
import openpyxl
from pprint import pprint


def convert_list_from_string(somerange):
    '''
    数字とアルファベットの羅列をリストに変換する
    '''

    # 文字列判定
    if not type(somerange) == str:
        print("argument is not string" % somerange)
        return 1

    # 空白等を排除
    numoralp = ''.join(somerange.split())

    # アルファベットか数字か判定
    # '-',','を削除する
    numoralp_t = numoralp.replace('-', '').replace(',', '')
    mode = ''

    if numoralp_t.isdigit():
        # 数字
        mode = 'numeric'
    elif numoralp_t.isalpha():
        # 英字
        mode = 'alphabet'
    else:
        print("argument %s is not numeric or alphabet" % somerange)
        return 1

    # , を指定していた場合、リストに変換
    if ',' in numoralp:
        na_range_tmp = numoralp.split(',')
    else:
        na_range_tmp = [numoralp]

    na_range = []
    alphabet_list = [chr(i) for i in range(65, 65+26)]

    for elem in na_range_tmp:

        # - を指定されているか確認
        if '-' in elem:

            # 数字の場合
            if mode == 'numeric':
                first_n = int(elem[0:elem.index('-')])
                second_n = int(elem[elem.index('-')+1:len(elem)])

                for i in range(min(first_n, second_n), max(first_n, second_n)+1):
                    na_range.append(str(i))

            # 英語の場合
            else:
                first_c = alphabet_list.index(elem[0:elem.find('-')].upper())
                second_c = alphabet_list.index(
                    elem[elem.find('-')+1:len(elem)].upper())
                for j in range(min(first_c, second_c), max(first_c, second_c)+1):
                    na_range.append(alphabet_list[j])

        # - が指定されていない場合、そのまま格納
        else:
            na_range.append(elem)

    na_range.sort()

    return na_range


def print_excel_data(filepath, sheetname, mode, target_range):
    '''
    エクセルファイルを読み込む
    '''

    # ファイル存在チェック
    if not os.path.exists(filepath):
        print("Not found %s" % filepath)
        return 1

    # エクセルファイルを開く
    wb = openpyxl.load_workbook(filepath)

    # シート名のチェック
    if not sheetname in wb.sheetnames:
        print("Not found %s" % sheetname)
        return 1

    sheet = wb[sheetname]

    print(target_range)
    for i in range(0, len(target_range)):
        cell_list = sheet[target_range[i] + ':' + target_range[i]]

    for j in range(0, len(cell_list)):
        print(cell_list[j].value)

    return 0


if __name__ == '__main__':
    # 直接起動のみ実行

    #　引数のパーサー
    parser = argparse.ArgumentParser(description='エクセルの指定した列また行を読み込み出力する')
    # 引数の追加

    parser.add_argument('--excelpath', '-f', type=str, required=True,
                        help='path of excel file')

    parser.add_argument('--target', '-t', choices=['row', 'column'], default='row',
                        help='row or column mode')

    parser.add_argument('--sheetname', '-s',
                        default='sheet1', help='row or column mode')

    parser.add_argument('--range', '-r', required=True, type=str,
                        help='row range or cloumn range\n Ex: 1) B-J\n2)1,2,10')

    # パースして結果をargsに格納
    args = parser.parse_args()

    result = print_excel_data(
        args.excelpath, args.sheetname, args.target, convert_list_from_string(args.range))

    print(result)
