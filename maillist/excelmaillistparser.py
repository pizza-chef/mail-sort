from .maillistparser import MailListParser
import numpy as np
import pandas as pd
from .maillist import MailList

class ExcelMailListParser(MailListParser):
    def __init__(self, include_headers, sheetNumber):
        super(ExcelMailListParser, self).__init__(include_headers)
        self.sheetNumber = 0 if sheetNumber == "" else int(sheetNumber) - 1

    def readList(self, file_path):
        try:
            if self.include_headers:
                spreadsheet = pd.read_excel(file_path, na_filter=False, dtype=str, sheet_name=self.sheetNumber)
                headers = spreadsheet.columns.to_list()
            else:
                spreadsheet = pd.read_excel(file_path, header=None, na_filter=False, dtype=str,
                                            sheet_name=self.sheetNumber)

                headers = ["Column " + str(i) for i in range(0, len(spreadsheet.columns))]

            content = np.transpose(spreadsheet.to_numpy())
            file_name = file_path.split("\\")[-1].split(".")[0]

            new_list = MailList(headers, content, file_name)
            new_list.address_columns = MailListParser.identifyAddressField(new_list.headers)
            return new_list

        except (FileNotFoundError, ValueError):
            return MailList([], [], "")

