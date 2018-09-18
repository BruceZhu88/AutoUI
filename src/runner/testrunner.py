
# Author: Bruce.Zhu(Jialin)

import unittest
import datetime
from .HTMLTestRunner import HTMLTestRunner


class TestRunner(object):
    """docstring for TestRunner"""

    def __init__(self):
        pass

    @staticmethod
    def add_test(tc):
        t_u = unittest.TestSuite()
        for test in tc:
            t_u.addTest(unittest.makeSuite(test))
        return t_u

    @staticmethod
    def run(name, title, tester, testunit):
        report_name = '{}_test_report_{}.html'.format(name, datetime.datetime.now().strftime('%m%d%H%M%S'))
        report_path = './templates/report/{}'.format(report_name)
        with open(report_path, 'wb') as fp:
            runner = HTMLTestRunner(
                stream=fp,
                title=title,
                # description=description,
                tester=tester,
                verbosity=2)
            runner.run(testunit)
        return report_name
