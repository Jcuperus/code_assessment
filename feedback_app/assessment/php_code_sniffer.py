import code_assessment.settings
from .cli_tool_wrapper import CliToolWrapper

class PHPCodeSnifferWrapper(CliToolWrapper):
    def __init__(self):
        super(PHPCodeSnifferWrapper, self).__init__(code_assessment.settings.BASE_DIR + '/vendor/squizlabs/php_codesniffer/bin/phpcs')

    def getAssessmentCommand(self, path, rules='PSR2', output_type='xml'):
        return [self.cli_path, path, '--standard=' + rules, '--report=' + output_type]
