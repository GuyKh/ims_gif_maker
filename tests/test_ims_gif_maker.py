# Sample Test passing with nose and pytest
from ims_gif_maker import ImsGifMaker
import unittest
import os.path


class TestIms(unittest.TestCase):
    def test_create_latest_gif(self):
        ims = ImsGifMaker('/Users/guyk/workspace/python/ims_gif_maker/tmp', '/Users/guyk/workspace/python/ims_gif_maker/output')
        ims.run()
        assert os.path.exists('/Users/guyk/workspace/python/ims_gif_maker/output/movie.gif'), "File Exists"
