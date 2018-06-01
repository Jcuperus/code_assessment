import subprocess

class CliToolWrapper(object):
    def __init__(self, cli_path):
        self.cli_path = cli_path

    def assess(self, path, rules, output_type):
        output = subprocess.run(self.getAssessmentCommand(path, rules, output_type), stdout=subprocess.PIPE)
        return output.stdout.decode('utf-8')

    def getAssessmentCommand(self, path, rules, output_type):
        raise NotImplementedError