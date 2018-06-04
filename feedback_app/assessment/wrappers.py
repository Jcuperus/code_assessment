import subprocess
from xml.etree import ElementTree

import code_assessment.settings
from feedback_app.models import Assessment, SourceFile, Error

class CliToolWrapper(object):
    def __init__(self, cli_path):
        self.cli_path = cli_path

    def assess(self, path, rules, output_type):
        output = subprocess.run(self.getAssessmentCommand(path, rules, output_type), stdout=subprocess.PIPE)
        return output.stdout.decode('utf-8')

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
        root = ElementTree.fromstring(output)

        if root.find('file') != None:
            assessment = Assessment()
            assessment.save()
            
            for file_node in root.findall('file'):
                source_file = SourceFile(assessment = assessment, name = file_node.get('name'))
                source_file.save()
                
                for error_node in file_node.findall('error'):
                    error = Error(source_file = source_file, 
                            begin_line = error_node.get('line'),
                            end_line = error_node.get('line'),
                            priority = error_node.get('severity'), 
                            category = error_node.get('source'), 
                            text = error_node.text)
                    error.save()
            return assessment
        return None

class PHPMessDetectorWrapper(CliToolWrapper):
    def __init__(self):
        super(PHPMessDetectorWrapper, self).__init__(code_assessment.settings.BASE_DIR + '/vendor/phpmd/phpmd/src/bin/phpmd')

    def assess(self, path, rules='cleancode,codesize,controversial,design,naming,unusedcode', output_type='xml'):
        return super(PHPMessDetectorWrapper, self).assess(path, rules, output_type)

    def getAssessmentCommand(self, path, rules, output_type):
        return [self.cli_path, path, output_type, rules]

    def parseCommandOutput(self, output):
        root = ElementTree.fromstring(output)

        if root.find('file') != None:
            assessment = Assessment()
            assessment.save()

            for file_node in root.findall('file'):
                source_file = SourceFile(assessment = assessment, name = file_node.get('name'))
                source_file.save()

                for error_node in file_node.findall('violation'):
                    error = Error(source_file = source_file,
                            begin_line = error_node.get('beginline'),
                            end_line = error_node.get('endline'),
                            priority = error_node.get('priority'),
                            category = error_node.get('rule'),
                            text = error_node.text)
                    error.save()
            return assessment
        return None
