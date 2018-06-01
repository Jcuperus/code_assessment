from django.test import TestCase
import code_assessment.settings
from .assessment.wrappers import PHPMessDetectorWrapper, PHPCodeSnifferWrapper

# Create your tests here.
class PHPMessDetectorWrapperTestCase(TestCase):
    def test_assess_returns_xml(self):
        phpmd = PHPMessDetectorWrapper()
        file_path = code_assessment.settings.BASE_DIR + '/feedback_app/tmp/test.php'
        output = phpmd.assess(file_path, 'codesize', 'xml')

        self.assertIsInstance(output, str)
        self.assertIn('<?xml version="1.0" encoding="UTF-8"', output)

class PHPCodeSnifferTestCase(TestCase):
    def test_assess_returns_data(self):
        phpcs = PHPCodeSnifferWrapper()
        file_path = code_assessment.settings.BASE_DIR + '/feedback_app/tmp/test.php'
        output = phpcs.assess(file_path, 'PSR2', 'xml')

        self.assertIsInstance(output, str)
        self.assertIn('<?xml version="1.0" encoding="UTF-8"', output)
