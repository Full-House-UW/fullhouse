import pep8
import os
from django.test import TestCase
from django.conf import settings


class StyleGuide(TestCase):
    def test_fullhouse_FullHouse(self):
        filepath = os.path.join(settings.PROJECT_ROOT,
                                'fullhouse/FullHouse')
        arglist = [filepath]
        pep8.process_options(arglist)
        pep8.input_dir(filepath)
        #self.assertEquals(pep8.get_count(), 0, 'Style Guide Errors')

    def test_fullhouse_dashboard_py(self):
        ''' Check style guide in dashboard root level. This excludes the
        south migration folder.
        '''
        filepath = os.path.join(settings.PROJECT_ROOT,
                                'fullhouse/dashboard/*.py')

        arglist = [filepath]
        pep8.process_options(arglist)
        pep8.input_dir(filepath)
        #self.assertEquals(pep8.get_count(), 0, 'Style Guide Errors')

    def test_fullhouse_settings(self):
        filepath = os.path.join(settings.PROJECT_ROOT,
                                'fullhouse/settings')

        arglist = [filepath]
        pep8.process_options(arglist)
        pep8.input_dir(filepath)
        #self.assertEquals(pep8.get_count(), 0, 'Style Guide Errors')

    def test_fullhouse_test(self):
        filepath = os.path.join(settings.PROJECT_ROOT,
                                'fullhouse/test')

        arglist = [filepath]
        pep8.process_options(arglist)
        pep8.input_dir(filepath)
        #self.assertEquals(pep8.get_count(), 0, 'Style Guide Errors')
