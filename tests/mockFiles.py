from maillist.maillist import MailList
from printpost.readprintpost import ReadPrintPost
import random
import pandas as pd


def list_organiseSmall():
    """
    Creates a mail sort object with some dummy data
    :return: A Mail List object, a dictionary with the totals that appear in each state
    """
    listSize = 100
    headers = ["Name", "Postcode", "State", "MS_SortCode"]
    totals = {"ACT": 0, "NSW": 0, "VIC": 0, "QLD": 0, "SA": 0, "WA": 0, "TAS": 0, "NT": 0, "Other": 0}
    content = [["test" + str(i) for i in range(0, listSize)], [], [], []]

    # Loading postcode data
    postcode_to_plan = ReadPrintPost.get_instance().postcode_to_plan
    plan_to_state = ReadPrintPost.get_instance().plan_to_state
    postcodes = []
    for key, value in postcode_to_plan.items():
        postcodes.append(key)

    # Selecting random postcodes and adding them into the list
    for i in range(0, listSize - 1):
        position = random.randint(0, len(postcodes))
        content[1].append(postcodes[position])
        state = plan_to_state[postcode_to_plan[postcodes[position]]]
        content[2].append(state)
        content[3].append(postcode_to_plan[postcodes[position]])
        totals[state] += 1

    # Add an 'other' entry in to test any part that calls other
    content[1].append("")
    content[2].append("")
    content[3].append("")
    totals["Other"] += 1

    return MailList(headers, content, "test list"), totals

    # If the same state then possible for postcode direct
    # min_quantity = 30 if weight <= 250 else (15 if weight <= 500 else 10)

    # Calculating Area direct
    # min_quantity = 50 if weight <= 250 else (25 if weight <= 500 else 15)


def list_organiseLarge1(postcodeSize, areaSize):
    """
    Generates a mailing list with 30 postcode directs in it for the state VIC and 50 values for area direct
    for the state WA
    """

    headers = ["Name", "Postcode", "State", "MS_SortCode"]

    # If Area Numbers is odd we need the correct split
    areaSize1 = areaSize // 2
    areaSize2 = areaSize - areaSize1

    content = [["test" + str(i) for i in range(postcodeSize + areaSize + 1)],
               # Need 2 postcodes in same area otherwise it'd count as postcode direct
               ["3000" for i in range(postcodeSize)] + ["6000" for i in range(areaSize1)]
               + ["6012" for i in range(areaSize2)],
               ["VIC" for i in range(postcodeSize)] + ["WA" for i in range(areaSize)],
               ["022" for i in range(postcodeSize)] + ["049" for i in range(areaSize)]]

    # Adding an 'other' in there to ensure coverage
    content[1].append("")
    content[2].append("")
    content[3].append("")

    return MailList(headers, content, "organiseLarge1")


def expectedCategories1(postcodeSize, areaSize):
    """
    Returns the expected categories that relate to the list generated in from list_organiseLarge1
    """
    sort_divisions = {"ACT": [], "NSW": [], "VIC": [["Postcode", "022", [["3000", postcodeSize]]]],
                      "QLD": [], "SA": [], "WA": [["Area", "049", areaSize]], "TAS": [],
                      "NT": [], "Other": [["Residue", "", 1]]}

    return sort_divisions


def list_organiseLarge2(postcodeSize, areaSize):
    """
    Generates a list with multiple postcode directs under one presort indicator, postcode directs in more than one
    state, residue values in other states, and area direct in other states too.
    """

    # If Area Numbers is odd we need the correct split
    areaSize1 = areaSize // 2
    areaSize2 = areaSize - areaSize1

    residueSize = 8

    headers = ["Name", "Postcode", "State", "MS_SortCode"]
    content = [["test" + str(i) for i in range(postcodeSize*3 + areaSize + residueSize)],
               # Need 2 postcodes in same area otherwise it'd count as postcode direct
               ["3000"]*postcodeSize + ["3001"]*postcodeSize + ["6000"]*areaSize1
               + ["6012"]*areaSize2 + ["1637"]*postcodeSize + ["4518"]*residueSize,
               ["VIC"]*postcodeSize*2 + ["WA"]*areaSize + ["NSW"]*postcodeSize + ["QLD"]*residueSize,
               ["022"]*postcodeSize*2 + ["049"]*areaSize + ["003"]*postcodeSize + ["002"]*residueSize]

    return MailList(headers, content, "organiseLarge2")


def expectedCategories2(postcodeSize, areaSize):
    """
    Returns the expected categories that relate to the list generated in from list_organiseLarge1.

    """
    sort_divisions = {"ACT": [], "NSW": [["Residue", "", postcodeSize]], "VIC": [["Postcode", "022", [["3000", postcodeSize], ["3001", postcodeSize]]]],
                      "QLD": [["Residue", "", 8]], "SA": [], "WA": [["Area", "049", areaSize]], "TAS": [],
                      "NT": [], "Other": []}

    return sort_divisions


def write_mockFile(toWrite: MailList):
    """
    Writes a mail list to a text tab delimited file which can be used for manual testing to validate pdf generation is
    correct
    """
    fileName = "C:\\Users\\Dylan\\Downloads\\" + toWrite.name + ".txt"
    fileContents = ""

    for i in range(0, len(toWrite.headers) - 1):
        fileContents += toWrite.headers[i] + "\t"
    fileContents += toWrite.headers[-1] + "\n"

    for i in range(0, len(toWrite.content[0])):
        for j in range(0, len(toWrite.content)-1):
            fileContents += toWrite.content[j][i] + "\t"
        fileContents += toWrite.content[-1][1] + "\n"

    with open(fileName, "w") as f:
        f.write(fileContents)


if __name__ == "__main__":
    write_mockFile(list_organiseLarge1(50, 30))
    write_mockFile(list_organiseLarge2(50, 30))
    print("DONE")