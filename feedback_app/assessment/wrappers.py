import subprocess
from xml.etree import ElementTree

import code_assessment.settings

class CliToolWrapper(object):
    def __init__(self, cli_path):
        self.cli_path = cli_path

    def assess(self, path, rules, output_type):
        output = subprocess.run(self.getAssessmentCommand(path, rules, output_type), stdout=subprocess.PIPE)
        return self.parseCommandOutput(output.stdout.decode('utf-8'))

    def getAssessmentCommand(self, path, rules, output_type):
        raise NotImplementedError

    def parseCommandOutput(self, output):
        raise NotImplementedError

class PHPCodeSnifferWrapper(CliToolWrapper):
    def __init__(self):
        super(PHPCodeSnifferWrapper, self).__init__(code_assessment.settings.BASE_DIR + '/vendor/squizlabs/php_codesniffer/bin/phpcs')

    def assess(self, path, rules='PSR2', output_type='xml'):
        return super(PHPCodeSnifferWrapper, self).assess(path, rules, output_type)

    def getAssessmentCommand(self, path, rules, output_type):
        return [self.cli_path, path, '--standard=' + rules, '--report=' + output_type]

    def parseCommandOutput(self, output):
        xml = ElementTree.fromstring(output)

        print(xml)

        return output

class PHPMessDetectorWrapper(CliToolWrapper):
    def __init__(self):
        super(PHPMessDetectorWrapper, self).__init__(code_assessment.settings.BASE_DIR + '/vendor/phpmd/phpmd/src/bin/phpmd')

    def assess(self, path, rules='cleancode,codesize,controversial,design,naming,unusedcode', output_type='xml'):
        return super(PHPMessDetectorWrapper, self).assess(path, rules, output_type)

    def getAssessmentCommand(self, path, rules, output_type):
        return [self.cli_path, path, output_type, rules]

    def parseCommandOutput(self, output):
        return output