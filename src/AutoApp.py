
# Author: Bruce.Zhu(Jialin)

import sys
import time
import datetime
from AutoUI.src.common.adb import adb
from AutoUI.src.common.AppiumHelper import AppiumHelper
from AutoUI.src.common.util import split_dict


class AutoApp(object):
    def __init__(self, config, log):
        self.config = config
        self.log = log

    def connect_phone(self):
        if not adb.check_device_status():
            self.log.error('Please check your phone')
            sys.exit()
        self.log.info('Connecting with your phone ...')
        try:
            AppiumHelper().connect(self.config.get('remote_server'),
                                   {'platformName': self.config.get('platform_name'),
                                    'deviceName': self.config.get('device_name'),
                                    'timeout': self.config.get('timeout'),
                                    'appPackage': self.config.get('app_package'),
                                    'appActivity': self.config.get('app_activity'),
                                    })
        except Exception as e:
            self.log.error('Cannot connect to your phone: {}'.format(e))
            sys.exit()

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
            self.print_log('{}.{}\n'.format(step_id, s))
            if action_name.lower() == 'sleep':
                time.sleep(float(values.get('text')))
            elif values.get('ele_action') == 'click':
                status = AppiumHelper().my_click(values.get('ele_type'), values.get('ele_value'), values.get('text'))
            elif values.get('ele_action') == 'send_keys':
                status = AppiumHelper().input(values.get('ele_type'), values.get('ele_value'), values.get('text'))
            elif values.get('ele_action') == 'assert':
                status = AppiumHelper().find_text(values.get('text'))
            if not status:
                shot_path = './log/screenshot'
                timestamp = datetime.datetime.now().strftime('%m%d%H%M%S')
                shot_name = '{}_error_{}'.format(values.get('ele_action'), timestamp)
                self.print_log('Error screenshot path: {}/{}.png\n'.format(shot_path, shot_name))
                AppiumHelper().shot(shot_path, shot_name)
            assert status is True
        return True


