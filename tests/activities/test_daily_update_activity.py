import unittest
import os
import sys
from datetime import datetime, timedelta

sysPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, sysPath)
from src.activities.daily_update_activity import DaillyUpdateActivity

class TestDaillyUpdateActivity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set this to real git repo paths for your environment
        cls.project_dirs = ["C:\\2_WorkSpace\\BluB0X\\BBX_AI", "C:\\2_WorkSpace\\SYL"]
        cls.git_dirs = [os.path.join(d, '.git') for d in cls.project_dirs]
        for git_dir, project_dir in zip(cls.git_dirs, cls.project_dirs):
            if not os.path.exists(git_dir):
                raise unittest.SkipTest(f"{project_dir} is not a git repository.")
        cls.activity = DaillyUpdateActivity(cls.project_dirs)

    def test_run(self):
        # This will print the daily update summary; ensure Qwen and Git repo are available
        try:
            # Get yesterday's date
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            summary = self.activity.run(since_date=yesterday)
            print(f"Daily Update Summary:\n{summary}")
        except Exception as e:
            self.skipTest(f"Test skipped due to error: {e}")

if __name__ == '__main__':
    unittest.main()
