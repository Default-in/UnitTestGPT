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

    def _call_openai_completion(self, model, prompt, suffix=None, max_tokens=16, temp=1, top_p=1, n=1, stream=False,
                                logprobs=None, echo=False, stop=None, presence_penalty=0, frequency_penalty=0,
                                best_of=1, logit_bias=None, user=None):

        try:
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=max_tokens,
                n=n,
                stop=stop,
                temperature=temp,
                suffix=suffix,
                top_p=top_p,
                stream=stream,
                logprobs=logprobs,
                echo=echo,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                best_of=best_of,
                logit_bias=logit_bias,
                user=user

            )
            return True, response['choices'][0]['text']
        except openai.InvalidRequestError as e:
            return False, f"call_chatgpt \n Input too long \n {e}"
        except Exception as e:
            return False, str(e)

    def _call_openai_chat_completion(self, model, message, temperature, top_p, n, stream, stop, max_tokens,
                                     presence_penalty, frequency_penalty, logit_bias, user):

        try:
            response = openai.ChatCompletion.create(
                engine=model,
                message=message,
                max_tokens=max_tokens,
                n=n,
                stop=stop,
                temperature=temperature,
                user=user,
                logit_bias=logit_bias,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                top_p=top_p,
                stream=stream,
            )
            return True, response['choices'][0]['message']
        except openai.InvalidRequestError as e:
            return False, f"call_chatgpt \n Input too long \n {e}"
        except Exception as e:
            return False, str(e)

    def _call_openai_embeddings(self, model, documents):
        try:
            response = openai.Embed.create(
                engine=model,
                documents=documents
            )
            return True, response["data"][0]["embedding"]

        except Exception as e:
            return False, str(e)

    def _call_openai_fine_tune(self, training_file, validation_file, model="curie", n_epochs=4,
                               batch_size=None, learning_rate_multipler=None, prompt_loss_weight=None,
                               ):
        try:
            response = openai.FineTune.create(
                training_file=training_file,
                validation_file=validation_file,
                model=model,
                n_epochs=n_epochs,
                batch_size=batch_size,
                learning_rate_multipler=learning_rate_multipler,
                prompt_loss_weight=prompt_loss_weight
            )
            return True, response["id"]
        except Exception as e:
            return False, str(e)

    def completion(self, model, prompt, suffix=None, max_tokens=16, temp=1, top_p=1, n=1, stream=False,
                   logprobs=None, echo=False, stop=None, presence_penalty=0, frequency_penalty=0,
                   best_of=1, logit_bias=None, user=None):

        return self._call_openai_completion(model, prompt, suffix=suffix, max_tokens=max_tokens, temp=temp, top_p=top_p,
                                            n=n, stream=stream,
                                            logprobs=logprobs, echo=echo, stop=stop, presence_penalty=presence_penalty,
                                            frequency_penalty=frequency_penalty,
                                            best_of=best_of, logit_bias=logit_bias, user=user)

    def chat_completion(self, model, message, temperature=1, top_p=1, n=1, stream=False, stop=None,
                        max_tokens=float('inf'),
                        presence_penalty=0, frequency_penalty=0, logit_bias=None, user=None):

        return self._call_openai_chat_completion(model=model, message=message, temperature=temperature, top_p=top_p,
                                                 n=n, stream=stream, stop=stop, max_tokens=max_tokens,
                                                 presence_penalty=presence_penalty, frequency_penalty=frequency_penalty,
                                                 logit_bias=logit_bias, user=user)

    def embeddings(self, model, documents):
        return self._call_openai_embeddings(model, documents)

    def upload_file(self, file_path, purpose):

        response = openai.File.create(
            file=open(file_path, "rb"),
            purpose=purpose
        )

        return response["id"]

    def fine_tune(self, training_file_path, purpose, validation_file_path="", model="curie", n_epochs=4,
                  batch_size=None, learning_rate_multipler=None, prompt_loss_weight=None,
                  ):
        training_file = self.upload_file(training_file_path, purpose)
        validation_file = None

        if validation_file_path != "":
            validation_file = open(validation_file_path, "rb")

        return self._call_openai_fine_tune(training_file=training_file, validation_file=validation_file, model=model,
                                           n_epochs=n_epochs,
                                           batch_size=batch_size, learning_rate_multipler=learning_rate_multipler,
                                           prompt_loss_weight=prompt_loss_weight, )
