import subprocess
from django.core.files.storage import default_storage

from code_assessment.settings import MEDIA_ROOT
from .wrappers import PHPCodeSnifferWrapper, PHPMessDetectorWrapper
from .wrappers import CliToolWrapper
from feedback_app.models import Assessment, SourceFile

def save_file(file):
    """Saves a given file to the temporary file storage location. Returns file path
    
    Arguments:
        file {InputFile} -- Request file object
    
    Returns:
        str -- Temporary file storage location
    """

    file_path = 'tmp/tmp.php'

    with default_storage.open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return MEDIA_ROOT + file_path

def get_assessments(path):    
    testing_engines = [PHPCodeSnifferWrapper(), PHPMessDetectorWrapper()]
    assessments = []

    for engine in testing_engines:
        assessments.append(engine.assess(path))

    return assessments

def assess(files):
    """Runs an assessment for all provided files for all relevant testing tools
    
    Arguments:
        files {List<SourceFile>} -- Collection of assessed source files
    
    Returns:
        Assessment -- Assessment object containing all files and their respective errors
    """
    testing_tools = [CliToolWrapper.factory('phpcs'), CliToolWrapper.factory('phpmd')]
    assessment = Assessment.objects.create()

    for file in files:
        source_file = SourceFile.objects.create(assessment=assessment, name=file)
        for tool in testing_tools:
            tool.assess(source_file)

    return assessment