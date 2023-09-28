from frontend.google_sheets.actions import GoogleSheet
from settings.celery import app


@app.task(queue='unittestgpt')
def write_code_generation_data_into_google_sheet(
        action: str,
        initial_language: str,
        input_code: str,
        target_language: str,
        unit_test_package: str,
        result: str,
        process: str
):
    google_sheet = GoogleSheet()
    google_sheet.write_row([action, initial_language, input_code, target_language, unit_test_package, result, process])
    return True
