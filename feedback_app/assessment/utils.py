import subprocess
import code_assessment.settings
from .php_code_sniffer import PHPCodeSnifferWrapper

def save_file(file):
    tmp_file_path = code_assessment.settings.BASE_DIR + '/feedback_app/tmp/tmp.php'

    with open(tmp_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return tmp_file_path

def get_feedback(path):
    phpcs = PHPCodeSnifferWrapper()
    feedback = phpcs.assess(path, 'PSR2', 'xml')
    return feedback