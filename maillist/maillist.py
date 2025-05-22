import numpy as np
import os
from printpost.readprintpost import ReadPrintPost


class MailList:

    def __init__(self, headers, content, name):
        if isinstance(headers, list):
            headers = np.array(headers, dtype=np.dtype('U100'))
        # Check that the headers type is > 7 i.e. array can hold strings of length 7 at max (len("Postcode") == 7)
        elif headers.dtype < np.dtype('U8'):
            headers = np.array(np.asarray(headers), dtype=np.dtype('U100'))

        if isinstance(content, list):
            content = np.array(content, dtype=np.dtype('U100'))

        self.headers = headers
        self.content = content
        self.name = name
        # ["country", "state", "postcode"]
        self.address_columns = np.full(3, -1)
        self.num_records = content.shape[1] if len(self.content) > 0 else 0
        self.incorrect_states = None

    @staticmethod
    def subset(headers: list[str], mail_list: 'MailList', new_name="", new_headers=[]):
        """
        :param headers: String[]
            A subset of column headers that should be extracted from the mail_list
        :param mail_list: MailList
        :param new_name: String
            Optional parameter of a new name for the list
        :param new_headers: String[]
            Optional parameter of new column names to overwrite the old header names
        :return: MailList
            A Mail List that is a subset of the given Mail List with content matching only the headers given
        :raises ValueError
            Every string in headers must be present in mail_list.headers
        """
        column_names = headers

        if len(new_headers) != 0:
            assert len(new_headers) == len(headers)
            column_names = np.array(new_headers)

        indices = []
        for header in headers:
            where = np.where(mail_list.headers == header)
            if len(where[0]) != 0:
                # Column names should be unique so take the first instance of it occurring.
                # Taking [0][0] because where returns a tuple of arrays for different dimensions
                indices.append(where[0][0])

        content = np.empty(shape=(len(headers), len(mail_list.content[0])), dtype=np.dtype('U100'))

        for i in range(0, len(mail_list.content[0])):
            for j in range(0, len(indices)):
                content[j][i] = mail_list.content[indices[j]][i]

        name = mail_list.name
        if new_name != "":
            name = new_name

        return MailList(column_names, content, name)

    def assign_sort_codes(self):
        """
            Assigns sort codes to each entry based on the postcode along with a corresponding state to where that sort
            code belongs. This functions should be called after the postcode column has been identified.
        """
        printPost = ReadPrintPost.get_instance()
        postcode_to_plan = printPost.postcode_to_plan
        plan_to_state = printPost.plan_to_state

        self.headers = np.concatenate((self.headers, ["MS_State", "MS_SortCode"]))

        p_idx = self.address_columns[-1]

        sort_codes = np.empty((1, len(self.content[p_idx])), dtype=np.dtype("U100"))
        stateColumns = np.empty((1, len(self.content[p_idx])), dtype=np.dtype("U100"))

        for i in range(0, len(self.content[p_idx])):
            if self.content[p_idx][i] in postcode_to_plan:
                sort_codes[0][i] = postcode_to_plan[self.content[p_idx][i]]
                stateColumns[0][i] = plan_to_state[sort_codes[0][i]]
            else:
                sort_codes[0][i] = ""

        self.content = np.concatenate((self.content, stateColumns, sort_codes))

    def identify_bad_states(self):
        """
            Identifies any entry that has a state that does not match the postcode i.e. that postcode does not
            exist in that state. This function assumes that the user has selected which column corresponds to the
            state or it was automatically identified already.
        """
        # TODO: Something more advanced for flagging things on the border. Legit mistakes getting lost in these close calls
        # User hasn't selected state so can't identify bad states
        if self.address_columns[1] == -1:
            return

        plan_to_state = ReadPrintPost.get_instance().plan_to_state
        state_idx = self.address_columns[1]
        self.incorrect_states = []

        # Each state can be expressed as an abbreviation or their expanded form so must check both
        synonyms = {"NSW": ["nsw", "new south wales"], "VIC": ["vic", "victoria"], "TAS": ["tas", "tasmania"],
                    "WA": ["wa", "western australia"], "SA": ["sa", "south australia"],
                    "NT": ["nt", "northern territory"], "QLD": ["qld", "queensland"],
                    "ACT": ["act", "australian capital territory"]}

        # Loop using last column as it is where the sort codes are stored
        for i in range(0, len(self.content[-1])):
            if self.content[-1][i] in plan_to_state:
                print_post_state = plan_to_state[self.content[-1][i]]

                if print_post_state in synonyms and self.content[state_idx][i].lower() not in synonyms[print_post_state]:
                    self.incorrect_states.append([i, print_post_state])
