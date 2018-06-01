import code_assessment.settings
from .cli_tool_wrapper import CliToolWrapper

class PHPMDWrapper(CliToolWrapper):
    def __init__(self):
        super(PHPMDWrapper, self).__init__(code_assessment.settings.BASE_DIR + '/vendor/phpmd/phpmd/src/bin/phpmd')

    def getAssessmentCommand(self, path, rules, output_type='xml'):
        return [self.cli_path, path, output_type, rules]
