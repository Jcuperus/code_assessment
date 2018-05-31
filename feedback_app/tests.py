from django.test import TestCase
import code_assessment.settings
from .utils import AssessmentHelper

# Create your tests here.
class AssessmentHelperTestCase(TestCase):
    def test_assess_code_returns_xml(self):
        file_path = code_assessment.settings.BASE_DIR + '/feedback_app/tmp/test.php'
        output_type = 'xml'
        ruleset = 'codesize'
        output = AssessmentHelper.assess_code([file_path, output_type, ruleset])

        self.assertIsInstance(output, str)
        self.assertIn('<?xml version="1.0" encoding="UTF-8" ?>', output)
