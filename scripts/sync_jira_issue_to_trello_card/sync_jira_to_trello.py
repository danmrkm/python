#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
import string
import json


class SyncJiraToTrello:
    """
    指定された複数の Project のJIRA の課題を Trello に同期させるクラス
    """

    def __init__(
        self,
        jira_base_url,
        jira_user_id,
        jira_api_key,
        jira_project_list,
        trello_base_url,
        trello_board_id,
        trello_api_key,
        trello_api_token,
        trello_jira_status_mapping,
    ):
        self.jira_base_url = jira_base_url
        self.jira_user_id = jira_user_id
        self.jira_api_key = jira_api_key
        self.jira_project_list = jira_project_list
        self.trello_base_url = trello_base_url
        self.trello_board_id = trello_board_id
        self.trello_api_key = trello_api_key
        self.trello_api_token = trello_api_token
        self.trello_jira_status_mapping = trello_jira_status_mapping
        self.trello_lists = []
        self.trello_cards = []
        self.trello_labels = []

    def main(self):
        """
        docstringを記載
        """

        # label を取得
        self.trello_labels = self.list_trello_labels()
        labelname_list = [i["name"] for i in self.trello_labels]

        # 未使用カラーリスト作成
        all_colors = [
            "orange",
            "yellow",
            "green",
            "red",
            "purple",
            "blue",
            "sky",
            "lime",
            "pink",
            "black",
        ]
        reserved_colors = all_colors.copy()
        for label in self.trello_labels:
            if (label["color"] in reserved_colors) and (label["name"] != ""):
                reserved_colors.remove(label["color"])

        # Trello のラベルに存在しない、JIRA ProjectKEY のラベルを作成
        for projectkey in self.jira_project_list:
            if projectkey not in labelname_list:
                if len(reserved_colors) == 0:
                    new_label_color = all_colors[0]
                else:
                    new_label_color = reserved_colors[0]
                    self.create_trello_label(projectkey, new_label_color)
                    reserved_colors.remove(new_label_color)

        # Trello の list 一覧を取得
        self.trello_lists = self.list_trello_lists()

        # Trello の カード一覧を取得
        self.trello_cards = self.list_trello_cards()

        trello_card_list = {}

        for card in self.trello_cards:
            jira_issue_key = ""

            if ":" in card["name"]:
                jira_issue_key = card["name"].split(":")[0]
            else:
                continue

            trello_card_list[jira_issue_key] = {
                "id": card["id"],
                "name": card["name"],
                "description": card["desc"],
                "idList": card["idList"],
                "idBoard": card["idBoard"],
                "idLabels": card["idLabels"],
            }

        # JIRA のステータス一覧を取得
        # for projectkey in self.jira_project_list:
        #     self.get_jira_status_list(projectkey)

        # JIRA の自分の担当課題の一覧を取得
        for projectkey in self.jira_project_list:
            print("============ " + projectkey + "  ============")

            # ラベルの ID を取得
            trello_label_id = self.get_trello_labelid_from_jira_projectkey(projectkey)
            issue_list = self.get_jira_issue_list(projectkey)

            for issue in issue_list:
                issue_key = issue["key"]
                if issue_key in trello_card_list.keys():
                    # すでに課題にリンクしたカードがある場合は、内容の更新要否を確認し、必要であれば更新する。
                    params = {}
                    # タイトル
                    if (issue_key + ": " + issue["fields"]["summary"]) != (
                        trello_card_list[issue_key]["name"]
                    ):
                        params["name"] = issue_key + ": " + issue["fields"]["summary"]

                    # 説明文
                    # memo: JIRA 側の形式が特殊なため、更新しない
                    # if issue["summary"] != (trello_card_list[issue_key]["name"]):
                    #     params["name"] = issue_key + ": " + issue["summary"]

                    # ステータス
                    if (
                        self.get_trello_listid_from_jira_status(
                            issue["fields"]["status"]["name"]
                        )
                        != trello_card_list[issue_key]["idList"]
                    ):
                        params["idList"] = self.get_trello_listid_from_jira_status(
                            issue["fields"]["status"]["name"]
                        )

                    # ラベル
                    if trello_label_id not in trello_card_list[issue_key]["idLabels"]:
                        params["idLabel"] = trello_label_id

                    # 情報の更新がひとつでもあれば、カードをアップデート
                    if len(params.keys()) > 0:
                        self.update_trello_card(
                            trello_card_list[issue_key]["id"], params
                        )
                        print("Updaded: " + trello_card_list[issue_key]["name"])
                else:
                    if issue["fields"]["resolution"] is None:
                        # まだ課題にリンクしたカードがない場合
                        params = {
                            "name": issue_key + ": " + issue["fields"]["summary"],
                            "desc": "",
                            "pos": "bottom",
                            "idList": self.get_trello_listid_from_jira_status(
                                issue["fields"]["status"]["name"]
                            ),
                        }

                        # 新規カード作成
                        new_card = self.create_trello_card(params)
                        new_card_id = new_card["id"]

                        # ラベル追加
                        self.add_trello_label_to_card(new_card_id, trello_label_id)

                        # JIRA Link 追加
                        self.add_trello_issuelink_to_card(
                            new_card_id, self.jira_base_url + "/browse/" + issue_key
                        )
                        print(
                            "Created: " + issue_key + ": " + issue["fields"]["summary"]
                        )

    def get_trello_listid_from_jira_status(self, status):
        """
        JIRA Status から対応する Trello の list の id を返す
        """

        if len(self.trello_lists) < 1:
            raise "self.trello_lists is empty"

        trello_list_name = ""
        for j in self.trello_jira_status_mapping.keys():
            if status in self.trello_jira_status_mapping[j]["jira"]:
                trello_list_name = self.trello_jira_status_mapping[j]["trello"]

        if trello_list_name == "":
            trello_list_name = self.trello_jira_status_mapping["inprogress"]["trello"]

        for trello_list in self.trello_lists:
            if trello_list["name"] == trello_list_name:
                return trello_list["id"]

        return self.trello_lists[0]["id"]

    def get_jira_status_list(self, projectkey):
        """
        JIRA の特定プロジェクトのステータス一覧を取得
        """
        url = self.jira_base_url + "/rest/api/3/project/" + projectkey + "/statuses"
        headers = {"User-Agent": "curl", "content-type": "application/json"}
        r = requests.get(
            url, headers=headers, auth=(self.jira_user_id, self.jira_api_key),
        )
        result = json.loads(r.text)
        print(projectkey)
        statuses = [i["untranslatedName"] for i in result[0]["statuses"]]

        for status in statuses:
            print(status + ": " + self.get_trello_listid_from_jira_status(status))

    def get_jira_issue_list(self, projectkey):
        """
        JIRA の特定プロジェクトの課題一覧を取得
        """
        url = self.jira_base_url + "/rest/api/3/search"
        pointer = 0

        issue_list = []
        counter = 0
        while True:
            counter += 1
            query = {
                "jql": 'project="' + projectkey + '" AND assignee = currentuser()',
                "startAt": pointer,
            }

            headers = {"User-Agent": "curl", "content-type": "application/json"}

            r = requests.get(
                url,
                headers=headers,
                auth=(self.jira_user_id, self.jira_api_key),
                params=query,
            )
            issue_list.extend(json.loads(r.text)["issues"])

            if (len(issue_list) >= json.loads(r.text)["total"]) or (counter > 200):
                break
            pointer = len(issue_list)

        return issue_list

    def generate_trello_new_id(self):
        """
        Trello 用の新しい ID を生成する
        """
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=32))

    def list_trello_labels(self):
        """
        Trello のボードのラベル一覧を取得
        """

        url = self.trello_base_url + "/1/boards/" + self.trello_board_id + "/labels"

        headers = {"User-Agent": "curl", "content-type": "application/json"}

        query = {"key": self.trello_api_key, "token": self.trello_api_token}

        r = requests.get(url, headers=headers, params=query)
        result = json.loads(r.text)
        return result

    def list_trello_cards(self):
        """
        Trello のボードのラベル一覧を取得
        """

        url = self.trello_base_url + "/1/boards/" + self.trello_board_id + "/cards"

        headers = {"User-Agent": "curl", "content-type": "application/json"}

        query = {"key": self.trello_api_key, "token": self.trello_api_token}

        r = requests.get(url, headers=headers, params=query)
        return json.loads(r.text)

    def get_trello_labelid_from_jira_projectkey(self, label_name):
        """
        Trello のラベルの ID を返す
        """

        if len(self.trello_labels) < 1:
            raise "self.trello_labels is empty"

        for label in self.trello_labels:
            if label_name == label["name"]:
                return label["id"]

        return self.trello_labels[0]["id"]

    def list_trello_lists(self):
        """
        Trello のボードのリストを取得
        """
        url = self.trello_base_url + "/1/boards/" + self.trello_board_id + "/lists"

        headers = {"User-Agent": "curl", "content-type": "application/json"}

        query = {"key": self.trello_api_key, "token": self.trello_api_token}

        r = requests.get(url, headers=headers, params=query)
        return json.loads(r.text)

    def update_trello_card(self, card_id, params):
        """
        Trello のカード情報をアップデート
        """

        url = self.trello_base_url + "/1/cards/" + card_id

        headers = {"User-Agent": "curl", "content-type": "application/json"}

        params["key"] = self.trello_api_key
        params["token"] = self.trello_api_token

        r = requests.put(url, headers=headers, params=params)
        return json.loads(r.text)

    def add_trello_label_to_card(self, card_id, label_id):
        """
        Trello のカードにラベルを追加
        """

        url = self.trello_base_url + "/1/cards/" + card_id + "/idLabels"

        headers = {"User-Agent": "curl", "content-type": "application/json"}

        query = {
            "key": self.trello_api_key,
            "token": self.trello_api_token,
            "value": label_id,
        }

        r = requests.put(url, headers=headers, params=query)
        return json.loads(r.text)

    def add_trello_issuelink_to_card(self, card_id, jira_issue_url):
        """
        Trello のカードに JIRA 課題のリンクを追加
        """

        url = self.trello_base_url + "/1/cards/" + card_id + "/attachments"

        headers = {"User-Agent": "curl", "content-type": "application/json"}

        query = {
            "key": self.trello_api_key,
            "token": self.trello_api_token,
            "name": jira_issue_url,
            "url": jira_issue_url,
        }

        r = requests.post(url, headers=headers, params=query)
        return json.loads(r.text)

    def create_trello_card(self, params):
        """
        Trello のカードを新規作成する
        """

        url = self.trello_base_url + "/1/cards"

        headers = {"User-Agent": "curl", "content-type": "application/json"}

        params["key"] = self.trello_api_key
        params["token"] = self.trello_api_token

        r = requests.post(url, headers=headers, params=params)
        return json.loads(r.text)

    def create_trello_label(self, label_name, label_color):
        """
        Trello のボードのラベルを新規作成
        """

        url = self.trello_base_url + "/1/boards/" + self.trello_board_id + "/labels"

        headers = {"User-Agent": "curl", "content-type": "application/json"}

        query = {
            "key": self.trello_api_key,
            "token": self.trello_api_token,
            "id": self.generate_trello_new_id(),
            "name": label_name,
            "color": label_color,
        }

        r = requests.post(url, headers=headers, params=query)
        return json.loads(r.text)
