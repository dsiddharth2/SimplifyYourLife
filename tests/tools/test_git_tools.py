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
        cls.project_dirs = ["C:\\2_WorkSpace\\SYL", "C:\\2_WorkSpace\\BluB0X\\BluB0X_Web_2"]
        cls.git_dirs = [os.path.join(d, '.git') for d in cls.project_dirs]
        for git_dir, project_dir in zip(cls.git_dirs, cls.project_dirs):
            if not os.path.exists(git_dir):
                raise unittest.SkipTest(f"{project_dir} is not a git repository.")
        cls.git_tools = GitTools(cls.project_dirs, mark_as_safe=True)

    def test_get_current_changes(self):
        results = self.git_tools.get_current_changes(with_diffs=True)
        self.assertIsInstance(results, list)
        for result in results:
            if result is None:
                continue
            self.assertIn('added', result)
            self.assertIn('modified', result)
            self.assertIn('removed', result)
            self.assertIn('project_dir', result)
            self.assertIn('diffs', result)
            self.assertIsInstance(result['diffs'], dict)

    def test_get_changes_since_date(self):
        # Use a date far in the past to ensure some commits exist
        results = self.git_tools.get_changes_since_date('2025-07-01', with_diffs=True, with_commit_messages=True)
        self.assertIsInstance(results, list)
        for result in results:
            if result is None:
                continue
            self.assertIn('changed_files', result)
            self.assertIn('project_dir', result)
            self.assertIn('diffs', result)
            self.assertIsInstance(result['changed_files'], list)
            self.assertIsInstance(result['diffs'], dict)

if __name__ == '__main__':
    unittest.main()
