import subprocess
import code_assessment.settings

def assess_code(args):
    assessment_tool_path = code_assessment.settings.BASE_DIR + '/vendor/phpmd/phpmd/src/bin/phpmd'
    command = [assessment_tool_path] + args
    command_output = subprocess.run(command, stdout=subprocess.PIPE)
    return command_output.stdout.decode('utf-8')

def test():
    file_path = code_assessment.settings.BASE_DIR + '/feedback_app/tmp/test.php'
    output_type = 'xml'
    rulesets = 'codesize,unusedcode,naming'

    print(assess_code([file_path, output_type, rulesets]))