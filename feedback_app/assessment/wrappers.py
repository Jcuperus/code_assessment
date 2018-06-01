import subprocess
import code_assessment.settings

class CliToolWrapper(object):
    def __init__(self, cli_path):
        self.cli_path = cli_path

    def assess(self, path, rules, output_type):
        output = subprocess.run(self.getAssessmentCommand(path, rules, output_type), stdout=subprocess.PIPE)
        return output.stdout.decode('utf-8')

    def getAssessmentCommand(self, path, rules, output_type):
        raise NotImplementedError

class PHPCodeSnifferWrapper(CliToolWrapper):
    def __init__(self):
        super(PHPCodeSnifferWrapper, self).__init__(code_assessment.settings.BASE_DIR + '/vendor/squizlabs/php_codesniffer/bin/phpcs')

    def getAssessmentCommand(self, path, rules='PSR2', output_type='xml'):
        return [self.cli_path, path, '--standard=' + rules, '--report=' + output_type]

class PHPMessDetectorWrapper(CliToolWrapper):
    def __init__(self):
        super(PHPMessDetectorWrapper, self).__init__(code_assessment.settings.BASE_DIR + '/vendor/phpmd/phpmd/src/bin/phpmd')

    def getAssessmentCommand(self, path, rules, output_type='xml'):
        return [self.cli_path, path, output_type, rules]
