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


def unit_tests_from_function(
        function_to_test: str,
        language: str = "python",
        unit_test_package: str = "pytest",
        approx_min_cases_to_cover: int = 7,
        print_text: bool = False,
        explain_model: str = "gpt-3.5-turbo",
        plan_model: str = "gpt-3.5-turbo",
        execute_model: str = "gpt-3.5-turbo-16k",
        temperature: float = 0.4,
        reruns_if_fail: int = 1,
):
    """Returns a unit test for a given function, using a 3-step GPT prompt."""

    # Step 1: Generate an explanation of the function
    explain_system_message = {
        "role": "system",
        "content": f"You are a world-class {language} developer with an eagle eye for unintended bugs and edge cases. "
                   "You carefully explain code with great detail and accuracy. You organize your explanations in "
                   "markdown-formatted, bulleted lists.",
    }
    explain_user_message = {
        "role": "user",
        "content": f"""Please explain the following {language} function. Review what each element of the function is 
        doing precisely and what the author's intentions may have been. Organize your explanation as a 
        markdown-formatted, bulleted list.

    ```{language}
    {function_to_test}
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

    # Step 2: Generate a plan to write a unit test
    plan_user_message = {
        "role": "user",
        "content": f"""A good unit test suite should aim to:
                        - Test the function's behavior for a wide range of possible inputs
                        - Test edge cases that the author may not have foreseen
                        - Take advantage of the features of `{unit_test_package}` to make the tests easy to write and 
                          maintain - Be easy to read and understand, with clean code and descriptive names - Be 
                          deterministic, so that the tests always pass or fail in the same way

            To help unit test the function above, list diverse scenarios that the function should be able to handle (
            and under each scenario, include a few examples as sub-bullets).""",
    }
    plan_messages = [
        explain_system_message,
        explain_user_message,
        explain_assistant_message,
        plan_user_message,
    ]
    if print_text:
        print_messages([plan_user_message])
    plan_response = openai.ChatCompletion.create(
        model=plan_model,
        messages=plan_messages,
        temperature=temperature,
        stream=True,
    )
    plan = ""
    for chunk in plan_response:
        delta = chunk["choices"][0]["delta"]
        if print_text:
            print_message_delta(delta)
        if "content" in delta:
            plan += delta["content"]
    plan_assistant_message = {"role": "assistant", "content": plan}

    # Step 2b: If the plan is short, ask GPT to elaborate further
    num_bullets = max(plan.count("\n-"), plan.count("\n*"))
    elaboration_needed = num_bullets < approx_min_cases_to_cover
    if elaboration_needed:
        elaboration_user_message = {
            "role": "user",
            "content": f"""In addition to those scenarios above, list a few rare or unexpected edge cases (and as 
            before, under each edge case, include a few examples as sub-bullets).""",
        }
        elaboration_messages = [
            explain_system_message,
            explain_user_message,
            explain_assistant_message,
            plan_user_message,
            plan_assistant_message,
            elaboration_user_message,
        ]
        if print_text:
            print_messages([elaboration_user_message])
        elaboration_response = openai.ChatCompletion.create(
            model=plan_model,
            messages=elaboration_messages,
            temperature=temperature,
            stream=True,
        )
        elaboration = ""
        for chunk in elaboration_response:
            delta = chunk["choices"][0]["delta"]
            if print_text:
                print_message_delta(delta)
            if "content" in delta:
                elaboration += delta["content"]
        elaboration_assistant_message = {"role": "assistant", "content": elaboration}

    # Step 3: Generate the unit test
    execute_system_message = {
        "role": "system",
        "content": f"You are a world-class {language} developer with an eagle eye for unintended bugs and edge cases. "
                   "You write careful, accurate unit tests. When asked to reply only with code, you write all of your "
                   "code in a single block.",
    }
    execute_user_message = {
        "role": "user",
        "content": f"""Using {language} and the `{unit_test_package}` package, write a suite of unit tests for the 
        function, following the cases above. Include helpful comments to explain each line. Reply only with code, 
        formatted as follows:

```{language}
# imports used for our unit tests including {unit_test_package}
{{insert other imports as needed}}

# function to test
{function_to_test}

# unit tests
{{insert unit test code here}}
```""",
    }
    execute_messages = [
        execute_system_message,
        explain_user_message,
        explain_assistant_message,
        plan_user_message,
        plan_assistant_message,
    ]
    if elaboration_needed:
        execute_messages += [elaboration_user_message, elaboration_assistant_message]
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

    # Check the output for errors
    code = execution.split(f"```{language}")[1].split("```")[0].strip()
    process = [execute_messages, execution]
    # Return the entire process and unit test code as a string
    return process, code
