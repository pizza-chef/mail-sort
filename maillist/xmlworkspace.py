from .workspace import Workspace
from lxml import etree
import numpy as np
from .maillist import MailList


class XMLWorkspace(Workspace):
    def __init__(self):
        super(XMLWorkspace, self).__init__()

    def saveWorkspace(self):
        if self.path == "":
            raise ValueError("Workspace is trying to be saved with an unset path")

        doctype = "<!DOCTYPE msw>\n"

        root = etree.Element("workspace")
        name = etree.SubElement(root, "name")
        name.text = self.name

        for i in range(0, len(self.lists)):
            curr_list_root = etree.SubElement(root, "list", id=str(i+1))
            list_name = etree.SubElement(curr_list_root, "name")
            list_name.text = self.lists[i].name
            num_records = etree.SubElement(curr_list_root, "records")
            num_records.text = str(self.lists[i].num_records)
            header_root = etree.SubElement(curr_list_root, "headers")

            for j in range(0, len(self.lists[i].headers)):
                column = etree.SubElement(header_root, "column")
                column.text = self.lists[i].headers[j]
            for j in range(0, len(self.lists[i].content[0])):
                row_root = etree.SubElement(curr_list_root, "row", number=str(j))
                for k in range(0, len(self.lists[i].content)):
                    value = etree.SubElement(row_root, "value")
                    value.text = self.lists[i].content[k][j]

        tree = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8', doctype=doctype)

        with open(self.path + self.name + ".msw", 'wb') as f:
            f.write(tree)

        return True

    def createWorkspace(self, file_path):
        self.setPath(file_path)

        doctype = "<!DOCTYPE msw>\n"

        root = etree.Element("workspace")
        name = etree.SubElement(root, "name")
        name.text = self.name

        tree = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8', doctype=doctype)
        with open(file_path, 'wb') as f:
            f.write(tree)

    def openWorkspace(self, file_path):
        """
        Opens a XML file and restores the state of the workspace if the saved workspace file is valid

        :param file_path: string
                          The absolute file path of the workspace file
        :return: bool
                 status of the workspace file being successfully read
        """

        try:
            tree = etree.parse(file_path)
        except IOError:
            return False

        root = tree.getroot()
        if root.tag != "workspace" or len(root) < 1:
            return False

        workspace_name = root[0].text
        mail_lists = []

        # Iterate over children of the root element.
        for c in range(1, len(root)):
            # The child tags of a list be name, records, headers before the row data can be shown. 1 row is required.

            if self.verifyList(root[c]) != "Valid":
                return False

            name = root[c][0].text
            num_records = int(root[c][1].text)

            # Initialising a numpy array for unknown length strings (dtype=object)
            headers = np.empty(len(root[c][2]), dtype=object)

            for i in range(0, len(headers)):
                headers[i] = root[c][2][i].text

            content = np.empty((num_records, headers.size), dtype=object)
            row_count = 0

            # Iterate over the row data stored in the XML file for the current list
            for i in range(3, len(root[c])):
                for j, value in enumerate(root[c][i]):
                    content[row_count][j] = value.text if value.text is not None else ""
                row_count += 1

            # Number of records doesnt match number of rows saved. Something has gone wrong saving the workspace.
            if row_count != num_records:
                return False

            content = np.transpose(content)
            mail_lists.append(MailList(headers, content, name))

        self.lists = mail_lists
        self.setPath(file_path)
        return True

    def verifyList(self, xml_element):
        """
        Verifies if a root element of a XML tree is in the correct format required of a saved mail list.

        :param xml_element: xml.etree.ElementTree.Element
                            the root element of a mail list that was saved in xml format
        :return: string
                 'Valid' if the XML element is a valid saved list, otherwise an error message describing what was wrong
        """
        if xml_element.tag != "list":
            return "Root element was not a list."
        elif len(xml_element) < 4:
            return "There are not enough child elements. A list needs a name, records, headers, and one or more " \
                   "content rows."
        elif xml_element[0].tag != "name":
            return "The first child element should be a 'name'"
        elif xml_element[1].tag != "records":
            return "The second child element should be the number of 'records'"
        elif xml_element[2].tag != "headers":
            return "The third child element should be a subtree of 'headers'"
        else:
            return "Valid"

    def getName(self):
        return self.name
