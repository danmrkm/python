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
from flask import Flask, request, abort
from datetime import datetime

def load_config(configfile):
    '''
    Config ファイルからサーバの情報をロード
    '''

    # 引数がファイル形式で
    if not type(configfile) == 'File':
        print('Specify config file as file format.')
        return False
    
    # ファイルパスチェック
    if not os.path.exists(config_path):
        print("Config file is not found: %s" % config_path)
        return False

    # 初期化
    config = configparser.ConfigParser()

    # コンフィグの読み込み
    config.read(config_path)

    try:
        # Server config を読み込み
        server_config = config['Server']
        return server_config

    except:
        # 値が見つからない場合はエラーを返す
        print('Not found server config in config file!')
        return False

# app = Flask(__name__)

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


# @app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def run_httpd_server(configfile, jsonfile):
    '''
    メイン関数 
    '''

    # サーバ設定の読み込み
    server_config = config_load(configfile)

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
    query_json_data = json.load(jsonfile)

    # SSL が有効な場合、暗号化方式および証明書、鍵を設定
    if ssl_switch == 'ON':
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(cert_file, key_file)

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
                        nargs='?', type=argparse.FileType('r'), required=True, default=sys.stdin)

    # オプション追加 --json でjsonファイルを指定
    parser.add_argument('--json', help="specify json file. \nex: ./api.json",
                        nargs='?', type=argparse.FileType('r'), required=True, default=sys.stdin)

    args = parser.parse_args()

    run_httpd_server(args.config, args.json)


