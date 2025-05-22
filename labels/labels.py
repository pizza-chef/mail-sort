from datetime import datetime
from lxml import etree
import os
import math


class Labels:
    serviceIndicatorsTable = None
    statesTable = {"ACT": 1, "NSW": 2, "VIC": 3, "QLD": 4, "SA": 5, "WA": 6, "TAS": 7, "NT": 8}

    def __init__(self, deliveryStandard: str, size: str, mailTotals, name: str, weight: int, date: datetime):
        """
        Initialises a Labels class object, which is ready to be written to any path that exists when the user is ready
        :param deliveryStandard: "priority" or "regular"
        :param size: 'L' or 'S' (Large or small article)
        :param mailTotals: DataFrame where each column is the name of victorian states. Each row should be a list
            of length 3 is of either of the three formats:
            ['Area', <presort indicator>, number of articles]
            ['Residue', '', number of articles]
            ['Postcode', <postcode>, number of articles]
        :param name: name of the label plan file to import.
        :param weight: the weight of the article in grams
        """
        self.version = "3v0-700"  # This may change overtime.
        self.deliveryStandard = deliveryStandard

        assert size == "L" or size == "S"
        self.size = size

        assert weight > 0
        self.weight = weight
        self.mailTotals = mailTotals.copy()
        self.mailTotals.pop("Other", None)  # Remove other as we don't need it for labels

        self.name = name
        self.lodgementState = "3"  # 3 = VIC
        self.companyName = "Maroondah Printing"  # Default company
        self.companyContact = "9878 1555"
        self.date = Labels.getDateString(date)
        self.labelPlanFileText = ""
        self.articlesPerTray = None
        self.planDetails = []  # A list of lists with the format [state, sortPlan, label quantity, article quantity]

    def calculateArticlesPerTray(self, thickness, paperSize: str):
        """
        Calculates the number of articles that could fit into a tray given the thickness and paper size. This method
        should be called before running any other methods.
        :param thickness: thickness of spine of article in mm
        :param paperSize: This should be 'C5' or 'Other'. This determines whether the article is aligned so that the
                spine is parallel to the ground or perpendicular
        """
        trayLength = 400  # mm

        # Determining Size for Small Articles
        if self.size == "S":
            maxWeight = 9500  # g
            self.articlesPerTray = trayLength / thickness

        # Determining Size for Large Articles
        else:
            maxWeight = 16000  # g
            # A C5 orientation is placed in a tub with a different orientation
            if paperSize == "C5":
                self.articlesPerTray = trayLength / thickness
            # Any other large letter that's not a C5 orientation is stacked vertically
            else:
                trayHeight = 200  # mm
                self.articlesPerTray = trayHeight / thickness

        # If the weight of the number of articles that fit (according to dimension) in a tray exceeds the max weight
        # then fit as many articles as possible until we reach that max weight (it'll be < articlesPerTray so fits)
        if self.articlesPerTray * self.weight >= maxWeight:
            self.articlesPerTray = maxWeight // self.weight


    @staticmethod
    def getServiceIndicatorsTable():
        """
        Retrieves a dictionary of key-value pairs that contain type/service numbers related to the product
        configurations i.e. Large Article Residue PrintPost Regular Delivery. This should be used over accessing the
        table directly as the table may be none if the file has not been read.
        :return: dict
        """
        if Labels.serviceIndicatorsTable is None:
            Labels.readServiceIndicatorsTable()

        return Labels.serviceIndicatorsTable

    @staticmethod
    def readServiceIndicatorsTable():
        """
        Reads the ServiceIndicators.xml file and retrieves information of the type number and service number for
        different product configurations i.e. Large Article Residue PrintPost Regular Delivery. The result is saved
        in the static variable serviceIndicatorsTable
        """
        indicators = {}
        directory = os.path.dirname(os.path.realpath(__file__))
        file_name = directory + "/ServiceIndicators.xml"
        # If any of this code fails then don't recover gracefully. This is required to label.
        tree = etree.parse(file_name)
        root = tree.getroot()

        assert root.tag == "PrintPost"

        for c in range(0, len(root)):
            indicators[root[c].tag.lower()] = Labels.extractServiceIndicatorsFromRoot(root[c])

        if "postcode" not in indicators or "area" not in indicators or "residue" not in indicators:
            raise KeyError("Missing Area Keys when reading the labels file.")

        Labels.serviceIndicatorsTable = indicators

    @staticmethod
    def extractServiceIndicatorsFromRoot(root):
        """
        Extracts the text from a tag and places the key value pair of tag, text into a dictionary.
        :param root: a xml node
        :return: dict
            a dictionary containing a type, priority, and regular key which provides either the 'type' number for
            either residue/area/postcode direct, or the service code for the delivery service.
        """
        services = {}
        for i in range(0, len(root)):
            services[root[i].tag.lower()] = root[i].text

        if "type" not in services or "priority" not in services or "regular" not in services:
            raise KeyError("Missing Type/Delivery Standard keys when reading the labels file.")

        return services

    @staticmethod
    def getDateString(date):
        # Returns current date in the string format required
        return date.strftime("%d %b %Y")


    def createFileText(self):
        """
        Aggregates the various methods that create sections and compiles it into one string ready for output
        """
        self.planDetails = []
        fileText = self.createVersionSection()
        fileText += "#Label Plan File\n\n"
        fileText += self.createLabelPlanHeaderSection()
        fileText += self.createLabelDetails()
        fileText += "#End Of File"
        self.labelPlanFileText = fileText
        return fileText

    def createVersionSection(self):
        """
        Creates the header for the version of the visa labels software.
        :return: str
        """
        versionText = "#Australia Post Visa Tray Label System - Ver:\n"
        versionText += self.version + "\n"
        return versionText

    def createLabelPlanHeaderSection(self):
        """
        Creates the header for the label plan file based on the company details
        :return: str
        """
        headerText = "#Label Plan Header\n"
        headerText += self.name + "," + self.companyName + "," + self.companyContact + "," + self.lodgementState + ","
        headerText += self.date + "\n\n"
        return headerText

    def createLabelDetails(self):
        """
        Iterates over the mail totals of residue, area, and postcode direct for each state and calculates the number
        of labels needed for every entry. These are added as a line to the label plan file.
        :return: str
        """
        assert self.articlesPerTray is not None, "Please call the calculateArticlesPerTray method first"

        serviceIndicatorsTable = Labels.getServiceIndicatorsTable()

        detailsText = "#Label Details\n"
        detailsText += "#Service,Sort_Plan_Type,Sort_Plan,Destination_ID,Mail_Size,Label_Qty,Date\n"

        for column in self.mailTotals.keys():
            # Loop through first index as all the lists are wrapped in a list because of the dataframe
            for row in self.mailTotals[column]:
                if row[2] != 0:
                    indicatorCategory = serviceIndicatorsTable[row[0].lower()]
                    sortPlanType = indicatorCategory['type']
                    service = indicatorCategory[self.deliveryStandard]

                    # Residue uses the given state as sort plan, whereas row[1] stores the PSI or postcode for options
                    if row[0].lower() == "residue":
                        sortPlan = str(Labels.statesTable[column])
                    else:
                        sortPlan = row[1]

                    # If it's postcode then there's potentially multiple postcodes under one pre sort indicator that
                    # needs labels for each postcode.
                    if row[0].lower() == "postcode":

                        for postcodeTotal in row[2]:
                            postcode = postcodeTotal[0]
                            numArticles = postcodeTotal[1]
                            detailsText = self.__writeDetailEntry(detailsText, service, sortPlanType, postcode,
                                                                  numArticles, column)

                    else:
                        detailsText = self.__writeDetailEntry(detailsText, service, sortPlanType, sortPlan, row[2]
                                                              , column)

        return detailsText

    def __writeDetailEntry(self, text, service, sortPlanType, sortPlan, totalArticles, state):
        """
        Creates a custom string based on the following parameters given that is in the format required for the label
        plan detail section. Note this also recalculates the number of labels bassed on the weight given
        :param text: current text content of the label plan file that's been added so far
        :param service: service value associated with the delivery standard, sortPlanType, and Sorting plan
        :param sortPlanType: value associated with residue, area direct, or postcode direct
        :param sortPlan: either a presort indicator or postcode (only postcode for postcode direct)
        :param totalArticles: number of articles for that sort division/postcode
        :return:
        """
        sortPlanStates = [str(i) for i in range(1, 9)]  # These are all possible values that residue can be.
        labelQuantity = math.ceil(totalArticles/self.articlesPerTray)
        # If the sort plan is less than 10 it means it is for a state, which goes to residue
        self.planDetails.append([state, "Residue" if sortPlan in sortPlanStates else
                                 sortPlan, labelQuantity, totalArticles])

        # Adding the line of text for this label entry based on the variables calculated and provided
        text += service + "," + str(sortPlanType) + "," + str(sortPlan) + "," + self.size + ","
        text += str(labelQuantity) + "," + self.date + "\n"
        return text


