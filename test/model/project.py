import unittest

from unittest.mock import MagicMock
from marshmallow.exceptions import ValidationError

from lynx.model import *


class ProjectTestCase(unittest.TestCase):
    def test_project_dump(self):
        project = Project()
        project.id = MagicMock(return_value=1)
        data = ProjectSchema().dump(project)
        self.assertEqual(data['id'], 1)

    def test_project_load(self):
        data = dict(id=1, name='Mark 1', description='This is a test project for testing project schema.')
        project = ProjectSchema().load(data)
        self.assertEqual(project['id'], 1)

    def test_project_load_validate(self):
        with self.assertRaises(ValidationError):
            data = dict(name='Mark 1', description='This is a test project for testing project schema.')
            ProjectSchema().load(data)
        with self.assertRaises(ValidationError):
            data = dict(id=1, description='This is a test project for testing project schema.')
            ProjectSchema().load(data)
        with self.assertRaises(ValidationError):
            data = dict(id=1, name='Mark 1')
            ProjectSchema().load(data)


if __name__ == '__main__':
    unittest.main()
