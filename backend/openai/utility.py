from typing import Optional

import requests

from backend.openai.constants import CHATGPTConstants
from settings.base import OPENAI_API_KEY, CHAT_GPT_LOGIN_BEARER_TOKEN


class ChatGptUtility:
    def __init__(self):
        self.openai_api_key = OPENAI_API_KEY
        self.chatgpt_constants = CHATGPTConstants()
        self.openai_bearer_token = CHAT_GPT_LOGIN_BEARER_TOKEN

    def _chatgpt_login(self, token) -> tuple[bool, Optional[dict]]:
        headers = {
            'Authorization': 'Bearer ' + str(token)
        }

        response = requests.post(self.chatgpt_constants.LOGIN, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None

    def _chatgpt_credits(self, token) -> (bool, dict):
        headers = {
            'Authorization': 'Bearer ' + str(token)
        }
        response = requests.get(self.chatgpt_constants.CREDIT_GRANTS, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None

    def _get_session_id_after_login(self, ):
        status, response = self._chatgpt_login(self.openai_bearer_token)

        if status:
            return response.get("user").get("session").get("sensitive_id")

    # --------------------------------
    #     Public methods
    # --------------------------------
    def chatgpt_usage(self, start_date, end_date) -> (bool, dict):
        url = self.chatgpt_constants.USAGE.format(start_date=start_date, end_date=end_date)

        headers = {
            'Authorization': 'Bearer ' + str(self.openai_api_key)
        }
        response = requests.get(url, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None

    def chatgpt_credits(self, ):
        session_id = self._get_session_id_after_login()
        status, response = self._chatgpt_credits(session_id)

        if status:
            return response
