# Author: Bruce.Zhu(Jialin)

import xlrd


class ReadExcel(object):

    def __init__(self, file_name):
        self.wb = xlrd.open_workbook(file_name)

    def close(self):
        self.wb.close()

    def read_sheet(self, sheet_name, rows_start=0, cols_start=0):
        sheet = self.wb.sheet_by_name(sheet_name)
        for row in range(rows_start, sheet.nrows):
            values = []
            for col in range(cols_start, sheet.ncols):
                value = sheet.cell(row, col).value
                values.append(value)
            yield values
