from django.test import TestCase
import code_assessment.settings
from .assessment.wrappers import PHPMessDetectorWrapper, PHPCodeSnifferWrapper
from .models import Assessment, SourceFile, Error

# Create your tests here.
class PHPMessDetectorWrapperTestCase(TestCase):
    test_file_path = code_assessment.settings.BASE_DIR + '/feedback_app/tmp/test.php'

    def test_assess_returns_xml(self):
        phpmd = PHPMessDetectorWrapper()
        output = phpmd.assess(self.test_file_path)

        self.assertIsInstance(output, str)
        self.assertIn('<?xml version="1.0" encoding="UTF-8"', output)

    def test_parse_command_output_returns(self):
        phpmd = PHPMessDetectorWrapper()
        raw_output = phpmd.assess(self.test_file_path)
        assessment = phpmd.parseCommandOutput(raw_output)

        self.assertIsInstance(assessment, Assessment)
        
        assessment_files = assessment.sourcefile_set.all()
        self.assertTrue(len(assessment_files) > 0)

        for source_file in assessment_files:
            self.assertIsInstance(source_file, SourceFile)
            file_errors = source_file.error_set.all()
            self.assertTrue(len(file_errors) > 0)

            for error in file_errors:
                self.assertIsInstance(error, Error)

class PHPCodeSnifferTestCase(TestCase):
    test_file_path = code_assessment.settings.BASE_DIR + '/feedback_app/tmp/test.php'

    def test_assess_returns_data(self):
        phpcs = PHPCodeSnifferWrapper()
        output = phpcs.assess(self.test_file_path)

        self.assertIsInstance(output, str)
        self.assertIn('<?xml version="1.0" encoding="UTF-8"', output)

    def test_parse_command_output_returns_data(self):
        phpcs = PHPCodeSnifferWrapper()
        raw_output = phpcs.assess(self.test_file_path)
        assessment = phpcs.parseCommandOutput(raw_output)
        
        self.assertIsInstance(assessment, Assessment)
        
        assessment_files = assessment.sourcefile_set.all()

        self.assertTrue(len(assessment_files) > 0)

        for source_file in assessment_files:
            self.assertIsInstance(source_file, SourceFile)
            file_errors = source_file.error_set.all()
            self.assertTrue(len(file_errors) > 0)

            for error in file_errors:
                self.assertIsInstance(error, Error)
