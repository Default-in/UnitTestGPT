import openai
from backend.openai.constants import CHATGPTConstants
from settings.base import OPENAI_API_KEY


class ChatGptAPI:
    def __init__(self):
        self.openai_api_key = OPENAI_API_KEY
        self.chatgpt_constants = CHATGPTConstants()
        self._set_openai_api_key()

    def _set_openai_api_key(self):
        openai.api_key = self.openai_api_key

    def _call_openai_completion(self, prompt):

        try:
            response = openai.Completion.create(
                engine=self.chatgpt_constants.COMPLETION_ENGINE,
                prompt=prompt,
                max_tokens=self.chatgpt_constants.COMPLETION_MAX_TOKENS,
                n=1,
                stop=None,
                temperature=self.chatgpt_constants.COMPLETION_TEMPERATURE,
            )
            return True, response
        except openai.InvalidRequestError as e:
            return False, f"call_chatgpt \n Input too long \n {e}"
        except Exception as e:
            return False, str(e)

    def _call_openai_chat_completion(self, prompt):

        try:
            response = openai.ChatCompletion.create(
                engine=self.chatgpt_constants.CHAT_COMPLETION_ENGINE,
                prompt=prompt,
                max_tokens=self.chatgpt_constants.CHAT_COMPLETION_MAX_TOKENS,
                n=1,
                stop=None,
                temperature=self.chatgpt_constants.CHAT_COMPLETION_TEMPERATURE,
            )
            return True, response
        except openai.InvalidRequestError as e:
            return False, f"call_chatgpt \n Input too long \n {e}"
        except Exception as e:
            return False, str(e)

    def completion(self, prompt):
        return self._call_openai_completion(prompt)

    def chat_completion(self, prompt):
        return self._call_openai_chat_completion(prompt)
