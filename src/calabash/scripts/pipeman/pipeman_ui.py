# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\guest1\Documents\maya\modules\calabash\scripts\calabash\makeLive_ui.ui'
#
# Created: Thu Mar 21 10:42:46 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_mainUI(object):
    def setupUi(self, mainUI):
        mainUI.setObjectName("mainUI")
        mainUI.resize(834, 404)
        self.gridLayout = QtWidgets.QGridLayout(mainUI)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget_pipeman = QtWidgets.QTabWidget(mainUI)
        self.tabWidget_pipeman.setObjectName("tabWidget_pipeman")
        self.pipeman_anim = QtWidgets.QWidget()
        self.pipeman_anim.setObjectName("pipeman_anim")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.pipeman_anim)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.pipeman_anim)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.pipeman_anim)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.listWidget_shots = QtWidgets.QListWidget(self.pipeman_anim)
        self.listWidget_shots.setObjectName("listWidget_shots")
        self.horizontalLayout_7.addWidget(self.listWidget_shots)
        self.treeWidget_animVersions = QtWidgets.QTreeWidget(self.pipeman_anim)
        self.treeWidget_animVersions.setMinimumSize(QtCore.QSize(402, 0))
        self.treeWidget_animVersions.setLineWidth(1)
        self.treeWidget_animVersions.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.treeWidget_animVersions.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeWidget_animVersions.setAlternatingRowColors(True)
        self.treeWidget_animVersions.setIndentation(10)
        self.treeWidget_animVersions.setItemsExpandable(False)
        self.treeWidget_animVersions.setWordWrap(True)
        self.treeWidget_animVersions.setExpandsOnDoubleClick(False)
        self.treeWidget_animVersions.setObjectName("treeWidget_animVersions")
        self.treeWidget_animVersions.header().setCascadingSectionResizes(True)
        self.treeWidget_animVersions.header().setDefaultSectionSize(200)
        self.treeWidget_animVersions.header().setHighlightSections(True)
        self.treeWidget_animVersions.header().setMinimumSectionSize(200)
        self.horizontalLayout_7.addWidget(self.treeWidget_animVersions)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.pushButton_anim_makelive = QtWidgets.QPushButton(self.pipeman_anim)
        self.pushButton_anim_makelive.setObjectName("pushButton_anim_makelive")
        self.horizontalLayout_8.addWidget(self.pushButton_anim_makelive)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.tabWidget_pipeman.addTab(self.pipeman_anim, "")
        self.pipeman_assets = QtWidgets.QWidget()
        self.pipeman_assets.setObjectName("pipeman_assets")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.pipeman_assets)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(self.pipeman_assets)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.pipeman_assets)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.listWidget_assets = QtWidgets.QListWidget(self.pipeman_assets)
        self.listWidget_assets.setObjectName("listWidget_assets")
        self.horizontalLayout_4.addWidget(self.listWidget_assets)
        self.treeWidget_versions = QtWidgets.QTreeWidget(self.pipeman_assets)
        self.treeWidget_versions.setMinimumSize(QtCore.QSize(402, 0))
        self.treeWidget_versions.setLineWidth(1)
        self.treeWidget_versions.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.treeWidget_versions.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeWidget_versions.setAlternatingRowColors(True)
        self.treeWidget_versions.setIndentation(10)
        self.treeWidget_versions.setItemsExpandable(False)
        self.treeWidget_versions.setWordWrap(True)
        self.treeWidget_versions.setExpandsOnDoubleClick(False)
        self.treeWidget_versions.setObjectName("treeWidget_versions")
        self.treeWidget_versions.header().setCascadingSectionResizes(True)
        self.treeWidget_versions.header().setDefaultSectionSize(200)
        self.treeWidget_versions.header().setHighlightSections(True)
        self.treeWidget_versions.header().setMinimumSectionSize(200)
        self.horizontalLayout_4.addWidget(self.treeWidget_versions)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.pushButton_makelive = QtWidgets.QPushButton(self.pipeman_assets)
        self.pushButton_makelive.setObjectName("pushButton_makelive")
        self.horizontalLayout_3.addWidget(self.pushButton_makelive)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.tabWidget_pipeman.addTab(self.pipeman_assets, "")
        self.gridLayout.addWidget(self.tabWidget_pipeman, 0, 0, 1, 1)

        self.retranslateUi(mainUI)
        self.tabWidget_pipeman.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainUI)

    def retranslateUi(self, mainUI):
        mainUI.setWindowTitle(QtWidgets.QApplication.translate("mainUI", "Make Live Editor", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("mainUI", "Shot", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("mainUI", "Versions", None, -1))
        self.treeWidget_animVersions.headerItem().setText(0, QtWidgets.QApplication.translate("mainUI", "Version", None, -1))
        self.treeWidget_animVersions.headerItem().setText(1, QtWidgets.QApplication.translate("mainUI", "Status", None, -1))
        self.pushButton_anim_makelive.setText(QtWidgets.QApplication.translate("mainUI", "Make Live", None, -1))
        self.tabWidget_pipeman.setTabText(self.tabWidget_pipeman.indexOf(self.pipeman_anim), QtWidgets.QApplication.translate("mainUI", "Animation", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("mainUI", "Assets", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("mainUI", "Versions", None, -1))
        self.treeWidget_versions.headerItem().setText(0, QtWidgets.QApplication.translate("mainUI", "Version", None, -1))
        self.treeWidget_versions.headerItem().setText(1, QtWidgets.QApplication.translate("mainUI", "Status", None, -1))
        self.pushButton_makelive.setText(QtWidgets.QApplication.translate("mainUI", "Make Live", None, -1))
        self.tabWidget_pipeman.setTabText(self.tabWidget_pipeman.indexOf(self.pipeman_assets), QtWidgets.QApplication.translate("mainUI", "Assets", None, -1))

