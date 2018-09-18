
# Author: Bruce.Zhu(Jialin)

import unittest
import sys
import sqlite3
from datetime import datetime
from AutoUI.src.CaseHelper import CaseHelper
from AutoUI.src.common.util import *
from AutoUI.src.AutoWeb import AutoWeb
from AutoUI.src.runner.testrunner import TestRunner
from AutoUI.src.AutoApp import AutoApp

log = MyLog("main").get_log()

# auto run: appium -a 127.0.0.1 -p 4723
# After finished, need to auto kill appium process!


class TestWeb(unittest.TestCase):

    auto_web = None

    def setUp(self):
        self.auto_web.browser.start(self.auto_web.url)
        pass

    def tearDown(self):
        self.auto_web.browser.quit()
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


def run_test_case(file_path, case_id):
    case_helper = CaseHelper()
    case_helper.read_case_file(file_path)
    case_config = case_helper.config_info
    report_name, report_title, tester = case_config.get('report_name'), case_config.get('report_title'), case_config.get(
        'tester')
    test_case = case_helper.get_case()
    if 'url' in case_config:
        auto_web = AutoWeb(case_config, MyLog("auto_web").get_log())
        TestWeb.auto_web = auto_web
        testCase = append_case(test_case, auto_web, TestWeb)
    else:
        auto_app = AutoApp(case_config, MyLog("auto_app").get_log())
        testCase = append_case(test_case, auto_app, TestApp)
        auto_app.connect_phone()

    TR = TestRunner()
    test_unit = TR.add_test(testCase)
    report_name = TR.run(report_name, report_title, tester, test_unit)
    over_time = datetime.now().strftime('%y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('./data/running_status.db')
    c = conn.cursor()
    sql = "UPDATE RUNNING_STATUS SET STATUS=\'{}\', OVER_TIME=\'{}\', LINK_REPORT=\'{}\' WHERE id={}"\
        .format('100%', over_time, report_name, case_id)
    c.execute(sql)
    conn.commit()
    conn.close()
