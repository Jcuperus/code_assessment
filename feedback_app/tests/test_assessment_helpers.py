from django.test import TestCase, tag
from django.core.files import File
from django.core.files.uploadedfile import UploadedFile
from code_assessment.settings import BASE_DIR
from feedback_app.models import Assessment, Error
from feedback_app.assessment.helpers import assess

TEST_FILE_PATH = BASE_DIR + '/feedback_app/tmp/test.php'
TEST_FILE_2_PATH = BASE_DIR + '/feedback_app/tmp/test2.php'

@tag('helpers', 'assessment')
class AssessmentHelperTestCase(TestCase):
    def test_assess_returns_valid_assessment_for_one_file(self):
        files = [TEST_FILE_PATH]

        assessment = assess(files)
        
        self.assertIsInstance(assessment, Assessment)
        self.assertEqual(len(assessment.sourcefile_set.all()), len(files))

        for source_file in assessment.sourcefile_set.all():
            self.assertGreater(len(source_file.error_set.all()), 0)
            
            for error in source_file.error_set.all():
                self.assertIsInstance(error, Error)

    @tag('helpers', 'assessments')
    def test_assess_returns_valid_assessment_for_multiple_files(self):
        files = [TEST_FILE_PATH, TEST_FILE_2_PATH]

        assessment = assess(files)

        self.assertIsInstance(assessment, Assessment)
        self.assertEqual(len(assessment.sourcefile_set.all()), len(files))

        for source_file in assessment.sourcefile_set.all():
            self.assertGreater(len(source_file.error_set.all()), 0)

            for error in source_file.error_set.all():
                self.assertIsInstance(error, Error)