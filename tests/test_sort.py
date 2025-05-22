import pytest

from maillist.sort import PrintPostSort
from mockFiles import *



def test_organiseSmall():
    """
    Tests that organiseSmall correctly counts the number of articles per state
    """
    fakeList, totals = list_organiseSmall()

    categories = PrintPostSort.organiseCategories(fakeList, 50, "small", "VIC")

    match = True

    for state in categories.keys():
        # If there's no entry for that state then there should be no value
        if len(categories[state]) == 0:
            if totals[state] != 0:
                match = False
        # If there's an entry for the state check if matches the totals
        elif categories[state][0][2] != totals[state]:
            match = False

    assert match

@pytest.mark.parametrize("mailList, expectedCategories, weight", [
    (list_organiseLarge1(30, 50), expectedCategories1(30, 50), 125),
    (list_organiseLarge1(30, 50), expectedCategories1(30, 50), 250),
    (list_organiseLarge1(15, 25), expectedCategories1(15, 25), 251),
    (list_organiseLarge1(15, 25), expectedCategories1(15, 25), 500),
    (list_organiseLarge1(10, 15), expectedCategories1(10, 15), 501),
    (list_organiseLarge1(10, 15), expectedCategories1(10, 15), 1000),
    (list_organiseLarge2(30, 50), expectedCategories2(30, 50), 125)
])
def test_organiseLarge(mailList, expectedCategories, weight):
    """
    Tests the __organise_Large function correctly organises a mail list's entries into the right categories given
    the the weight. The following weight ranges have different total article boundaries for classifying a presort
    indicator as Area Direct or a postcode as Postcode direct: 0-250g, 251-500g, 501-1000g. Each boundary on either side
    will be tested alongside ensuring that the code correctly handles having multiple postcode directs under one
    presort indicator.
    """
    #TODO: Numbers don't match and test passes still.
    categories = PrintPostSort.organiseCategories(mailList, weight, "large", "VIC")

    match = True

    for state in categories.keys():
        values = categories[state]
        expectedValues = expectedCategories[state]

        # If they aren't the same length it means not the same. IndexErrors will occur if we try to compare then.
        if len(values) - len(expectedValues) != 0:
            match = False
        else:
            for i in range(0, len(values)):
                if values[i][0] in ["Residue", "Area"]:
                    if not (values[i][1] == expectedValues[i][1] and values[i][2] == expectedValues[i][2]):
                        match = False
                else:
                    # Postcode direct requires different comparing
                    for j in range(0, len(values[i][2])):
                        postcode = values[i][2][j]
                        expectedPostcode = expectedValues[i][2][j]
                        if not (postcode[0] == expectedPostcode[0] and postcode[1] == expectedPostcode[1]):
                            match = False
    assert match