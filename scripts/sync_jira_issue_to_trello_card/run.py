#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sync_jira_to_trello

JIRA_BASE_URL = "https://yourdomain.atlassian.net"
TRELLO_BASE_URL = "https://api.trello.com"

JIRA_USER_ID = "your_jira_user_id"
JIRA_API_KEY = "your_jira_api_key"

TRELLO_BOARD_ID = "your_trello_board_id"
TRELLO_API_KEY = "your_trello_api_key"
TRELLO_API_TOKEN = "your_trello_api_token"


JIRA_PROJECT_LIST = ["JIRA_PROJECT"]

TRELLO_JIRA_STATUS_MAPPING = {
    "backlog": {"trello": "Backlog", "jira": ["Backlog", "バックログ"]},
    "todo": {"trello": "ToDo", "jira": ["To Do", "Selected for Development"]},
    "inprogress": {
        "trello": "In Progress",
        "jira": ["In Progress", "IN PROGRESS", "進行中"],
    },
    "pending": {
        "trello": "Pending",
        "jira": ["レビュー", "サスペンド", "WAITING", "Waiting", "Review"],
    },
    "done": {"trello": "Closed", "jira": ["Done", "完了"]},
}

if __name__ == "__main__":
    # 直接起動のみ実行

    sync_jira_to_trello = sync_jira_to_trello.SyncJiraToTrello(
        JIRA_BASE_URL,
        JIRA_USER_ID,
        JIRA_API_KEY,
        JIRA_PROJECT_LIST,
        TRELLO_BASE_URL,
        TRELLO_BOARD_ID,
        TRELLO_API_KEY,
        TRELLO_API_TOKEN,
        TRELLO_JIRA_STATUS_MAPPING,
    )
    sync_jira_to_trello.main()
