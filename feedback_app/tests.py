from django.test import TestCase
import code_assessment.settings
from .assessment.wrappers import PHPMessDetectorWrapper, PHPCodeSnifferWrapper
from .models import Assessment, SourceFile, Error

# Create your tests here.
class PHPMessDetectorWrapperTestCase(TestCase):
    test_file_path = code_assessment.settings.BASE_DIR + '/feedback_app/tmp/test.php'

    def test_assess_raw_returns_xml(self):
        phpmd = PHPMessDetectorWrapper()
        output = phpmd.assessRaw(self.test_file_path)

        self.assertIsInstance(output, str)
        self.assertIn('<?xml version="1.0" encoding="UTF-8"', output)

    def test_assess_returns_errors(self):
        phpmd = PHPMessDetectorWrapper()
        assessment = phpmd.assess(self.test_file_path)
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

    def test_assess_raw_returns_xml(self):
        phpcs = PHPCodeSnifferWrapper()
        output = phpcs.assessRaw(self.test_file_path)

        self.assertIsInstance(output, str)
        self.assertIn('<?xml version="1.0" encoding="UTF-8"', output)

    def test_assess_returns_errors(self):
        phpcs = PHPCodeSnifferWrapper()
        assessment = phpcs.assess(self.test_file_path)
        self.assertIsInstance(assessment, Assessment)
        
        assessment_files = assessment.sourcefile_set.all()
        self.assertTrue(len(assessment_files) > 0)

        for source_file in assessment_files:
            self.assertIsInstance(source_file, SourceFile)
            file_errors = source_file.error_set.all()
            self.assertTrue(len(file_errors) > 0)

            for error in file_errors:
                self.assertIsInstance(error, Error)
