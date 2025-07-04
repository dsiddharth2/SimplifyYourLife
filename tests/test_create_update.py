import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DaillyUpdate.create_update import get_git_status, main
from git import Repo

class TestCreateUpdate(unittest.TestCase):
    def setUp(self):
        self.test_dir = "C:\\2_WorkSpace\\BluB0X\\BBX_AI"

    @unittest.skip("Skipping test_get_git_status as it requires a git repository setup")
    def test_get_git_status(self):
        # Initialize a git repo in the temp dir
        added, modified, removed = get_git_status(self.test_dir)
        print('Added:', added)
        print('Modified:', modified)
        print('Removed:', removed)
        self.assertIsInstance(added, list)
        self.assertIsInstance(modified, list)
        self.assertIsInstance(removed, list)
        
    def test_call_main(self):
        # Initialize a git repo in the temp dir
        a_= main(self.test_dir)
    #end def
    
if __name__ == '__main__':
    unittest.main()