from abc import ABC, abstractmethod
import numpy as np

class MailListParser(ABC):
    def __init__(self, include_headers):
        self.include_headers = include_headers

    @abstractmethod
    def readList(self, file_path):
        pass

    @staticmethod
    def identifyAddressField(column_names):

        field_names = [["country"], ["state"], ["postcode", "pcode"]]
        address_columns = np.array([-1, -1, -1])

        for i in range(0, len(column_names)):
            for j in range(0, len(field_names)):
                if column_names[i].lower().replace(" ", "") in field_names[j]:
                    address_columns[j] = i

        return address_columns
