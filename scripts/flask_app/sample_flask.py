#!/bin/env python3
# -*- coding: utf-8 -*-

import os
import ssl
import sys
import signal
import configparser
import json
import argparse

from builtins import bytes
from flask import Flask, request, abort, jsonify
from datetime import datetime

def load_config(configfile):
    '''
    Config ファイルからサーバの情報をロード
    '''
    # ファイルパスチェック
    if not os.path.exists(configfile):
        print("Config file is not found: %s" % config_path)
        return False

    # 初期化
    config = configparser.ConfigParser()

    # コンフィグの読み込み
    config.read(configfile)

    try:
        # Server config を読み込み
        server_config = config['SERVER']
        return server_config

    except:
        # 値が見つからない場合はエラーを返す
        print('Not found server config in config file!')
        return False



def simple_log(text):
    '''
    ログメッセージ生成
    '''
    now = datetime.now()
    print("%s %s" % (now.strftime("%Y/%m/%d %H:%M:%S"), text))

def create_body(text):
    if PY3:
        return [bytes(text, 'utf-8')]
    else:
        return text

def sig_exit(signal, frame):
    '''
    Signalを受信したときに実行。プログラムを正常終了
    '''
    sys.exit(0)

def run_httpd_server(configfile, jsonfile):
    '''
    メイン関数 
    '''

    # サーバ設定の読み込み
    server_config = load_config(configfile)

    # エラーチェック
    if server_config == False:
        print('Some error happened. Exit this program.')
        sys.exit(1)

    # httpd serverに必要な設定値の取得
    try:
        server_name = server_config['HTTPS_SERVER_NAME']
        url = server_config['URL']
        num_of_query = server_config['NUMBER_OF_QUERY']
        ssl_switch = server_config['SSL']
        server_port = server_config['PORT']

        # SSL が指定されたときのみCERTFILEとKEYFILEをロード
        if ssl_switch == 'ON':
            key_file = server_config['CERT_KEY_FILE']
            cert_file = server_config['CERT_FILE']
        
    except IndexError:
        # パラメータが設定されていない場合
        print('Could not read some config in server_config')
        sys.exit(1)

        
    # Reply設定用jsonファイルの読み込み
    reply_json_data = json.load(jsonfile)

    # Flask の設定
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config["JSON_SORT_KEYS"] = False

    
    @app.route(url)
    def return_json():

        response = ""
        default_response = ""
        
        # json に設定されているURLでフィルタ
        if url == reply_json_data['url']:
            query_name = reply_json_data['query_name']
            query = request.args.get(query_name)

            for i in range(0,len(reply_json_data['reply'])):                

                if reply_json_data['reply'][i]['tag'] == 'DEFAULT':
                    default_response = jsonify(reply_json_data['reply'][i]['reply_data'])
                    default_response.status_code = reply_json_data['reply'][i]['status_code']
                
                if reply_json_data['reply'][i][query_name] == query:
                    response = jsonify(reply_json_data['reply'][i]['reply_data'])
                    response.status_code = reply_json_data['reply'][i]['status_code']
                    break


            # マッチする設定が定義されていない場合
            if response == "":
                # デフォルト設定が定義されていればそれを用いる
                if default_response != '':
                    response = default_response
                    response.status_code = default_response.status_code

                # デフォルト設定が定義されていない場合
                else:
                    result_query = {
                        'status': 'NG'
                    }
                    response = jsonify(result_q=result_query)
                    response.status_code = 200

        # json ファイルに定義されていないものはstatus:OKとして返す
        else:
            result_query = {
                'status': 'OK'
            }

            response = jsonify(result_q=result_query)
            response.status_code = 200
            
        return response

    
    # SSL が有効な場合、暗号化方式および証明書、鍵を設定
    if ssl_switch == 'ON':
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

        # Keyfile が指定されていなければ、証明書と鍵が同一ファイル前提で SSL を設定
        if len(key_file) > 3:
            context.load_cert_chain(cert_file, key_file)
        else:
            context.load_cert_chain(cert_file)
            
    try:
        # SIGNALを受信したら、sig_exit関数を実行
        signal.signal(signal.SIGINT, sig_exit)

        if ssl_switch == 'ON':        
            app.run(host=server_name, port=server_port,ssl_context=context, debug=True, threaded=True)
        else:
            app.run(host=server_name, port=server_port, debug=True, threaded=True)
            
    except EOFError:
        pass


if __name__ == '__main__':

    # argparse で引数解析
    parser = argparse.ArgumentParser(description='Run httpd server')

    # オプション追加 --config で設定ファイルを指定
    parser.add_argument('--config', help="specify config file. \nex: ./config.ini",
                         type=str, required=True, default=sys.stdin)

    # オプション追加 --json でjsonファイルを指定
    parser.add_argument('--json', help="specify json file. \nex: ./api.json",
                        nargs='?', type=argparse.FileType('r'), required=True, default=sys.stdin)

    args = parser.parse_args()

    run_httpd_server(args.config, args.json)


