from enum import Enum

import openai
from backend.openai.constants import CHATGPTConstants
from settings.base import OPENAI_API_KEY


class OpenAIParameters(Enum):
    PROMPT_LOSS_WEIGHT = "prompt_loss_weight"
    LEARNING_RATE_MULTIPLIER = "learning_rate_multiplier"
    BATCH_SIZE = "batch_size"
    N_EPOCHS = "n_epochs"
    VALIDATION_FILE = "validation_file"
    TRAINING_FILE = "training_file"
    MODEL = "model"
    MESSAGE = "messages"
    TEMPERATURE = "temperature"
    TOP_P = "top_p"
    N = "n"
    STREAM = "stream"
    STOP = "stop"
    MAX_TOKENS = "max_tokens"
    PRESENCE_PENALTY = "presence_penalty"
    FREQUENCY_PENALTY = "frequency_penalty"
    LOGIT_BIAS = "logit_bias"
    USER = "user"
    PROMPT = "prompt"
    SUFFIX = "suffix"
    TEMP = "temp"
    LOGPROBS = "logprobs"
    ECHO = "echo"
    BEST_OF = "best_of"
    INPUT = "input"


class ChatGptAPI:
    def __init__(self):
        self.openai_api_key = OPENAI_API_KEY
        self.chatgpt_constants = CHATGPTConstants()
        self._set_openai_api_key()

    def _set_openai_api_key(self):
        openai.api_key = self.openai_api_key

    def _call_openai_completion(self, model, prompt, suffix=None, max_tokens=16, temp=1, top_p=1, n=1, stream=False,
                                logprobs=None, echo=False, stop=None, presence_penalty=0, frequency_penalty=0,
                                best_of=1, logit_bias=None, user=None):

        try:
            params = {
                OpenAIParameters.MODEL.value: model,
                OpenAIParameters.PROMPT.value: prompt,
                OpenAIParameters.SUFFIX.value: suffix,
                OpenAIParameters.MAX_TOKENS.value: max_tokens,
                OpenAIParameters.TEMPERATURE.value: temp,
                OpenAIParameters.TOP_P.value: top_p,
                OpenAIParameters.N.value: n,
                OpenAIParameters.STREAM.value: stream,
                OpenAIParameters.LOGPROBS.value: logprobs,
                OpenAIParameters.ECHO.value: echo,
                OpenAIParameters.STOP.value: stop,
                OpenAIParameters.PRESENCE_PENALTY.value: presence_penalty,
                OpenAIParameters.FREQUENCY_PENALTY.value: frequency_penalty,
                OpenAIParameters.BEST_OF.value: best_of,
                OpenAIParameters.LOGIT_BIAS.value: logit_bias,
                OpenAIParameters.USER.value: user
            }

            response = openai.Completion.create(**params)
            return True, response['choices'][0]['text']
        except openai.InvalidRequestError as e:
            return False, f"call_chatgpt \n Input too long \n {e}"
        except Exception as e:
            return False, str(e)

    def _call_openai_chat_completion(self, model, message, temperature, top_p, n, stream, stop, max_tokens,
                                     presence_penalty, frequency_penalty, logit_bias, user):

        try:
            params = {
                OpenAIParameters.MODEL.value: model,
                OpenAIParameters.MESSAGE.value: message,
                OpenAIParameters.TEMPERATURE.value: temperature,
                OpenAIParameters.TOP_P.value: top_p,
                OpenAIParameters.N.value: n,
                OpenAIParameters.STREAM.value: stream,
                OpenAIParameters.STOP.value: stop,
                OpenAIParameters.MAX_TOKENS.value: max_tokens,
                OpenAIParameters.PRESENCE_PENALTY.value: presence_penalty,
                OpenAIParameters.FREQUENCY_PENALTY.value: frequency_penalty,
                OpenAIParameters.LOGIT_BIAS.value: logit_bias,
                OpenAIParameters.USER.value: user,

            }

            response = openai.ChatCompletion.create(**params)

            return True, response['choices'][0]['message']

        except Exception as e:

            return False, str(e)

    def _call_openai_embeddings(self, model, documents):
        try:
            params = {
                OpenAIParameters.MODEL.value: model,
                OpenAIParameters.INPUT.value: documents
            }

            response = openai.Embedding.create(**params)
            return True, response["data"][0]["embedding"]

        except Exception as e:
            return False, str(e)

    def _call_openai_fine_tune(self, training_file, validation_file, model="curie", n_epochs=4,
                               batch_size=None, learning_rate_multipler=None, prompt_loss_weight=None,
                               ):
        try:
            params = {
                OpenAIParameters.TRAINING_FILE.value: training_file,
                OpenAIParameters.VALIDATION_FILE.value: validation_file,
                OpenAIParameters.MODEL.value: model,
                OpenAIParameters.N_EPOCHS.value: n_epochs,
                OpenAIParameters.BATCH_SIZE.value: batch_size,
                OpenAIParameters.LEARNING_RATE_MULTIPLIER.value: learning_rate_multipler,
                OpenAIParameters.PROMPT_LOSS_WEIGHT.value: prompt_loss_weight
            }

            response = openai.FineTune.create(**params)
            return True, response["id"]
        except Exception as e:
            return False, str(e)

    def _upload_file(self, file_path, purpose):

        response = openai.File.create(
            file=open(file_path, "rb"),
            purpose=purpose
        )

        return response["id"]

    # ------------------------------
    # Public methods
    # ------------------------------

    def completion(self, model, prompt, suffix=None, max_tokens=16, temp=1, top_p=1, n=1, stream=False,
                   logprobs=None, echo=False, stop=None, presence_penalty=0, frequency_penalty=0,
                   best_of=1, logit_bias=None, user=None):

        return self._call_openai_completion(model, prompt, suffix=suffix, max_tokens=max_tokens, temp=temp, top_p=top_p,
                                            n=n, stream=stream,
                                            logprobs=logprobs, echo=echo, stop=stop, presence_penalty=presence_penalty,
                                            frequency_penalty=frequency_penalty,
                                            best_of=best_of, logit_bias=logit_bias, user=user)

    def chat_completion(self, model, message, temperature=1, top_p=1, n=1, stream=False, stop=None,
                        max_tokens=16,
                        presence_penalty=0, frequency_penalty=0, logit_bias=None, user=None):

        return self._call_openai_chat_completion(model=model, message=message, temperature=temperature, top_p=top_p,
                                                 n=n, stream=stream, stop=stop, max_tokens=max_tokens,
                                                 presence_penalty=presence_penalty, frequency_penalty=frequency_penalty,
                                                 logit_bias=logit_bias, user=user)

    def embeddings(self, model, documents):
        return self._call_openai_embeddings(model, documents)

    def fine_tune(self, training_file_path, purpose, validation_file_path="", model="curie", n_epochs=4,
                  batch_size=None, learning_rate_multipler=None, prompt_loss_weight=None,
                  ):

        training_file = self._upload_file(training_file_path, purpose)
        validation_file = None

        if validation_file_path != "":
            validation_file = open(validation_file_path, "rb")

        return self._call_openai_fine_tune(training_file=training_file, validation_file=validation_file, model=model,
                                           n_epochs=n_epochs,
                                           batch_size=batch_size, learning_rate_multipler=learning_rate_multipler,
                                           prompt_loss_weight=prompt_loss_weight, )


