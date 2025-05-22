from .article import Article
from lxml import etree
import os
import datetime


class SmallArticle(Article):
    instance = None

    def __init__(self):
        super().__init__()
        self.read_file()

    def read_file(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        file_name = directory + "/article_small.xml"
        # If any of this code fails then don't recover gracefully. This is crucial to sorting and pricing.
        tree = etree.parse(file_name)
        root = tree.getroot()

        assert root.tag == "SmallArticle"

        for c in range(0, len(root)):
            if root[c].tag == "Expiry":
                date = datetime.datetime.strptime(root[c].text, "%d/%m/%y")
                self.expiry_date = date.date()
            if root[c].tag == "Requirements":
                for i in range(0, len(root[c])):
                    if root[c][i].tag == "MaxWeight":
                        self.max_weight = int(root[c][i].text)
                    elif root[c][i].tag == "MinSize":
                        # The first and second children of MinSize are Width and Length
                        self.min_size = (root[c][i][0].text, root[c][i][1].text)
                    elif root[c][i].tag == "MaxSize":
                        self.max_size = (root[c][i][0].text, root[c][i][1].text)
            elif root[c].tag == "Pricing":
                for i in range(0, len(root[c])):
                    if root[c][i].tag == "Priority":
                        # There is only residue available for small articles
                        self.priority_pricing = [root[c][i][0][0][0].text, root[c][i][0][0][1].text]
                    elif root[c][i].tag == "Regular":
                        self.regular_pricing = [root[c][i][0][0][0].text, root[c][i][0][0][1].text]

    def meets_requirements(self, size, weight):
        if self.min_weight <= weight <= self.max_weight:
            if size[0] >= self.min_size[0] and size[1] >= self.min_size[1]:
                if size[1] <= self.max_size[1] and size[1] <= self.max_size[1]:
                    return True
        return False

    def determine_weight_range(self, weight):
        return "0-125"

    @staticmethod
    def get_instance():
        if SmallArticle.instance is None:
            SmallArticle.instance = SmallArticle()
        return SmallArticle.instance

    #TODO NEED A WEIGHT METHOD LIKE LARGE TO CONFORM TO LISKOV SUBSTITUTION PRINCIPLE