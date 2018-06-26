#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


def p_index(chapter, index):

    if type(chapter) != str:
        print('Invalid chapter_name!')

    print("********* %d. %s *********" % (index, chapter))
    return index + 1


index = 1

############## Coding 規約 ##############
index = p_index('Coding 規約', index)
# 参考URL: http://pep8-ja.readthedocs.io/ja/latest/

### インデント ###
# インデントはスペース4文字を推奨。タブは使っても良いが、スペースと混ぜることは禁止。
# 行を継続する場合は、折り返された要素を縦に揃えるべき。
# 例

# foo = long_function_name(var_one, var_two,
#                         var_three, var_four)

### 改行, スペース ###
# 一行は最大79文字までにする
# トップレベルの関数やクラスは2行はあけるn
# クラス内部では、1行ずつ空けてメソッドを定義する
# 2項演算子には空白を入れる
# ただし複数の演算子を利用する場合は優先度が一番引くものに絞った方がよい
# キーワード引数や、デフォルトパラメータの=には空白を入れない
# 関数アノテーションには基本的に直後に空白を入れる
# 複合文(;で複数行を記載）は基本的に用いない

### import ###
# importは1行ずつ指定します。
# importする際は絶対importを利用します。相対importは
# importは以下の順番で記載します
# 1. 標準ライブラリ
# 2. サードパーティに関連するもの
# 3. ローカルな アプリケーション/ライブラリ に特有のもの

### その他 ###
# インラインコメントは避ける
# ブロックコメントは該当するコードと同じインデントを行う。

### docstring ###


############## 四則演算 ##############
index = p_index('四則演算', index)

# 浮動小数点の除算
result = 9 / 5
print(result)

# 整数の除算
result = 9 // 5
print(result)

# 剰余
result = 9 % 5
print(result)

# 算術演算子は=の前に追加する形で代入と組み合わせ可能
# 以下の2項式は同じ結果を返す
# 通常の記載
a = 100
a = a + 3
print(a)

# 略式記載
a = 100
a += 3
print(a)


############## 基数 ##############
index = p_index('基数', index)

# 2進数
result = 0b10
print(result)

# 8進数
result = 0o10
print(result)

# 16進数
result = 0x10
print(result)


############## 変数 ##############
index = p_index('変数', index)

# 変数の型を調べる
sample = 'test'
result = type(sample)
print(result)

# 変数の型をそのまま出力可能
print(list)

# int型に変換
result = int('-100')
print(type(result))

# Trueは1, Flaseは0になる
print(int(True))
print(int(False))

# 整数 => 整数変換もエラーにはならない
print(int(result))

# 浮動小数点数に変換
result = float('99.00')
print(type(result))
print(result)


############## 文字列 ##############
index = p_index('文字列', index)

# 文字列型に変換
print("%f: %s" % (result, type(result)))
result = str(result)
print("%s: %s" % (result, type(result)))

# エスケープ文字
# 改行やタブ
print('This is \nsample\ttext.')

# + による文字列連結
result = 'This' + " " + 'is' + " " + sample
print(result)

# * による文字列の繰り返し
result = 'Hey ' * 3
print(result)

# [] による文字列の抽出
letters = 'abcdefghijklmnopqrstuvwxyz'
print(letters[0])
print(letters[-1])
print(letters[5])

# [start:end:step]によるスライス
# 最初から最後の文字まで
print(letters[:])
# Startから最後の文字まで
print(letters[5:])
# 最初からEnd-1の文字まで
print(letters[:5])
# step文字ごとにStartからEnd-1まで
print(letters[5:20:2])
# 最後の3文字を取り出す
print(letters[-3:])
# stepは負の数も指定可能。その場合、逆順に取り出す。
print(letters[-1::-1])

# lenによる文字数の取得
print(len(letters))

# splitによる分割
sample = 'This, is, test, string.'
result = sample.split(',')
print(result)

# joinによる結合(joinの前に指定した文字列でリストを結合)
result = ''.join(result)
print(result)

# 先頭文字が特定の文字で始まっているか
print(letters.startswith('abc'))

# 末尾文字が特定の文字で終わっているか
print(letters.endswith('yz'))

# 指定した文字が最初に現れる位置を返す
print(letters.find('bc'))

# 指定した文字が最後に現れる位置を返す
print(letters.rfind('yz'))

# 指定した文字の出現回数
print(letters.count('yz'))

# 文字列が英数字かどうか判定
print(letters.isalnum())
print('10'.isalnum())

# 文字列置換(置換回数も指定可能)
result = letters.replace('de', '  ', 1)
print(result)

############## リスト ##############
index = p_index('リスト', index)

# 空リスト
empty_list = []
empty_list = list()

# リストの初期化
week = ['Sunday', 'Monday', 'Tuesday',
        'Wednesday', 'Thursday', 'Friday', 'Sutuday']
print(week)

# タプル -> リストへの変換
a_tuple = ('this', 'is', 'sumple')
print(a_tuple)
result = list(a_tuple)
print(result)

# リストの要素の取り出し
result = week[1]
print(result)
result = week[-2]
print(result)

# 複数の型をリストに格納する
a_list = [1, 'one', 3, 'three']
print(a_list)

# リストのリスト
b_list = [4, 'four', a_list]
print(b_list)

# リストのスライス
print(a_list[-1::-1])

# append()による末尾への要素の追加
a_list.append(2)
a_list.append('two')
print(a_list)

# insert()による指定したオフセットへの要素の追加
a_list.insert(2, 0)
a_list.insert(3, 'zero')
print(a_list)

# 存在しないオフセットの場合は末尾に追加される
a_list.insert(100, 'test')
a_list.insert(100, 'test')
a_list.insert(100, 'test')
print(a_list)

# delによる指定したオフセットの要素の削除
del a_list[-1]
print(a_list)

# removeによる値に基づく要素の削除
a_list.remove('test')
print(a_list)

# popによる指定したオフセットの要素の削除
print(a_list.pop())
print(a_list)

# index()による要素のオフセットの検索
print(a_list.index('zero'))

# リストのリストにして、中のリストを更新した場合、外のリストも更新される
print(b_list)

# 他のリストの書き換えを抑制したい場合は、copy(), list(), スライスを使う
b_list_dash = b_list[:]
b_list_dash = b_list.copy()
b_list_dash = list(b_list)
b_list_dash[0:2] = [7, 'seven']
print(b_list)
print(b_list_dash)

# extend()または+=を使ったリストの結合
c_list = [5, 'five']
a_list.extend(c_list)
print(a_list)
d_list = [6, 'six']
a_list += d_list
print(a_list)

# append()にリストを入れると、リストのリストになる
b_list.append(c_list)
print(b_list)

# in によるリストに値が含まれるかをチェックする(集合のほうが処理が速い)
result = 'one' in a_list
print(result)
result = 'hundred' in a_list
print(result)

# count を使った要素数のカウント
result = a_list.count('one')
print(result)

# リストをソートしてコピーする
result = sorted(a_list[0::2])
print(result)

# リスト自体をソートする
e_list = [1, 1, 100, 2, 44, 55]
e_list.sort()
print(e_list)

# 逆順ソート
e_list.sort(reverse=True)
print(e_list)


############## タプル ##############
index = p_index('タプル', index)

# 空のタプル
empty_tuple = ()

# タプルの定義に括弧は不要
a_tuple = 'This', 'is', 'test'
print(a_tuple)

# ただし、括弧をつけた方が明示的にタプルだとわかる
b_tuple = ('This', 'is', 'test')
print(b_tuple)

# タプルを使って、複数変数に同時に格納が可能
a, b, c = a_tuple
print("a: %s, b: %s, c: %s" % (a, b, c))


############## 辞書 ##############
index = p_index('辞書', index)

# 空の辞書を作成
empty_dict = {}

# 辞書のキーはイミュータブルな型であればOK. また、キーと対応する値が異なる型でもOK
a_dict = {'food': 'orange', 'age': 23, 'sex': 'man', 1: 'one'}
print(a_dict)

# dictの変換
# リストのリスト
b_dict = dict([['a', 'b'], ['c', 'd'], ['e', 'f']])
print(b_dict)

# リストのタプル
b_dict = dict([('a', 'b'), ('c', 'd'), ('e', 'f')])
print(b_dict)

# タプルのリスト
b_dict = dict((['a', 'b'], ['c', 'd'], ['e', 'f']))

# タプルのタプル
b_dict = dict((('a', 'b'), ('c', 'd'), ('e', 'f')))
print(b_dict)

# 2文字のリスト
b_dict = dict(['ab', 'cd', 'ef'])
print(b_dict)

# 2文字のタプル
b_dict = dict(('ab', 'cd', 'ef'))
print(b_dict)

# keyによる要素の取り出し
print(a_dict['age'])
print(a_dict[1])

# keyによる要素の更新
a_dict['age'] = 28
print(a_dict)

# リストと同じく=にすると同時に更新される
d_dict = a_dict
print(d_dict)

# updateによる辞書の結合
c_dict = {'hear': 'short', 2: 'two'}
a_dict.update(c_dict)
print(d_dict)

# 同じkeyがある場合は追加したほうの値が優先される
c_dict = {'hear': 'short', 2: 'two', 'age': 30}
a_dict.update(c_dict)
print(a_dict)

# delによる指定したkeyの要素を削除
del a_dict['food']
print(a_dict)

g# clearによる全ての要素の削除

############## 関数 ##############
index = p_index('関数', index)

if __name__ == '__main__':
    """関数概要
    この関数は、このPythonスクリプトを直接指定して実行したときにのみ実行されます。
    """
    print(sys.version)
