from django.test import TestCase
import code_assessment.settings
from .assessment.wrappers import PHPMessDetectorWrapper, PHPCodeSnifferWrapper

# Create your tests here.
class PHPMessDetectorWrapperTestCase(TestCase):
    test_file_path = code_assessment.settings.BASE_DIR + '/feedback_app/tmp/test.php'

    def test_assess_returns_xml(self):
        phpmd = PHPMessDetectorWrapper()
        output = phpmd.assess(self.test_file_path)

        self.assertIsInstance(output, str)
        self.assertIn('<?xml version="1.0" encoding="UTF-8"', output)
        print(output)

    def test_parse_command_output_returns(self):
        phpmd = PHPMessDetectorWrapper()
        raw_output = phpmd.assess(self.test_file_path)

        parsed_output = phpmd.parseCommandOutput(raw_output)

        self.assertNotEqual(raw_output, parsed_output)

class PHPCodeSnifferTestCase(TestCase):
    test_file_path = code_assessment.settings.BASE_DIR + '/feedback_app/tmp/test.php'

    def test_assess_returns_data(self):
        phpcs = PHPCodeSnifferWrapper()
        output = phpcs.assess(self.test_file_path)

        self.assertIsInstance(output, str)
        self.assertIn('<?xml version="1.0" encoding="UTF-8"', output)
        print(output)
