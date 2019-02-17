#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re
from requests.auth import HTTPDigestAuth
import lxml.html
import os
import time
import sys
import subprocess

def convert_exp(element, expression_t):
    op = element.attrib['class']

    if element.text is None:
        val = ''
    else:
        val = element.text

    if op == 'op_mul':
        pat = '(*'
    elif op == 'op_add':
        pat = '(+'
    elif op == 'op_sub':
        pat = '(-'
    else:
        pat = ''

    expression_t = expression_t + pat + ' ' + val

    for child_element in list(element):
        expression_t = convert_exp(child_element, expression_t)
        if child_element.attrib['class'] == 'op2':
            expression_t = expression_t + ')'

    return expression_t

def calc(html,htmltext):
        htmllines = htmltext.split('\n')
        for htmlline in htmllines:
            if 'expression' in htmlline:
                expressiontext = htmlline

        expressions=html.cssselect('#expression')[0]

        for expression in list(expressions):
            result =  convert_exp(expression, '')

        print('=========original===========')
        print(expressiontext)
        print('=========reverse===========')
        print(result)

        cmd_list='clisp -q -x'.split()
        cmd_list.append(result)
        runcmd = subprocess.check_output(cmd_list)
        answer = runcmd.decode().replace('\n','')

        print(answer)


        payload = {
            'answer': answer,
            'action': 'submit'
        }

        return payload

if __name__ == "__main__":

    #Initial setting
    url = "http://challenge.ctf.com:8012/"

    # reulst
    result_dir='./result'

    # header = {
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
    #     'Accept-Encoding': 'br, gzip, deflate',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     'Connection': 'keep-alive',
    #     'Accept-Language': 'ja',
    #     'Content-Type': 'application/x-www-form-urlencoded',
    #     'Upgrade-Insecure-Requests' : '1',
    #     'Cache-Control': 'max-age=0'
    # }

    ### Session start ###
    s = requests.Session()

#    s.headers = header

    ### Access ###
    r = s.get(url)
    cookies_a = r.cookies
    html = lxml.html.fromstring(r.content)
    htmltext = r.text

    stage= html.cssselect('#stage')[0]
    # print("stage: %s" % stage.text)
    stage_n = int(stage.text.split()[0])
    print("stage: %d" % stage_n)
    flag= html.cssselect('#flag')[0]
    print("%s" % flag.text)
    print('**************************************************')

    while stage_n != 500:
        payload = calc(html,htmltext)
        r = s.post(url, data=payload)

        html = lxml.html.fromstring(r.content)
        htmltext = r.text
        stage= html.cssselect('#stage')[0]
        stage_n = int(stage.text.split()[0])
        print("stage: %d" % stage_n)
        flag= html.cssselect('#flag')[0]
        print("%s" % flag.text)
        print('**************************************************')

    s.close()
