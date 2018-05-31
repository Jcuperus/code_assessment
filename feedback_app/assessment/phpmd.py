import subprocess

import code_assessment.settings

class PHPMDWrapper(object):
    def __init__(self):
        self.phpmd_path = code_assessment.settings.BASE_DIR + '/vendor/phpmd/phpmd/src/bin/phpmd'

    def assess(self, filepath, output_type, rulesets):
        command = [self.phpmd_path, filepath, output_type, rulesets]
        output = subprocess.run(command, stdout=subprocess.PIPE)
        return output.stdout.decode('utf-8')
