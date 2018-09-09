#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

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

    # パースして結果をargsに格納
    args = parser.parse_args()

    # 引数を利用する際は以下のように利用する
    print('arg of "--sum" is %d' % args.sum)
    
    
