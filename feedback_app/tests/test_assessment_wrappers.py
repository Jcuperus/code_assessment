from xml.etree import ElementTree
from django.test import TestCase, TransactionTestCase, tag
from code_assessment.settings import BASE_DIR
from feedback_app.assessment.wrappers import CliToolWrapper, PHPMessDetectorWrapper, PHPCodeSnifferWrapper
from feedback_app.models import Assessment, SourceFile, Error

TEST_FILE_PATH = BASE_DIR + '/feedback_app/tmp/test.php'

@tag('wrappers', 'assessment')
class CliToolWrapperTestCase(TestCase):
    def test_factory_creates_all_children(self):
        clitools = CliToolWrapper.__subclasses__()

        phpcs = CliToolWrapper.factory('phpcs')
        self.assertIsInstance(phpcs, PHPCodeSnifferWrapper)

        phpmd = CliToolWrapper.factory('phpmd')
        self.assertIsInstance(phpmd, PHPMessDetectorWrapper)


@tag('phpmd', 'wrappers', 'assessment')
class PHPMessDetectorWrapperTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.assessment = Assessment.objects.create()
        cls.source_file = SourceFile.objects.create(assessment=cls.assessment, name=TEST_FILE_PATH)
        cls.phpmd = PHPMessDetectorWrapper()

        phpmd_el = ElementTree.Element('pmd')
        file = ElementTree.SubElement(phpmd_el, 'file')
        error1 = ElementTree.SubElement(file, 'violation', {
            'beginline': '1',
            'endline': '2',
            'priority': '1',
            'rule': 'test'
        })
        error1.text = 'error'
        error2 = ElementTree.SubElement(file, 'violation', {
            'beginline': '2',
            'endline': '3',
            'priority': '2',
            'rule': 'test2'
        })
        error2.text = 'hello'
        cls.xml = ElementTree.tostring(phpmd_el)
    
    def test_assess_raw_returns_valid_xml(self):
        """Tests whether the assess_raw method returns valid xml for the default test file
        
        Arguments:
            TestCase {TestCase} -- Reference to current test instance
        """
        output = self.phpmd.assess_raw(TEST_FILE_PATH)

        self.assertIsInstance(output, str)
        self.assertIn('<?xml version="1.0" encoding="UTF-8"', output)
        
        try:
            ElementTree.fromstring(output)
        except ElementTree.ParseError:
            self.fail('fromstring() raised ParseError, xml could not be parsed.')

    def test_assess_returns_errors(self):
        source_file = self.phpmd.assess(self.source_file)
        self.assertIsInstance(source_file, SourceFile)
        self.assertGreater(len(self.assessment.sourcefile_set.all()), 0)

        for error in source_file.error_set.all():
            self.assertIsInstance(error, Error)

    def test_parse_xml_output_parses_xml(self):
        source_file = self.phpmd.parse_command_output(self.xml, self.source_file)
        self.assertEqual(len(source_file.error_set.all()), 2)

    def test_parse_xml_invalid_xml(self):
        xml = ''
        output = self.phpmd.parse_command_output(xml, self.source_file)

        self.assertIsNone(output)
        self.assertEqual(len(self.source_file.error_set.all()), 0)

@tag('phpcs', 'wrappers', 'assessment')
class PHPCodeSnifferTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.assessment = Assessment.objects.create()
        cls.source_file = SourceFile.objects.create(assessment=cls.assessment, name=TEST_FILE_PATH)
        cls.phpcs = PHPCodeSnifferWrapper()

        phpmd_el = ElementTree.Element('phpcs')
        file = ElementTree.SubElement(phpmd_el, 'file')
        error1 = ElementTree.SubElement(file, 'error', {
            'line': '1',
            'severity': '1',
            'source': 'test'
        })
        error1.text = 'error'
        error2 = ElementTree.SubElement(file, 'error', {
            'line': '2',
            'severity': '2',
            'source': 'test2'
        })
        error2.text = 'hello'
        cls.xml = ElementTree.tostring(phpmd_el)

    def test_assess_raw_returns_valid_xml(self):
        output = self.phpcs.assess_raw(TEST_FILE_PATH)

        self.assertIsInstance(output, str)
        self.assertIn('<?xml version="1.0" encoding="UTF-8"', output)

        try:
            ElementTree.fromstring(output)
        except ElementTree.ParseError:
            self.fail('fromstring() raised ParseError, xml could not be parsed.')

    def test_assess_returns_errors(self):
        source_file = self.phpcs.assess(self.source_file)
        self.assertIsInstance(source_file, SourceFile)
        self.assertGreater(len(self.assessment.sourcefile_set.all()), 0)

        for error in source_file.error_set.all():
            self.assertIsInstance(error, Error)

    def test_parse_xml_output_parses_xml(self):
        source_file = self.phpcs.parse_command_output(self.xml, self.source_file)
        self.assertEqual(len(source_file.error_set.all()), 2)

    def test_parse_xml_invalid_xml(self):
        xml = ''
        output = self.phpcs.parse_command_output(xml, self.source_file)

        self.assertIsNone(output)
        self.assertEqual(len(self.source_file.error_set.all()), 0)