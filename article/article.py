from abc import ABC, abstractmethod


class Article(ABC):

    def __init__(self):
        self.max_weight = 0
        self.min_weight = 0
        self.min_size = (0, 0)
        self.max_size = (0, 0)
        self.priority_pricing = None
        self.regular_pricing = None
        self.expiry_date = None

    @staticmethod
    @abstractmethod
    def get_instance():
        pass

    @abstractmethod
    def read_file(self, file_name):
        """
            It is the responsibility of the child class to set the above class variables.
        """
        pass

    @abstractmethod
    def meets_requirements(self, size, weight):
        pass

    @abstractmethod
    def determine_weight_range(self, weight):
        pass