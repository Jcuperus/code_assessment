import subprocess
from django.core.files.storage import default_storage
from django.core.files import File 

from code_assessment.settings import MEDIA_ROOT
from .wrappers import PHPCodeSnifferWrapper, PHPMessDetectorWrapper

def save_file(file):
    file_path = 'tmp/tmp.php'

    default_storage.save(file_path, file)

    # with File(default_storage.open(file_path)) as destination:
        # for chunk in file.chunks():
            # destination.write(chunk)

    return MEDIA_ROOT + file_path

def get_assessments(path):    
    testing_engines = [PHPCodeSnifferWrapper(), PHPMessDetectorWrapper()]
    assessments = []

    for engine in testing_engines:
        assessments.append(engine.assess(path))

    return assessments