from .article import Article
from lxml import etree
from .smallarticle import SmallArticle
import os
import datetime


class LargeArticle(Article):
    instance = None

    def __init__(self):
        super().__init__()
        self.read_file()

    def read_file(self):
        self.priority_pricing = [{}, {}, {}]
        self.regular_pricing = [{}, {}, {}]

        directory = os.path.dirname(os.path.realpath(__file__))
        file_name = directory + "/article_large.xml"
        # If any of this code fails then don't recover gracefully. This is crucial to sorting and pricing.
        tree = etree.parse(file_name)
        root = tree.getroot()

        assert root.tag == "LargeArticle"

        for c in range(0, len(root)):
            if root[c].tag == "Expiry":
                date = datetime.datetime.strptime(root[c].text, "%d/%m/%y")

                self.expiry_date = date.date()
            if root[c].tag == "Requirements":
                for i in range(0, len(root[c])):
                    if root[c][i].tag == "MaxWeight":
                        self.max_weight = int(root[c][i].text)
                    elif root[c][i].tag == "MaxSize":
                        self.max_size = (root[c][i][0].text, root[c][i][1].text)
            elif root[c].tag == "Pricing":
                for i in range(0, len(root[c])):
                    if root[c][i].tag == "Priority":
                        # There is only residue available for small articles
                        self.priority_pricing = self.__extractPricing(root[c][i])
                    elif root[c][i].tag == "Regular":
                        self.regular_pricing = self.__extractPricing(root[c][i])

    def determine_weight_range(self, weight):
        for i, (k, v) in enumerate(self.priority_pricing[1].items()):
            ranges = k.split("-")
            if int(ranges[0]) <= int(weight) <= int(ranges[1]):
                return k

    def __extractPricing(self, root):
        pricing = [{}, {}, {}]
        for c in range(0, len(root)):
            direct_prices = root[c]
            idx = None
            if root[c].tag == "PostcodeDirect":
                idx = 0
            elif root[c].tag == "AreaDirect":
                idx = 1
            elif root[c].tag == "Residue":
                idx = 2

            for i in range(0, len(direct_prices)):
                if idx == 0:
                    pricing[idx][direct_prices[i].tag[1:]] = direct_prices[i][0].text
                else:
                    pricing[idx][direct_prices[i].tag[1:]] = [direct_prices[i][0].text, direct_prices[i][1].text]

        return pricing

    def meets_requirements(self, size, weight):
        not_small = SmallArticle().meets_requirements(size, weight)

        if not not_small:
            if self.min_weight <= weight <= self.max_weight:
                if size[0] < self.max_size[0] and size[1] < self.max_size[1]:
                    return True

        return False

    @staticmethod
    def get_instance():
        if LargeArticle.instance is None:
            LargeArticle.instance = LargeArticle()
        return LargeArticle.instance
