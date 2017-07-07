"""
Unittest for generate a test course in an given modulestore
"""
import unittest
import ddt
from django.core.management import CommandError, call_command

from contentstore.management.commands.generate_test_course import Command
from xmodule.modulestore import ModuleStoreEnum
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.django import modulestore


class TestArgParsing(unittest.TestCase):
    """
    Tests for parsing arguments for the `create_course` management command
    """
    def setUp(self):
        super(TestArgParsing, self).setUp()
        self.command = Command()

    def test_invalid_json(self):
        error_msg = "Invalid JSON"
        with self.assertRaisesRegexp(CommandError, error_msg):
            arg = "invalid_json"
            self.command.handle(arg)

    def test_missing_fields(self):
        error_msg = "JSON must contain the following fields: {}".format(
            ["store","user","name","organization","number","fields"]
        )
        with self.assertRaisesRegexp(CommandError, error_msg):
            arg = "'{}'"
            self.command.handle(arg)

    def test_invalid_store(self):
        error_msg = "Modulestore must be one of {}".format(
            [ModuleStoreEnum.Type.mongo, ModuleStoreEnum.Type.split]
        )
        with self.assertRaisesRegexp(CommandError, error_msg):
            arg = ("'{"
            '"store":"invalid_store"'
            '"user":"user@example.com"'
            '"organization":"test-course-generator"'
            '"number":"1"'
            '"run":"1"'
            '"fields":{"display_name":"test-course"}'
            "}'")
            self.command.handle(arg)

    def test_invalid_user(self):
        error_msg = "User invalid_user not found"
        with self.assertRaisesRegexp(CommandError, error_msg):
            arg = ("'{"
            '"store":"split"'
            '"user":"invalid_user"'
            '"organization":"test-course-generator"'
            '"number":"1"'
            '"run":"1"'
            '"fields":{"display_name":"test-course"}'
            "}'")
            self.command.handle(arg)

    def test_duplicate_course(self):
        error_msg = "Unable to create course for {}".format(
            ["test-course-generate", "1", "1"]
        )
        with self.assertRaisesRegexp(CommandError, error_msg):
            arg = ("'{"
            '"store":"split"'
            '"user":"{}"'
            '"organization":"test-course-generator"'
            '"number":"1"'
            '"run":"1"'
            '"fields":{"display_name":"test-course"}'
            "}'").format(self.user.email)
            self.command.handle(arg)
            self.command.handle(arg)

@ddt.ddt
class TestGenerateTestCourse(ModuleStoreTestCase):
    """
    Unit tests for creating a course in either old mongo or split mongo via command line
    """
    @ddt.data(ModuleStoreEnum.Type.mongo, ModuleStoreEnum.Type.split)
    def test_generate_course_in_stores(self, store):
        arg = ("'{"
            '"store":"{}"'
            '"user":"{}"'
            '"organization":"test-course-generator"'
            '"number":"1"'
            '"run":"1"'
            '"fields":{"display_name":"test-course"}'
            "}'").format(self.user.email,store)
        call_command("generate_test_course", arg)
        key = modulestore().make_course_key("test-course-generator", "1", "1")
        self.assertTrue(modulestore().has_course(key))
