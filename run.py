
# Author: Bruce.Zhu(Jialin)

import unittest
import sys
from AutoUI.src.common.Logger import Logger
from AutoUI.src.CaseHelper import CaseHelper
from AutoUI.src.common.util import *
from AutoUI.src.AutoWeb import AutoWeb
from AutoUI.src.runner.testrunner import TestRunner
from AutoUI.src.AutoApp import AutoApp

log = Logger("main").logger()
# auto run: appium -a 127.0.0.1 -p 4723
# After finished, need to auto kill appium process!
test_case_path = './testfile/testcase'
run_list_path = '{}/runList.txt'.format(test_case_path)
run_list = []
with open(run_list_path, 'r') as f:
    for line in f.readlines():
        if line != '' and not line.startswith("#"):
            run_list.append(line.replace('\n', ''))


class TestWeb(unittest.TestCase):
    def setUp(self):
        auto_web.browser.start(auto_web.url)
        pass

    def tearDown(self):
        auto_web.browser.quit()
        pass


class TestApp(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


def test_generator(steps: list, auto):

    def test(self):
        sys.stderr.write('\n')
        self.assertEqual(auto.exec_step(steps), True)

    return test


def append_case(t_c, auto_func, unit_class):
    testCase = []
    test_id = 0
    for case in t_c:
        test_id += 1
        case_name, steps = split_dict(case)
        test_name = 'test_{}_{}'.format(test_id, case_name)
        test = test_generator(steps, auto_func)
        setattr(unit_class, test_name, test)
    testCase.append(unit_class)
    return testCase


if __name__ == '__main__':
    for file_name in run_list:
        case_helper = CaseHelper()
        case_helper.read_case_file('{}/{}'.format(test_case_path, file_name))
        case_config = case_helper.config_info
        report_name, report_title, tester = case_config.get('report_name'), case_config.get('report_title'), case_config.get(
            'tester')
        test_case = case_helper.get_case()
        if 'url' in case_config:
            auto_web = AutoWeb(case_config)
            testCase = append_case(test_case, auto_web, TestWeb)
        else:
            auto_app = AutoApp(case_config)
            testCase = append_case(test_case, auto_app, TestApp)
            auto_app.connect_phone()

        TR = TestRunner()
        test_unit = TR.add_test(testCase)
        TR.run(report_name, report_title, tester, test_unit)

