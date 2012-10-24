import pep8
import os
import unittest

from django.conf import settings


class Pep8Test(unittest.TestCase):

    def test_pep8(self):

        filepath = os.path.join(settings.PROJ_ROOT, 'fullhouse')

        arglist = [filepath]
        pep8.process_options(arglist)
        pep8.input_dir(filepath)

        self.assertEquals(pep8.get_count(), 0, 'No pep8 errors')
