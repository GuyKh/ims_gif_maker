# Sample Test passing with nose and pytest
import unittest

class TestSample(unittest.TestCase):
    
    def test_pass(self):
        assert True, "dummy sample test"
