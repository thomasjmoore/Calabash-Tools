# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\guest1\Documents\maya\modules\calabash\scripts\pipeman\pipeman_ui.ui'
#
# Created: Tue Apr  9 15:42:17 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_mainUI(object):
    def setupUi(self, mainUI):
        mainUI.setObjectName("mainUI")
        mainUI.resize(871, 359)
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
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_3 = QtWidgets.QLabel(self.pipeman_anim)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_7.addWidget(self.label_3)
        self.gridLayout_5.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)
        self.listWidget_shots = QtWidgets.QListWidget(self.pipeman_anim)
        self.listWidget_shots.setWordWrap(True)
        self.listWidget_shots.setObjectName("listWidget_shots")
        self.gridLayout_5.addWidget(self.listWidget_shots, 2, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_anim_openlatest = QtWidgets.QPushButton(self.pipeman_anim)
        self.pushButton_anim_openlatest.setObjectName("pushButton_anim_openlatest")
        self.horizontalLayout_5.addWidget(self.pushButton_anim_openlatest)
        self.gridLayout_5.addLayout(self.horizontalLayout_5, 3, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pushButton_anim_makelive = QtWidgets.QPushButton(self.pipeman_anim)
        self.pushButton_anim_makelive.setObjectName("pushButton_anim_makelive")
        self.horizontalLayout_8.addWidget(self.pushButton_anim_makelive)
        self.gridLayout_5.addLayout(self.horizontalLayout_8, 3, 1, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.pipeman_anim)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.gridLayout_5.addLayout(self.horizontalLayout_6, 1, 1, 1, 1)
        self.treeWidget_animVersions = QtWidgets.QTreeWidget(self.pipeman_anim)
        self.treeWidget_animVersions.setMinimumSize(QtCore.QSize(0, 0))
        self.treeWidget_animVersions.setLineWidth(1)
        self.treeWidget_animVersions.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.treeWidget_animVersions.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeWidget_animVersions.setAlternatingRowColors(True)
        self.treeWidget_animVersions.setIndentation(10)
        self.treeWidget_animVersions.setItemsExpandable(True)
        self.treeWidget_animVersions.setAnimated(True)
        self.treeWidget_animVersions.setWordWrap(True)
        self.treeWidget_animVersions.setExpandsOnDoubleClick(True)
        self.treeWidget_animVersions.setObjectName("treeWidget_animVersions")
        self.treeWidget_animVersions.header().setCascadingSectionResizes(True)
        self.treeWidget_animVersions.header().setDefaultSectionSize(0)
        self.treeWidget_animVersions.header().setHighlightSections(False)
        self.treeWidget_animVersions.header().setMinimumSectionSize(0)
        self.treeWidget_animVersions.header().setSortIndicatorShown(True)
        self.treeWidget_animVersions.header().setStretchLastSection(False)
        self.gridLayout_5.addWidget(self.treeWidget_animVersions, 2, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_5)
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
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treeWidget_assets = QtWidgets.QTreeWidget(self.pipeman_assets)
        self.treeWidget_assets.setMinimumSize(QtCore.QSize(0, 0))
        self.treeWidget_assets.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeWidget_assets.setAnimated(True)
        self.treeWidget_assets.setHeaderHidden(True)
        self.treeWidget_assets.setObjectName("treeWidget_assets")
        self.verticalLayout_3.addWidget(self.treeWidget_assets)
        self.gridLayout_4.addLayout(self.verticalLayout_3, 1, 0, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_2 = QtWidgets.QLabel(self.pipeman_assets)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_10.addWidget(self.label_2)
        self.gridLayout_4.addLayout(self.horizontalLayout_10, 0, 1, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.pushButton_asset_openlatest = QtWidgets.QPushButton(self.pipeman_assets)
        self.pushButton_asset_openlatest.setObjectName("pushButton_asset_openlatest")
        self.horizontalLayout_9.addWidget(self.pushButton_asset_openlatest)
        self.gridLayout_4.addLayout(self.horizontalLayout_9, 3, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.treeWidget_versions = QtWidgets.QTreeWidget(self.pipeman_assets)
        self.treeWidget_versions.setMinimumSize(QtCore.QSize(0, 0))
        self.treeWidget_versions.setLineWidth(1)
        self.treeWidget_versions.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.treeWidget_versions.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeWidget_versions.setAlternatingRowColors(True)
        self.treeWidget_versions.setIndentation(10)
        self.treeWidget_versions.setItemsExpandable(True)
        self.treeWidget_versions.setAnimated(True)
        self.treeWidget_versions.setWordWrap(True)
        self.treeWidget_versions.setExpandsOnDoubleClick(True)
        self.treeWidget_versions.setObjectName("treeWidget_versions")
        self.treeWidget_versions.header().setCascadingSectionResizes(True)
        self.treeWidget_versions.header().setDefaultSectionSize(0)
        self.treeWidget_versions.header().setHighlightSections(False)
        self.treeWidget_versions.header().setMinimumSectionSize(0)
        self.treeWidget_versions.header().setSortIndicatorShown(True)
        self.treeWidget_versions.header().setStretchLastSection(False)
        self.verticalLayout_4.addWidget(self.treeWidget_versions)
        self.gridLayout_4.addLayout(self.verticalLayout_4, 1, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.pipeman_assets)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.gridLayout_4.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_makelive = QtWidgets.QPushButton(self.pipeman_assets)
        self.pushButton_makelive.setObjectName("pushButton_makelive")
        self.horizontalLayout_3.addWidget(self.pushButton_makelive)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 3, 1, 1, 1)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_6 = QtWidgets.QLabel(self.pipeman_assets)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_12.addWidget(self.label_6)
        self.comment_asset = QtWidgets.QLabel(self.pipeman_assets)
        self.comment_asset.setText("")
        self.comment_asset.setTextFormat(QtCore.Qt.PlainText)
        self.comment_asset.setWordWrap(True)
        self.comment_asset.setObjectName("comment_asset")
        self.horizontalLayout_12.addWidget(self.comment_asset)
        self.gridLayout_4.addLayout(self.horizontalLayout_12, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.tabWidget_pipeman.addTab(self.pipeman_assets, "")
        self.gridLayout.addWidget(self.tabWidget_pipeman, 1, 0, 1, 1)

        self.retranslateUi(mainUI)
        self.tabWidget_pipeman.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainUI)

    def retranslateUi(self, mainUI):
        mainUI.setWindowTitle(QtWidgets.QApplication.translate("mainUI", "Pipeman", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("mainUI", "Shot", None, -1))
        self.listWidget_shots.setSortingEnabled(True)
        self.pushButton_anim_openlatest.setText(QtWidgets.QApplication.translate("mainUI", "Open Latest", None, -1))
        self.pushButton_anim_makelive.setText(QtWidgets.QApplication.translate("mainUI", "Make Live", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("mainUI", "Versions", None, -1))
        self.treeWidget_animVersions.headerItem().setText(0, QtWidgets.QApplication.translate("mainUI", "Version", None, -1))
        self.treeWidget_animVersions.headerItem().setText(1, QtWidgets.QApplication.translate("mainUI", "Status", None, -1))
        self.tabWidget_pipeman.setTabText(self.tabWidget_pipeman.indexOf(self.pipeman_anim), QtWidgets.QApplication.translate("mainUI", "Animation", None, -1))
        self.treeWidget_assets.setSortingEnabled(True)
        self.treeWidget_assets.headerItem().setText(0, QtWidgets.QApplication.translate("mainUI", "Type", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("mainUI", "Versions", None, -1))
        self.pushButton_asset_openlatest.setText(QtWidgets.QApplication.translate("mainUI", "Open Latest", None, -1))
        self.treeWidget_versions.headerItem().setText(0, QtWidgets.QApplication.translate("mainUI", "Version", None, -1))
        self.treeWidget_versions.headerItem().setText(1, QtWidgets.QApplication.translate("mainUI", "Status", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("mainUI", "Assets", None, -1))
        self.pushButton_makelive.setText(QtWidgets.QApplication.translate("mainUI", "Make Live", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("mainUI", "Comment:", None, -1))
        self.tabWidget_pipeman.setTabText(self.tabWidget_pipeman.indexOf(self.pipeman_assets), QtWidgets.QApplication.translate("mainUI", "Assets", None, -1))

