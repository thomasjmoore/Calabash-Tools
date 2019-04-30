# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\guest1\Documents\maya\modules\calabash\scripts\calabash\overscan_ui.ui'
#
# Created: Mon Apr 29 15:42:09 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_mainUI(object):
    def setupUi(self, mainUI):
        mainUI.setObjectName("mainUI")
        mainUI.resize(300, 149)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainUI.sizePolicy().hasHeightForWidth())
        mainUI.setSizePolicy(sizePolicy)
        mainUI.setMinimumSize(QtCore.QSize(300, 0))
        mainUI.setMaximumSize(QtCore.QSize(300, 149))
        self.gridLayout_2 = QtWidgets.QGridLayout(mainUI)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout.setObjectName("gridLayout")
        self.uniform_getres = QtWidgets.QPushButton(mainUI)
        self.uniform_getres.setObjectName("uniform_getres")
        self.gridLayout.addWidget(self.uniform_getres, 3, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.uniform_width = QtWidgets.QLineEdit(mainUI)
        self.uniform_width.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.uniform_width.setObjectName("uniform_width")
        self.verticalLayout.addWidget(self.uniform_width)
        self.uniform_height = QtWidgets.QLineEdit(mainUI)
        self.uniform_height.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.uniform_height.setObjectName("uniform_height")
        self.verticalLayout.addWidget(self.uniform_height)
        self.gridLayout.addLayout(self.verticalLayout, 3, 2, 1, 1)
        self.uniform_overscan = QtWidgets.QLineEdit(mainUI)
        self.uniform_overscan.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.uniform_overscan.setObjectName("uniform_overscan")
        self.gridLayout.addWidget(self.uniform_overscan, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(mainUI)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(mainUI)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.uniform_camera = QtWidgets.QLineEdit(mainUI)
        self.uniform_camera.setFrame(True)
        self.uniform_camera.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.uniform_camera.setDragEnabled(True)
        self.uniform_camera.setObjectName("uniform_camera")
        self.gridLayout.addWidget(self.uniform_camera, 0, 2, 1, 1)
        self.uniform_set = QtWidgets.QPushButton(mainUI)
        self.uniform_set.setObjectName("uniform_set")
        self.gridLayout.addWidget(self.uniform_set, 4, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(mainUI)
        QtCore.QMetaObject.connectSlotsByName(mainUI)
        mainUI.setTabOrder(self.uniform_camera, self.uniform_overscan)
        mainUI.setTabOrder(self.uniform_overscan, self.uniform_width)
        mainUI.setTabOrder(self.uniform_width, self.uniform_height)
        mainUI.setTabOrder(self.uniform_height, self.uniform_getres)
        mainUI.setTabOrder(self.uniform_getres, self.uniform_set)

    def retranslateUi(self, mainUI):
        mainUI.setWindowTitle(QtWidgets.QApplication.translate("mainUI", "Set Overscan", None, -1))
        self.uniform_getres.setText(QtWidgets.QApplication.translate("mainUI", "Get Resolution", None, -1))
        self.uniform_width.setPlaceholderText(QtWidgets.QApplication.translate("mainUI", "Width", None, -1))
        self.uniform_height.setPlaceholderText(QtWidgets.QApplication.translate("mainUI", "Height", None, -1))
        self.uniform_overscan.setPlaceholderText(QtWidgets.QApplication.translate("mainUI", "1.00", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("mainUI", "Overscan:", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("mainUI", "Camera:", None, -1))
        self.uniform_camera.setPlaceholderText(QtWidgets.QApplication.translate("mainUI", "Drag and Drop", None, -1))
        self.uniform_set.setText(QtWidgets.QApplication.translate("mainUI", "Set Overscan", None, -1))

