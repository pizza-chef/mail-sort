from .maillist import MailList
import numpy as np
import functools


class ExportList:
    """
        The ExportList class is responsible for joining multiple lists together in preparation for exporting.
        After the list sorts the and groups into the residue, area direct, and postcode direct categories, export list
        has to prepare the final list in an order that matches the manifest.
    """

    @staticmethod
    def join(lists: list[MailList]):
        assert len(lists) > 0
        # Join lists one at a time

        if len(lists) == 1:
            return lists[0].headers, lists[0].content

        headers, combined_list = ExportList.__join_two(lists[0], lists[1])

        for i in range(2, len(lists)):
            headers, combined_list = ExportList.__join_two(combined_list, lists[i])

        # Finding the MS_SortCode index so it can be shifted to the end column
        sort_idx = -1
        for i in range(0, len(headers)):
            if headers[i] == "MS_SortCode":
                sort_idx = i
                break

        dropped_content = combined_list[sort_idx]
        dropped_header = headers[sort_idx]

        new_headers = np.concatenate((np.delete(headers, sort_idx), [dropped_header]))
        new_content = np.concatenate((np.delete(combined_list, sort_idx, axis=0), [dropped_content]))

        return new_headers, new_content

    @staticmethod
    def __join_two(aList, bList):
        # First we need to identify if there are any names of columns that are similar between the two
        related = ExportList.__duplicate_headers(aList.headers, bList.headers)
        combined_list = aList.content.copy()
        total_related = len(aList.headers) - np.count_nonzero(related == -1)

        # Filling right side of aList with empty values for the remaining column that aren't matching in bList
        empty_columns = np.full((len(bList.headers) - total_related, len(combined_list[0])), '')

        combined_list = np.append(combined_list, empty_columns, axis=0)
        # Filling left side of bList with all blank columns to fill what will be aList (duplicates are included)
        empty_columns = np.full((len(aList.headers), len(bList.content[0])), '')

        to_combine_list = np.append(empty_columns, bList.content, axis=0)

        to_delete = []
        # Removing the extra columns in to_combine_list and setting them so they align with the matching ones in aList
        for i in range(0, len(related)):
            if related[i] != -1:
                to_delete.append(related[i] + len(aList.headers))
                to_combine_list[i] = bList.content[related[i]]

        to_combine_list = np.delete(to_combine_list, to_delete, 0)

        # Stacking the new lists on top of each other
        combined_list = np.hstack((combined_list, to_combine_list))
        headers = aList.headers.copy()
        for i in range(0, len(bList.headers)):
            if i not in related:
                headers = np.append(headers, [bList.headers[i]])

        return headers, combined_list

    @staticmethod
    def __duplicate_headers(aHeader: list[str], bHeader: list[str]):
        related = np.full(len(aHeader), -1)
        for i in range(0, len(aHeader)):
            for j in range(0, len(bHeader)):
                if aHeader[i].lower() == bHeader[j].lower():
                    related[i] = j
                    break

        return related

    @staticmethod
    def __compareByIndex(item1, item2, idx):
        """
        Compares two lists together by using the value at the index given by idx
        :param item1: first list to compare
        :param item2: second list to compare
        :param idx: value of the list to compare
        :return: 1 if item1 is less, 0 if they are the same, -1 if item2 is less
        """
        if item1[idx] < item2[idx]:
            return 1
        elif item1[idx] > item2[idx]:
            return -1
        else:
            return 0

    @staticmethod
    def createExportList(listToSort: MailList, categories):
        """
        Creates the export list by resorting the the sorted
        :param listToSort: a MailList (must have a state and postcode header)
        :param categories: a list of lists of the format: [sortPlanType, presort indicator (leave blank if sort plan
            type is residue), total number of articles]. If sortPlanType is postcode then total number of articles
            should be a list that contains lists of the format [postcode, total number of articles]. As more than one
            postcode may be direct within the same pre sort indicator
        :return:
        """
        psiMap = {}
        # First create a mapping from a presort indicator to a [sort plan type (residue, area, postcode)]
        for column in categories.keys():
            # Loop through first index as all the lists are wrapped in a list because of the dataframe
            for row in categories[column]:
                psi, sortPlanType = row[1], row[0]
                if psi not in psiMap:
                    # psiMap stores an array that describes all postcodes in postcode direct. A blank dict means its
                    # only area direct
                    psiMap[psi] = {}
                if sortPlanType.lower() == "postcode":
                    for postcode in row[2]:
                        psiMap[psi][postcode[0]] = True

        stateIdx, postcodeIdx = listToSort.address_columns[1], listToSort.address_columns[2]

        # Transpose the contents first as we need to sort by row and not column (its stored in columns)
        exportListContent = np.transpose(listToSort.content)

        def compareFunction(item1, item2):
            # If both have the same state and non empty presort indicator then they are from AUS but different spots
            if item1[stateIdx] == item2[stateIdx] and item1[-1] != "" and item2[-1] != "":
                if item1[-1] == item2[-1]:
                    # If its in the psiMap it means item1/item2 may be postcode direct
                    if item1[-1] in psiMap:
                        # Within the same presort indicator, postcode directs are sorted first in order of postcodes
                        # If both item1 and item2 are postcode direct then take the smallest one
                        postMap = psiMap[item1[-1]]
                        if item1[postcodeIdx] in postMap and item2[postcodeIdx] in postMap:
                            return ExportList.__compareByIndex(item1, item2, postcodeIdx)
                        # If only one of the two is in postcode direct then it gets sorted first
                            # item 1 is postcode direct and item 2 is not so item 1 goes first
                        elif item1[postcodeIdx] in postMap and item2[postcodeIdx] not in postMap:
                            return 1
                        # item 2 is postcode direct and item 1 is not
                        elif item1[postcodeIdx] not in postMap and item2[postcodeIdx] in postMap:
                            return -1

                    # Otherwise just sort them based on postcode if they are both area direct or residue
                    return ExportList.__compareByIndex(item1, item2, postcodeIdx)
                # Same state, but different presort indicators
                else:
                    # If both of these aren't in the psiMap it means both are residue
                    if item1[-1] not in psiMap and item2[-1] not in psiMap:
                        # Compare by presort indicator and then by postcode to determine correct sort order
                        comparePSI = ExportList.__compareByIndex(item1, item2, -1)
                        if comparePSI == 0:
                            return ExportList.__compareByIndex(item1, item2, postcodeIdx)

                        return comparePSI
                    # Item 2 is not in residue, but item 1 is. Non-residue is placed first
                    elif item1[-1] not in psiMap and item2[-1] in psiMap:
                        return -1
                    # Item 1 is not in residue, but item 2 is. Non-residue is placed first
                    elif item1[-1] in psiMap and item2[-1] not in psiMap:
                        return 1
                    # Both are not not residue so we should compare by presort indicator
                    else:
                        return ExportList.__compareByIndex(item1, item2, -1)

            # If item1 is overseas it instantly gets ranked to bottom. Presort indicator == "" if other
            if item1[-1] == "":
                return -1

            # If item2 is overseas it instantly gets ranked to bottom
            if item2[-1] == "":
                return 1

            return ExportList.__compareByIndex(item1, item2, stateIdx)

        listToSort.content = np.transpose(sorted(exportListContent, key=functools.cmp_to_key(compareFunction), 
                                                 reverse=True))
        return listToSort
