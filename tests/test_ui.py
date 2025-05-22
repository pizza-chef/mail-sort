from PySide6 import QtCore
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox, QCheckBox, QLineEdit, QLabel
import numpy as np
from maillist.maillist import MailList
from main import MailSort
import main
import pytest
from PySide6.QtTest import QTest
from maillist.xmlworkspace import XMLWorkspace
from manifest.createreport import CreateReport
from maillist.sort import PrintPostSort
from labels.labels import Labels
messageBoxOpened = False


@pytest.fixture
def app():
    # Only allowed one QApplication instance so we declare it once for all tests and just fetch instance - singleton
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()

    # Setting the app variable which is used to get window size in program
    main.app = app
    window = MailSort()
    window.show()

    # Yielding will return window and wait until after test is done to close it so we can try with a fresh window
    yield window

    window.close()


def getPageIndex(page_name):
    """
    Provides the index in the contentFrame stacked widget that corresponds to the page_name given as a parameter.
    In the off chance that the page numbers do change then rather than having to find all the changes in the code just
    this function can be changed.
    :param page_name: str
    """
    name = page_name.lower()
    if name == "empty workspace":
        return 0
    elif name == "table view":
        return 1
    elif name == "import":
        return 2
    elif name == "sort":
        return 3
    elif name == "export":
        return 4
    else:
        raise ValueError("Test is trying to check for a page that does not exist.")


def skipLaunchPage(app):
    app.ui.pages.setCurrentIndex(0)
    app.onEndLaunch()


def closeMessageBox():
    """
    closeMessageBox finds the first QMessageBox and closes it so it doesnt block dialog.
    A Global Variable must be used here because this is called via single shot which means this function can neither
    accept or return any values. The only way to check that a message box has actually been opened is to set this global
    variable.
    """

    topLevelWidgets = QApplication.topLevelWidgets()
    for widget in topLevelWidgets:
        if isinstance(widget, QMessageBox):
            widget.close()
            global messageBoxOpened
            messageBoxOpened = True
            return


@pytest.mark.parametrize("workspace_name, pageIndex, showMessageBox, fileOpened", [
    ("", 1, False, True),  # Tests when a user closes file dialog box (they didn't select a file)
    ("test", 0, False, True),  # Tests when a user successfully opens a file
    ("test", 1, True, False)  # Tests when a file can't be found
])
def test_launchBtnOpenWorkspace(app, monkeypatch, workspace_name, pageIndex, showMessageBox, fileOpened):
    """
    Tests the launchBtnOpenWorkspace button correctly changes the pages current index to display the workspace page
    if the user successfully chooses a file that opens correctly. Otherwise the page should not change.
    pageIndex in this case represents the index for either the launch or main page
    """

    def mock_openWorkspace(*args, **kwargs):
        return fileOpened

    def mock_getOpenFileName(*args, **kwargs):
        return [workspace_name]

    monkeypatch.setattr(QFileDialog, "getOpenFileName", mock_getOpenFileName)
    monkeypatch.setattr(XMLWorkspace, "openWorkspace", mock_openWorkspace)

    """
    Setting a singleShot to execute a function after a time period. This is because the UI thread
    is blocked by QMessageBox and therefore code to find the message box can't be called after without
    this timer.
    """
    global messageBoxOpened
    messageBoxOpened = False
    QTimer.singleShot(250, closeMessageBox)
    QTest.mouseClick(app.ui.launchBtnOpenWorkspace, Qt.LeftButton)

    # Patching the openWorkspace method in the workspace since we only care about the function of the open button and
    # not the function of actually opening a workspace. That can be done in more specific unit tests.

    assert app.ui.pages.currentIndex() == pageIndex and showMessageBox == messageBoxOpened


def test_launchBtnNewWorkspace(app):
    """
    Tests the launchBtnNewWorkspace widget correctly changes the page and creates an fresh, empty workspace object.
    """
    QTest.mouseClick(app.ui.launchBtnNewWorkspace, Qt.LeftButton)
    assert len(app.workspace.lists) == 0 and app.workspace.path == "" and app.workspace.name == "" \
           and app.ui.contentFrame.currentIndex() == getPageIndex("empty workspace")


def test_contentBtnImportList(app):
    """
    Tests that the contentBtnImportList widget correctly changes the index to the import page
    """
    # Set up workspace so to be on the emptyWorkspacePage with a fresh workspace
    skipLaunchPage(app)
    app.ui.contentFrame.setCurrentIndex(getPageIndex("empty workspace"))

    QTest.mouseClick(app.ui.contentBtnImportList, Qt.LeftButton)
    assert app.ui.contentFrame.currentIndex() == getPageIndex("import")


@pytest.mark.parametrize("mailLists, pageIndex", [
    ([], getPageIndex("empty workspace")),
    ([MailList(["test"], [["test"]], "test")], getPageIndex("table view"))
])
def test_contentBtnCancelImport_NothingImported(app, mailLists, pageIndex):
    """
    Tests that the user is correctly sent back to the empty workspace page when cancelling an import before actually
    browsing any files
    """
    skipLaunchPage(app)
    app.ui.contentFrame.setCurrentIndex(getPageIndex("import"))
    app.workspace.lists = mailLists

    QTest.mouseClick(app.ui.contentBtnCancelImport, Qt.LeftButton)
    assert app.ui.contentFrame.currentIndex() == pageIndex


def test_contentBtnCancelImport_listImported(app):
    """
    Tests that the user is prompted by a message box before being a cancel being accepted when the user has already
    started the import process
    """
    skipLaunchPage(app)
    app.ui.contentFrame.setCurrentIndex(getPageIndex("import"))
    # Setting pending list to a non-none element
    app.workspace.pending_list = MailList(["test"], [["test"]], "test")

    global messageBoxOpened
    messageBoxOpened = False
    QTimer.singleShot(250, closeMessageBox)
    QTest.mouseClick(app.ui.contentBtnCancelImport, Qt.LeftButton)
    assert messageBoxOpened


def setupImportPage(app):
    """
    Calls the required function to navigate to the import page and reset the required values
    """
    # Set up that's used for when the mail list
    app.resetImportMailListUI()
    # Moving to import page by skipping launch and navigating directly to import
    skipLaunchPage(app)
    app.ui.contentFrame.setCurrentIndex(getPageIndex("import"))


def test_contentBtnBrowseMailFile_emptyPath(app, monkeypatch):
    """
    Tests that when the user doesn't enter a path after clicking the browse button the user interface stays the same
    """

    def mock_getOpenFileName(*args, **kwargs):
        return [""]

    monkeypatch.setattr(QFileDialog, "getOpenFileName", mock_getOpenFileName)

    setupImportPage(app)
    QTest.mouseClick(app.ui.contentBtnBrowseMailFile, Qt.LeftButton)

    # These are the fields that are required to have no created UI elements in them i.e. there should be nothing shown
    uiElementsRequiredEmpty = [app.editFieldNames, app.addFieldBoxes, app.fieldNameLabels]
    # These fields should be hidden until a list is imported correctly
    uiElementsRequiredHidden = [app.ui.contentBtnConfirmImport, app.ui.addressConfirmationFrame]

    validUi = True
    for importElement in uiElementsRequiredEmpty:
        validUi = validUi and len(importElement) == 0

    for importElement in uiElementsRequiredHidden:
        validUi = validUi and importElement.isHidden()

    assert validUi


def mock_mailListObject():
    headers = ["Name", "State", "Postcode"]
    content = [["A", "B"], ["VIC", "NSW"], ["3171", "2250"]]
    mailList = MailList(headers, content, "test")
    mailList.address_columns = np.array([-1, 1, 2])
    return mailList


def test_contentBrowseMailFileBtn_successfulRead(app, monkeypatch):
    """
    Tests that when the user selects a valid file that the user interface will be updated accordingly. Requires all
    labels, line edits, combo boxes, and check boxes to be validated that there is the correct number of them (if
    applicable) and that they display the correct text.
    """

    def mock_getOpenFileName(*args, **kwargs):
        return ["test"]

    setupImportPage(app)
    monkeypatch.setattr(QFileDialog, "getOpenFileName", mock_getOpenFileName)
    monkeypatch.setattr(XMLWorkspace, "createMailList", lambda x, y, z, w: True)

    mockMailList = mock_mailListObject()
    app.workspace.pending_list = mockMailList

    # Clicking browse
    QTest.mouseClick(app.ui.contentBtnBrowseMailFile, Qt.LeftButton)

    validUI = True
    # These are the fields that are required to have no created UI elements in them i.e. there should be nothing shown
    importElements = [app.editFieldNames, app.addFieldBoxes, app.fieldNameLabels]

    # Each import element must match length of headers
    for importElement in importElements:
        validUI = validUI and len(importElement) == len(mockMailList.headers)

    # If it's still a validUI then check that each element has the correct text
    if validUI:
        # Checking that the labels and edit fields display the correct text
        for i in range(0, len(app.editFieldNames)):
            validUI = validUI and app.editFieldNames[i].text() == mockMailList.headers[i]
            validUI = validUI and app.fieldNameLabels[i].text() == mockMailList.headers[i]

    validUI = validUI and app.ui.stateComboBox.currentText() == "State"
    validUI = validUI and app.ui.postcodeComboBox.currentText() == "Postcode"

    # These fields should be hidden until a list is imported correctly
    uiElementsRequiredVisible = [app.ui.contentBtnConfirmImport, app.ui.addressConfirmationFrame]
    for element in uiElementsRequiredVisible:
        validUI = validUI and not element.isHidden()

    assert validUI


def test_contentBrowseMailFileBtn_failedToRead(app, monkeypatch):
    """
    Tests that when the user selects a valid file that the user interface will be updated accordingly
    """

    def mock_getOpenFileName(*args, **kwargs):
        return ["test"]

    setupImportPage(app)
    monkeypatch.setattr(QFileDialog, "getOpenFileName", mock_getOpenFileName)
    monkeypatch.setattr(XMLWorkspace, "createMailList", lambda x, y, z, w: False)

    global messageBoxOpened
    messageBoxOpened = False

    # Check for QMessageBox appearing
    QTest.mouseClick(app.ui.contentBtnBrowseMailFile, Qt.LeftButton)
    QTimer.singleShot(250, closeMessageBox)

    stillHidden = True
    uiElementsRequiredHidden = [app.ui.contentBtnConfirmImport, app.ui.addressConfirmationFrame]
    for importElement in uiElementsRequiredHidden:
        stillHidden = stillHidden and importElement.isHidden()

    assert messageBoxOpened and stillHidden


def mock_importPageUiUpdate(app, headers):
    """
    Mocks some of the behaviour of the browse mail file button on click. This will create some of the necessary ui
    elements.
    """
    for header in headers:
        app.addFieldBoxes.append(QCheckBox(""))
        app.addFieldBoxes[-1].setCheckState(Qt.Checked)
        app.editFieldNames.append(QLineEdit(header))
        app.fieldNameLabels.append(QLabel(header))


def test_contentConfirmImportBtn_filledFields(app):
    """
    Tests a file is successfully imported when all the required fields are filled. In this test case we will isolate
    the functions of the import btn by programmatically settings all the required fields needed rather than relying on
    the browse functionality.
    """

    skipLaunchPage(app)
    setupImportPage(app)

    mockMailList = mock_mailListObject()
    app.workspace.pending_list = mockMailList

    # Show the import button
    app.ui.contentBtnConfirmImport.show()

    # Set combo box values
    for header in mockMailList.headers:
        app.ui.stateComboBox.addItem(header)
        app.ui.postcodeComboBox.addItem(header)

    # Setting the indices for the address columns that match each combo box
    app.ui.stateComboBox.setCurrentIndex(mockMailList.address_columns[1])
    app.ui.postcodeComboBox.setCurrentIndex(mockMailList.address_columns[2])

    # Setting name field
    app.ui.fileNameEdit.setText("test")

    # Add necessary UI elements that are created for importing
    mock_importPageUiUpdate(app, mockMailList.headers)

    QTest.mouseClick(app.ui.contentBtnConfirmImport, Qt.LeftButton)
    print(len(app.workspace.lists))
    assert len(app.workspace.lists) == 1 and app.workspace.pending_list is None \
           and app.ui.contentFrame.currentIndex() == getPageIndex("table view")


def test_contentConfirmImportBtn_blankFields(app):
    """
    Tests a file is successfully rejected when all the required fields have not been filled yet. A message box
    should be displayed to the user stopping them
    """
    skipLaunchPage(app)
    setupImportPage(app)

    mockMailList = mock_mailListObject()
    app.workspace.pending_list = mockMailList

    # Show the import button
    app.ui.contentBtnConfirmImport.show()

    # Set combo box values as blank i.e. not set
    app.ui.stateComboBox.setCurrentIndex(-1)
    app.ui.postcodeComboBox.setCurrentIndex(-1)

    # Add necessary UI elements that are created for importing
    mock_importPageUiUpdate(app, mockMailList.headers)

    # QMessageBox should appear stopping the import as the combo boxes aren't filled out correctly
    global messageBoxOpened
    messageBoxOpened = False
    QTest.mouseClick(app.ui.contentBtnConfirmImport, Qt.LeftButton)
    QTimer.singleShot(250, closeMessageBox)

    assert messageBoxOpened and app.ui.contentFrame.currentIndex() == getPageIndex("import")


def test_contentConfirmImportBtn_duplicateFields(app):
    """
    Tests a file is successfully rejected when there are duplicate fields in the combo boxes
    """
    skipLaunchPage(app)
    setupImportPage(app)

    mockMailList = mock_mailListObject()
    app.workspace.pending_list = mockMailList

    # Show the import button
    app.ui.contentBtnConfirmImport.show()

    # Set combo box values as both having Postcode
    app.ui.stateComboBox.addItem("Postcode")
    app.ui.postcodeComboBox.addItem("Postcode")

    # Add necessary UI elements that are created for importing
    mock_importPageUiUpdate(app, mockMailList.headers)

    # QMessageBox should appear stopping the import as the combo boxes aren't filled out correctly
    global messageBoxOpened
    messageBoxOpened = False
    QTest.mouseClick(app.ui.contentBtnConfirmImport, Qt.LeftButton)
    QTimer.singleShot(250, closeMessageBox)

    assert messageBoxOpened and app.ui.contentFrame.currentIndex() == getPageIndex("import")


def test_contentConfirmImportBtn_duplicateHeaders(app):
    """
    Tests a file is successfully rejected when there are duplicate header names in the combo box
    """
    skipLaunchPage(app)
    setupImportPage(app)

    mockMailList = mock_mailListObject()
    app.workspace.pending_list = mockMailList

    # Show the import button
    app.ui.contentBtnConfirmImport.show()

    # Set combo box values as both having Postcode
    app.ui.stateComboBox.addItem("Postcode")
    app.ui.postcodeComboBox.addItem("Postcode")

    # Mock all the headers as the same so a message box should be displayed since all headers are the same
    mock_importPageUiUpdate(app, ["State", "State", "State"])

    # QMessageBox should appear stopping the import as the combo boxes aren't filled out correctly
    global messageBoxOpened
    messageBoxOpened = False
    QTest.mouseClick(app.ui.contentBtnConfirmImport, Qt.LeftButton)
    QTimer.singleShot(250, closeMessageBox)

    assert messageBoxOpened and app.ui.contentFrame.currentIndex() == getPageIndex("import")


@pytest.mark.parametrize("lists, pageName, showMsgBox", [
    ([], "empty workspace", True),
    ([mock_mailListObject()], "sort", False)
])
def test_menuSortBtn(app, lists, pageName, showMsgBox):
    """
    Tests the behaviour of the menu sort button for navigation. A user should be denied access to the page if the user
    has not got any imported lists and a message box should appear. Otherwise a user should see their page change with
    no message box.
    """
    skipLaunchPage(app)
    app.workspace.lists = lists

    global messageBoxOpened
    messageBoxOpened = False
    QTest.mouseClick(app.ui.menuSortBtn, Qt.LeftButton)

    # Check for QMessageBox appearing
    QTimer.singleShot(250, closeMessageBox)

    assert app.ui.contentFrame.currentIndex() == getPageIndex(pageName) and messageBoxOpened == showMsgBox


@pytest.mark.parametrize("lists, pageName, showMsgBox", [
    ([], "empty workspace", True),
    ([mock_mailListObject()], "export", False)
])
def test_menuExportBtn(app, lists, pageName, showMsgBox):
    """
    Tests the behaviour of the menu export button for navigation. A user should be denied access to the page if the user
    has not got any imported lists and a message box should appear. Otherwise a user should see their page change with
    no message box.
    """
    skipLaunchPage(app)

    app.workspace.lists = lists
    # Setting export list since its required for
    app.workspace.export_list = mock_mailListObject()

    global messageBoxOpened
    messageBoxOpened = False
    QTest.mouseClick(app.ui.menuExportBtn, Qt.LeftButton)

    # Check for QMessageBox appearing
    QTimer.singleShot(250, closeMessageBox)

    assert app.ui.contentFrame.currentIndex() == getPageIndex(pageName) and messageBoxOpened == showMsgBox


@pytest.mark.parametrize("lists, pageName", [
    ([], "empty workspace"),
    ([mock_mailListObject()], "table view")
])
def test_menuHomeBtn(app, lists, pageName):
    """
    Tests that clicking the menu home button with no lists and one or more lists exhibits the correct behaviour
    """
    skipLaunchPage(app)
    app.workspace.lists = lists
    QTest.mouseClick(app.ui.menuHomeBtn, Qt.LeftButton)

    assert app.ui.contentFrame.currentIndex() == getPageIndex(pageName)


@pytest.mark.parametrize("articleWeight, articleSize, deliveryStandard, printPostNum, pubTitle, showMsgBox", [
    ("0", 0, 0, "1", "1", True),  # Article has no weight
    ("-10", 0, 0, "1", "1", True),  # Article has a negative weight
    ("1050", 0, 0, "1", "1", True),  # Large article goes beyond maximum weight
    ("1000", 1, 0, "1", "1", True),  # Small article goes beyond maximum weight
    ("1000", 0, 1, "1", "1", False),  # Large article is on very border of weight range
    ("125", 1, 0, "1", "1", False),  # Small article is on very border of weight range
    ("1", 0, 0, "1", "1", False),  # Large article is on lowest border of weight range
    ("1", 1, 1, "1", "1", False),  # Small article is on lowest border of weight range
    ("", 0, 0, "1", "1", True),  # Weight range left blank
    ("250", 0, 0, "", "1", True),  # Print post number is left blank
    ("250", 0, 1, "1", "", True),  # Publication title is left blank
])
def test_sortPage(app, monkeypatch, articleWeight, articleSize, deliveryStandard, printPostNum, pubTitle, showMsgBox):
    """
    Tests that the sort page correctly validates the input given based on the different possible combinations before
    it generates the manifest.
    """
    skipLaunchPage(app)
    mockedMailList = mock_mailListObject()
    app.workspace.lists.append(mockedMailList)
    app.ui.contentFrame.setCurrentIndex(getPageIndex("sort"))

    def mock_createPdf(*args, **kwargs):
        # We don't want to create the actual pdf so just do nothing instead. We are only checking for validation here.
        pass

    def mock_labelsInit(*args, **kwargs):
        pass

    # Mocking functionality of these functions that are used to generate manifest as we only focus on ui validation here
    monkeypatch.setattr(CreateReport, "create_pdf", mock_createPdf())
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda x, y, z, w: "")
    monkeypatch.setattr(PrintPostSort, "organiseCategories", lambda x, y, z, w: [])
    monkeypatch.setattr(PrintPostSort, "preprocessList", lambda x: mockedMailList)
    monkeypatch.setattr(Labels, "__init__", mock_labelsInit)


    app.ui.sortLineEditWeight.setText(articleWeight)
    app.ui.sortComboBoxSize.setCurrentIndex(articleSize)
    app.ui.sortComboBoxDeliveryStandard.setCurrentIndex(deliveryStandard)
    app.ui.sortLineEditPrintPostNumber.setText(printPostNum)
    app.ui.sortLineEditPublicationTitle.setText(pubTitle)

    global messageBoxOpened
    messageBoxOpened = False

    QTest.mouseClick(app.ui.contentBtnSort, Qt.LeftButton)

    # Check for QMessageBox appearing
    QTimer.singleShot(250, closeMessageBox)

    assert messageBoxOpened == showMsgBox

# TODO: Still need to test
"""
    Should test small and large articles in their respective workspace sort functions.
    
    If time allows then test the read of a file, but not too worried about that right now.
"""
