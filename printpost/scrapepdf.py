import os

import PyPDF2
import datetime
import re

class ScrapePDF:
    """
    This file should be run offline when the a sorting plan expires to generate a new sorting plan from the new pdf.
    """

    @staticmethod
    def scrape(fileName):
        """
        Extracts the presort indicators and their corresponding postcodes for each state.
        :param fileName: name of the file to read
        :return: writes the result of the file
        """
        pdf = PyPDF2.PdfFileReader(fileName)

        expiryDate = None
        # States Should appear on the print post sort plan in this order
        statesText = ["Australian Capital Territory", "New South Wales", "Victoria", "Queensland", "South Australia",
                      "Western Australia", "Tasmania", "Northern Territory"]
        # Maps the full state names to their abbreviations
        stateMap = {"Australian Capital Territory": "ACT", "New South Wales": "NSW", "Victoria": "VIC",
                    "Queensland": "QLD", "South Australia": "SA", "Western Australia": "WA", "Tasmania": "TAS",
                    "Northern Territory": "NT"}

        statesIdx = 0
        currPSI = -1  # Current presort indicator
        psiDict = {}
        currState = None
        toWrite = ""
        saText = ""  # Text for South Australia because of how weird it is
        for page in range(0, pdf.numPages - 1):
            pageText = pdf.getPage(page).extractText()

            if page == 0:
                expiryDate = ScrapePDF.__pageTextExpiryDate(pageText)
                toWrite += expiryDate + "\n"

            pageText = ScrapePDF.__cleanText(pageText)
            pageText = pageText.replace("˜", "-")
            splitText = pageText.split("\n")

            for text in splitText:
                text = text.strip()
                text = text.replace("Sub Divisions", "")

                # We've encountered a new state so we should write current PSI and reset the dict
                if statesText[statesIdx] in text:
                    # Write the values for the current state before updating the state indices and current state
                    if len(psiDict) > 0:
                        toWrite = ScrapePDF.__writeDict(toWrite, psiDict, stateMap[currState])
                        psiDict = {}

                    currState = statesText[statesIdx]
                    statesIdx = statesIdx + 1 if statesIdx != len(statesText) - 1 else statesIdx

                # South Australia is different because of the sub divisions so requires special attention
                # It also has odd formatting so needs extra precomputation to interpret it
                if stateMap[currState] == "SA":
                    saText += text + "\n"
                else:
                    psiDict, currPSI = ScrapePDF.__decodeStates(text, psiDict, currPSI)


        # Write the final state's PSIs
        toWrite = ScrapePDF.__writeDict(toWrite, psiDict, stateMap[currState])

        # After everything has been written then process South Australia and write it
        psiDictSA = ScrapePDF.__decodeSouthAustralia(saText)
        toWrite = ScrapePDF.__writeDict(toWrite, psiDictSA, "SA")

        # Removing the new line at the end that was written on final write
        toWrite = toWrite[:-1]

        directory = os.path.dirname(os.path.realpath(__file__))
        writeLocation = directory + "\\test.txt"
        with open(writeLocation, "w") as f:
            f.write(toWrite)

    @staticmethod
    def __writeDict(toWrite: str, psiDict: dict, state: str):
        """
        Writes a dictionary's contents to a string for a given state.
        :param toWrite: The string to write to
        :param psiDict: a dictionary with keys of presort indicator codes and values of a string that represents
                        all postcodes under that psi i.e. postcode1; postcode2-postcode3; ... etc.
        :param state: the abbreviated name for a state: ACT, NSW, QLD, SA, VIC, NT, TAS, WA
        :return: the toWrite parameter updated with the data from the psiDict
        """
        toWrite += "STATE:" + state + "\n"

        # Write everything in the current dictionary for that state and then wipe dictionary
        for psi, postcodes in psiDict.items():
            toWrite += psi + " " + postcodes + "\n"

        return toWrite

    @staticmethod
    def __decodeStates(text: str, psiDict: dict, currPSI: str):
        """
        Decodes the text from the pdf into a dictionary for all Australian states other than SA.
        :param text: A line of text
        :param psiDict: a dictionary of presort indicators mapping to a string of postcodes
        :param currPSI: Current pre sort indicator
        :return: The dictionary with updated values and a new presort indicator if it changed
        """
        # If the text is 3 long and consists only of digits its a presort indicator
        if len(text) == 3 and text.isnumeric():
            currPSI = text
            psiDict[currPSI] = ""
        # If first 7 characters are numeric and are followed by a '-', ';' then its a PSI and postcode(s)
        elif len(text) > 6 and text[0:7].isnumeric() and text[7] in ["-", ";"]:
            currPSI = text[0:3]
            postcodes = text[3:]
            psiDict[currPSI] = ScrapePDF.__processPostcodes(postcodes)
        # If the first 4 characters are numeric followed by '-' its postcodes belonging to current indicator
        elif len(text) > 3 and text[0:4].isnumeric():
            newPSI = currPSI
            # There is a potential in some lines here that after the postcodes there is an address then a PSI
            if text[-3:].isnumeric() and not text[-4].isnumeric():
                newPSI = text[-3:]

            postcodes = ScrapePDF.__processPostcodes(text)
            if psiDict[currPSI] == "":
                psiDict[currPSI] = postcodes
            else:
                psiDict[currPSI] = psiDict[currPSI] + "; " + postcodes

            if newPSI != currPSI:
                psiDict[newPSI] = ""
            currPSI = newPSI
        # If the line has the presort indicator at the end after an address we need to extract it
        # The PSI will be right next to another character without a space if this occurs. Not to be confused with an
        # address for a postcode i..e DANDENONG SOUTH VIC 3175 in the sort division column
        elif len(text) > 3 and text[-3:].isnumeric() and not text[-4].isnumeric():
            currPSI = text[-3:]
            psiDict[currPSI] = ""

        return psiDict, currPSI

    @staticmethod
    def __decodeSouthAustralia(text: str):
        """
        Decodes the text from the pdf into a dictionary for SA.
        :param text: Text that represents the entire table from the south australia table
        :return: A dictionary that maps PSI to postcodes i.e. map[PSI] = 'postcode1; postcode2; ... postcodeN
        """
        # Remove all the sub divisions first
        text = re.sub(r"5[0-9][0-9][a-z]:", "\n", text)

        # Join lines where postcodes are cut off
        count = 0
        splitText = text.split("\n")
        startIndex = len(splitText)
        # Combining lines that may have been cut off due to formatting
        for i in range(startIndex-1, 0, -1):
            line = splitText[i].strip()

            # Remove any blank lines
            if line == "":
                splitText.pop(i)
                count += 1
            # These are the possibly scenarios where lines with postcode ranges are cut off
            elif line[0] == "-" or (line[0].isnumeric() and line[1].isnumeric() and line[2] == "-"):
                splitText[i-1] += line
                # Remove this from the list as we add it to the one before
                splitText.pop(i)
                count += 1


        # After processing we can use the regular algorithm to decipher it
        splitText.pop(0)  # Remove the state name
        psiDict = {}
        currPSI = ""
        for text in splitText:
            psiDict, currPSI = ScrapePDF.__decodeStates(text.strip(), psiDict, currPSI)

        return psiDict

    @staticmethod
    def __processPostcodes(text: str):
        """
        Takes a string and extracts the postcodes from it into a readable format. The postcodes given
        should already be in the general format of postcode-postcode; postcode-postcode, but some may
        have trailing text that needs removal

        :param text: a text containing postcodes. This should start with 4 digits (0-9), followed by a -
        :return: a string in the format of: postcode-postcode; postcode-postcode
        """

        # Step back until something numeric is encountered.
        i = len(text) - 1
        while i > 0 and not text[i].isnumeric():
            i -= 1

        text = text[0:i+1]
        # When reading SA postcodes there may be a subdivision tacked on the end
        # Get the last postcode listed. If it isn't 4 long it means a subdivision got added from pdf formatting
        postcodeLength = len(text.split(";")[-1].split("-")[-1].strip())
        if postcodeLength > 4:
            text = text[:len(text)-(postcodeLength-4)]
        return text

    @staticmethod
    def __cleanText(pageText: str):
        """
        Removes trailing text that appears at the start and the end of the document that isn't needed
        for processing the data on the page. i.e. headers, table column names, page numbers, branding etc.
        :param pageText: Text from a page
        :return: A string less than or equal to the pageText given in length
        """
        # The last word that appears before the data on the page starts being displayed
        lastHeaderText = "Division"
        headerIndex = pageText.index(lastHeaderText)

        pageText = pageText[headerIndex+len(lastHeaderText):]

        # The first word appears before trailing text appears
        firstFooterText = "Australia Post"

        footerIndex = pageText.index(firstFooterText)
        pageText = pageText[:footerIndex-1]  # -1 to remove the last \n
        return pageText

    @staticmethod
    def __pageTextExpiryDate(pageText: str):
        """
        pageTexts the expiry date of this print post sort plan from the very first page
        :param pageText: Text from the first page
        :return: A string of the expiry date in the form of dd/mm/yy
        """
        startDateIndex = pageText.index("Valid")

        # Read until after we read the word 'to' which denotes the start of the expiry date
        while startDateIndex < len(pageText) and pageText[startDateIndex:startDateIndex + 2] != "to":
            startDateIndex += 1

        # Skip fast 'to ' and start reading until encountering a new line
        startDateIndex += 3

        endDateIndex = startDateIndex
        while pageText[endDateIndex] != "\n":
            endDateIndex += 1

        date = datetime.datetime.strptime(pageText[startDateIndex:endDateIndex], "%d %B %Y")
        return date.strftime("%d/%m/%y")


if __name__ == "__main__":
    ScrapePDF.scrape("C:\\Users\\Dylan\\Downloads\\print-post-sort-plan-september-2021.pdf")
    #ScrapePDF.scrape("C:\\Users\\Dylan\\Downloads\\print-post-sort-plan-march-2021.pdf")
