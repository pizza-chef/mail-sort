# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1125, 655)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_25 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.verticalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.pages = QStackedWidget(self.centralwidget)
        self.pages.setObjectName(u"pages")
        self.mainPage = QWidget()
        self.mainPage.setObjectName(u"mainPage")
        self.horizontalLayout = QHBoxLayout(self.mainPage)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.menuFrame = QFrame(self.mainPage)
        self.menuFrame.setObjectName(u"menuFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.menuFrame.sizePolicy().hasHeightForWidth())
        self.menuFrame.setSizePolicy(sizePolicy1)
        self.menuFrame.setMaximumSize(QSize(300, 16777215))
        self.menuFrame.setFrameShape(QFrame.StyledPanel)
        self.menuFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.menuFrame)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.sideMenuLayout = QVBoxLayout()
        self.sideMenuLayout.setSpacing(0)
        self.sideMenuLayout.setObjectName(u"sideMenuLayout")
        self.menuHomeBtn = QPushButton(self.menuFrame)
        self.menuHomeBtn.setObjectName(u"menuHomeBtn")

        self.sideMenuLayout.addWidget(self.menuHomeBtn)

        self.menuImportListBtn = QPushButton(self.menuFrame)
        self.menuImportListBtn.setObjectName(u"menuImportListBtn")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.menuImportListBtn.sizePolicy().hasHeightForWidth())
        self.menuImportListBtn.setSizePolicy(sizePolicy2)

        self.sideMenuLayout.addWidget(self.menuImportListBtn)

        self.menuSortBtn = QPushButton(self.menuFrame)
        self.menuSortBtn.setObjectName(u"menuSortBtn")
        sizePolicy2.setHeightForWidth(self.menuSortBtn.sizePolicy().hasHeightForWidth())
        self.menuSortBtn.setSizePolicy(sizePolicy2)

        self.sideMenuLayout.addWidget(self.menuSortBtn)

        self.menuExportBtn = QPushButton(self.menuFrame)
        self.menuExportBtn.setObjectName(u"menuExportBtn")
        sizePolicy2.setHeightForWidth(self.menuExportBtn.sizePolicy().hasHeightForWidth())
        self.menuExportBtn.setSizePolicy(sizePolicy2)

        self.sideMenuLayout.addWidget(self.menuExportBtn)

        self.menuLabelsBtn = QPushButton(self.menuFrame)
        self.menuLabelsBtn.setObjectName(u"menuLabelsBtn")

        self.sideMenuLayout.addWidget(self.menuLabelsBtn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.sideMenuLayout.addItem(self.verticalSpacer)

        self.menuSaveWorkspaceBtn = QPushButton(self.menuFrame)
        self.menuSaveWorkspaceBtn.setObjectName(u"menuSaveWorkspaceBtn")

        self.sideMenuLayout.addWidget(self.menuSaveWorkspaceBtn)

        self.menuNewWorkspaceBtn = QPushButton(self.menuFrame)
        self.menuNewWorkspaceBtn.setObjectName(u"menuNewWorkspaceBtn")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.menuNewWorkspaceBtn.sizePolicy().hasHeightForWidth())
        self.menuNewWorkspaceBtn.setSizePolicy(sizePolicy3)

        self.sideMenuLayout.addWidget(self.menuNewWorkspaceBtn)

        self.menuOpenWorkspaceBtn = QPushButton(self.menuFrame)
        self.menuOpenWorkspaceBtn.setObjectName(u"menuOpenWorkspaceBtn")
        sizePolicy2.setHeightForWidth(self.menuOpenWorkspaceBtn.sizePolicy().hasHeightForWidth())
        self.menuOpenWorkspaceBtn.setSizePolicy(sizePolicy2)

        self.sideMenuLayout.addWidget(self.menuOpenWorkspaceBtn)

        self.menuSettingsBtn = QPushButton(self.menuFrame)
        self.menuSettingsBtn.setObjectName(u"menuSettingsBtn")
        sizePolicy3.setHeightForWidth(self.menuSettingsBtn.sizePolicy().hasHeightForWidth())
        self.menuSettingsBtn.setSizePolicy(sizePolicy3)

        self.sideMenuLayout.addWidget(self.menuSettingsBtn)

        self.sideMenuLayout.setStretch(0, 1)
        self.sideMenuLayout.setStretch(1, 1)
        self.sideMenuLayout.setStretch(2, 1)
        self.sideMenuLayout.setStretch(3, 1)
        self.sideMenuLayout.setStretch(5, 12)
        self.sideMenuLayout.setStretch(6, 1)
        self.sideMenuLayout.setStretch(7, 1)
        self.sideMenuLayout.setStretch(8, 1)
        self.sideMenuLayout.setStretch(9, 1)

        self.verticalLayout_20.addLayout(self.sideMenuLayout)


        self.horizontalLayout.addWidget(self.menuFrame)

        self.contentFrame = QStackedWidget(self.mainPage)
        self.contentFrame.setObjectName(u"contentFrame")
        self.emptyWorkspacePage = QWidget()
        self.emptyWorkspacePage.setObjectName(u"emptyWorkspacePage")
        self.horizontalLayout_8 = QHBoxLayout(self.emptyWorkspacePage)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_5)

        self.titleLabelEmptyWorkspace = QLabel(self.emptyWorkspacePage)
        self.titleLabelEmptyWorkspace.setObjectName(u"titleLabelEmptyWorkspace")
        font = QFont()
        font.setPointSize(30)
        self.titleLabelEmptyWorkspace.setFont(font)

        self.verticalLayout_4.addWidget(self.titleLabelEmptyWorkspace, 0, Qt.AlignHCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_11)

        self.contentBtnImportList = QPushButton(self.emptyWorkspacePage)
        self.contentBtnImportList.setObjectName(u"contentBtnImportList")

        self.horizontalLayout_9.addWidget(self.contentBtnImportList)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_10)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_6)

        self.verticalLayout_4.setStretch(0, 5)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 3)
        self.verticalLayout_4.setStretch(3, 1)
        self.verticalLayout_4.setStretch(4, 10)

        self.horizontalLayout_8.addLayout(self.verticalLayout_4)

        self.contentFrame.addWidget(self.emptyWorkspacePage)
        self.workspaceListViewPage = QWidget()
        self.workspaceListViewPage.setObjectName(u"workspaceListViewPage")
        self.horizontalLayout_10 = QHBoxLayout(self.workspaceListViewPage)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.listTableWidget = QTableWidget(self.workspaceListViewPage)
        self.listTableWidget.setObjectName(u"listTableWidget")
        self.listTableWidget.setAlternatingRowColors(False)

        self.verticalLayout_5.addWidget(self.listTableWidget)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.workspaceDetailedFrame = QFrame(self.workspaceListViewPage)
        self.workspaceDetailedFrame.setObjectName(u"workspaceDetailedFrame")
        self.workspaceDetailedFrame.setFrameShape(QFrame.StyledPanel)
        self.workspaceDetailedFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.workspaceDetailedFrame)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.workspaceLabelListSummary = QLabel(self.workspaceDetailedFrame)
        self.workspaceLabelListSummary.setObjectName(u"workspaceLabelListSummary")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.workspaceLabelListSummary.sizePolicy().hasHeightForWidth())
        self.workspaceLabelListSummary.setSizePolicy(sizePolicy4)

        self.verticalLayout_6.addWidget(self.workspaceLabelListSummary, 0, Qt.AlignTop)

        self.verticalSpacer_16 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_16)

        self.listSelectComboBox = QComboBox(self.workspaceDetailedFrame)
        self.listSelectComboBox.setObjectName(u"listSelectComboBox")
        self.listSelectComboBox.setMinimumSize(QSize(0, 25))
        self.listSelectComboBox.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_6.addWidget(self.listSelectComboBox, 0, Qt.AlignTop)

        self.verticalSpacer_17 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_17)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.contentBtnDeleteList = QPushButton(self.workspaceDetailedFrame)
        self.contentBtnDeleteList.setObjectName(u"contentBtnDeleteList")
        self.contentBtnDeleteList.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_12.addWidget(self.contentBtnDeleteList)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_6)

        self.horizontalLayout_12.setStretch(0, 1)
        self.horizontalLayout_12.setStretch(1, 2)

        self.verticalLayout_6.addLayout(self.horizontalLayout_12)

        self.verticalSpacer_18 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_18)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setSpacing(10)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.verticalLayout_23 = QVBoxLayout()
        self.verticalLayout_23.setSpacing(2)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.fieldLabelRecords = QLabel(self.workspaceDetailedFrame)
        self.fieldLabelRecords.setObjectName(u"fieldLabelRecords")

        self.verticalLayout_23.addWidget(self.fieldLabelRecords)

        self.fieldLabelColumns = QLabel(self.workspaceDetailedFrame)
        self.fieldLabelColumns.setObjectName(u"fieldLabelColumns")

        self.verticalLayout_23.addWidget(self.fieldLabelColumns)


        self.horizontalLayout_19.addLayout(self.verticalLayout_23)

        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setSpacing(2)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.valueLabelRecords = QLabel(self.workspaceDetailedFrame)
        self.valueLabelRecords.setObjectName(u"valueLabelRecords")

        self.verticalLayout_24.addWidget(self.valueLabelRecords)

        self.valueLabelColumns = QLabel(self.workspaceDetailedFrame)
        self.valueLabelColumns.setObjectName(u"valueLabelColumns")

        self.verticalLayout_24.addWidget(self.valueLabelColumns)


        self.horizontalLayout_19.addLayout(self.verticalLayout_24)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_20)


        self.verticalLayout_6.addLayout(self.horizontalLayout_19)

        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_15)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)


        self.horizontalLayout_11.addWidget(self.workspaceDetailedFrame)

        self.workspaceSummaryFrame = QFrame(self.workspaceListViewPage)
        self.workspaceSummaryFrame.setObjectName(u"workspaceSummaryFrame")
        self.workspaceSummaryFrame.setFrameShape(QFrame.StyledPanel)
        self.workspaceSummaryFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.workspaceSummaryFrame)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.warningsScrollBox = QScrollArea(self.workspaceSummaryFrame)
        self.warningsScrollBox.setObjectName(u"warningsScrollBox")
        self.warningsScrollBox.setWidgetResizable(True)
        self.warningsScrollArea = QWidget()
        self.warningsScrollArea.setObjectName(u"warningsScrollArea")
        self.warningsScrollArea.setGeometry(QRect(0, 0, 403, 157))
        self.verticalLayout_21 = QVBoxLayout(self.warningsScrollArea)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(6, 6, 6, 6)
        self.workspaceWarningVLayout = QVBoxLayout()
        self.workspaceWarningVLayout.setObjectName(u"workspaceWarningVLayout")
        self.workspaceLabelWarningsTitle = QLabel(self.warningsScrollArea)
        self.workspaceLabelWarningsTitle.setObjectName(u"workspaceLabelWarningsTitle")

        self.workspaceWarningVLayout.addWidget(self.workspaceLabelWarningsTitle, 0, Qt.AlignTop)

        self.verticalSpacer_14 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.workspaceWarningVLayout.addItem(self.verticalSpacer_14)

        self.warningsDescription = QLabel(self.warningsScrollArea)
        self.warningsDescription.setObjectName(u"warningsDescription")
        self.warningsDescription.setLineWidth(2)
        self.warningsDescription.setWordWrap(True)

        self.workspaceWarningVLayout.addWidget(self.warningsDescription, 0, Qt.AlignTop)

        self.verticalSpacer_13 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.workspaceWarningVLayout.addItem(self.verticalSpacer_13)

        self.warningsLabel = QLabel(self.warningsScrollArea)
        self.warningsLabel.setObjectName(u"warningsLabel")
        self.warningsLabel.setWordWrap(True)
        self.warningsLabel.setMargin(5)

        self.workspaceWarningVLayout.addWidget(self.warningsLabel, 0, Qt.AlignTop)


        self.verticalLayout_21.addLayout(self.workspaceWarningVLayout)

        self.warningsScrollBox.setWidget(self.warningsScrollArea)

        self.verticalLayout_9.addWidget(self.warningsScrollBox)


        self.horizontalLayout_11.addWidget(self.workspaceSummaryFrame)

        self.horizontalLayout_11.setStretch(0, 1)
        self.horizontalLayout_11.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_11)

        self.verticalLayout_5.setStretch(0, 3)
        self.verticalLayout_5.setStretch(1, 1)

        self.horizontalLayout_10.addLayout(self.verticalLayout_5)

        self.contentFrame.addWidget(self.workspaceListViewPage)
        self.importMailListPage = QWidget()
        self.importMailListPage.setObjectName(u"importMailListPage")
        self.horizontalLayout_4 = QHBoxLayout(self.importMailListPage)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.importFrame = QFrame(self.importMailListPage)
        self.importFrame.setObjectName(u"importFrame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.importFrame.sizePolicy().hasHeightForWidth())
        self.importFrame.setSizePolicy(sizePolicy5)
        self.importFrame.setMinimumSize(QSize(750, 0))
        self.importFrame.setMaximumSize(QSize(1000, 16777215))
        self.importFrame.setFrameShape(QFrame.StyledPanel)
        self.importFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.importFrame)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, -1, -1, 6)
        self.headerLabelSourceFile = QLabel(self.importFrame)
        self.headerLabelSourceFile.setObjectName(u"headerLabelSourceFile")

        self.horizontalLayout_7.addWidget(self.headerLabelSourceFile)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_9)

        self.contentBtnCancelImport = QPushButton(self.importFrame)
        self.contentBtnCancelImport.setObjectName(u"contentBtnCancelImport")

        self.horizontalLayout_7.addWidget(self.contentBtnCancelImport)

        self.horizontalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.includeHeadersCheckBox = QCheckBox(self.importFrame)
        self.includeHeadersCheckBox.setObjectName(u"includeHeadersCheckBox")
        self.includeHeadersCheckBox.setEnabled(True)
        sizePolicy.setHeightForWidth(self.includeHeadersCheckBox.sizePolicy().hasHeightForWidth())
        self.includeHeadersCheckBox.setSizePolicy(sizePolicy)
        self.includeHeadersCheckBox.setIconSize(QSize(32, 32))
        self.includeHeadersCheckBox.setChecked(True)
        self.includeHeadersCheckBox.setTristate(False)

        self.verticalLayout_2.addWidget(self.includeHeadersCheckBox)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 6)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.fileTypeComboBox = QComboBox(self.importFrame)
        self.fileTypeComboBox.setObjectName(u"fileTypeComboBox")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.fileTypeComboBox.sizePolicy().hasHeightForWidth())
        self.fileTypeComboBox.setSizePolicy(sizePolicy6)

        self.horizontalLayout_18.addWidget(self.fileTypeComboBox)

        self.contentBtnBrowseMailFile = QPushButton(self.importFrame)
        self.contentBtnBrowseMailFile.setObjectName(u"contentBtnBrowseMailFile")
        self.contentBtnBrowseMailFile.setStyleSheet(u"")

        self.horizontalLayout_18.addWidget(self.contentBtnBrowseMailFile)

        self.horizontalLayout_18.setStretch(0, 7)
        self.horizontalLayout_18.setStretch(1, 2)

        self.verticalLayout.addLayout(self.horizontalLayout_18)

        self.sheetNumLineEdit = QLineEdit(self.importFrame)
        self.sheetNumLineEdit.setObjectName(u"sheetNumLineEdit")

        self.verticalLayout.addWidget(self.sheetNumLineEdit)

        self.fileNameEdit = QLineEdit(self.importFrame)
        self.fileNameEdit.setObjectName(u"fileNameEdit")

        self.verticalLayout.addWidget(self.fileNameEdit)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 1)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.horizontalLayout_3.setStretch(0, 6)
        self.horizontalLayout_3.setStretch(1, 10)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.scrollArea = QScrollArea(self.importFrame)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 442, 254))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 5, 0, 5)
        self.fieldNameGridLayout = QGridLayout()
        self.fieldNameGridLayout.setObjectName(u"fieldNameGridLayout")
        self.fieldNameGridLayout.setHorizontalSpacing(0)
        self.fieldNameGridLayout.setVerticalSpacing(10)

        self.verticalLayout_3.addLayout(self.fieldNameGridLayout)

        self.addressConfirmationLayout = QVBoxLayout()
        self.addressConfirmationLayout.setSpacing(0)
        self.addressConfirmationLayout.setObjectName(u"addressConfirmationLayout")
        self.addressConfirmationLayout.setContentsMargins(-1, 5, 5, -1)
        self.verticalSpacer_9 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.addressConfirmationLayout.addItem(self.verticalSpacer_9)

        self.addressConfirmationFrame = QFrame(self.scrollAreaWidgetContents)
        self.addressConfirmationFrame.setObjectName(u"addressConfirmationFrame")
        self.verticalLayout_10 = QVBoxLayout(self.addressConfirmationFrame)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.headerLabelAddressConfirmation = QLabel(self.addressConfirmationFrame)
        self.headerLabelAddressConfirmation.setObjectName(u"headerLabelAddressConfirmation")

        self.verticalLayout_10.addWidget(self.headerLabelAddressConfirmation, 0, Qt.AlignTop)

        self.contentLabelAddressDescription = QLabel(self.addressConfirmationFrame)
        self.contentLabelAddressDescription.setObjectName(u"contentLabelAddressDescription")

        self.verticalLayout_10.addWidget(self.contentLabelAddressDescription, 0, Qt.AlignTop)

        self.verticalSpacer_10 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_10.addItem(self.verticalSpacer_10)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.subheaderLabelCountry = QLabel(self.addressConfirmationFrame)
        self.subheaderLabelCountry.setObjectName(u"subheaderLabelCountry")

        self.horizontalLayout_5.addWidget(self.subheaderLabelCountry)

        self.label_4 = QLabel(self.addressConfirmationFrame)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout_10.addLayout(self.horizontalLayout_5)

        self.countryComboBox = QComboBox(self.addressConfirmationFrame)
        self.countryComboBox.setObjectName(u"countryComboBox")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.countryComboBox.sizePolicy().hasHeightForWidth())
        self.countryComboBox.setSizePolicy(sizePolicy7)
        self.countryComboBox.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_10.addWidget(self.countryComboBox, 0, Qt.AlignTop)

        self.verticalSpacer_11 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_10.addItem(self.verticalSpacer_11)

        self.subheaderLabelState = QLabel(self.addressConfirmationFrame)
        self.subheaderLabelState.setObjectName(u"subheaderLabelState")

        self.verticalLayout_10.addWidget(self.subheaderLabelState)

        self.stateComboBox = QComboBox(self.addressConfirmationFrame)
        self.stateComboBox.setObjectName(u"stateComboBox")
        self.stateComboBox.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_10.addWidget(self.stateComboBox)

        self.verticalSpacer_12 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_10.addItem(self.verticalSpacer_12)

        self.subheaderLabelPostcode = QLabel(self.addressConfirmationFrame)
        self.subheaderLabelPostcode.setObjectName(u"subheaderLabelPostcode")

        self.verticalLayout_10.addWidget(self.subheaderLabelPostcode, 0, Qt.AlignTop)

        self.postcodeComboBox = QComboBox(self.addressConfirmationFrame)
        self.postcodeComboBox.setObjectName(u"postcodeComboBox")
        sizePolicy7.setHeightForWidth(self.postcodeComboBox.sizePolicy().hasHeightForWidth())
        self.postcodeComboBox.setSizePolicy(sizePolicy7)
        self.postcodeComboBox.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_10.addWidget(self.postcodeComboBox)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_4)


        self.addressConfirmationLayout.addWidget(self.addressConfirmationFrame)


        self.verticalLayout_3.addLayout(self.addressConfirmationLayout)

        self.verticalLayout_3.setStretch(1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_8)

        self.contentLabelRecordsRead = QLabel(self.importFrame)
        self.contentLabelRecordsRead.setObjectName(u"contentLabelRecordsRead")
        self.contentLabelRecordsRead.setStyleSheet(u"margin-right: 20px;")

        self.horizontalLayout_6.addWidget(self.contentLabelRecordsRead)

        self.contentBtnConfirmImport = QPushButton(self.importFrame)
        self.contentBtnConfirmImport.setObjectName(u"contentBtnConfirmImport")

        self.horizontalLayout_6.addWidget(self.contentBtnConfirmImport)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(4, 20)

        self.verticalLayout_14.addLayout(self.verticalLayout_2)


        self.horizontalLayout_4.addWidget(self.importFrame)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 2)
        self.contentFrame.addWidget(self.importMailListPage)
        self.sortPage = QWidget()
        self.sortPage.setObjectName(u"sortPage")
        self.horizontalLayout_23 = QHBoxLayout(self.sortPage)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.sortFrame = QFrame(self.sortPage)
        self.sortFrame.setObjectName(u"sortFrame")
        self.sortFrame.setFrameShape(QFrame.StyledPanel)
        self.sortFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.sortFrame)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.sortTitleLabelSort = QLabel(self.sortFrame)
        self.sortTitleLabelSort.setObjectName(u"sortTitleLabelSort")

        self.verticalLayout_8.addWidget(self.sortTitleLabelSort)

        self.sortLabelSortChoice = QLabel(self.sortFrame)
        self.sortLabelSortChoice.setObjectName(u"sortLabelSortChoice")

        self.verticalLayout_8.addWidget(self.sortLabelSortChoice)

        self.sortComboBoxSortPlan = QComboBox(self.sortFrame)
        self.sortComboBoxSortPlan.setObjectName(u"sortComboBoxSortPlan")
        self.sortComboBoxSortPlan.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_8.addWidget(self.sortComboBoxSortPlan)

        self.sortLabelArticleWeight = QLabel(self.sortFrame)
        self.sortLabelArticleWeight.setObjectName(u"sortLabelArticleWeight")

        self.verticalLayout_8.addWidget(self.sortLabelArticleWeight)

        self.sortLineEditWeight = QLineEdit(self.sortFrame)
        self.sortLineEditWeight.setObjectName(u"sortLineEditWeight")
        self.sortLineEditWeight.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_8.addWidget(self.sortLineEditWeight)

        self.sortLabelSize = QLabel(self.sortFrame)
        self.sortLabelSize.setObjectName(u"sortLabelSize")

        self.verticalLayout_8.addWidget(self.sortLabelSize)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.sortComboBoxSize = QComboBox(self.sortFrame)
        self.sortComboBoxSize.setObjectName(u"sortComboBoxSize")
        self.sortComboBoxSize.setMinimumSize(QSize(250, 0))
        self.sortComboBoxSize.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_14.addWidget(self.sortComboBoxSize)

        self.widthLineEdit = QLineEdit(self.sortFrame)
        self.widthLineEdit.setObjectName(u"widthLineEdit")
        self.widthLineEdit.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_14.addWidget(self.widthLineEdit)

        self.lengthLineEdit = QLineEdit(self.sortFrame)
        self.lengthLineEdit.setObjectName(u"lengthLineEdit")
        self.lengthLineEdit.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_14.addWidget(self.lengthLineEdit)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_21)

        self.horizontalLayout_14.setStretch(0, 10)

        self.verticalLayout_8.addLayout(self.horizontalLayout_14)

        self.sortLabelDeliveryStandard = QLabel(self.sortFrame)
        self.sortLabelDeliveryStandard.setObjectName(u"sortLabelDeliveryStandard")

        self.verticalLayout_8.addWidget(self.sortLabelDeliveryStandard)

        self.sortComboBoxDeliveryStandard = QComboBox(self.sortFrame)
        self.sortComboBoxDeliveryStandard.setObjectName(u"sortComboBoxDeliveryStandard")
        self.sortComboBoxDeliveryStandard.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_8.addWidget(self.sortComboBoxDeliveryStandard)

        self.sortLabelPrintPostNumber = QLabel(self.sortFrame)
        self.sortLabelPrintPostNumber.setObjectName(u"sortLabelPrintPostNumber")

        self.verticalLayout_8.addWidget(self.sortLabelPrintPostNumber)

        self.sortLineEditPrintPostNumber = QLineEdit(self.sortFrame)
        self.sortLineEditPrintPostNumber.setObjectName(u"sortLineEditPrintPostNumber")
        self.sortLineEditPrintPostNumber.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_8.addWidget(self.sortLineEditPrintPostNumber)

        self.sortLabelPublicationTitle = QLabel(self.sortFrame)
        self.sortLabelPublicationTitle.setObjectName(u"sortLabelPublicationTitle")

        self.verticalLayout_8.addWidget(self.sortLabelPublicationTitle)

        self.sortLineEditPublicationTitle = QLineEdit(self.sortFrame)
        self.sortLineEditPublicationTitle.setObjectName(u"sortLineEditPublicationTitle")
        self.sortLineEditPublicationTitle.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_8.addWidget(self.sortLineEditPublicationTitle)

        self.sortLabelDate = QLabel(self.sortFrame)
        self.sortLabelDate.setObjectName(u"sortLabelDate")

        self.verticalLayout_8.addWidget(self.sortLabelDate)

        self.sortLineEditDate = QLineEdit(self.sortFrame)
        self.sortLineEditDate.setObjectName(u"sortLineEditDate")
        self.sortLineEditDate.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_8.addWidget(self.sortLineEditDate)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.contentBtnSort = QPushButton(self.sortFrame)
        self.contentBtnSort.setObjectName(u"contentBtnSort")
        sizePolicy8 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.contentBtnSort.sizePolicy().hasHeightForWidth())
        self.contentBtnSort.setSizePolicy(sizePolicy8)
        self.contentBtnSort.setMinimumSize(QSize(250, 0))
        self.contentBtnSort.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_20.addWidget(self.contentBtnSort, 0, Qt.AlignLeft)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_22)


        self.verticalLayout_8.addLayout(self.horizontalLayout_20)

        self.verticalSpacer_19 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_19)


        self.horizontalLayout_24.addLayout(self.verticalLayout_8)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.sortTitleLabelPrices = QLabel(self.sortFrame)
        self.sortTitleLabelPrices.setObjectName(u"sortTitleLabelPrices")

        self.verticalLayout_11.addWidget(self.sortTitleLabelPrices, 0, Qt.AlignTop)

        self.sortInfoLabelPrices = QLabel(self.sortFrame)
        self.sortInfoLabelPrices.setObjectName(u"sortInfoLabelPrices")

        self.verticalLayout_11.addWidget(self.sortInfoLabelPrices, 0, Qt.AlignTop)

        self.priceGridLayout = QGridLayout()
        self.priceGridLayout.setObjectName(u"priceGridLayout")

        self.verticalLayout_11.addLayout(self.priceGridLayout)

        self.verticalSpacer_20 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_20)


        self.horizontalLayout_24.addLayout(self.verticalLayout_11)

        self.horizontalLayout_24.setStretch(0, 1)
        self.horizontalLayout_24.setStretch(1, 1)

        self.horizontalLayout_21.addWidget(self.sortFrame)

        self.horizontalLayout_21.setStretch(0, 1)

        self.horizontalLayout_23.addLayout(self.horizontalLayout_21)

        self.contentFrame.addWidget(self.sortPage)
        self.exportPage = QWidget()
        self.exportPage.setObjectName(u"exportPage")
        self.verticalLayout_15 = QVBoxLayout(self.exportPage)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.exportedListTableWidget = QTableWidget(self.exportPage)
        self.exportedListTableWidget.setObjectName(u"exportedListTableWidget")

        self.verticalLayout_13.addWidget(self.exportedListTableWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)

        self.contentBtnExport = QPushButton(self.exportPage)
        self.contentBtnExport.setObjectName(u"contentBtnExport")

        self.horizontalLayout_2.addWidget(self.contentBtnExport)


        self.verticalLayout_13.addLayout(self.horizontalLayout_2)


        self.verticalLayout_15.addLayout(self.verticalLayout_13)

        self.contentFrame.addWidget(self.exportPage)
        self.labelsPage = QWidget()
        self.labelsPage.setObjectName(u"labelsPage")
        self.verticalLayout_26 = QVBoxLayout(self.labelsPage)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_22 = QVBoxLayout()
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.labelsTitleLabel = QLabel(self.labelsPage)
        self.labelsTitleLabel.setObjectName(u"labelsTitleLabel")

        self.verticalLayout_22.addWidget(self.labelsTitleLabel)

        self.verticalSpacer_27 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_22.addItem(self.verticalSpacer_27)

        self.labelsSubtitleThickness = QLabel(self.labelsPage)
        self.labelsSubtitleThickness.setObjectName(u"labelsSubtitleThickness")

        self.verticalLayout_22.addWidget(self.labelsSubtitleThickness)

        self.labelsThicknessLineEdit = QLineEdit(self.labelsPage)
        self.labelsThicknessLineEdit.setObjectName(u"labelsThicknessLineEdit")
        self.labelsThicknessLineEdit.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_22.addWidget(self.labelsThicknessLineEdit)

        self.labelsSubtitleDate = QLabel(self.labelsPage)
        self.labelsSubtitleDate.setObjectName(u"labelsSubtitleDate")

        self.verticalLayout_22.addWidget(self.labelsSubtitleDate)

        self.labelsDateLineEdit = QLineEdit(self.labelsPage)
        self.labelsDateLineEdit.setObjectName(u"labelsDateLineEdit")
        self.labelsDateLineEdit.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_22.addWidget(self.labelsDateLineEdit)

        self.verticalSpacer_26 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_22.addItem(self.verticalSpacer_26)

        self.labelsSubtitlePaperSize = QLabel(self.labelsPage)
        self.labelsSubtitlePaperSize.setObjectName(u"labelsSubtitlePaperSize")

        self.verticalLayout_22.addWidget(self.labelsSubtitlePaperSize)

        self.label_12 = QLabel(self.labelsPage)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMaximumSize(QSize(250, 16777215))
        self.label_12.setWordWrap(True)

        self.verticalLayout_22.addWidget(self.label_12)

        self.labelsPaperSizeComboBox = QComboBox(self.labelsPage)
        self.labelsPaperSizeComboBox.setObjectName(u"labelsPaperSizeComboBox")
        self.labelsPaperSizeComboBox.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_22.addWidget(self.labelsPaperSizeComboBox)

        self.contentBtnGenerateLabels = QPushButton(self.labelsPage)
        self.contentBtnGenerateLabels.setObjectName(u"contentBtnGenerateLabels")
        self.contentBtnGenerateLabels.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_22.addWidget(self.contentBtnGenerateLabels)

        self.verticalSpacer_24 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_22.addItem(self.verticalSpacer_24)

        self.labelsTitlePlanFile = QLabel(self.labelsPage)
        self.labelsTitlePlanFile.setObjectName(u"labelsTitlePlanFile")

        self.verticalLayout_22.addWidget(self.labelsTitlePlanFile)

        self.labelPlanTableWidget = QTableWidget(self.labelsPage)
        self.labelPlanTableWidget.setObjectName(u"labelPlanTableWidget")
        sizePolicy.setHeightForWidth(self.labelPlanTableWidget.sizePolicy().hasHeightForWidth())
        self.labelPlanTableWidget.setSizePolicy(sizePolicy)

        self.verticalLayout_22.addWidget(self.labelPlanTableWidget)

        self.verticalSpacer_25 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_22.addItem(self.verticalSpacer_25)

        self.contentBtnPrintLabels = QPushButton(self.labelsPage)
        self.contentBtnPrintLabels.setObjectName(u"contentBtnPrintLabels")
        self.contentBtnPrintLabels.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_22.addWidget(self.contentBtnPrintLabels)

        self.verticalSpacer_23 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_23)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")

        self.verticalLayout_22.addLayout(self.horizontalLayout_22)


        self.verticalLayout_26.addLayout(self.verticalLayout_22)

        self.contentFrame.addWidget(self.labelsPage)
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName(u"settingsPage")
        self.verticalLayout_17 = QVBoxLayout(self.settingsPage)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.workspaceLabelDefaultOpenDirectory = QLabel(self.settingsPage)
        self.workspaceLabelDefaultOpenDirectory.setObjectName(u"workspaceLabelDefaultOpenDirectory")

        self.verticalLayout_12.addWidget(self.workspaceLabelDefaultOpenDirectory)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.defaultDirectoryLineEdit = QLineEdit(self.settingsPage)
        self.defaultDirectoryLineEdit.setObjectName(u"defaultDirectoryLineEdit")
        self.defaultDirectoryLineEdit.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_25.addWidget(self.defaultDirectoryLineEdit)

        self.contentBtnDefaultOpenDir = QPushButton(self.settingsPage)
        self.contentBtnDefaultOpenDir.setObjectName(u"contentBtnDefaultOpenDir")

        self.horizontalLayout_25.addWidget(self.contentBtnDefaultOpenDir)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_24)


        self.verticalLayout_12.addLayout(self.horizontalLayout_25)

        self.workspaceLabelVisaCommand = QLabel(self.settingsPage)
        self.workspaceLabelVisaCommand.setObjectName(u"workspaceLabelVisaCommand")

        self.verticalLayout_12.addWidget(self.workspaceLabelVisaCommand)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.VisaCommandLineEdit = QLineEdit(self.settingsPage)
        self.VisaCommandLineEdit.setObjectName(u"VisaCommandLineEdit")
        self.VisaCommandLineEdit.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_27.addWidget(self.VisaCommandLineEdit)

        self.contentBtnVisaCommand = QPushButton(self.settingsPage)
        self.contentBtnVisaCommand.setObjectName(u"contentBtnVisaCommand")

        self.horizontalLayout_27.addWidget(self.contentBtnVisaCommand)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_25)


        self.verticalLayout_12.addLayout(self.horizontalLayout_27)

        self.workspaceLabelEnableAutoSave = QLabel(self.settingsPage)
        self.workspaceLabelEnableAutoSave.setObjectName(u"workspaceLabelEnableAutoSave")

        self.verticalLayout_12.addWidget(self.workspaceLabelEnableAutoSave)

        self.label_2 = QLabel(self.settingsPage)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(100000, 16777215))
        self.label_2.setWordWrap(True)

        self.verticalLayout_12.addWidget(self.label_2)

        self.label_7 = QLabel(self.settingsPage)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_12.addWidget(self.label_7)

        self.enableAutoSaveCheckBox = QCheckBox(self.settingsPage)
        self.enableAutoSaveCheckBox.setObjectName(u"enableAutoSaveCheckBox")

        self.verticalLayout_12.addWidget(self.enableAutoSaveCheckBox)

        self.label_8 = QLabel(self.settingsPage)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_12.addWidget(self.label_8)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.saveDirectoryLineEdit = QLineEdit(self.settingsPage)
        self.saveDirectoryLineEdit.setObjectName(u"saveDirectoryLineEdit")
        self.saveDirectoryLineEdit.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_31.addWidget(self.saveDirectoryLineEdit)

        self.contentBtnDefaultSaveDirectory = QPushButton(self.settingsPage)
        self.contentBtnDefaultSaveDirectory.setObjectName(u"contentBtnDefaultSaveDirectory")

        self.horizontalLayout_31.addWidget(self.contentBtnDefaultSaveDirectory)

        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer_27)


        self.verticalLayout_12.addLayout(self.horizontalLayout_31)

        self.label_3 = QLabel(self.settingsPage)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_12.addWidget(self.label_3)

        self.manifestNameLineEdit = QLineEdit(self.settingsPage)
        self.manifestNameLineEdit.setObjectName(u"manifestNameLineEdit")
        self.manifestNameLineEdit.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_12.addWidget(self.manifestNameLineEdit)

        self.label_5 = QLabel(self.settingsPage)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_12.addWidget(self.label_5)

        self.labelPlanNameLineEdit = QLineEdit(self.settingsPage)
        self.labelPlanNameLineEdit.setObjectName(u"labelPlanNameLineEdit")
        self.labelPlanNameLineEdit.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_12.addWidget(self.labelPlanNameLineEdit)

        self.label_6 = QLabel(self.settingsPage)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_12.addWidget(self.label_6)

        self.exportListNameLineEdit = QLineEdit(self.settingsPage)
        self.exportListNameLineEdit.setObjectName(u"exportListNameLineEdit")
        self.exportListNameLineEdit.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_12.addWidget(self.exportListNameLineEdit)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.contentBtnSaveSettings = QPushButton(self.settingsPage)
        self.contentBtnSaveSettings.setObjectName(u"contentBtnSaveSettings")

        self.horizontalLayout_28.addWidget(self.contentBtnSaveSettings)

        self.horizontalSpacer_26 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_26)


        self.verticalLayout_12.addLayout(self.horizontalLayout_28)

        self.verticalSpacer_22 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_22)


        self.verticalLayout_17.addLayout(self.verticalLayout_12)

        self.contentFrame.addWidget(self.settingsPage)

        self.horizontalLayout.addWidget(self.contentFrame)

        self.horizontalLayout.setStretch(0, 2)
        self.pages.addWidget(self.mainPage)
        self.launchPage = QWidget()
        self.launchPage.setObjectName(u"launchPage")
        self.verticalLayout_18 = QVBoxLayout(self.launchPage)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setSpacing(6)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalSpacer_12 = QSpacerItem(40, 166, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_12)

        self.launchTitleImage = QLabel(self.launchPage)
        self.launchTitleImage.setObjectName(u"launchTitleImage")
        self.launchTitleImage.setMaximumSize(QSize(16777215, 166))
        self.launchTitleImage.setPixmap(QPixmap(u"images/logo.png"))

        self.horizontalLayout_13.addWidget(self.launchTitleImage, 0, Qt.AlignBottom)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_13)


        self.verticalLayout_16.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_14)

        self.launchLabelTitle = QLabel(self.launchPage)
        self.launchLabelTitle.setObjectName(u"launchLabelTitle")

        self.horizontalLayout_15.addWidget(self.launchLabelTitle, 0, Qt.AlignTop)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_15)


        self.verticalLayout_16.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_18)

        self.label = QLabel(self.launchPage)
        self.label.setObjectName(u"label")

        self.horizontalLayout_17.addWidget(self.label, 0, Qt.AlignTop)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_19)


        self.verticalLayout_16.addLayout(self.horizontalLayout_17)

        self.verticalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_16.addItem(self.verticalSpacer_8)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalSpacer_16 = QSpacerItem(80, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_16)

        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.launchBtnNewWorkspace = QPushButton(self.launchPage)
        self.launchBtnNewWorkspace.setObjectName(u"launchBtnNewWorkspace")

        self.verticalLayout_19.addWidget(self.launchBtnNewWorkspace, 0, Qt.AlignTop)

        self.launchBtnOpenWorkspace = QPushButton(self.launchPage)
        self.launchBtnOpenWorkspace.setObjectName(u"launchBtnOpenWorkspace")

        self.verticalLayout_19.addWidget(self.launchBtnOpenWorkspace, 0, Qt.AlignTop)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_19.addItem(self.verticalSpacer_7)


        self.horizontalLayout_16.addLayout(self.verticalLayout_19)

        self.horizontalSpacer_17 = QSpacerItem(80, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_17)

        self.horizontalLayout_16.setStretch(0, 2)
        self.horizontalLayout_16.setStretch(1, 3)
        self.horizontalLayout_16.setStretch(2, 2)

        self.verticalLayout_16.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalSpacer_23 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_23)

        self.launchWarningIconLabel = QLabel(self.launchPage)
        self.launchWarningIconLabel.setObjectName(u"launchWarningIconLabel")
        self.launchWarningIconLabel.setMaximumSize(QSize(25, 25))
        self.launchWarningIconLabel.setPixmap(QPixmap(u"images/warning_icon.png"))

        self.horizontalLayout_26.addWidget(self.launchWarningIconLabel, 0, Qt.AlignBottom)

        self.launchWarningLabelDescription = QLabel(self.launchPage)
        self.launchWarningLabelDescription.setObjectName(u"launchWarningLabelDescription")

        self.horizontalLayout_26.addWidget(self.launchWarningLabelDescription)


        self.verticalLayout_16.addLayout(self.horizontalLayout_26)

        self.verticalSpacer_21 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_16.addItem(self.verticalSpacer_21)


        self.verticalLayout_18.addLayout(self.verticalLayout_16)

        self.pages.addWidget(self.launchPage)

        self.verticalLayout_25.addWidget(self.pages)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.pages.setCurrentIndex(0)
        self.contentFrame.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menuHomeBtn.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.menuImportListBtn.setText(QCoreApplication.translate("MainWindow", u"Import List", None))
        self.menuSortBtn.setText(QCoreApplication.translate("MainWindow", u"Sort", None))
        self.menuExportBtn.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.menuLabelsBtn.setText(QCoreApplication.translate("MainWindow", u"Labels", None))
        self.menuSaveWorkspaceBtn.setText(QCoreApplication.translate("MainWindow", u"Save Workspace", None))
        self.menuNewWorkspaceBtn.setText(QCoreApplication.translate("MainWindow", u"New Workspace", None))
        self.menuOpenWorkspaceBtn.setText(QCoreApplication.translate("MainWindow", u"Open Workspace", None))
        self.menuSettingsBtn.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.titleLabelEmptyWorkspace.setText(QCoreApplication.translate("MainWindow", u"No files have been imported", None))
        self.contentBtnImportList.setText(QCoreApplication.translate("MainWindow", u"Import List", None))
        self.workspaceLabelListSummary.setText(QCoreApplication.translate("MainWindow", u"Imported Lists", None))
        self.contentBtnDeleteList.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.fieldLabelRecords.setText(QCoreApplication.translate("MainWindow", u"Number of records:", None))
        self.fieldLabelColumns.setText(QCoreApplication.translate("MainWindow", u"Number of columns:", None))
        self.valueLabelRecords.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.valueLabelColumns.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.workspaceLabelWarningsTitle.setText(QCoreApplication.translate("MainWindow", u"Warnings", None))
        self.warningsDescription.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.warningsLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.headerLabelSourceFile.setText(QCoreApplication.translate("MainWindow", u"Upload File", None))
        self.contentBtnCancelImport.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.includeHeadersCheckBox.setText(QCoreApplication.translate("MainWindow", u"Include headers", None))
        self.contentBtnBrowseMailFile.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.sheetNumLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Sheet number: default is 1", None))
        self.headerLabelAddressConfirmation.setText(QCoreApplication.translate("MainWindow", u"Address Field Confirmation", None))
        self.contentLabelAddressDescription.setText(QCoreApplication.translate("MainWindow", u"Please select the following column fields imported that correspond to the headings below.", None))
        self.subheaderLabelCountry.setText(QCoreApplication.translate("MainWindow", u"Country ", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"(Leave blank for Australia default)", None))
        self.subheaderLabelState.setText(QCoreApplication.translate("MainWindow", u"State", None))
        self.subheaderLabelPostcode.setText(QCoreApplication.translate("MainWindow", u"Postcode", None))
        self.contentLabelRecordsRead.setText(QCoreApplication.translate("MainWindow", u"Records read: ", None))
        self.contentBtnConfirmImport.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.sortTitleLabelSort.setText(QCoreApplication.translate("MainWindow", u"Sort", None))
        self.sortLabelSortChoice.setText(QCoreApplication.translate("MainWindow", u"Sorting plan", None))
        self.sortLabelArticleWeight.setText(QCoreApplication.translate("MainWindow", u"Weight per Article", None))
        self.sortLineEditWeight.setPlaceholderText(QCoreApplication.translate("MainWindow", u"grams", None))
        self.sortLabelSize.setText(QCoreApplication.translate("MainWindow", u"Size", None))
        self.widthLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Width (mm)", None))
        self.lengthLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Length (mm)", None))
        self.sortLabelDeliveryStandard.setText(QCoreApplication.translate("MainWindow", u"Delivery Standard", None))
        self.sortLabelPrintPostNumber.setText(QCoreApplication.translate("MainWindow", u"Print Post Number", None))
        self.sortLabelPublicationTitle.setText(QCoreApplication.translate("MainWindow", u"Publication Title", None))
        self.sortLabelDate.setText(QCoreApplication.translate("MainWindow", u"Date (Optional)", None))
        self.contentBtnSort.setText(QCoreApplication.translate("MainWindow", u"Generate Sort Manifest", None))
        self.sortTitleLabelPrices.setText(QCoreApplication.translate("MainWindow", u"Prices", None))
        self.sortInfoLabelPrices.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.contentBtnExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.labelsTitleLabel.setText(QCoreApplication.translate("MainWindow", u"Labels", None))
        self.labelsSubtitleThickness.setText(QCoreApplication.translate("MainWindow", u"Thickness", None))
        self.labelsSubtitleDate.setText(QCoreApplication.translate("MainWindow", u"Date (Optional)", None))
        self.labelsSubtitlePaperSize.setText(QCoreApplication.translate("MainWindow", u"Paper Size", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"C5 articles means that articles are oriented in the tray with addresses facing the front of the tray", None))
        self.contentBtnGenerateLabels.setText(QCoreApplication.translate("MainWindow", u"Generate Label File", None))
        self.labelsTitlePlanFile.setText(QCoreApplication.translate("MainWindow", u"Label Plan File", None))
        self.contentBtnPrintLabels.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.workspaceLabelDefaultOpenDirectory.setText(QCoreApplication.translate("MainWindow", u"Default Open Directory", None))
        self.contentBtnDefaultOpenDir.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.workspaceLabelVisaCommand.setText(QCoreApplication.translate("MainWindow", u"Visa Command", None))
        self.contentBtnVisaCommand.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.workspaceLabelEnableAutoSave.setText(QCoreApplication.translate("MainWindow", u"Enable Auto Save", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Enables the auto save feature so you no longer have to choose a file location. Files are saved to a given location with a set name instead. ", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Warning - old files with the same name in the selected location will be overriden with this feature enabled", None))
        self.enableAutoSaveCheckBox.setText(QCoreApplication.translate("MainWindow", u"Enable", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Default Save Directory", None))
        self.contentBtnDefaultSaveDirectory.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Manifest Name", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Label Plan Name", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Export List Name", None))
        self.contentBtnSaveSettings.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.launchTitleImage.setText("")
        self.launchLabelTitle.setText(QCoreApplication.translate("MainWindow", u"Mail Sort", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Version 1.1", None))
        self.launchBtnNewWorkspace.setText(QCoreApplication.translate("MainWindow", u"Create New Workspace", None))
        self.launchBtnOpenWorkspace.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.launchWarningIconLabel.setText("")
        self.launchWarningLabelDescription.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

