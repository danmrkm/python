#!/usr/bin/env python

import csv
import sys
import os
import uuid

if __name__ == '__main__':

    # 入力CSVファイルヘッダー
    INPUT_CSVHEADER = ["A", "B", "C", "D", "Z"]
    # 出力CSVファイルヘッダー
    OUTPUT_CSVHEADER = ["F", "B", "C", "A", "D", "E", "Z"]

    # Key COULOUM
    KEYCOLUMN = {"C": {"value": 1, "parm": "str"},
                 "Z": {"@CentOS-7": 'CENT', "custom": "aaaa"}}

    MAKE_CSVHEADER = True
    # Kye mapping
    KEYMAP = {"Z": "E"}

    # 引数取得
    args = sys.argv

    # 引数判定
    if len(args) != 4:
        print(
            'Usage: python3 ./exchange.py INPUT_CSVFILE_PATH OUTPUT_CSVFILE_PATH START_ID')
        quit()

    # CSVファイル存在チェック
    csvfilepath = args[1]
    if not (os.path.exists(csvfilepath)):
        print('Invalid csv file path.')
        quit()

    # 出力用CSVファイルの存在チェック
    outcsvfilepath = args[2]
    if (os.path.exists(outcsvfilepath)):
        print("Dou you want to ovewrite %s ? [y/n]" % outcsvfilepath)
        yn = input('Answer: ')
        if yn != 'y':
            print('Terminate this script.')
            quit()

    # START_ID
    start_id = args[3]
    STARTFLAG = 'A'

    count = 0
    flag = False

    outputlist = []

    with open(csvfilepath, newline='') as csvfile:
        reader = csv.DictReader(
            csvfile, fieldnames=INPUT_CSVHEADER, restkey='EXTERNAL_COLUMNS')
        for row in reader:
            count = count + 1
            tmpdict = {}

            if row['A'] == start_id:
                flag = True

            if flag:
                tmpdict["F"] = str(uuid.uuid4())

                for key in KEYCOLUMN.keys():
                    if key in row:
                        if row[key] in KEYCOLUMN[key]:
                            row[key] = KEYCOLUMN[key][row[key]]

                for mapkey in KEYMAP.keys():
                    if mapkey in row:
                        tmpdict[KEYMAP[mapkey]] = row[mapkey]

                tmpdict.update(row)
                outputlist.append(tmpdict)

    with open(outcsvfilepath, 'w', newline='') as outcsvfile:

        writer = csv.DictWriter(
            outcsvfile, fieldnames=OUTPUT_CSVHEADER, extrasaction='ignore')

        if MAKE_CSVHEADER:
            writer.writeheader()

        for i in range(0, len(outputlist)):
            writer.writerow(outputlist[i])

    print("Complete! Check %s" % outcsvfilepath)
