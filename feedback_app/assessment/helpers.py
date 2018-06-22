import subprocess
from django.core.files.uploadedfile import TemporaryUploadedFile

from .wrappers import CliToolWrapper
from feedback_app.models import Assessment, SourceFile     

def get_tmp_file_paths(files):
    """Returns a list of paths to temporarily stored files
    
    Arguments:
        files {TemporaryUploadFile} -- List containing uploaded files
    
    Returns:
        List<str> -- List of paths to given files
    """
    tmp_file_paths = []
    for file in files:
        if isinstance(file, TemporaryUploadedFile):
            tmp_file_paths.append(file.temporary_file_path())
    return tmp_file_paths

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