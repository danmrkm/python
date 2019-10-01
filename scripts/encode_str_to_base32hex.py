#!/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import signal
import json
import configparser
from base32hex import *

from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config["JSON_SORT_KEYS"] = False

configfile = "config.ini"


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
        apikey_config = config['API_KEY']
        return apikey_config

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


@app.route('/')
def run_httpd_server():
    '''
    メイン関数
    '''

    # サーバ設定の読み込み
    apikey_config = load_config(configfile)

    # エラーチェック
    if apikey_config == False:
        print('Some error happened. Exit this program.')
        sys.exit(1)

    response = ""
    default_response = ""
    auth_flag = False

    try:
        api_keys = apikey_config['API_KEY'].replace(
            '[', '').replace(']', '').replace('"', '').split(',')

    except IndexError:
        # パラメータが設定されていない場合
        result_query = {
            'result': 'NG',
            'msg': 'Internal Server Error (Invalid config)',
            'encoded_string': ''
        }
        response = jsonify(result_query)
        response.status_code = 500

    req_authorization = request.headers.get('Authorization')

    # Authorization ヘッダ が設定されていない
    if req_authorization is None:
        result_query = {
            'result': 'NG',
            'msg': 'Unauthorized',
            'encoded_string': ''
        }
        response = jsonify(result_query)
        response.headers['WWW-Authenticate'] = 'Bearer realm="token_required"'
        response.status_code = 401
        return response

    tokens = req_authorization.split()

    # token が bearer 形式でない、指定されていない
    if (tokens[0].lower() != "bearer") or ((len(tokens) < 2) or len(tokens) > 2):
        result_query = {
            'result': 'NG',
            'msg': 'Bad request',
            'encoded_string': ''
        }
        response = jsonify(result_query)
        response.headers['WWW-Authenticate'] = 'Bearer error="invalid_request"'
        response.status_code = 400
        return response

    # token チェック
    for api_key in api_keys:
        if tokens[1] == api_key:
            auth_flag = True

    # api_key が未設定または一致しない場合
    if not (auth_flag):
        result_query = {
            'result': 'NG',
            'msg': 'Unauthorized',
            'encoded_string': ''
        }
        response = jsonify(result_query)
        response.headers['WWW-Authenticate'] = 'Bearer error="invalid_token"'
        response.status_code = 401
        return response

    # 認証成功時
    org_string = request.args.get('string')

    # string 未定義
    if org_string is None:
        result_query = {
            'result': 'NG',
            'msg': 'Bad request',
            'encoded_string': ''
        }
        response = jsonify(result_query)
        response.headers['WWW-Authenticate'] = 'Bearer error="invalid_request"'
        response.status_code = 400
        return response

    # string が 0 のときはそのまま返す
    if len(org_string) <= 0:
        result_query = {
            'result': 'NG',
            'msg': 'String length must be bigger than 0',
            'encoded_string': ''
        }
        response = jsonify(result_query)
        response.headers['WWW-Authenticate'] = 'Bearer error="invalid_request"'
        response.status_code = 400
        return response

    # リクエスト成功時
    bstring = org_string.encode()
    encoded_string = base32hex_encode(bstring).decode().lower().replace(
        '=', '')

    result_query = {
        'result': 'OK',
        'msg': 'Success',
        'encoded_string': encoded_string
    }
    response = jsonify(result_query)
    response.status_code = 200
    return response


if __name__ == '__main__':

    # run_httpd_server()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
