#!/bin/env python

import argparse
import sys
import json


# 与えられた引数が辞書オブジェクトだったとき、辞書のキーと場所を返す
def search_key(args, position, key_list):

    # リスト型の場合はpositionリストにリストの何番目の要素かを追加し、再度search_keyを呼び出す。
    if isinstance(args, list):
        for i in range(0, len(args)):
            position.append(i)
            key_list = search_key(args[i], position, key_list)

    # 辞書型の場合はpositionリストに辞書の場所を追加し、key_listに辞書の項目を追加、再度search_keyを呼び出す。
    elif isinstance(args, dict):
        for key in args.keys():
            if key in key_list:
                key_list[key].append(position)
            else:
                key_list[key] = [position]

            position.append(key)
            key_list = search_key(args[key], position, key_list)

    # リスト型と辞書型以外の値である場合はスルー
    else:
        pass

    return key_list


if __name__ == "__main__":

    # argparse で引数解析
    parser = argparse.ArgumentParser(description='Parse JSON data')

    # オプション追加 --input で入力用 json ファイルを指定
    parser.add_argument('--inputfile', help="Specify JSON file",
                        nargs='?', type=argparse.FileType('r'), required=True, default=sys.stdin)

    # オプション追加 --target で取得したい要素を指定
    parser.add_argument('--target', help="Specify target key",
                        required=True)

    # オプション追加 サーチパターンを追加
    parser.add_argument('ss', help="Specify search pattern", nargs='*')

    args = parser.parse_args()

    # json データをダンプ
    json_data = json.load(args.inputfile)

    print(len(args.ss))

    # サーチパターンに指定した引数が「要素、検索値」になっていない場合はエラー
    if (not (len(args.ss) % 2) == 0) or len(args.ss) == 0:
        print("Specify searchstring pair")
        quit()

    count = 0

    # jsonデータで辞書のキーと場所を検索
    key_list = search_key(json_data, [], {})

    result = ''
    skey_list = []
    print(key_list)
    #  サーチパターンの数だけ繰り返す
    for i in range(0, len(args.ss) + 1, 2):
        if args.ss[i] in key_list.keys():
            print("args.ss[i]: %s" % args.ss[i]) # debug            
            for ps in key_list[args.ss[i]]:
                exec_str = 'json_data'
                print("ps: %s" % ps) # debug
                for j in range(0, len(ps)):
                    
                    if not isinstance(ps[j], str):
                        exec_str = exec_str + '[' + str(ps[j]) + ']'
                    else:
                        exec_str = exec_str + '["' + ps[j] + '"]'


                exec_str = 'skey_list = ' + exec_str
                print("exec_str: %s" % exec_str)                
                exec(exec_str)

                if isinstance(skey_list[args.ss[i]],[list,dict]):
                    continue
                    
                else:
                    if skey_list[args.ss[i]] == args.ss[i+1]:
                        if args.target in skey_list.keys():
                            # 検索結果を出力
                            print(skey_list[args.target])
                            break
                    continue
                            

                
                
        else:
            print("Not found keyname: %s" % args.ss[count])


            
    # if args.ss[count] in json_data.keys():

    #     print(json_data[args.ss[count]])
    #     print("type: %s" % type(json_data[args.ss[count]]))
    # else:
