import subprocesss

import code_assessment.settings

class PHPCodeSnifferWrapper(object):
    def __init__(self):
        self.cli_path = code_assessment.settings.BASE_DIR + '/vendor/squizlabs/php_codesniffer/bin/phpcs'

    def assess(self, filepath):
        command = [self.cli_path, '--help']
        output = subprocesss.run(command, stdout=subprocesss.PIPE)
        return output.stdout.decode('utf-8')