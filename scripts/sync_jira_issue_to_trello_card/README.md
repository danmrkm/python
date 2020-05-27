# sync_jira_issue_to_trello_card

## 概要
JIRA の複数プロジェクトの課題を TRELLO の特定のボードにカードとして同期させるスクリプト

## 事前準備

### 1. ATLASSIAN の API トークンを取得
[Atlassian API トークンの取得](https://confluence.atlassian.com/cloud/api-tokens-938839638.html)
のページを参考に JIRA にアクセス可能な API Token を取得する

### 2. Trello の API キー、API トークンを取得
[Trello API トークンの取得](https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/)
のページを参考に Trello にアクセス可能な API Key, API Token を取得する

### 3. Trello 側へのリストの追加
JIRA のステータスに対応させるため、Trello のリストを作成、編集する。
デフォルトでは以下 5 つのパターンのリストを想定。

- backlog
- todo
- inprogress
- pending
- done

### 4. Trello 側で JIRA 連携の Power-Up を有効化する
Trello の JIRA 連携 Power-Up 機能を有効化し、連携させたい JIRA Project の課題をカードに連携できるように設定する。
[Jira Power-Upを使用する](https://help.trello.com/article/1081-using-the-jira-power-up)

### 5. 各種パラメータの設定
`run.py` の各パラメータについて、設定する。設定項目は以下。

| 項目 | 内容 |
| --- | --- |
| JIRA_BASE_URL | JIRA Project API Endpoint の BASE URL を設定 |
| TRELLO_BASE_URL | Trello の API Endpoint の BASE URL を設定 |
| JIRA_USER_ID | Jira のユーザ ID (基本はメールアドレス) |
| JIRA_API_TOKEN | 上記の手順で取得した JIRA にアクセスするための API トークン |
| TRELLO_BOARD_ID | JIRA の課題を同期させたい Trello のボート ID を指定（Trello のボードの URL のランダム文字列）|
| TRELLO_API_KEY | 上記の手順で取得した　Trello にアクセスするための API キー |
| TRELLO_API_TOKEN | 上記の手順で取得した　Trello にアクセスするための API トークン |
| JIRA_PROJECT | 同期させたい JIRA プロジェクトを LIST 型で指定（複数指定可）|
| TRELLO_JIRA_STATUS_MAPPING | JIRA のステータスと Trello のリストをマッピングする設定|

## 実行
`python3 run.py`
で実行可能。
