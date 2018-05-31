from django.test import TestCase
import code_assessment.settings
from .assessment.phpmd import PHPMDWrapper

# Create your tests here.
class PHPMDWrapperTestCase(TestCase):
    def test_assess_returns_xml(self):
        phpmd = PHPMDWrapper()
        file_path = code_assessment.settings.BASE_DIR + '/feedback_app/tmp/test.php'
        output_type = 'xml'
        ruleset = 'codesize'
        output = phpmd.assess(file_path, output_type, ruleset)

        self.assertIsInstance(output, str)
        self.assertIn('<?xml version="1.0" encoding="UTF-8" ?>', output)
