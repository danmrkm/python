#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import traceback


def conv_rgb_to_web(red,green,blue):

    '''
    RGBで指定された値をWEBカラーに変換する
    '''
    ans_str = '#' + format(red, 'x').zfill(2) + format(green,'x').zfill(2) + format(blue,'x').zfill(2)
    print(ans_str)
    return 0


def equal_value_num(number_str):
    '''
    引数が0~255の範囲か判定
    '''

    number = int(number_str)

    if ((int(number) >= 0) and (int(number) <= 255) or int(number) == -1):
        return int(number)
    else:
        msg = "%d is not 0-255 number" % number
        # エラーの場合、引数エラーを返す
        raise argparse.ArgumentTypeError(msg)


if __name__ == '__main__':
    # 直接起動のみ実行

    #　引数のパーサー
    parser = argparse.ArgumentParser(description='このPythonスクリプトの説明')

    # 引数のタイプ判別に自作関数を指定することも可能
    parser.add_argument('red', type=equal_value_num, nargs='?', default=-1,
                        help='Red number')

    parser.add_argument('green', type=equal_value_num,  nargs='?', default=-1,
                        help='Green number')

    parser.add_argument('blue', type=equal_value_num,  nargs='?', default=-1,
                        help='Blue number')

    # パースして結果をargsに格納
    args = parser.parse_args()

    # 引数判定
    if ((args.red == -1) or (args.green == -1) or (args.blue == -1)):
        number_str = input('Input RGB:').strip().replace('\t',' ')
        numbers = number_str.split(' ')
        errflag = False

        if len(numbers) > 2:
            for i in range(0,len(numbers)):
                if numbers[i].isdecimal():
                    if ((int(numbers[i]) < 0) or (int(numbers[i]) > 255)):
                        errflag = True
                else:
                    errflag = True

        else:
            errflag = True

        if errflag:
            print('Invalid input')
            sys.exit(1)

        else:
            conv_rgb_to_web(int(numbers[0]),int(numbers[1]),int(numbers[2]))
    else:
        conv_rgb_to_web(int(args.red),int(args.green),int(args.blue))
