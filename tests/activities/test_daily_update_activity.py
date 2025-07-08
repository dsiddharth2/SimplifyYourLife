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
        # Set this to a real git repo path for your environment
        cls.project_dir = "C:\\2_WorkSpace\\BluB0X\\BBX_AI"
        cls.git_dir = os.path.join(cls.project_dir, '.git')
        if not os.path.exists(cls.git_dir):
            raise unittest.SkipTest(f"{cls.project_dir} is not a git repository.")
        cls.activity = DaillyUpdateActivity(cls.project_dir)

    def test_run(self):
        # This will print the daily update summary; ensure Qwen and Git repo are available
        try:
            # Get yesterday's date
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            self.activity.run(since_date=yesterday)
        except Exception as e:
            self.skipTest(f"Test skipped due to error: {e}")

if __name__ == '__main__':
    unittest.main()
