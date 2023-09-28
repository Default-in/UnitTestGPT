import openai.error
from django.shortcuts import render

from backend.openai.translation_service import translate_code
from backend.openai.unit_test_service import unit_tests_from_function
from frontend.constants import UnitTestPackageAccordingToLanguage, PYTHON, JAVASCRIPT, JAVA, PHP, RUST, GO
from frontend.forms import CodeInputForm
from frontend.tasks import write_code_generation_data_into_google_sheet


def process_code(code, initial_language, target_language, action):
    try:
        if action == 'translate':
            process, result = translate_code(initial_code=code, initial_language=initial_language,
                                             target_language=target_language)
            # write_code_generation_data_into_google_sheet(action=action, initial_language=initial_language,
            #                                              input_code=code, target_language=target_language,
            #                                              unit_test_package="", result=result,
            #                                              process=str(process))
        else:
            if initial_language == PYTHON:
                unit_test_package = UnitTestPackageAccordingToLanguage.python
            elif initial_language == JAVASCRIPT:
                unit_test_package = UnitTestPackageAccordingToLanguage.javascript
            elif initial_language == JAVA:
                unit_test_package = UnitTestPackageAccordingToLanguage.java
            elif initial_language == PHP:
                unit_test_package = UnitTestPackageAccordingToLanguage.php
            elif initial_language == RUST:
                unit_test_package = UnitTestPackageAccordingToLanguage.rust
            elif initial_language == GO:
                unit_test_package = UnitTestPackageAccordingToLanguage.go
            else:
                return "Invalid language"
            process, result = unit_tests_from_function(function_to_test=code, language=initial_language,
                                                       unit_test_package=unit_test_package)
            write_code_generation_data_into_google_sheet.delay(action=action, initial_language=initial_language,
                                                               input_code=code, target_language="",
                                                               unit_test_package=unit_test_package, result=result,
                                                               process=str(process))
    except openai.error.RateLimitError:
        result = "OpenAI API rate limit exceeded. Please try again later."
    return result


def code_input_view(request):
    result = None

    if request.method == 'POST':
        form = CodeInputForm(request.POST)
        if form.is_valid():
            # Get form data
            action = form.cleaned_data['action']
            initial_language = form.cleaned_data['initial_language']
            input_code = form.cleaned_data['input_code']
            target_language = form.cleaned_data['target_language']

            # Call your processing function with the form data
            result = process_code(input_code, initial_language, target_language, action)
    else:
        form = CodeInputForm()

    return render(request, 'code_input_form.html', {'form': form, 'result': result})
