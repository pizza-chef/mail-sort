from .splitmaillistparser import SplitMailListParser
from .excelmaillistparser import ExcelMailListParser

class ListParserFactory:
    def __init__(self):
        pass

    @staticmethod
    def createMailList(file_type, include_headers, sheetNumber):
        parser = None
        if file_type.find("txt") != -1:
            parser = SplitMailListParser("\t", include_headers)
        elif file_type.find("csv") != -1:
            parser = SplitMailListParser(",", include_headers)
        elif file_type.find("xlsx") != -1 or file_type.find("xls") != -1:
            parser = ExcelMailListParser(include_headers, sheetNumber)
        return parser
