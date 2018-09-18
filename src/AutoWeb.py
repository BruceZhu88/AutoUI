
# Author: Bruce.Zhu(Jialin)

import time
import sys
from AutoUI.src.common.SeleniumHelper import SeleniumHelper
from AutoUI.src.common.util import *


class AutoWeb(object):

    def __init__(self, config, log):
        self.browser = SeleniumHelper()
        self.url = config.get('url')
        self.log = log

    def print_log(self, s):
        self.log.debug(s)
        sys.stderr.write(s)

    def exec_step(self, steps: list):
        step_id = 0
        for step in steps:
            step_id += 1
            status = True
            action_name, values = split_dict(step)
            s = '{}: {}'.format(action_name, values.get('text')) if values.get('text') is not '' else action_name
            # sys.stderr.write('{}.{}\n'.format(step_id, s))
            self.print_log('{}.{}\n'.format(step_id, s))
            if action_name.lower() == 'sleep':
                time.sleep(float(values.get('text')))
            elif values.get('ele_action') == 'assert':  # xpath_
                trials_num = 5
                for i in range(1, trials_num + 1):
                    ele = self.browser.find_element(values.get('ele_type'),
                                               values.get('ele_value').format('\"' + values.get('text') + '\"'))
                    if ele is not None:
                        break
                    else:
                        time.sleep(5)
                        self.log.debug('Try to find text {}'.format(values.get('text')))
                    if i == trials_num:
                        self.print_log('Failed to find text {}'.format(values.get('text')))
                        status = False
            else:
                ele = self.browser.find_element(values.get('ele_type'), values.get('ele_value'))
                if values.get('ele_type') != 'xpath_':
                    status = self.browser.exec_ele(ele, values.get('ele_action'), values.get('text')) is True
            assert status is True
        return True
