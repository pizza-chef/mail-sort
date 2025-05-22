"""
    Sort plan:
    https://auspost.com.au/content/dam/auspost_corp/media/documents/print-post-sort-plan-march-2021.pdf
    Actual guide:
    https://auspost.com.au/content/dam/auspost_corp/media/documents/print-post-service-guide.pdf
    Pricing:
    https://auspost.com.au/business/marketing-and-communications/business-letter-services/bulk-mail-options/print-post#tab2

    Sizes: Small (125g maximum), Large (1kg maximum, but different pricing for 13 weight steps)



    Rules of sorting:

    1. There must be at least 100 articles
    2. Small articles go straight to residue
    3. After sorting all the postcodes into

    Rates if it gets overseas?? Does it just count as other state
    SA SUBDIVISIONS??
"""
from printpost.readprintpost import ReadPrintPost
from .maillist import MailList
from .exportlist import ExportList
import numpy as np
import pandas as pd


class PrintPostSort:

    VALID_STATES = ["ACT", "NSW", "VIC", "QLD", "SA", "WA", "TAS", "NT", "Other"]

    @staticmethod
    def preprocessList(lists: list[MailList]):
        assert len(lists) > 0

        # Join the lists together
        headers, combined_list = ExportList.join(lists)

        combined_list = np.transpose(combined_list)

        df = pd.DataFrame(combined_list, columns=headers)

        combined_list = df.sort_values(['MS_SortCode', 'Postcode'], ascending=[True, True])
        combined_list = np.transpose(combined_list.values)

        preprocessedList = MailList(headers, combined_list, "Exported List")

        # Identifying address columns again for the lists after they've been all joined together
        for i in range(0, len(headers)):
            if headers[i] == "MS_State":
                preprocessedList.address_columns[1] = i
            elif headers[i] == "Postcode":
                preprocessedList.address_columns[2] = i

        return preprocessedList

    @staticmethod
    def organiseCategories(mail_list, weight: int, size, lodgement_state):
        assert 0 < weight <= 1000, "Weight must be in the range (0, 1000]"

        df = pd.DataFrame(np.transpose(mail_list.content), columns=mail_list.headers)

        # If the article size is small than everything goes into residue
        if size.lower() == "small":
            return PrintPostSort.__organise_small(df)

        if size.lower() != "large":
            return False

        return PrintPostSort.__organise_large(df, weight, lodgement_state)

    @staticmethod
    def __organise_large(mail_list: pd.DataFrame, weight: int, lodgement_state: str):
        """
        Organise the list for each state into residue, area direct, and postcode direct
        :param mail_list: the list to organise
        :param weight: weight per article
        :param lodgement_state: the state that the mail is being lodged in (must be a valid Australian state)
        :return: a dictionary with keys of VALID_STATES and values as lists.
        """
        assert lodgement_state in PrintPostSort.VALID_STATES and lodgement_state.lower() != "other"

        stateCounts = {}
        for state in PrintPostSort.VALID_STATES:
            """
            Each state will hold a dictionary with two keys: count, areaCounts
            areaCount contains a dictionary where each key is a presort indicator.
            The value will be a dictionary with two keys: count, postcodeCounts
            Postcode count will hold a key for the postcode and a value for total number of postcodes 
            """
            stateCounts[state] = {"count": 0, "areaCounts": {}}

        indicator_to_state = ReadPrintPost.get_instance().plan_to_state
        for i in range(0, len(mail_list["Postcode"])):
            presort_indicator, postcode = mail_list['MS_SortCode'][i], mail_list['Postcode'][i]
            if presort_indicator in indicator_to_state:
                state = indicator_to_state[presort_indicator]

                stateCounts[state]["count"] += 1

                # Adding one to the count of that presort indicator
                if presort_indicator in stateCounts[state]["areaCounts"]:
                    stateCounts[state]["areaCounts"][presort_indicator]["count"] += 1
                # Adding the presort indicator to the data structure if it doesn't exist
                else:
                    stateCounts[state]["areaCounts"][presort_indicator] = {"count": 1, "postcodeCounts": {}}

                # Adding one to the count of that postcode
                if postcode in stateCounts[state]["areaCounts"][presort_indicator]["postcodeCounts"]:
                    stateCounts[state]["areaCounts"][presort_indicator]["postcodeCounts"][postcode] += 1
                # Adding the postcode to the data structure if it doesn't exist
                else:
                    stateCounts[state]["areaCounts"][presort_indicator]["postcodeCounts"][postcode] = 1
            # If we can't identify the presort indicator then it's Other
            else:
                stateCounts["Other"]["count"] += 1

        return PrintPostSort.__groupTotals(stateCounts, weight, lodgement_state)

    @staticmethod
    def __groupTotals(stateCounts, weight, lodgement_state):
        """
        Groups the totals calculated
        :param stateCounts: __organise_large describes it
        :param weight: weight per article
        :param lodgement_state: the state that the mail is being lodged in (must be a valid Australian state)
        """
        sortDivisions = {}
        for state in PrintPostSort.VALID_STATES:
            sortDivisions[state] = []

        areaQuantity = 50 if weight <= 250 else (25 if weight <= 500 else 15)
        postcodeQuantity = 30 if weight <= 250 else (15 if weight <= 500 else 10)
        for state in sortDivisions.keys():
            # Postcode Direct is only valid in the lodgement state
            # Check if any presort indicator meets area direct minimum quantities
            totalAreaDirect = 0

            if state == lodgement_state:
                for psi in stateCounts[state]["areaCounts"]:
                    qualifiedPostcodes = []
                    postcodeCount = 0
                    for postcode, value in stateCounts[state]["areaCounts"][psi]["postcodeCounts"].items():

                        if value >= postcodeQuantity:
                            qualifiedPostcodes.append([postcode, value])
                            postcodeCount += value

                    areaDirectQuantity = stateCounts[state]["areaCounts"][psi]["count"] - postcodeCount

                    totalAreaDirect += postcodeCount

                    if len(qualifiedPostcodes) > 0:
                        sortDivisions[state].append(["Postcode", psi, qualifiedPostcodes])
                        if areaDirectQuantity > 0:
                            sortDivisions[state].append(["Area", psi, areaDirectQuantity])
                            totalAreaDirect += areaDirectQuantity
                    # If none are postcode direct then check there's enough in the psi to make area direct
                    elif areaDirectQuantity >= areaQuantity:
                        sortDivisions[state].append(["Area", psi, areaDirectQuantity])
                        totalAreaDirect += areaDirectQuantity
            else:
                for psi, value in stateCounts[state]["areaCounts"].items():
                    value = value["count"]  # Extracting count attribute from it as we don't care about postcode counts
                    if value >= areaQuantity:
                        totalAreaDirect += value
                        sortDivisions[state].append(["Area", psi, value])

            # Add anything leftover to residue
            stateResidue = stateCounts[state]["count"] - totalAreaDirect
            if stateResidue > 0:
                sortDivisions[state].append(["Residue", "", stateResidue])

        return sortDivisions

    @staticmethod
    def __organise_small(mail_list):
        """
        Counts the number of articles going into each state (including Other i.e. articles not going inside Australia).
        :param mail_list: MailList that must have the MS_SortCode Column
        :return: Returns a dictionary with keys in VALID_STATES. Values are either an empty list if there's no articles
                 going to that state or a list inside a list that describes the number of articles for that state i.e.
                 [["Residue", "", numberOfArticles]]
        """
        sort_divisions = {}
        for state in PrintPostSort.VALID_STATES:
            sort_divisions[state] = [["Residue", "", 0]]

        i = 0
        indicator_to_state = ReadPrintPost.get_instance().plan_to_state

        while i < len(mail_list["MS_SortCode"]):
            presort_indicator = mail_list['MS_SortCode'][i]
            indicator_count = 1
            i += 1
            while i < len(mail_list["MS_SortCode"]) and mail_list["MS_SortCode"][i] == presort_indicator:
                indicator_count += 1
                i += 1

            if presort_indicator not in indicator_to_state:
                sort_divisions["Other"][0][2] += indicator_count
            else:
                sort_divisions[indicator_to_state[presort_indicator]][0][2] += indicator_count

        for key in sort_divisions.keys():
            # If there's no residue values then pop it so we aren't dealing with categories that have no values
            if sort_divisions[key][0][2] == 0:
                sort_divisions[key].pop()

        return sort_divisions
