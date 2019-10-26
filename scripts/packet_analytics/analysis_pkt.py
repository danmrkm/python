#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import traceback
from scapy.all import *
import re
from operator import itemgetter

def analysis_():
    '''
    docstringを記載
    '''

    packets = rdpcap('hidden.pcap').filter(lambda p: Raw in p and TCP in p and p[TCP].sport == 80)
    sessions = packets.sessions()

    sessions_list = [sessions[s] for s in sessions]

    contents = []
    d = {}
    for session in sessions_list:
        for i, p in enumerate(session):
            data = p[Raw].load
            if i == 0:
                m = re.search(b'(?P<bytes>(\d+)-(\d+))/(\d+)\r\n\r\n(?P<payload>(.*))', data, flags=(re.MULTILINE | re.DOTALL))
                if m is not None:
                    d = m.groupdict()
            else:
                d['payload'] += data
        contents.append(d)

    new_contents = sorted(contents, key=itemgetter('bytes'))
    f = open('flag.png', 'wb')
    for i in new_contents:
        f.write(i['payload'])
    f.close()


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
    parser = argparse.ArgumentParser(description='引数で渡されたパケットファイルを解析する')
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

    ERROR_LOG = './some_error.log'

    # スタックトレースをエラーファイルに追加する
    try:
        result = not_found_function()
    except:
        with open(ERROR_LOG, 'a') as f:
            traceback.print_exc(file=f)
