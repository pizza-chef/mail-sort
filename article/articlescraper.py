from datetime import date
from dateutil.relativedelta import relativedelta
import requests
from bs4 import BeautifulSoup
from lxml import etree
from smallarticle import SmallArticle
from largearticle import LargeArticle
import os


class ArticleScraper:
#TODO UPDATE SCRAPER
    @staticmethod
    def scrapePrintPostPrices():
        """
        Scrapes the print post pricing for articles being delivered via priority or regular standards and stores
        that information into a dictionary.
        """
        url = "https://auspost.com.au/business/marketing-and-communications/business-letter-services/bulk-mail" \
              "-options/print-post#tab2 "
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "lxml")

        # Use string= to get things with text, can evne use function
        pricingBlocks = soup.find_all("div", class_="accordion")

        largePricing = {"Priority": {}, "Regular": {}}
        smallPricing = {"Priority": {}, "Regular": {}}
        i = 0  # Counter to keep track of if its priority or regular timetable.
        for block in pricingBlocks:
            if i < 3:
                standard = "Priority"
            elif i < 6:
                standard = "Regular"
            else:
                raise ValueError("More than two delivery standards listed?")

            categoryBlock = block.find("div", class_="rte-wrapper")
            if categoryBlock is None:
                raise SyntaxError("AusPost has changed their website structure.")

            categoryName = categoryBlock.text.strip().replace(" ", "")
            if categoryName == "PostcodeDirect":
                largeArticleDict = ArticleScraper.__decodePostcodeArea(block, ArticleScraper.__decode2ColumnTable)
            elif categoryName == "AreaDirect":
                largeArticleDict = ArticleScraper.__decodePostcodeArea(block, ArticleScraper.__decode3ColumnTable)
            elif categoryName == "Residue":
                smallArticleDict, largeArticleDict = ArticleScraper.__decodeResidue(block)
                smallPricing[standard][categoryName] = smallArticleDict
            else:
                raise SyntaxError("Names changed for each category.")

            largePricing[standard][categoryName] = largeArticleDict

            i += 1
        return smallPricing, largePricing

    @staticmethod
    def __getTableRows(pricingBlock):
        """
        Gets the table rows and the article size for each table present in the article section i.e.
        all tables under the postocde direct, area direct, or residue timetable sections on the webpage.
        :param pricingBlock: Bs4 object that contains the table tag somewhere inside it
        :return:
            A list where each entry describes the [article size, bs4 object that describes the table rows]
        """
        tableWrapper = pricingBlock.find("article", class_="expandable-block-content")
        results = tableWrapper.find_all("table")

        tables = []
        for i in range(0, len(results)):

            articleSizeBlock = results[i].find("caption")

            if articleSizeBlock is not None:
                sizeText = articleSizeBlock.text.strip().lower()
            else:
                sizeText = ""  # Residue doesn't have the size text listed as a caption for regular timetable

            tableBody = results[i].find("tbody")
            tableRows = tableBody.find_all("tr")
            tables.append([sizeText, tableRows])
        return tables

    @staticmethod
    def __decodePostcodeArea(pricingBlock, decodeFunction):
        """
        Postcode Direct and Area direct have mostly the same structure with only how the table is read.
        A decode function can be used to extract the data from the tables but getting the table data
        itself is the same method
        :param decodeFunction: A function that's responsibility is to interpret the table and create a
            dictionary object
        :return: a dict
        """
        tables = ArticleScraper.__getTableRows(pricingBlock)

        if len(tables) != 1:
            raise ValueError("Postcode/Area direct should only have one table")

        articleSize = tables[0][0]

        if "large letter items" not in articleSize:
            raise ValueError("Large letter items should be the article size only.")

        tableRows = tables[0][1]

        return decodeFunction(tableRows)

    @staticmethod
    def __decode2ColumnTable(tableRows):
        """
        Decodes the data for a table with only two columns (weight, same state)
        :param tableRows: A list of BS4 objects that reference the tr tag
        :return: a dict of that shows the delivery standard, the destination (same or other state), the weight,
            and the price
        """
        priceDict = {}
        # Start at index 1 since first row is column names
        for i in range(1, len(tableRows)):
            weightTag = tableRows[i].find("th")

            weight = weightTag.text.strip()

            priceTag = tableRows[i].find("td")
            # Inside a <p><b> it says Same State. The text shows the value

            price = priceTag.text.strip().split("\n")

            destination, cost, weight = ArticleScraper.__processPrice(price, weight)

            if weight not in priceDict:
                priceDict[weight] = {}

            priceDict[weight][destination] = cost
        return priceDict

    @staticmethod
    def __decode3ColumnTable(tableRows):
        """
        Decodes the data for a table that has 3 columns (weight, same state, other state).
        :param tableRows: A list of BS4 objects that reference the tr tag
        :return: a dict of that shows the delivery standard, the destination (same or other state), the weight,
            and the price
        """
        priceDict = {}
        # Start at index 1 since first row is column names
        for i in range(1, len(tableRows)):

            weightTag = tableRows[i].find("th")
            weight = weightTag.text.strip()

            priceTags = tableRows[i].find_all("td")
            # Here it differs to postcode direct as it is both same state/other state rather than just same state
            if len(priceTags) != 2:
                raise ValueError("There should be same state and other state for 3 columns")

            for j in range(0, len(priceTags)):

                price = priceTags[j].text.strip().split("\n")
                destination, cost, weight = ArticleScraper.__processPrice(price, weight)

                if weight not in priceDict:
                    priceDict[weight] = {}

                priceDict[weight][destination] = cost

        return priceDict

    @staticmethod
    def __decodeResidue(pricingBlock):
        """
        Decodes both the small letters and large letters table in the residue section for same and other state.
        :param pricingBlock:
        :return: 2 dicts of that shows the delivery standard, the destination (same or other state), the weight,
            and the price for small letters and large letters
        """
        tables = ArticleScraper.__getTableRows(pricingBlock)

        if len(tables) != 2:
            raise ValueError("There should be two tables for the residue section")

        # Residue doesn't have smaller letter and large letter for their captions like the other does for regular
        # so we have to rely on that the first is small letters and next is large letters
        smallArticlesDict = ArticleScraper.__decode3ColumnTable(tables[0][1])
        largeArticlesDict = ArticleScraper.__decode3ColumnTable(tables[1][1])
        return smallArticlesDict, largeArticlesDict

    @staticmethod
    def __processPrice(price, weight: str):
        """
        Processes the price text into a format that can be saved into a dict for easy writing to a
        xml file
        :param price: An array of length two where the first index is Same state/Other state and the next
            index is the price with a $ out the front
        :param weight: The weight range
        :return: destination: SameState/OtherState, cost: str of a float, weight: a range of two ints i.e. int1-int2
        """
        destination = 'SameState' if price[0].lower() == "same state" else "OtherState"
        cost = price[1][1:]
        weight = weight.replace("g", "")

        # Replacing the k for kgs for a gram measurement
        if weight[-1] == "k":
            weight = weight[:-1] + "000"

        return destination, cost, weight

    @staticmethod
    def writePrices(smallFileName: str, largeFileName: str):
        """
        Writes the contents of the web scraper if it is successful into a xml document for both small and large
        articles.
        :param smallFileName: The name of the xml file for small article pricing
        :param largeFileName: The name of the xml file for large article pricing
        :return:
        """
        # Getting the current stored articles to record their dimensions as these don't change
        largeArticle = LargeArticle.get_instance()
        smallArticle = SmallArticle.get_instance()

        # Fetching the prices
        smallPrices, largePrices = ArticleScraper.scrapePrintPostPrices()

        # Writing the small and large articles
        ArticleScraper.__writeTree(smallFileName, smallArticle.max_weight, smallArticle.max_size,
                                   smallArticle.expiry_date, smallPrices, "SmallArticle")

        ArticleScraper.__writeTree(largeFileName, largeArticle.max_weight, largeArticle.max_size,
                                   largeArticle.expiry_date, largePrices, "LargeArticle")

    @staticmethod
    def __writeTree(fileName: str, maxWeight: int, maxSize: tuple, expiry: date, prices: dict, rootName: str):
        """
        Writes the article pricing to the file name given.
        :param fileName: name of the file to write to. This will be saved in the article/ directory
        :param maxWeight: Maximum weight the article can be
        :param maxSize: A tuple of width, length maximums
        :param expiry: a date object
        :param prices: a dictionary of all the prices. Retrieved with scrapePrintPostPrices
        :param rootName: Name of the root (Should be SmallArticle or LargeArticle)
        """
        doctype = "<!DOCTYPE xml>\n"

        root = etree.Element(rootName)
        # Calculating the expiry i.e. when the prices should next be updated from the website
        expiryNode = etree.SubElement(root, "Expiry")
        # TODO: This may change in the future to being longer than 1 month tbh
        nextExpiry = expiry.today() + relativedelta(months=1)
        expiryNode.text = nextExpiry.strftime("%d/%m/%y")

        # Creating nodes to store basic information on sizing for the list
        articleRequirements = etree.SubElement(root, "Requirements")
        weightRequirements = etree.SubElement(articleRequirements, "MaxWeight")
        weightRequirements.text = str(maxWeight)
        sizeRequirements = etree.SubElement(articleRequirements, "MaxSize")
        sizeRequirements.attrib["units"] = "mm"
        widthRequirement = etree.SubElement(sizeRequirements, "Width")
        widthRequirement.text = str(maxSize[0])
        lengthRequirements = etree.SubElement(sizeRequirements, "Length")
        lengthRequirements.text = str(maxSize[1])

        pricingNode = etree.SubElement(root, "Pricing")
        # Looping through the delivery standards i.e. Priority and Regular
        for standard in list(prices.keys()):
            standardNode = etree.SubElement(pricingNode, standard)
            # Loop through the categories PostcodeDirect, AreaDirect, Residue (note that these might not all exist)
            for category in list(prices[standard].keys()):
                categoryNode = etree.SubElement(standardNode, category)
                # Loop through the dictionaries for each weight that contain pricing for same state and other state
                for weight, destinationPrice in prices[standard][category].items():
                    weightNode = etree.SubElement(categoryNode, "S" + weight)
                    # Loop through the prices for same state and other state
                    for destination, price in destinationPrice.items():
                        destinationNode = etree.SubElement(weightNode, destination)
                        destinationNode.text = price

        tree = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8', doctype=doctype)

        directory = os.path.dirname(os.path.realpath(__file__))
        file_name = directory + "\\" + fileName + ".xml"
        with open(file_name, 'wb') as f:
            f.write(tree)
