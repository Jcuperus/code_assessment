from subprocess import run

class AssessmentHelper(object):
    
    @staticmethod
    def assess_code(args):
        assessment_tool_path = "../vendor/phpmd/phpmd/src/bin/phpmd"

        run([assessment_tool_path, args])