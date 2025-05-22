import datetime
import os

class ReadPrintPost:
    instance = None

    def __init__(self):
        self.plan_to_state = None
        self.postcode_to_plan = None
        self.expiry_date = None

    @staticmethod
    def get_instance():
        if ReadPrintPost.instance is None:
            instance = ReadPrintPost()
            instance.readCodeList(os.path.dirname(os.path.realpath(__file__)) + "/printpost.txt")
        return instance

    def readCodeList(self, file_name: str):
        plan_to_state = {}
        postcode_to_plan = {}
        f = open(file_name, "r")

        expiry = f.readline()
        date = datetime.datetime.strptime(expiry.strip(), "%d/%m/%y")
        self.expiry_date = date.date()

        state = None
        line = f.readline()
        while line:
            # Expected that first line after expiry is always a state
            if "STATE" in line:
                state = line.split(":")[1].strip()
            else:
                row = line.replace(";", "").strip().split(" ")

                # Add the sort indicator and its corresponding state to a look up table
                plan_no = row[0]
                row.pop(0)
                plan_to_state[plan_no] = state

                for i in range(0, len(row)):
                    if "-" in row[i]:
                        min_max = row[i].split("-")

                        if min_max[0] > min_max[1]:
                            print(min_max[0], min_max[1])
                            raise SyntaxError("Syntax incorrect in the file. Postcode range went from high to low.")

                        for j in range(int(min_max[0]), int(min_max[1])+1):
                            # Add 0 to any postcodes less than a 1000 as they have to be 4 digits
                            postcode_to_plan[str(j) if j >= 1000 else "0" + str(j)] = plan_no
                    else:
                        postcode_to_plan[row[i]] = plan_no

            line = f.readline()

        f.close()

        self.plan_to_state = plan_to_state
        self.postcode_to_plan = postcode_to_plan

