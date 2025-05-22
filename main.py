import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QAbstractItemView, \
    QMessageBox, QLabel, QLineEdit, QCheckBox, QTableWidgetItem, QDialog, QFrame, QTableView
from PySide6.QtCore import QDir, QFileInfo, Qt, QSize, QTimer, QPoint
from PySide6.QtGui import QDoubleValidator, QPixmap, QIcon, QBrush, QColor, QIntValidator

from labels.labels import Labels
from maillist.exportlist import ExportList
from maillist.xmlworkspace import XMLWorkspace
from settings.readsettings import Settings
from ui_form import Ui_MainWindow
from maillist.maillist import MailList
from printpost.readprintpost import ReadPrintPost
from maillist.sort import PrintPostSort
from article.largearticle import LargeArticle
from article.smallarticle import SmallArticle
from manifest.createreport import CreateReport
from maillist.maillistparser import MailListParser
import datetime
import numpy as np


class MailSort(QMainWindow):
    # TODO: FIX BUG OF COMBO BOX SHOWING A LIST TWICE. I AM NOT SURE HOW TO REPLICATE THIS. IT JUST HAPPENS?
    def __init__(self):
        super(MailSort, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.path = os.path.dirname(os.path.abspath(__file__))
        # How to set a window title
        self.setWindowTitle("Mail Sort")
        self.load_stylesheet()

        self.workspace = XMLWorkspace()

        self.fileTypeOptions = ["Tab-delimited (*.txt)", "CSV (*.csv)", "Excel (*.xlsx *.xls)"]

        # Storing list of these UI elements to  make it easy to loop over throughout multiple methods
        self.addressFieldBoxes = [self.ui.countryComboBox, self.ui.stateComboBox, self.ui.postcodeComboBox]

        # Storing lists of UI elements that are created programmatically and have usage across multiple methods
        self.headerLabels: list[QLabel] = []
        self.editFieldNames: list[QLineEdit] = []
        self.addFieldBoxes: list[QCheckBox] = []
        self.fieldNameLabels: list[QLabel] = []

        # Keeps track of the current imported list that is rendered so it isn't re-rendered always to save time
        self.currentTableList = -1

        self.activeBtn = self.ui.menuHomeBtn
        self.settings = Settings.getSettings()
        self.connect_ui()

        # Setup for the launch screen
        self.onLaunch()
        self.date = datetime.datetime.today().date()

    def connect_ui(self):
        """
            Associates the functionality within the methods outlined in this file with user interface elements.
        """
        self.ui.menuSettingsBtn.clicked.connect(self.on_menuSettings_clicked)
        self.ui.menuNewWorkspaceBtn.clicked.connect(self.on_menuNewWorkspaceBtn_clicked)
        self.ui.menuOpenWorkspaceBtn.clicked.connect(self.on_menuOpenWorkspaceBtn_clicked)
        self.ui.menuImportListBtn.clicked.connect(self.on_menuImportListBtn_clicked)
        self.ui.contentBtnImportList.clicked.connect(self.on_menuImportListBtn_clicked)
        self.ui.contentBtnConfirmImport.clicked.connect(self.on_contentConfirmImportBtn_clicked)
        self.ui.contentBtnCancelImport.clicked.connect(self.on_contentCancelImportBtn_clicked)
        self.ui.contentBtnBrowseMailFile.clicked.connect(self.on_contentBrowseMailFileBtn_clicked)
        self.ui.listSelectComboBox.activated[int].connect(self.renderListTableView)
        self.ui.contentBtnDeleteList.clicked.connect(self.on_contentDeleteListBtn_clicked)
        self.ui.menuSortBtn.clicked.connect(self.on_menuSortBtn_clicked)
        self.ui.contentBtnSort.clicked.connect(self.on_contentSortBtn_clicked)
        self.ui.menuExportBtn.clicked.connect(self.on_menuExportBtn_clicked)
        self.ui.sortComboBoxSize.currentTextChanged.connect(self.on_sortComboBoxSize_changed)
        self.ui.sortComboBoxDeliveryStandard.currentTextChanged.connect(self.update_pricing)
        self.ui.sortLineEditWeight.textChanged.connect(self.update_pricing)
        self.ui.contentBtnExport.clicked.connect(self.on_contentExportBtn_clicked)
        self.ui.launchBtnNewWorkspace.clicked.connect(self.on_launchBtnNewWorkspace_clicked)
        self.ui.launchBtnOpenWorkspace.clicked.connect(self.on_launchBtnOpenWorkspace_clicked)
        self.ui.menuHomeBtn.clicked.connect(self.on_menuHomeBtn_clicked)
        self.ui.menuSaveWorkspaceBtn.clicked.connect(self.on_menuSaveWorkspaceBtn_clicked)
        self.ui.contentBtnSaveSettings.clicked.connect(self.on_contentBtnSaveSettings_clicked)
        self.ui.contentBtnDefaultSaveDirectory.clicked.connect(self.on_contentBtnDefaultSaveDirectory_clicked)
        self.ui.contentBtnVisaCommand.clicked.connect(self.on_contentBtnVisaCommand_clicked)
        self.ui.contentBtnDefaultOpenDir.clicked.connect(self.on_contentBtnDefaultOpenDir_clicked)
        self.ui.fileTypeComboBox.activated[int].connect(self.on_fileTypeComboBox_activated)
        self.ui.menuLabelsBtn.clicked.connect(self.on_menuLabelsBtn_clicked)
        self.ui.contentBtnGenerateLabels.clicked.connect(self.on_contentBtnGenerateLabels_clicked)
        self.ui.contentBtnPrintLabels.clicked.connect(self.on_contentBtnPrintLabels_clicked)

    def load_stylesheet(self):
        with open(self.path + "\\styles.qss", "r") as f:
            _style = f.read()
            # Have to replace any icons with an absolute path dynamically since css can't read that
            _style = _style.replace("%path%", self.path.replace("\\", "/") + "/images")
            self.setStyleSheet(_style)

    def checkDataSheetExpiryDates(self):
        """
            Checks if any of the data sheets used for pricing or postcode to presort indicator translation have
            expired and need updating or are coming close to expiry.
            :return: str
                If something has expired the name of the data sheet that has expired will be returned otherwise an empty
                string.
        """
        warning_message = ""
        large_article_expiry = self.days_to_expiry(LargeArticle.get_instance().expiry_date)
        if large_article_expiry <= 7:
            if large_article_expiry <= 0:
                warning_message += "Article price data sheet has already expired. Contact Dylan for an updated version"
            else:
                warning_message += "Article price data sheet is expiring in " + str(large_article_expiry) + " days"
        try:
            printPost_expiry = self.days_to_expiry(ReadPrintPost.get_instance().expiry_date)

            if printPost_expiry <= 0:
                warning_message += " Print post sort plan has expired. Contact Dylan for an updated version."
            elif printPost_expiry <= 7:
                warning_message += " Print post sort plan is expiring in " + str(printPost_expiry) + " days."

        except SyntaxError:
            warning_message = "Error when reading the sort plan. Please fix this immediately before attempting to use" \
                              " the program."

        self.ui.launchWarningLabelDescription.setText(warning_message)
        return warning_message

    def days_to_expiry(self, date):
        """
        Calculates the number of days until expiry from today
        :param date - the date of expiry
        :return: int
            number of days
        """
        return (date - datetime.datetime.today().date()).days

    #########################################################################
    # LAUNCH PAGE FUNCTIONS
    #########################################################################

    def onLaunch(self):
        """
            Performs the necessary user interface configurations for displaying the launch
            screen where a user can select to create a new workspace, browse for an old workspace,
            and open recent files.
        """
        image_path = self.path + "\\images\\"
        # Setting the page on the stacked widget to be the launch page
        self.ui.pages.setCurrentIndex(1)

        # Fixing initial launch screen size
        self.resize(800, 450)

        # Setting images for UI elements
        self.setWindowIcon(QIcon(image_path + "taskbar_icon.png"))
        self.ui.launchTitleImage.setPixmap(QPixmap(image_path + "logo.png"))
        self.ui.launchBtnNewWorkspace.setIcon(QIcon(image_path + "new_icon.png"))
        self.ui.launchBtnOpenWorkspace.setIcon(QIcon(image_path + "open_icon.png"))

        # Setting icon for the warning
        warningIcon = QPixmap(image_path + "warning_icon.png")
        self.ui.launchWarningIconLabel.setPixmap(warningIcon.scaled(25, 25, Qt.KeepAspectRatio))

        warning_message = self.checkDataSheetExpiryDates()
        # Hide warning messages if there are none
        if warning_message == "":
            self.ui.launchWarningIconLabel.hide()
            self.ui.launchWarningLabelDescription.hide()

    def on_launchBtnNewWorkspace_clicked(self):
        """
            Creates a new, blank workspace that a user can import files into. The workspace is
            be default not saved. The user can choose to save later, but sometimes a workspace
            isn't needed to be saved.
        """
        self.workspace = XMLWorkspace()
        self.onEndLaunch()

    def on_launchBtnOpenWorkspace_clicked(self):
        """
            Opens an existing workspace (.msw extension) and updates the UI with the corresponding workspace
            data. If opening the workspace is successful than the user will be directed to the workspace page.
        """
        result = self.on_menuOpenWorkspaceBtn_clicked()
        if result == 0:
            self.onEndLaunch()

    def onEndLaunch(self):
        """
            Readjusts the user interface screen size and changes to the workspace page.
            TODO: This isn't a perfect solution with maximising/minimising. Low priority.
        """

        max_width = app.primaryScreen().availableSize().width()
        max_height = app.primaryScreen().availableSize().height()

        start_width = 1200
        start_height = 800

        self.setMaximumSize(max_width, max_height - 25)

        self.setGeometry((max_width - start_width) // 2, (max_height - start_height) // 2, start_width, start_height)

        self.ui.pages.setCurrentIndex(0)

        self.ui.contentFrame.setCurrentIndex(self.navigate("home"))

        # Calling the different functions for setting up the different pages required.
        self.setupMenuUI()
        self.setupImportUI()
        self.setupSortUI()
        self.setupExportUI()
        self.setupLabelsUI()
        self.setupSettings()

    #########################################################################
    # SETUP FUNCTIONS
    #########################################################################

    def setupMenuUI(self):
        """
            Sets up the user interface for the menu by loading any icons and images required.
        """
        self.ui.menuHomeBtn.setIcon(QIcon(self.path + "\\images\\home_icon.png"))
        self.ui.menuImportListBtn.setIcon(QIcon(self.path + "\\images\\import_list_icon.png"))
        self.ui.menuSortBtn.setIcon(QIcon(self.path + "\\images\\sort_icon.png"))
        self.ui.menuExportBtn.setIcon(QIcon(self.path + "\\images\\export_icon.png"))
        self.ui.menuSaveWorkspaceBtn.setIcon(QIcon(self.path + "\\images\\save_icon.png"))
        self.ui.menuNewWorkspaceBtn.setIcon(QIcon(self.path + "\\images\\new_icon.png"))
        self.ui.menuOpenWorkspaceBtn.setIcon(QIcon(self.path + "\\images\\open_icon.png"))
        self.ui.menuSettingsBtn.setIcon(QIcon(self.path + "\\images\\settings_icon.png"))
        self.ui.menuLabelsBtn.setIcon(QIcon(self.path + "\\images\\labels_icon.png"))

        self.changeActiveBtnStyle(self.ui.menuHomeBtn)

    def setupImportUI(self):
        """
            Sets up the user interface for the import page page by creating any labels, showing icons, filling
            combo boxes, and hiding elements.
        """
        self.headerLabels.append(QLabel("Field Name in File", objectName="importTableTitle"))
        self.headerLabels.append(QLabel("Import Name", objectName="importTableTitle"))
        self.headerLabels.append(QLabel("Include Field", objectName="importTableTitle"))

        self.ui.sheetNumLineEdit.setValidator(QIntValidator())

        [self.ui.fieldNameGridLayout.addWidget(self.headerLabels[i], 0, i) for i in range(0, len(self.headerLabels))]

        self.ui.contentBtnImportList.setIcon(QIcon(self.path + "\\images\\import_list_icon.png"))
        self.ui.contentBtnImportList.setIconSize(QSize(40, 40))

        for file_type in self.fileTypeOptions:
            self.ui.fileTypeComboBox.addItem(file_type)

        self.ui.listTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.sheetNumLineEdit.hide()

        self.hideImportElements()

    def setupSortUI(self):
        """
            Sets up the user interface for the import page page by creating any labels, hiding elements and filling
            combo boxes.
        """
        self.ui.sortComboBoxDeliveryStandard.addItem("Regular")
        self.ui.sortComboBoxDeliveryStandard.addItem("Priority")

        self.ui.sortComboBoxSize.addItem("Large letter")
        self.ui.sortComboBoxSize.addItem("Small letter")

        self.ui.sortComboBoxSortPlan.addItem("Print Post")

        # TODO: Manual entry
        # self.ui.sortComboBoxSize.addItem("Manual entry")

        # Setting validators to enforce specific types of entry into line edits.
        self.ui.widthLineEdit.setValidator(QDoubleValidator())
        self.ui.lengthLineEdit.setValidator(QDoubleValidator())
        self.ui.sortLineEditWeight.setValidator(QDoubleValidator())

        self.ui.sortInfoLabelPrices.setText("Enter a weight to see prices.")
        self.ui.sortLineEditDate.setPlaceholderText("Leave blank for today's date: " + self.date.strftime("%d/%m/%y"))

    def setupLabelsUI(self):
        self.ui.labelsThicknessLineEdit.setValidator(QDoubleValidator())
        self.ui.labelsPaperSizeComboBox.addItem("Other")
        self.ui.labelsPaperSizeComboBox.addItem("C5")
        self.ui.labelPlanTableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.ui.labelsDateLineEdit.setPlaceholderText("Leave blank for today's date: " + self.date.strftime("%d/%m/%y"))


    def setupExportUI(self):
        self.ui.exportedListTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def setupSettings(self):

        self.ui.defaultDirectoryLineEdit.setText(self.settings.openDir)
        self.ui.saveDirectoryLineEdit.setText(self.settings.saveDir)
        self.ui.VisaCommandLineEdit.setText(self.settings.visaCommand)
        self.ui.labelPlanNameLineEdit.setText(self.settings.labelPlanName)
        self.ui.manifestNameLineEdit.setText(self.settings.manifestName)
        self.ui.exportListNameLineEdit.setText(self.settings.exportListName)
        self.ui.enableAutoSaveCheckBox.setChecked(self.settings.enableAutoSave)

    #########################################################################
    # MENU FUNCTIONS
    #########################################################################

    def changeActiveBtnStyle(self, new_active):
        """
            Highlights the new current menu button that was selected and returns the old active
            to an inactive style that isn't highlighted
        :param new_active: QPushButton
            The button to make permanently highlighted while it is active
        """
        activeStyle = "font-weight: bold; background-color: rgb(247,247,247);"
        inactiveStyle = "font-weight: none; background-color: rgb(252,252,252);"

        self.activeBtn.setStyleSheet(inactiveStyle)
        new_active.setStyleSheet(activeStyle)
        self.activeBtn = new_active

    def on_menuSaveWorkspaceBtn_clicked(self):
        self.load_stylesheet()
        if self.workspace.path != "":
            self.workspace.saveWorkspace()

        path = self.openFileSelection("Choose the location to save your workspace", "Mail Sort Workspace (*.msw)")

        if path == "":
            return

        self.workspace.setPath(path)
        self.workspace.saveWorkspace()

    def on_menuHomeBtn_clicked(self):
        self.changeActiveBtnStyle(self.ui.menuHomeBtn)
        self.ui.contentFrame.setCurrentIndex(self.navigate("home"))
        self.ui.menuHomeBtn.setStyleSheet("font-weight: bold; background-color: rgb(247,247,247);")

    def on_menuNewWorkspaceBtn_clicked(self):
        """
           This slot function is utilised for the contentNewWorkspaceBtn and subWorkspaceNewBtn. When
           clicked a file dialog will be opened prompting the user to select a location and a name. A
           new .msw file will be created upon a successful name and location selected.
        """
        result = True
        if len(self.workspace.lists) > 0 and self.workspace.path == "":
            result = self.createConfirmationBox("Are you sure you want to create a new workspace without saving the"
                                                " changes of the current workspace?")

        # TODO: NOT RESETTING TABLE PAGE?
        if result:
            self.workspace = XMLWorkspace()
            self.resetTableView()
            self.on_menuHomeBtn_clicked()

    def on_menuOpenWorkspaceBtn_clicked(self):
        """
           This slot function is utilised for both the contentOpenWorkspaceBtn and subWorkspaceOpenBtn
           widgets. When clicked a file dialog will be opened prompting the user to select a file
           from their system to be opened as the workspace. Currently .msw is a valid file extension
           to be opened.
           :returns - int
                An int flag representing the status of opening a workspace
                0 indicates success
                1 indicates a failure in opening the selected workspace
                2 indicates the user cancelled/closed the file dialog.
        """

        file_path = QFileDialog.getOpenFileName(self, "Open workspace", self.settings.openDir, "Mail sort workspace (*.msw)")[0]

        if file_path == '':
            return 2

        result = self.workspace.openWorkspace(file_path)

        if not result:
            QMessageBox.warning(self, "Unable to open workspace", "There was an error when opening the workspace. "
                                                                  "The file structure may be invalid.")
            return 1

        for mail_list in self.workspace.lists:
            self.ui.listSelectComboBox.addItem(mail_list.name)

        self.ui.listSelectComboBox.setCurrentIndex(0)
        self.on_menuHomeBtn_clicked()
        return 0

    def on_menuImportListBtn_clicked(self):
        """
           This slot function is utilised for both the subWorkspaceImportListBtn and
           contentImportWorkspaceBtn widgets. When these widgets are clicked the current page of the
           stacked widget, contentFrame, will be changed to the importMailListPage.
        """
        self.changeActiveBtnStyle(self.ui.menuImportListBtn)
        self.resetImportMailListUI()
        self.ui.contentFrame.setCurrentIndex(self.navigate("import"))

    def on_menuSortBtn_clicked(self):
        if len(self.workspace.lists) == 0:
            QMessageBox.warning(self, "Unable to sort lists", "Please import a list before sorting.")
            return

        self.changeActiveBtnStyle(self.ui.menuSortBtn)
        # Clear current UI contents before sorting
        self.ui.sortLineEditWeight.clear()
        self.ui.sortLineEditPrintPostNumber.clear()
        self.ui.sortLineEditPublicationTitle.clear()
        self.ui.sortComboBoxSize.setCurrentIndex(0)
        self.ui.sortComboBoxDeliveryStandard.setCurrentIndex(0)
        self.ui.sortComboBoxSortPlan.setCurrentIndex(0)
        self.ui.contentFrame.setCurrentIndex(self.navigate("sort"))

    def on_menuExportBtn_clicked(self):
        if len(self.workspace.lists) == 0:
            QMessageBox.warning(self, "Unable to export lists", "Please sort a list before exporting.")
            return

        if self.workspace.export_list is None:
            QMessageBox.warning(self, "Unable to open export page", "Please sort the list before generating the export "
                                                                    "list")
            return

        self.changeActiveBtnStyle(self.ui.menuExportBtn)
        self.ui.exportedListTableWidget.setColumnCount(len(self.workspace.export_list.headers))
        self.ui.exportedListTableWidget.setRowCount(self.workspace.export_list.num_records)
        self.ui.exportedListTableWidget.setHorizontalHeaderLabels(self.workspace.export_list.headers)

        for i in range(0, len(self.workspace.export_list.content)):
            for j in range(0, len(self.workspace.export_list.content[i])):
                self.ui.exportedListTableWidget.setItem(j, i,
                                                        QTableWidgetItem(self.workspace.export_list.content[i][j]))
        self.ui.contentFrame.setCurrentIndex(self.navigate("export"))

    def on_menuLabelsBtn_clicked(self):
        if self.workspace.labels is None:
            QMessageBox.warning(self, "Unable to show labels", "Please sort a list before creating/printing labels.")
            return

        self.changeActiveBtnStyle(self.ui.menuLabelsBtn)
        self.ui.contentFrame.setCurrentIndex(self.navigate("labels"))

        if self.workspace.labels.labelPlanFileText != "":
            self.ui.contentBtnPrintLabels.show()
        else:
            self.ui.contentBtnPrintLabels.hide()

    def on_menuSettings_clicked(self):
        self.ui.contentFrame.setCurrentIndex(self.navigate("settings"))
        self.changeActiveBtnStyle(self.ui.menuSettingsBtn)

    #########################################################################
    # SETTINGS FUNCTIONS
    #########################################################################

    def setSettingsDirectory(self, lineEdit):
        directory_path = QFileDialog.getExistingDirectory(self, "Select Directory", QDir.homePath())

        if directory_path == "":
            return

        lineEdit.setText(directory_path)

    def on_contentBtnSaveSettings_clicked(self):
        openDir = self.ui.defaultDirectoryLineEdit.text()
        saveDir = self.ui.saveDirectoryLineEdit.text()
        visaCommandDir = self.ui.VisaCommandLineEdit.text()
        labelPlanName = self.ui.labelPlanNameLineEdit.text()
        manifestName = self.ui.manifestNameLineEdit.text()
        exportListName = self.ui.exportListNameLineEdit.text()
        enableAutoSave = self.ui.enableAutoSaveCheckBox.isChecked()
        lineEdits = [openDir, saveDir, visaCommandDir, labelPlanName, manifestName, exportListName]
        for text in lineEdits:
            if text == "":
                QMessageBox.warning(self, "Empty settings", "One or more settings have been left blank.")
                return

        self.settings.setValues(openDir, visaCommandDir, enableAutoSave, saveDir, manifestName,
                                labelPlanName, exportListName)

        self.settings.writeSettings()

    def on_contentBtnDefaultSaveDirectory_clicked(self):
        self.setSettingsDirectory(self.ui.saveDirectoryLineEdit)

    def on_contentBtnVisaCommand_clicked(self):
        self.setSettingsDirectory(self.ui.VisaCommandLineEdit)

    def on_contentBtnDefaultOpenDir_clicked(self):
        self.setSettingsDirectory(self.ui.defaultDirectoryLineEdit)

    #########################################################################
    # IMPORT FILE FUNCTIONS
    #########################################################################

    def on_contentBrowseMailFileBtn_clicked(self):
        """
          When the contentBrowseMailFileBtn widget is clicked this function will open a file
          dialog prompting the user to select a mail file of their chosen extension to be imported
          into the workspace.
        """
        filter_selection = self.ui.fileTypeComboBox.currentIndex()
        self.resetImportMailListUI()

        if filter_selection >= len(self.fileTypeOptions):
            raise IndexError("Selection from the box was more than number of options.")

        file_path = QFileDialog.getOpenFileName(self, "Select a mail list to import", QDir.homePath(),
                                                self.fileTypeOptions[filter_selection])[0]

        if file_path == "":
            return

        self.ui.fileNameEdit.setText(QFileInfo(file_path).baseName())

        # Check if user wants to include headers
        include_headers = self.ui.includeHeadersCheckBox.isChecked()

        # Sheet number in case it is an excel document
        sheetNumber = self.ui.sheetNumLineEdit.text()

        result = self.workspace.createMailList(file_path, self.fileTypeOptions[filter_selection], include_headers,
                                               sheetNumber)

        # If workspace failed to open the file and convert it into a MailList type then report error.
        if not result:
            QMessageBox.warning(self, "Error", "Error when reading the file. If "
                                               "selecting excel ensure the sheet number inputted exists.")
            return

        # Show the next elements that should be filled in by the user
        self.showImportElements()

        # Display number of records so the user can check if number of records imported matches the file.
        self.ui.contentLabelRecordsRead.setText("Records read: " + str(self.workspace.pending_list.num_records))

        # Show the headers and auto fill combobox with any address (i.e country/postcode) fields that were detected
        self.updateImportMailListUI(self.workspace.pending_list.headers)

    def on_fileTypeComboBox_activated(self, index):
        if "Excel" in self.fileTypeOptions[index]:
            self.ui.sheetNumLineEdit.show()
        else:
            self.ui.sheetNumLineEdit.hide()

    def on_importCheckBox_clicked(self, _):
        """
           When a clicked signal is detected from a checkbox that is on the importMailListPage this
           function will be executed. Combo boxes will be updated to only show the fields that are checked
           and text edits will be disabled if checked off.

           A more efficient method is to find the corresponding checkbox state that was changed
           and update the UI so its corresponding text edit is changed to be editable/non editable
           and the combo boxes will either insert/remove that option from their list.

           Use the above method if there are performance difficulties. Otherwise it's easier and more readable using
           the below method.
        """

        for comboBox in self.addressFieldBoxes:
            comboBox.clear()

        self.addressFieldBoxes[0].addItem("")  # The first combo box, country, is optional.

        headers = self.workspace.pending_list.headers

        selected_headers = []

        for i in range(0, len(self.addFieldBoxes)):
            checkBool = True if self.addFieldBoxes[i].checkState() == Qt.CheckState.Checked else False
            if checkBool:
                # Adding option to combo boxes
                for comboBox in self.addressFieldBoxes:
                    comboBox.addItem(headers[i])
                selected_headers.append(headers[i])

            # Toggling ability to edit based on check status
            self.editFieldNames[i].setEnabled(checkBool)

        selected_address_fields = MailListParser.identifyAddressField(selected_headers)

        for i in range(0, len(self.addressFieldBoxes)):
            if selected_address_fields[i] != -1:
                if i == 0:  # Country box has an option of blank so the indexes are increased by 1
                    self.addressFieldBoxes[i].setCurrentIndex(selected_address_fields[i] + 1)
                else:
                    self.addressFieldBoxes[i].setCurrentIndex(selected_address_fields[i])
            else:
                self.addressFieldBoxes[i].setCurrentIndex(-1)

    def showImportElements(self):
        """
           Hides certain elements on the importMailListPage that should only be displayed after
           the user completes certain steps
        """
        self.ui.fileNameEdit.show()
        self.ui.contentBtnConfirmImport.show()
        self.ui.addressConfirmationFrame.show()
        self.ui.contentLabelRecordsRead.show()
        [self.headerLabels[i].show() for i in range(0, len(self.headerLabels))]


    def hideImportElements(self):
        """
           Shows certain elements on the importMailListPage that are displayed after certain steps
           have been completed by the user.
        """
        self.ui.fileNameEdit.hide()
        self.ui.contentBtnConfirmImport.hide()
        self.ui.addressConfirmationFrame.hide()
        self.ui.contentLabelRecordsRead.hide()
        [self.headerLabels[i].hide() for i in range(0, len(self.headerLabels))]

    def updateImportMailListUI(self, headers):
        """
           Updates the importMailListPage's interface to display labels, text edits, and check boxes
           for editing header information that has been read from a file.
           Parameters:
                headers - the headers of a MailList file that has been read
         """


        for i in range(0, len(headers)):
            self.fieldNameLabels.append(QLabel(headers[i], objectName="contentLabel"))
            self.editFieldNames.append(QLineEdit(headers[i], objectName="contentLineEdit"))
            self.addFieldBoxes.append(QCheckBox("", self, objectName="contentCheckBox"))

            self.addFieldBoxes[-1].clicked[bool].connect(self.on_importCheckBox_clicked)

            self.addFieldBoxes[-1].setCheckState(Qt.Checked)

            self.ui.fieldNameGridLayout.addWidget(self.fieldNameLabels[-1], i + 1, 0)

            self.ui.fieldNameGridLayout.addWidget(self.editFieldNames[-1], i + 1, 1)

            self.ui.fieldNameGridLayout.addWidget(self.addFieldBoxes[-1], i + 1, 2)

            for j in range(0, len(self.addressFieldBoxes)):
                self.addressFieldBoxes[j].addItem(headers[i])

        address_fields = self.workspace.pending_list.address_columns

        # Add an optional for the country field
        self.ui.countryComboBox.addItem("")

        for i in range(0, len(self.addressFieldBoxes)):
            self.addressFieldBoxes[i].setCurrentIndex(address_fields[i])

    def resetImportMailListUI(self):
        """
            Resets the ImportMailList page user interface to a state before a list was imported.
           This function will delete any half made MailLists that are created during the import process
           and delete any UI element on the screen that was dynamically rendered for the list imported.
        """
        self.workspace.cancelImport()

        for i in range(len(self.editFieldNames) - 1, -1, -1):
            self.ui.fieldNameGridLayout.removeWidget(self.editFieldNames[i])
            self.ui.fieldNameGridLayout.removeWidget(self.addFieldBoxes[i])
            self.ui.fieldNameGridLayout.removeWidget(self.fieldNameLabels[i])

            self.editFieldNames[i].deleteLater()
            self.addFieldBoxes[i].deleteLater()
            self.fieldNameLabels[i].deleteLater()

        self.editFieldNames = []
        self.addFieldBoxes = []
        self.fieldNameLabels = []

        for box in self.addressFieldBoxes:
            box.clear()

        self.hideImportElements()

    def on_contentConfirmImportBtn_clicked(self):
        """
           The contentImportBtn slot function for when the button is clicked will finalise any changes
           that the user made when importing the list and save it to the workspace in memory and into
           the created workspace file. This function also utilises the resetImportMailListUI
           function to reset the workspace and UI.
        """
        new_name = self.ui.fileNameEdit.text()
        new_column_names, selected_headers = [], []

        for i in range(0, len(self.addFieldBoxes)):
            if self.addFieldBoxes[i].checkState() == Qt.CheckState.Checked:
                new_column_names.append(self.editFieldNames[i].text())
                selected_headers.append(self.workspace.pending_list.headers[i])

        if len(selected_headers) == len(self.workspace.pending_list.headers):
            # If user wants to get all columns then don't waste time reconstructing a new list
            new_mail_list = self.workspace.pending_list
            new_mail_list.name = new_name
            new_mail_list.headers = np.array(new_column_names)
        else:
            new_mail_list = MailList.subset(selected_headers, self.workspace.pending_list, new_name, new_column_names)

        # Validate the list before finalising the import
        result = self.validateImport(new_mail_list)

        if result != "":
            QMessageBox.warning(self, "Error when importing", result)
            return

        # Setting address fields from what user has selected in combo boxes
        address_fields = self.workspace.pending_list.address_columns

        for i in range(0, len(self.addressFieldBoxes)):
            address_fields[i] = self.addressFieldBoxes[i].currentIndex()

        # If the user chosen to set a state so they can check for bad postcode/state combinations then rename column
        if address_fields[1] != -1:
            new_mail_list.headers[address_fields[1]] = "State"

        # Setting the postcode column name as postcode
        new_mail_list.headers[address_fields[-1]] = "Postcode"

        self.workspace.pending_list = new_mail_list
        self.workspace.pending_list.address_columns = address_fields
        # Adding the list as a possible selection in the table view
        self.ui.listSelectComboBox.addItem(self.workspace.pending_list.name)
        # Assign sort codes to the postcode
        self.workspace.pending_list.assign_sort_codes()

        # Identify any issues where postcode is not in state
        self.workspace.pending_list.identify_bad_states()

        self.workspace.addMailList()
        # Only save the workspace if the user has chosen create a workspace file on hard disk.
        if self.workspace.path != "":
            self.workspace.saveWorkspace()

        # Setting export_list to None as a new list needs to be sorted with the rest
        self.workspace.export_list = None
        self.workspace.labels = None

        self.resetImportMailListUI()

        self.on_menuHomeBtn_clicked()

        # Rerender the table view and change combo box to display the list that was just imported
        self.ui.listSelectComboBox.setCurrentIndex(len(self.workspace.lists) - 1)
        self.renderListTableView(len(self.workspace.lists) - 1)

    def validateImport(self, to_validate):
        """
           A Mail List uploaded by the user is validated before being allowed to upload. A Mail List
           must have the correct address fields present to be valid for import.
           An error message describing what went wrong when importing will be returned if unsuccessful.
           Otherwise an empty string indicates success.
        """

        duplicates = np.zeros(len(to_validate.headers))
        if self.ui.postcodeComboBox.currentIndex() == -1 or self.ui.stateComboBox.currentIndex() == -1:
            return "Please enter the column corresponding to postcode or state."

        # Checking for duplicates
        for i in range(0, len(self.addressFieldBoxes)):
            currentIdx = self.addressFieldBoxes[i].currentIndex()

            if currentIdx >= 0:
                duplicates[currentIdx] += 1

            if duplicates[currentIdx] > 1:
                return "More than address field option is using the same column."

        # Checking that header names are unique
        if len(set(to_validate.headers)) != len(to_validate.headers):
            return "More than one column header has the same name"

        return ""

    def on_contentCancelImportBtn_clicked(self):
        """
           The contentCancelImportBtn slot function cancels the current file import that is in progress
           and returns to the main workspace.
        """
        if self.workspace.pending_list is not None:
            result = self.createConfirmationBox("A list is currently being imported", "Do you want to cancel?")

            if not result:
                return

        self.resetImportMailListUI()
        self.on_menuHomeBtn_clicked()

    #########################################################################
    # MAIL LIST TABLE PAGE FUNCTIONS
    #########################################################################

    def resetTableView(self):
        self.ui.listTableWidget.clear()
        self.ui.listSelectComboBox.clear()
        self.ui.warningsDescription.clear()
        self.ui.warningsLabel.clear()
        self.currentTableList = -1

    def renderListTableView(self, index, rerender=0):
        """
              The renderListTableView slot function updates the workspaceListView page. This includes upating
              the rows and columns in the listTableWidget to display the contents of the MailList selected
              through the listSelectComboBox widget, if required. Summary information about the list and
              workspace will be updated on the page also.
              Parameters:
               index - a valid index of a MailList stored in the workspace
               rerender - an optional boolean value specifiying to forcible rerender the list even if the
                          same table is being displayed. Useful for when the combo box indexes change or
                          the values in a table change.

              Note: listSelectComboBox widget is connected with the activated signal instead of the
              signal for the current index changed. This main difference is that activated is a signal
              that only executes its slot function when the user makes the change instead of executing
              on both programmatic and user changes.
           """
        # Don't rebuild the table view if it's the same as before and not being forcibly rerendered
        if (self.currentTableList == index and not rerender) or index < 0 or index >= len(self.workspace.lists):
            return

        # Clear the table view if its previously occupied
        if self.currentTableList != -1:
            self.ui.listTableWidget.clear()

        mail_list: MailList = self.workspace.lists[index]

        self.ui.valueLabelRecords.setText(str(mail_list.num_records))
        self.ui.valueLabelColumns.setText(str(len(mail_list.headers)))

        # The check for incorrect states may not be completed as this is something that is computed not stored
        # so we need to attempt to recompute it again
        if mail_list.incorrect_states is None:
            mail_list.address_columns = MailListParser.identifyAddressField(mail_list.headers)
            mail_list.identify_bad_states()

        warningIndices = []

        # If incorrect_states is still none it means that the State column was never detected or supplied.
        if mail_list.incorrect_states is not None and len(mail_list.incorrect_states) == 0:
            self.ui.warningsLabel.setText("")
            self.ui.warningsDescription.setText("There are no warnings to display.")
        elif mail_list.incorrect_states is not None:
            self.ui.warningsDescription.setText("Below are lines that have postcodes that don't belong in the given "
                                                "state as described in the PreSort Indicator Plan.\n")
            warningsText = ""
            warningsText += "Number of warnings: " + str(len(mail_list.incorrect_states)) + "\n"
            for warning in mail_list.incorrect_states:
                warningsText += "Line " + str(warning[0] + 1) + ": Matching state should be " + warning[
                    1].upper() + "\n"

                # Getting just the indices of warning cells
                warningIndices.append(warning[0])

            self.ui.warningsLabel.setText(warningsText.strip())

        self.currentTableList = index
        self.ui.listTableWidget.setColumnCount(len(mail_list.headers))
        self.ui.listTableWidget.setRowCount(mail_list.num_records)
        self.ui.listTableWidget.setHorizontalHeaderLabels(mail_list.headers)

        # Note QTableWidget won't take an int as an argument and will not provide warnings and therefore just render ""
        for i in range(0, len(mail_list.content)):
            for j in range(0, len(mail_list.content[i])):
                table_widget_item = QTableWidgetItem(mail_list.content[i][j])
                if j in warningIndices:
                    table_widget_item.setBackground(QBrush(QColor(Qt.yellow)))
                self.ui.listTableWidget.setItem(j, i, table_widget_item)

    def on_contentDeleteListBtn_clicked(self):
        """
           After getting confirmation of deleted from a confirmation box, the current mail list will
           be deleted from the workspace and the UI updated to reflect that. The UI may also change
           screens if the list that was deleted was the only list in the workspace.
        """
        delete_list = self.createConfirmationBox("Delete this mail list.", "Are you sure you want to delete this"
                                                                           " list?")
        if not delete_list:
            return

        curr_list_idx = self.ui.listSelectComboBox.currentIndex()
        self.workspace.removeMailList(curr_list_idx)
        self.ui.listSelectComboBox.removeItem(curr_list_idx)

        # If we have emptied the lists in the workspace then change pages
        if len(self.workspace.lists) == 0:
            self.currentTableList = -1
            self.on_menuHomeBtn_clicked()
            return

        self.renderListTableView(self.ui.listSelectComboBox.currentIndex(), True)

    #########################################################################
    # SORT FILE PAGE FUNCTIONS
    #########################################################################

    def update_pricing(self):
        """
            Updates the contentLabelPrice UI element to display the price of sending a single article given
            the weight, type of letter, and the type of delivery service.
        """
        if self.ui.sortLineEditWeight.text() == '':
            self.ui.sortInfoLabelPrices.setText("Enter a weight to see prices.")
            self.clear_price_table()
            return

        # Even with a validator for numbers only it allows e since its technically a number so has to be checked for
        if "e" == self.ui.sortLineEditWeight.text()[-1] or "-" == self.ui.sortLineEditWeight.text()[-1]:
            self.ui.sortLineEditWeight.setText((self.ui.sortLineEditWeight.text()[:-1]))
            return

        lArticle = LargeArticle.get_instance()
        sArticle = SmallArticle.get_instance()

        weight = int(self.ui.sortLineEditWeight.text())
        weight_category = lArticle.determine_weight_range(weight)
        price_text = ""

        if self.ui.sortComboBoxSize.currentText() == "Small letter":
            if weight > 125 or weight < 0:
                price_text = "No prices available for weights greater than 125g for a small letter."
                self.clear_price_table()
            else:
                if self.ui.sortComboBoxDeliveryStandard.currentText() == "Priority":
                    residue = sArticle.priority_pricing
                else:
                    residue = sArticle.regular_pricing
                self.render_price_table(residue, [], "0")
        else:
            if weight > 1000 or weight < 0:
                price_text = "No prices available for weights greater than 1000g for a large letter."
                self.clear_price_table()
            else:
                if self.ui.sortComboBoxDeliveryStandard.currentText() == "Priority":
                    residue = lArticle.priority_pricing[2][weight_category]
                    area = lArticle.priority_pricing[1][weight_category]
                    postcode = lArticle.priority_pricing[0][weight_category]
                else:
                    residue = lArticle.regular_pricing[2][weight_category]
                    area = lArticle.regular_pricing[1][weight_category]
                    postcode = lArticle.regular_pricing[0][weight_category]

                self.render_price_table(residue, area, postcode)

        self.ui.sortInfoLabelPrices.setText(weight_category + "g" if price_text == "" else price_text)

    def clear_price_table(self):
        """
            Removes all widgets from the priceGridLayout
        """
        # if there is an item at position 0, 1 it means the table has bee filled to some extent
        if self.ui.priceGridLayout.itemAtPosition(0, 1) is not None:
            # Removing all widgets from the layout
            for row in range(0, 4):
                for column in range(0, 3):
                    label = self.ui.priceGridLayout.itemAtPosition(row, column)
                    if label is not None:
                        label = label.widget()
                        label.deleteLater()

    def render_price_table(self, residue: list[str], area: list[str], postcode: str):
        """
        Renders the priceGridLayout to display the pricing of the residue, area, and postcode values given.
        :param residue:
            A length 2 list of prices for residue in same state and other state. An empty list should be passed for
            small letters.
        :param area:
            A length 2 list of prices for area direct in same state and other state. An empty list should be passed
            for small letters.
        :param postcode:
            Price for postcode direct. Leave as 0 if its for small letters.
        """
        # Note if this shows performance issues then rather than redrawing, a reference can be kept and text set
        self.clear_price_table()

        # Building the tables row/column headers
        self.ui.priceGridLayout.addWidget(QLabel("Same state", objectName="priceTableTitles"), 0, 1)
        self.ui.priceGridLayout.addWidget(QLabel("Other state", objectName="priceTableTitles"), 0, 2)

        if len(residue) > 0:
            self.ui.priceGridLayout.addWidget(QLabel("Residue", objectName="priceTableTitles"), 1, 0)
            self.ui.priceGridLayout.addWidget(QLabel("$" + str(residue[0])), 1, 1)
            self.ui.priceGridLayout.addWidget(QLabel("$" + str(residue[1])), 1, 2)

        if len(area) > 0:
            self.ui.priceGridLayout.addWidget(QLabel("Area Direct", objectName="priceTableTitles"), 2, 0)
            self.ui.priceGridLayout.addWidget(QLabel("$" + str(area[0])), 2, 1)
            self.ui.priceGridLayout.addWidget(QLabel("$" + str(area[1])), 2, 2)

        if float(postcode) > 0:
            self.ui.priceGridLayout.addWidget(QLabel("Postcode Direct", objectName="priceTableTitles"), 3, 0)
            self.ui.priceGridLayout.addWidget(QLabel("$" + str(postcode)), 3, 1)
            self.ui.priceGridLayout.addWidget(QLabel("-"), 3, 2)

    def on_sortComboBoxSize_changed(self, value):
        """
        Updates the user interface to allow manual entry of width and length for the size of an article if
        the manua entry combo box item was selected.
        :param value: The current value of the combo box i.e. the text in the current selected index of the combo box
        """
        if value != "Manual entry":
            self.ui.widthLineEdit.hide()
            self.ui.lengthLineEdit.hide()
        else:
            self.ui.contentLabelPrice.hide()
            self.ui.widthLineEdit.show()
            self.ui.lengthLineEdit.show()

        self.update_pricing()

    def validateDate(self, date):
        """
        Checks the date is of DD/MM/YY format
        :param date: date to validate
        :return: boolean
        """
        validDate = True
        try:
            self.date = datetime.datetime.strptime(date, "%d/%m/%y").date()
        except ValueError:
            validDate = False
            # Reset the date if it's incorrect
            self.date = datetime.datetime.today().date()

        if date != "":
            if not validDate:
                QMessageBox.warning(self, "Invalid Date", "Please enter a date in the format DD/MM/YY")
                return False
        else:
            # Reset the date if it's left blank
            self.date = datetime.datetime.today().date()

        return True

    def validateSort(self):
        if not self.validateDate(self.ui.sortLineEditDate.text()):
            return False

        if self.ui.sortLineEditWeight.text() == "":
            QMessageBox.warning(self, "Missing fields", "Please enter a weight value.")
            return False

        weight = int(self.ui.sortLineEditWeight.text())

        if self.ui.sortComboBoxSize.currentText() == "Large letter":
            if weight < 0 or weight > 1000:
                QMessageBox.warning(self, "Out of range weight", "Please enter a valid weight for large letters.")
                return False

        elif self.ui.sortComboBoxSize.currentText() == "Small letter":
            if weight < 0 or weight > 125:
                QMessageBox.warning(self, "Out of range weight", "Please enter a valid weight for small letters.")
                return False

        if self.ui.sortLineEditPrintPostNumber.text() == "" or \
                self.ui.sortLineEditPublicationTitle.text() == "":
            QMessageBox.warning(self, "Missing fields", "Please enter values into all fields before sorting.")
            return False

        return True

    def determine_article_size(self):
        """
        Determines the size of an article based on the weight and dimensions of an article.
        :return: 'Large', 'Small', or 'Dimensions or weight exceed maximum allowed'
        """
        weight = int(self.ui.sortLineEditWeight.text())
        size = (float(self.ui.widthLineEdit.toPlainText()), float(self.ui.lengthLineEdit.toPlainText()))

        small_article = SmallArticle().meets_requirements(size, weight)
        if small_article:
            return "small"

        large_article = LargeArticle().meets_requirements(size, weight)
        if large_article:
            return "large"

        return "Dimensions or weight exceed maximum allowed."

    def on_contentSortBtn_clicked(self):
        if not self.validateSort():
            return

        # Set the labels date text to be the same if it passed
        self.ui.labelsDateLineEdit.setText(self.date.strftime("%d/%m/%y"))

        delivery_standard = self.ui.sortComboBoxDeliveryStandard.currentText()
        weight = int(self.ui.sortLineEditWeight.text())

        if weight <= 0:
            QMessageBox.warning(self, "Weight error", "The weight entered is less than or equal to 0")
            return

        # Converting a string in a format such as 100-250g and getting the number between
        if self.ui.sortComboBoxSize.currentText() == "Manual Entry":
            size = self.determine_article_size()

            # Invalid size given
            if size != "small" or size != "large":
                QMessageBox.warning(self, "Invalid size entered", "The size entered does not fit into either small "
                                                                  "or large article")
                # TODO: Show error that the manual entry size does not fit
                return
        else:
            # Extract the first word from the combo box text as only "small" or "large" is needed.
            size = self.ui.sortComboBoxSize.currentText().split(" ")[0]

        # First sort the list by presort indicator and postcode so we can calculate the categories
        preprocessedList = PrintPostSort.preprocessList(self.workspace.lists)

        categories = PrintPostSort.organiseCategories(preprocessedList, weight, size, "VIC")

        self.workspace.export_list = ExportList.createExportList(preprocessedList, categories)

        # Generate labels from the organised categories
        # TODO: Try catch to alert if failed to read
        # Taking size[0] as we only need first letter

        labelName = self.workspace.name
        if labelName == "":
            labelName = self.settings.labelPlanName

        self.workspace.labels = Labels(delivery_standard.lower(), size[0], categories, labelName, weight, self.date)
        # Generate manifest from organised categories
        post_number = self.ui.sortLineEditPrintPostNumber.text()
        title = self.ui.sortLineEditPublicationTitle.text()
        total = len(self.workspace.export_list.content[0])

        if size.lower() == "large":
            pricing = LargeArticle.get_instance()
        else:
            pricing = SmallArticle.get_instance()

        if self.settings.enableAutoSave:
            path_to_save = self.settings.saveDir + "/" + self.settings.manifestName + ".pdf"
        else:
            path_to_save = self.openFileSelection("Choose the location to save the manifest", "PDF (*.pdf)")

        if path_to_save == "":
            return

        report = CreateReport(self.date)

        report.create_pdf(path_to_save, categories, title, post_number, weight, delivery_standard, total,
                          size, pricing)

        self.createInformationBox("Print Post Manifest has been saved")

    #########################################################################
    # EXPORT FILE PAGE FUNCTIONS
    #########################################################################

    def on_contentExportBtn_clicked(self):
        if self.workspace.export_list is None:
            return

        to_write = '\t'.join(self.workspace.export_list.headers) + "\n"
        for i in range(0, self.workspace.export_list.num_records):
            for j in range(0, len(self.workspace.export_list.content) - 1):
                to_write += ("" if self.workspace.export_list.content[j][i] is None else
                             self.workspace.export_list.content[j][i]) + "\t"

            to_write += ("" if self.workspace.export_list.content[-1][i] is None else
                         self.workspace.export_list.content[-1][i]) + "\n"

        if not self.settings.enableAutoSave:
            path_to_save = self.openFileSelection("Choose the location to save the export file",
                                                  "Text Tab Delimited (*.txt)")
        else:
            path_to_save = self.settings.saveDir + "/" + self.settings.exportListName + ".txt"

        if path_to_save == "":
            return

        with open(path_to_save, "w") as f:
            f.write(to_write)

        self.createInformationBox("Export file has been saved")

    #########################################################################
    # LABELS PAGE FUNCTIONS
    #########################################################################

    def on_contentBtnGenerateLabels_clicked(self):
        """
        Generates the text for a label plan file (without writing it yet) and displays what labels would be generated
        and the corresponding quantities in the table.
        """
        if not self.validateDate(self.ui.labelsDateLineEdit.text()):
            return

        self.workspace.labels.date = Labels.getDateString(self.date)
        if not self.validateLabelsGeneration():
            QMessageBox.warning(self, "Invalid Thickness Entered", "Please enter a value for the thickness or ensure "
                                                                   "it is only numbers")
            return

        if self.workspace.labels is None:
            QMessageBox.warning(self, "Workspace has not been sorted", "Please sort the mail list before generating"
                                                                       "labels")
            return

        thickness = float(self.ui.labelsThicknessLineEdit.text())
        # Articles per tray needs to be called before label plan can be built
        self.workspace.labels.calculateArticlesPerTray(thickness, self.ui.labelsPaperSizeComboBox.currentText())
        # Generating the file text and plan details based on the information set above
        self.workspace.labels.createFileText()

        planDetails = self.workspace.labels.planDetails

        self.ui.labelPlanTableWidget.clear()

        self.ui.labelPlanTableWidget.setColumnCount(len(planDetails[0]) if len(planDetails) > 0 else 0)
        self.ui.labelPlanTableWidget.setRowCount(len(planDetails))
        self.ui.labelPlanTableWidget.setHorizontalHeaderLabels(["State", "Sort Plan", "Label Quantity"
                                                                , "Total Articles"])

        # Note QTableWidget won't take an int as an argument and will not provide warnings and therefore just render ""
        for i in range(0, len(planDetails)):
            for j in range(0, len(planDetails[i])):
                table_widget_item = QTableWidgetItem(str(planDetails[i][j]))
                self.ui.labelPlanTableWidget.setItem(i, j, table_widget_item)

        self.ui.contentBtnPrintLabels.show()

    def validateLabelsGeneration(self):
        if self.ui.labelsThicknessLineEdit.text() == "" or "e" in self.ui.labelsThicknessLineEdit.text():
            return False
        return True

    def on_contentBtnPrintLabels_clicked(self):
        """
        Saves the label plan file at either a user given location or the set auto-save location then imports and prints
        the label plan with VisaLabels.
        Windows update overwriting file name??
        """
        if self.settings.enableAutoSave:
            path_to_save = self.settings.saveDir + "\\" + self.settings.labelPlanName + ".lpf"

        else:
            path_to_save = self.openFileSelection("Choose the location to save the label plan file", "lpf (*.lpf)")

        if path_to_save == "":
            return

        labelPlanFileText = self.workspace.labels.labelPlanFileText

        with open(path_to_save, "w+") as f:
            f.write(labelPlanFileText)

        # VisaCommand won't accept / in the path_to_save and only accepts \
        path_to_save = path_to_save.replace("/", "\\")

        # Attempt to delete an existing one to override it
        command = '"' + self.settings.visaCommand + '" /d "' + self.workspace.labels.name + '"'
        subprocess.run(command, shell=True)

        # Import the label plan
        command = '"' + self.settings.visaCommand + '" /i "' + path_to_save + '"'
        subprocess.run(command, shell=True)

        # Print the label plan now
        command = '"' + self.settings.visaCommand + '" /p "' + self.workspace.labels.name + '"'
        subprocess.run(command, shell=True)

        self.createInformationBox("Label File Plan has been saved and printed")


    #########################################################################
    # ACCESSORY FUNCTIONS
    #########################################################################

    def createConfirmationBox(self, text, informative_text=""):
        """
           Creates a message box that records the result of the users choice for confirming or
           cancelling.
           Parameters:
                text - The main text to display to the message formatted in bold
                informative_text - extra information underneath the main text
           Returns:
                A boolean representing the users choice to confirm (true) or cancel (false)
        """
        msgBox = QMessageBox(parent=self)
        msgBox.setWindowTitle("Mail Sort")
        msgBox.setText(text)

        if informative_text != "":
            msgBox.setInformativeText(informative_text)

        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Ok)

        ret = msgBox.exec()

        if ret == QMessageBox.Ok:
            confirm = True
        elif ret == QMessageBox.Cancel:
            confirm = False
        else:
            raise ValueError("Value returned from message box is neither Ok or Cancel.")

        return confirm

    def createInformationBox(self, information: str):
        """
        Creates a non-modal dialog box that appears and does not take focus from the main UI. This attempts
        to behave similar to a toast like in android. This should display a short message to the user as
        feedback.
        :param information: Message to display to the user
        """
        # Look for any current dialog boxes showing and cancel them so there's no overlap.
        topLevelWidgets = QApplication.topLevelWidgets()
        for widget in topLevelWidgets:
            if type(widget) == QDialog:
                widget.close()

        msgBox = QDialog(self, objectName="dialogBox")
        frame = QFrame(msgBox, objectName="dialogFrame")
        label = QLabel(frame, objectName="dialogLabel")
        label.setText(information)

        # Determinig dimensions to resize the frame so the text feats neatly inside it
        labelWidth = label.fontMetrics().boundingRect(label.text()).width()
        labelHeight = label.fontMetrics().boundingRect(label.text()).height()
        frame.resize(labelWidth+30, labelHeight*1.8)

        # Sets the dialog to have no frame i.e. looks like a toast
        msgBox.setWindowFlag(Qt.FramelessWindowHint, True)
        msgBox.setAttribute(Qt.WA_TranslucentBackground)
        # Doesn't set the focus on the dialog when shown
        msgBox.setAttribute(Qt.WA_ShowWithoutActivating)

        # Map to global using a 0,0 point provides the absolute position of window in screen
        position = self.mapToGlobal(QPoint(0, 0))

        msgBox.move(position.x() + self.width()//2, position.y() + self.height() - 75)
        msgBox.show()

        QTimer.singleShot(1000, MailSort.closeDialog(msgBox))

    @staticmethod
    def closeDialog(dialog):
        def _closeDialog():
            dialog.close()
        return _closeDialog

    def openFileSelection(self, text: str, file_type: str):
        """
        Opens a FileDialog where the user can select a file. This path is returned.
        :param text: The prompt text to display to the user
        :param file_type: The file type accepted. Must be in the format of: <file type name> (*.<extension of type>)
        :return: the file_path of the user selected or blank if the user closes the dialog
        """
        start_directory = self.settings.openDir

        if start_directory == "":
            start_directory = QDir.homePath()

        file_path = QFileDialog.getSaveFileName(self, text, start_directory, file_type)[0]
        return file_path

    def navigate(self, page_name):
        """
           The navigate method provides a handy way to match a page name with its index. Indices of pages for the
           QStackedWidget may change in future so methods should rely on this rather than hard coding indices in
        """
        name = page_name.lower()
        if name == "home":
            if len(self.workspace.lists) == 0:
                return 0
            else:
                self.renderListTableView(0)
                return 1
        elif name == "import":
            return 2
        elif name == "sort":
            return 3
        elif name == "export":
            return 4
        elif name == "labels":
            return 5
        elif name == "settings":
            return 6
        else:
            raise ValueError("No page exists with that given name")


if __name__ == "__main__":
    app = QApplication([])
    window = MailSort()
    window.show()

    sys.exit(app.exec())
