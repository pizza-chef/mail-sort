from abc import ABC, abstractmethod
from maillist.listparserfactory import ListParserFactory


class Workspace(ABC):
    def __init__(self):
        self.lists = []
        self.path = ""
        self.name = ""
        self.pending_list = None
        self.export_list = None
        self.labels = None

    def createMailList(self, file_path, file_type, include_headers, sheetNum):
        parser = ListParserFactory.createMailList(file_type, include_headers, sheetNum)

        if parser is None:
            return False

        read_file = parser.readList(file_path)

        if read_file.num_records == 0:
            return False

        self.pending_list = read_file
        return True

    def addMailList(self):
        self.lists.append(self.pending_list)
        self.pending_list = None

    def removeMailList(self, list_idx):
        self.lists.pop(list_idx)
        if self.path != "":
            self.saveWorkspace()

    def setPath(self, file_path):
        # Sets the file path and extracts the name from the file_path and sets both the directory path and file name
        self.name = file_path.split("/")[-1].split(".")[0]
        self.path = file_path[:len(file_path)-len(self.name)-4]

    def cancelImport(self):
        self.pending_list = None

    @abstractmethod
    def saveWorkspace(self):
        pass

    @abstractmethod
    def createWorkspace(self, file_path):
        pass

    @abstractmethod
    def openWorkspace(self, file_path):
        pass

