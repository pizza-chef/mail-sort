from .maillistparser import MailListParser
import numpy as np
from .maillist import MailList


class SplitMailListParser(MailListParser):
    def __init__(self, split_on_string, include_headers):
        super(SplitMailListParser, self).__init__(include_headers)
        self.split_string = split_on_string

    # TODO: error handling when a line has more columns than headers
    def readList(self, file_path):
        try:
            file_contents = []
            with open(file_path, "r") as file:
                for line in file:
                    if line.strip() != "":
                        file_contents.append(line.split(self.split_string))
                        file_contents[-1][-1] = file_contents[-1][-1].strip()

            if self.include_headers:
                headers = file_contents[0]
                file_contents = file_contents[1:]
            else:
                headers = ["Column " + str(i+1) for i in range(0, len(file_contents[0]))]

            file_name = file_path.split("\\")[-1].split(".")[0]
            file_contents = np.array(file_contents)
            file_contents = np.transpose(file_contents)

            new_list = MailList(np.array(headers), file_contents, file_name)
            new_list.address_columns = MailListParser.identifyAddressField(new_list.headers)
            return self.remove_empty_columns(new_list)

        except FileNotFoundError:
            return MailList([], [], "")

    def remove_empty_columns(self, mail_list: MailList):
        """
            Remove any trailing columns that contain no data and appear due to formatting of the imported file. Strip
            can't be used on each line as it's impossible to tell while reading in line by line if a later line
            contains information in a column that another line may be blank at.
            :param: mail_list
                list to remove trailing columns
            :return: MailList
        """
        trailing_column = True
        current_column = len(mail_list.headers)-1
        cut_point = None

        while trailing_column and current_column >= 0:
            # Check each row of the column to see if they are all blank
            for i in range(0, len(mail_list.content[current_column])):
                if mail_list.content[current_column][i] != "":
                    trailing_column = False
                    break

            # If a trailing column then set cut point as that column onwards
            if trailing_column:
                cut_point = current_column
                current_column -= 1

        if cut_point is None:
            return mail_list

        new_list = MailList(mail_list.headers[0:cut_point], mail_list.content[0:cut_point], mail_list.name)
        new_list.address_columns = mail_list.address_columns
        return new_list
