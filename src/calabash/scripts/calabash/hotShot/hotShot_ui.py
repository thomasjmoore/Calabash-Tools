# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Thomas\Documents\GitHub\Calabash-Tools\src\calabash\scripts\calabash\hotShot\UI\hotShot.ui'
#
# Created: Thu Mar 01 00:07:17 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_hotShot_dlg(object):
    def setupUi(self, hotShot_dlg):
        hotShot_dlg.setObjectName("hotShot_dlg")
        hotShot_dlg.setWindowModality(QtCore.Qt.NonModal)
        hotShot_dlg.resize(405, 369)
        self.verticalLayout = QtWidgets.QVBoxLayout(hotShot_dlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.project_le = QtWidgets.QLineEdit(hotShot_dlg)
        self.project_le.setObjectName("project_le")
        self.horizontalLayout_2.addWidget(self.project_le)
        self.browse_btn = QtWidgets.QToolButton(hotShot_dlg)
        self.browse_btn.setObjectName("browse_btn")
        self.horizontalLayout_2.addWidget(self.browse_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.shotList_tbl = QtWidgets.QTableWidget(hotShot_dlg)
        self.shotList_tbl.setObjectName("shotList_tbl")
        self.shotList_tbl.setColumnCount(3)
        self.shotList_tbl.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.shotList_tbl.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.shotList_tbl.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.shotList_tbl.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.shotList_tbl)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.saveClose_btn = QtWidgets.QPushButton(hotShot_dlg)
        self.saveClose_btn.setObjectName("saveClose_btn")
        self.horizontalLayout.addWidget(self.saveClose_btn)
        self.noSave_btn = QtWidgets.QPushButton(hotShot_dlg)
        self.noSave_btn.setObjectName("noSave_btn")
        self.horizontalLayout.addWidget(self.noSave_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(hotShot_dlg)
        QtCore.QMetaObject.connectSlotsByName(hotShot_dlg)

    def retranslateUi(self, hotShot_dlg):
        hotShot_dlg.setWindowTitle(QtWidgets.QApplication.translate("hotShot_dlg", "HotShot", None, -1))
        self.browse_btn.setText(QtWidgets.QApplication.translate("hotShot_dlg", "...", None, -1))
        self.shotList_tbl.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("hotShot_dlg", "Shot", None, -1))
        self.shotList_tbl.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("hotShot_dlg", "Start Frame", None, -1))
        self.shotList_tbl.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("hotShot_dlg", "End Frame", None, -1))
        self.saveClose_btn.setText(QtWidgets.QApplication.translate("hotShot_dlg", "Save and Close", None, -1))
        self.noSave_btn.setText(QtWidgets.QApplication.translate("hotShot_dlg", "Close without Saving", None, -1))

