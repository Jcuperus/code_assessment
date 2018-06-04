import subprocess
import code_assessment.settings
from .wrappers import PHPCodeSnifferWrapper, PHPMessDetectorWrapper

def save_file(file):
    tmp_file_path = code_assessment.settings.BASE_DIR + '/feedback_app/tmp/tmp.php'

    with open(tmp_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return tmp_file_path

def get_assessments(path):    
    testing_engines = [PHPCodeSnifferWrapper(), PHPMessDetectorWrapper()]
    assessments = []

    for engine in testing_engines:
        assessments.append(engine.assess(path))

    return assessments