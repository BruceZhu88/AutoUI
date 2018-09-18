
# Author: Bruce.Zhu(Jialin)
# test_cases = [{case1: [step1, step2]},
#             {case2: [step1, step2]},
#             ]
# common = {comm1: [{step1: {text: 1234}},
#                   {step2: {text: 1234}},
#                   ],
#           comm2: }
# keywords = {{'登录': {'': ''}}
#             }

from .common.excel_module import ReadExcel


class CaseHelper(object):

    def __init__(self):
        self.case_info = None
        self.config_info = None

    def read_case_file(self, file_path):
        config = {}
        test_cases = []
        case_name = ''
        common = {}
        comm_name = ''
        keywords = {}
        wb = ReadExcel(file_path)
        for values in wb.read_sheet('config'):
            if values[0] is not None:
                config[values[0]] = values[1]

        test_steps = []
        for values in wb.read_sheet('testcase', 1):
            if values[1] is not '':
                if case_name is not '':
                    test_cases.append(test_steps)
                case_name = values[1]
                test_steps = {case_name: []}
            if values[2] is not '':
                test_steps[case_name].append(values[2])
        test_cases.append(test_steps)

        test_steps = []
        for values in wb.read_sheet('common', 1):
            if values[0] is not '':
                if comm_name is not '':
                    common[comm_name] = test_steps
                comm_name = values[0]
                test_steps = []
            if values[1] is not '':
                test_steps.append({values[1]: {'text': values[2]}})
        common[comm_name] = test_steps

        for values in wb.read_sheet('keywords'):
            if values[0] is not None:
                config[values[0]] = values[1]
            keywords[values[0]] = {'ele_type': values[1],
                                   'ele_value': values[2],
                                   'ele_action': values[3]}

        self.case_info = {'test_cases': test_cases, 'common': common, 'keywords': keywords}
        self.config_info = config

    def get_case(self):
        test_cases = []
        for case in self.case_info['test_cases']:
            name, steps = '', []
            for k, v in case.items():
                # print('test name: {}'.format(name))
                name, steps = k, v
            case_values = []
            for s in steps:
                step_values = {}
                comm_name = self.case_info['common'].get(s)
                if comm_name is not None:
                    for step in comm_name:
                        for action_name, value in step.items():
                            step_values = {}
                            keyword = self.case_info['keywords'].get(action_name)
                            # print({**step[action_name], **keyword})
                            step_values[action_name] = {**step[action_name], **keyword}
                            case_values.append(step_values)
                else:
                    keyword = self.case_info['keywords'].get(s)
                    step_values[s] = keyword
                    case_values.append(step_values)
            test_cases.append({name: case_values})
        return test_cases

    def count_steps(self):
        for case in self.get_case():
            for name, steps in case.items():
                print(name)
                print(len(steps))

