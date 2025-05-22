from lxml import etree
import os


class Settings:
    settings = None

    def __init__(self):
        self.openDir = ""
        self.visaCommand = ""
        self.enableAutoSave = False
        self.saveDir = ""
        self.manifestName = ""
        self.labelPlanName = ""
        self.exportListName = ""

    @staticmethod
    def getSettings():
        """
        Retrieves the global settings used for the program stored in Settings.settings. Follows the singleton pattern
        :return: Settings
        """
        if Settings.settings is None:
            Settings.readSettings()

        return Settings.settings

    @staticmethod
    def readSettings():
        """
        Reads the Settings.xml file
        """
        directory = os.path.dirname(os.path.realpath(__file__))
        file_name = directory + "/settings.xml"

        tree = etree.parse(file_name)
        root = tree.getroot()

        assert root.tag == "Settings"

        newSettings = Settings()

        for c in range(0, len(root)):
            if root[c].tag == "DefaultDirectory":
                for child in root[c]:
                    if child.tag == "Open":
                        newSettings.openDir = child.text
                    elif child.tag == "AutoSave":
                        newSettings.saveDir = child.text
                    elif child.tag == "VisaCommand":
                        newSettings.visaCommand = child.text

            if root[c].tag == "AutoSave":
                for child in root[c]:
                    if child.tag == "Enabled":
                        newSettings.enableAutoSave = True if child.text == "True" else False
                    elif child.tag == "ManifestName":
                        newSettings.manifestName = child.text
                    elif child.tag == "LabelPlanName":
                        newSettings.labelPlanName = child.text
                    elif child.tag == "ExportListName":
                        newSettings.exportListName = child.text

        Settings.settings = newSettings

    def setValues(self, openDir, visaCommand, enableAutoSave, saveDir, manifestName, labelPlanName, exportListName):
        # Function provides an easy way to set all the variables at once for when saving the settings
        self.openDir = openDir
        self.visaCommand = visaCommand
        self.enableAutoSave = enableAutoSave
        self.saveDir = saveDir
        self.manifestName = manifestName
        self.labelPlanName = labelPlanName
        self.exportListName = exportListName

    def writeSettings(self):
        doctype = "<!DOCTYPE msw>\n"

        root = etree.Element("Settings")
        defaultDirectory = etree.SubElement(root, "DefaultDirectory")

        openDir = etree.SubElement(defaultDirectory, "Open")
        openDir.text = self.openDir

        saveDir = etree.SubElement(defaultDirectory, "AutoSave")
        saveDir.text = self.saveDir

        visaCommand = etree.SubElement(defaultDirectory, "VisaCommand")
        visaCommand.text = self.visaCommand

        autoSave = etree.SubElement(root, "AutoSave")

        enabled = etree.SubElement(autoSave, "Enabled")
        enabled.text = str(self.enableAutoSave)

        manifestName = etree.SubElement(autoSave, "ManifestName")
        manifestName.text = self.manifestName

        labelPlanName = etree.SubElement(autoSave, "LabelPlanName")
        labelPlanName.text = self.labelPlanName

        exportListName = etree.SubElement(autoSave, "ExportListName")
        exportListName.text = self.exportListName

        tree = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8', doctype=doctype)

        directory = os.path.dirname(os.path.realpath(__file__))
        file_name = directory + "/settings.xml"
        with open(file_name, 'wb') as f:
            f.write(tree)
