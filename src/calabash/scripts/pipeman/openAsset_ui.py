# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\young\Documents\maya\modules\calabash\scripts\pipeman\openAsset_ui.ui'
#
# Created: Sat Aug 10 13:16:15 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_mainUI(object):
    def setupUi(self, mainUI):
        mainUI.setObjectName("mainUI")
        mainUI.resize(353, 319)
        self.verticalLayout = QtWidgets.QVBoxLayout(mainUI)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(mainUI)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.subnamelist = QtWidgets.QListWidget(mainUI)
        self.subnamelist.setObjectName("subnamelist")
        self.verticalLayout.addWidget(self.subnamelist)
        self.pushButton_openSelected = QtWidgets.QPushButton(mainUI)
        self.pushButton_openSelected.setObjectName("pushButton_openSelected")
        self.verticalLayout.addWidget(self.pushButton_openSelected)

        self.retranslateUi(mainUI)
        QtCore.QMetaObject.connectSlotsByName(mainUI)

    def retranslateUi(self, mainUI):
        mainUI.setWindowTitle(QtWidgets.QApplication.translate("mainUI", "Open Asset", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("mainUI", "Open Asset", None, -1))
        self.pushButton_openSelected.setText(QtWidgets.QApplication.translate("mainUI", "Open Selected", None, -1))

