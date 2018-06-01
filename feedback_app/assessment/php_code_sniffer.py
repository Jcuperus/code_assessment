import subprocess

import code_assessment.settings

class PHPCodeSnifferWrapper(object):
    def __init__(self):
        self.cli_path = code_assessment.settings.BASE_DIR + '/vendor/squizlabs/php_codesniffer/bin/phpcs'

    def assess(self, filepath, code_standard='PSR2', report_type='xml'):
        command = [self.cli_path, filepath, '--standard=' + code_standard, '--report=' + report_type]
        output = subprocess.run(command, stdout=subprocess.PIPE)
        return output.stdout.decode('utf-8')
