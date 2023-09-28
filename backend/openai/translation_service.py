import ast

import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY
openai.organization = settings.OPENAI_ORGANIZATION_ID

color_prefix_by_role = {
    "system": "\033[0m",  # gray
    "user": "\033[0m",  # gray
    "assistant": "\033[92m",  # green
}


def print_messages(messages, color_prefix_by_role=color_prefix_by_role):
    """Prints messages sent to or from GPT."""
    for message in messages:
        role = message["role"]
        color_prefix = color_prefix_by_role[role]
        content = message["content"]
        print(f"{color_prefix}\n[{role}]\n{content}")


def print_message_delta(delta, color_prefix_by_role=color_prefix_by_role):
    """Prints a chunk of messages streamed back from GPT."""
    if "role" in delta:
        role = delta["role"]
        color_prefix = color_prefix_by_role[role]
        print(f"{color_prefix}\n[{role}]\n", end="")
    elif "content" in delta:
        content = delta["content"]
        print(content, end="")


def translate_code(
        initial_code: str,
        initial_language: str,
        target_language: str,
        print_text: bool = False,
        explain_model: str = "gpt-3.5-turbo",
        execute_model: str = "gpt-3.5-turbo-16k",
        temperature: float = 0.4,
        reruns_if_fail: int = 1,
):
    """Translates given code to target language, using a 3-step GPT prompt."""

    # Step 1: Generate an explanation of the code
    explain_system_message = {
        "role": "system",
        "content": f"You are a world-class {initial_language} developer with an eagle eye for "
                   "unintended bugs and edge cases. "
                   "You carefully explain code with great detail and accuracy. You organize your explanations in "
                   "markdown-formatted, bulleted lists.",
    }
    explain_user_message = {
        "role": "user",
        "content": f"""Please explain the following {initial_language} code. Review what each element of the function is 
        doing precisely and what the author's intentions may have been. Organize your explanation as a 
        markdown-formatted, bulleted list.

    ```{initial_language}
    {initial_code}
    ```""",
    }
    explain_messages = [explain_system_message, explain_user_message]
    if print_text:
        print_messages(explain_messages)

    explanation_response = openai.ChatCompletion.create(
        model=explain_model,
        messages=explain_messages,
        temperature=temperature,
        stream=True,
    )
    explanation = ""
    for chunk in explanation_response:
        delta = chunk["choices"][0]["delta"]
        if print_text:
            print_message_delta(delta)
        if "content" in delta:
            explanation += delta["content"]
    explain_assistant_message = {"role": "assistant", "content": explanation}

    # Step 2: Generate a plan for translating the code
    execute_system_message = {
        "role": "system",
        "content": f"You are a world-class {target_language} developer with an eagle eye for unintended bugs and edge "
                   "cases. You write efficient, accurate code according to a given explanation. When asked to reply "
                   "only with code, you write all of your code in a single block.",
    }
    execute_user_message = {
        "role": "user",
        "content": f"""Following the cases above, write code in {target_language}. Include helpful comments to 
        explain each line. Reply only with code, formatted as follows:

```{target_language}
# imports used 
{{insert imports used in the translated code}}

# translated code
{{insert translated code here}}
```""",
    }
    execute_messages = [
        execute_system_message,
        explain_user_message,
        explain_assistant_message,
    ]

    execute_messages += [execute_user_message]
    if print_text:
        print_messages([execute_system_message, execute_user_message])

    execute_response = openai.ChatCompletion.create(
        model=execute_model,
        messages=execute_messages,
        temperature=temperature,
        stream=True,
    )
    execution = ""
    for chunk in execute_response:
        delta = chunk["choices"][0]["delta"]
        if print_text:
            print_message_delta(delta)
        if "content" in delta:
            execution += delta["content"]

    split_by_language = execution.split(f"```{target_language}")
    if len(split_by_language) > 1:
        translated_code = split_by_language[1].split("```")[0].strip()
        print(translated_code)
    else:
        translated_code = execution
    process = [execute_messages, execution]
    return process, translated_code


code = """package main

import (
    "fmt"
)

func binarySearch(arr []int, target int) int {
    left := 0
    right := len(arr) - 1

    for left <= right {
        mid := left + (right-left)/2

        if arr[mid] == target {
            return mid
        } else if arr[mid] < target {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }

    return -1 // Element not found
}

func main() {
    arr := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    target := 6

    index := binarySearch(arr, target)

    if index != -1 {
        fmt.Printf("Element %d found at index %d\n", target, index)
    } else {
        fmt.Printf("Element %d not found in the array\n", target)
    }
}
"""
#
# translate_code(initial_code=code,
#                initial_language="golang",
#                target_language="python",
#                print_text=False
#                )
