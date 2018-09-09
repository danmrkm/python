#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import traceback


def some_function():
    '''
    docstringを記載
    '''

    print('処理をここに書く')
    return 0


def equal_even_num(number_str):
    '''
    引数が偶数か判別
    '''
    number = int(number_str)

    if (int(number) / 2) == 0:
        return int(number)
    else:
        msg = "%d is not even number" % number
        # エラーの場合、引数エラーを返す
        raise argparse.ArgumentTypeError(msg)


def file_exist(filepath):
    '''
    引数に指定したパスにファイルが存在するか判別
    '''

    if not os.path.exists(filepath):
        print("Not found: %s" % filepath)
        return 1
    else:
        print("File existed %s" % filepath)
        return 0


if __name__ == '__main__':
    # 直接起動のみ実行

    #　引数のパーサー
    parser = argparse.ArgumentParser(description='このPythonスクリプトの説明')
    # 引数の追加
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')

    parser.add_argument('--sum', '-s', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    # 引数のタイプ判別に自作関数を指定することも可能
    parser.add_argument('evennum', type=equal_even_num,
                        help='even number')

    # パースして結果をargsに格納
    args = parser.parse_args()

    # 引数を利用する際は以下のように利用する
    print('arg of "--sum" is %d' % args.sum)

    ERROR_LOG = './some_error.log'

    # スタックトレースをエラーファイルに追加する
    try:
        result = not_found_function()
    except:
        with open(ERROR_LOG, 'a') as f:
            traceback.print_exc(file=f)
