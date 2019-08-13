# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\young\Documents\maya\modules\calabash\scripts\pipeman\retrofit_ui.ui'
#
# Created: Sun Aug 11 13:06:08 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_mainUI(object):
    def setupUi(self, mainUI):
        mainUI.setObjectName("mainUI")
        mainUI.resize(426, 264)
        self.gridLayout = QtWidgets.QGridLayout(mainUI)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(mainUI)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.changes = QtWidgets.QPlainTextEdit(mainUI)
        self.changes.setReadOnly(True)
        self.changes.setObjectName("changes")
        self.verticalLayout.addWidget(self.changes)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_continue = QtWidgets.QPushButton(mainUI)
        self.pushButton_continue.setObjectName("pushButton_continue")
        self.horizontalLayout.addWidget(self.pushButton_continue)
        self.pushButton_cancel = QtWidgets.QPushButton(mainUI)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(mainUI)
        QtCore.QMetaObject.connectSlotsByName(mainUI)

    def retranslateUi(self, mainUI):
        mainUI.setWindowTitle(QtWidgets.QApplication.translate("mainUI", "Project Retrofit", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("mainUI", "Old project detected! The following changes must be made to work with Pipeman 2.0", None, -1))
        self.pushButton_continue.setText(QtWidgets.QApplication.translate("mainUI", "Continue", None, -1))
        self.pushButton_cancel.setText(QtWidgets.QApplication.translate("mainUI", "Cancel", None, -1))

