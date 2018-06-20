import subprocess
from xml.etree import ElementTree

import code_assessment.settings
from feedback_app.models import Assessment, SourceFile, Error

class CliToolWrapper(object):
    def __init__(self, cli_path, rules, output_type):
        """CliToolWrapper constructor
        
        Arguments:
            object {CliToolWrapper} -- Reference to the created class instance
            cli_path {str} -- Path that is used to run commands with the relevant command line tool
            rules {str} -- String representing the used assessment rules that are passed to the relevant command line argument
            output_type {str} -- String representing the format the raw data will be returned as
        """
        self.cli_path = cli_path
        self.rules = rules
        self.output_type = output_type

    @staticmethod
    def factory(name):
        """CliToolWrapper factory method, allows for easy creation of child classes
        
        Arguments:
            name {str} -- Child class name
        
        Returns:
            CliToolWrapper -- wrapper instance object
        """

        if name == 'phpcs' or name == 'PHPCodeSnifferWrapper':
            return PHPCodeSnifferWrapper()
        elif name == 'phpmd' or name == 'PHPMessDetectorWrapper':
            return PHPMessDetectorWrapper()

    def assess(self, file):
        """Returns a parsed representation the provided files' assessment
        
        Arguments:
            file {SourceFile} -- The file that is assessed by the assessment tool
        
        Returns:
            SourceFile -- The provided source file with added error objects
        """
        return self.parse_command_output(self.assess_raw(file.name), file)

    def assess_raw(self, path):
        """Assesses the provided file and returns a string formatted in the set output format
        
        Arguments:
            path {str} -- Path to the assessed file
        
        Returns:
            str -- A formatted string containing a assessment of the commmand line tool
        """
        output = subprocess.run(self.get_assessment_command(path), stdout=subprocess.PIPE)
        return output.stdout.decode('utf-8')

    def get_assessment_command(self, path):
        """Returns the appropriate command for the command line tool and passes in all relevant arguments
        
        Arguments:
            path {str} -- Path to the file that is selected for assessment
        
        Raises:
            NotImplementedError -- Method is abstract, must be implemented by children
        """
        raise NotImplementedError

    def parse_command_output(self, output, source_file):
        """Parses the command assessment output to Error models and adds them to the provided SourceFile
        
        Arguments:
            output {str} -- Raw assessment output in the desired format for parsing
            source_file {SourceFile} -- File that was used for assessment
        
        Raises:
            NotImplementedError -- Method is abstract, must be implemented by children
        """
        raise NotImplementedError

class PHPCodeSnifferWrapper(CliToolWrapper):
    def __init__(self, cli_path=code_assessment.settings.BASE_DIR + '/vendor/squizlabs/php_codesniffer/bin/phpcs', rules='PSR2', output_type='xml'):
        super(PHPCodeSnifferWrapper, self).__init__(cli_path, rules, output_type)

    def get_assessment_command(self, path):
        """Returns the appropriate command for phpcs and passes in the rules and output_type args
        
        Arguments:
            path {str} -- Path to the file that is selected for assessment
        
        Returns:
            List<str> -- Returned phpcs command with appropriate arguments
        """
        return [self.cli_path, path, '--standard=' + self.rules, '--report=' + self.output_type]

    def parse_command_output(self, output, source_file):
        """Parses the command line tool output in xml format to Error models and addeds them to the provided SourceFile
        
        Arguments:
            output {str} -- Raw assessment output in the desired format for parsing
            source_file {SourceFile} -- File that was used for assessment
        
        Returns:
            SourceFile -- Assessed file with added Error objects
        """
        try:
            root = ElementTree.fromstring(output)

            if root.find('file') != None:
                for file_node in root.findall('file'):
                    for error_node in file_node.findall('error'):
                        Error.objects.create(
                            source_file = source_file,
                            begin_line = error_node.get('line'),
                            end_line = error_node.get('line'),
                            priority = error_node.get('severity'), 
                            category = error_node.get('source'),
                            source = 'phpcs',
                            text = error_node.text)
                return source_file
            return None
        except ElementTree.ParseError:
            return None

class PHPMessDetectorWrapper(CliToolWrapper):
    def __init__(self, cli_path=code_assessment.settings.BASE_DIR + '/vendor/phpmd/phpmd/src/bin/phpmd', rules='cleancode,codesize,controversial,design,naming,unusedcode', output_type='xml'):
        super(PHPMessDetectorWrapper, self).__init__(cli_path, rules, output_type)

    def get_assessment_command(self, path):
        """Returns the appropriate command for phpcs and passes in the rules and output_type args
        
        Arguments:
            path {str} -- Path to the file that is selected for assessment
        
        Returns:
            List<str> -- Returned phpcs command with appropriate arguments
        """
        return [self.cli_path, path, self.output_type, self.rules]

    def parse_command_output(self, output, source_file):
        """Parses the command line tool output in xml format to Error models and addeds them to the provided SourceFile
        
        Arguments:
            output {str} -- Raw assessment output in the desired format for parsing
            source_file {SourceFile} -- File that was used for assessment
        
        Returns:
            SourceFile -- Assessed file with added Error objects
        """
        try:
            root = ElementTree.fromstring(output)

            if root.find('file') != None:
                for file_node in root.findall('file'):
                    for error_node in file_node.findall('violation'):
                        Error.objects.create(
                            source_file = source_file,
                            begin_line = error_node.get('beginline'),
                            end_line = error_node.get('endline'),
                            priority = error_node.get('priority'),
                            category = error_node.get('rule'),
                            source = 'phpmd',
                            text = error_node.text)
                return source_file
            return None
        except ElementTree.ParseError:
            return None
