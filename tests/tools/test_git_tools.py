import unittest
import os
import sys

sysPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, sysPath)
from src.tools.git_tools import GitTools

class TestGitTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set this to a real git repo path for your environment
        cls.project_dir = "C:\\2_WorkSpace\\SYL"
        cls.git_dir = os.path.join(cls.project_dir, '.git')
        if not os.path.exists(cls.git_dir):
            raise unittest.SkipTest(f"{cls.project_dir} is not a git repository.")
        cls.git_tools = GitTools(cls.project_dir, mark_as_safe=True)

    def test_get_current_changes(self):
        result = self.git_tools.get_current_changes(with_diffs=True)
        self.assertIsInstance(result, dict)
        self.assertIn('added', result)
        self.assertIn('modified', result)
        self.assertIn('removed', result)
        self.assertIn('diffs', result)
        # Diffs should be a dict
        self.assertIsInstance(result['diffs'], dict)

    def test_get_changes_since_date(self):
        # Use a date far in the past to ensure some commits exist
        result = self.git_tools.get_changes_since_date('2025-07-01', with_diffs=True)
        self.assertIsInstance(result, dict)
        self.assertIn('changed_files', result)
        self.assertIn('diffs', result)
        self.assertIsInstance(result['changed_files'], list)
        self.assertIsInstance(result['diffs'], dict)

if __name__ == '__main__':
    unittest.main()
