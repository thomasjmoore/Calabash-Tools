# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\guest1\Documents\maya\modules\calabash\scripts\calabash\overscan_ui.ui'
#
# Created: Wed Apr 17 15:12:17 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_mainUI(object):
    def setupUi(self, mainUI):
        mainUI.setObjectName("mainUI")
        mainUI.resize(546, 222)
        self.gridLayout = QtWidgets.QGridLayout(mainUI)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(mainUI)
        self.tabWidget.setObjectName("tabWidget")
        self.uniform = QtWidgets.QWidget()
        self.uniform.setObjectName("uniform")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.uniform)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.uniform)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.uniform_width = QtWidgets.QLineEdit(self.uniform)
        self.uniform_width.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.uniform_width.setObjectName("uniform_width")
        self.gridLayout_2.addWidget(self.uniform_width, 3, 1, 1, 1)
        self.uniform_camera = QtWidgets.QLineEdit(self.uniform)
        self.uniform_camera.setFrame(True)
        self.uniform_camera.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.uniform_camera.setDragEnabled(True)
        self.uniform_camera.setObjectName("uniform_camera")
        self.gridLayout_2.addWidget(self.uniform_camera, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.uniform)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.uniform)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.uniform_height = QtWidgets.QLineEdit(self.uniform)
        self.uniform_height.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.uniform_height.setObjectName("uniform_height")
        self.gridLayout_2.addWidget(self.uniform_height, 3, 2, 1, 1)
        self.uniform_overscan = QtWidgets.QLineEdit(self.uniform)
        self.uniform_overscan.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.uniform_overscan.setObjectName("uniform_overscan")
        self.gridLayout_2.addWidget(self.uniform_overscan, 2, 1, 1, 1)
        self.unifrom_getres = QtWidgets.QPushButton(self.uniform)
        self.unifrom_getres.setObjectName("unifrom_getres")
        self.gridLayout_2.addWidget(self.unifrom_getres, 3, 3, 1, 1)
        self.uniform_set = QtWidgets.QPushButton(self.uniform)
        self.uniform_set.setObjectName("uniform_set")
        self.gridLayout_2.addWidget(self.uniform_set, 4, 3, 1, 1)
        self.tabWidget.addTab(self.uniform, "")
        self.wh = QtWidgets.QWidget()
        self.wh.setObjectName("wh")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.wh)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_5 = QtWidgets.QLabel(self.wh)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.wh)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 1, 1, 1)
        self.wh_camera = QtWidgets.QLineEdit(self.wh)
        self.wh_camera.setDragEnabled(True)
        self.wh_camera.setObjectName("wh_camera")
        self.gridLayout_3.addWidget(self.wh_camera, 0, 2, 1, 1)
        self.wh_horz = QtWidgets.QLineEdit(self.wh)
        self.wh_horz.setObjectName("wh_horz")
        self.gridLayout_3.addWidget(self.wh_horz, 1, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.wh)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.wh)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 3, 1, 1, 1)
        self.wh_vert = QtWidgets.QLineEdit(self.wh)
        self.wh_vert.setObjectName("wh_vert")
        self.gridLayout_3.addWidget(self.wh_vert, 2, 2, 1, 1)
        self.wh_width = QtWidgets.QLineEdit(self.wh)
        self.wh_width.setObjectName("wh_width")
        self.gridLayout_3.addWidget(self.wh_width, 3, 2, 1, 1)
        self.wh_height = QtWidgets.QLineEdit(self.wh)
        self.wh_height.setObjectName("wh_height")
        self.gridLayout_3.addWidget(self.wh_height, 3, 3, 1, 1)
        self.wh_getres = QtWidgets.QPushButton(self.wh)
        self.wh_getres.setObjectName("wh_getres")
        self.gridLayout_3.addWidget(self.wh_getres, 3, 4, 1, 1)
        self.wh_frameback_width = QtWidgets.QLineEdit(self.wh)
        self.wh_frameback_width.setObjectName("wh_frameback_width")
        self.gridLayout_3.addWidget(self.wh_frameback_width, 4, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.wh)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 4, 1, 1, 1)
        self.wh_getframeback = QtWidgets.QPushButton(self.wh)
        self.wh_getframeback.setObjectName("wh_getframeback")
        self.gridLayout_3.addWidget(self.wh_getframeback, 4, 4, 1, 1)
        self.wh_frameback_height = QtWidgets.QLineEdit(self.wh)
        self.wh_frameback_height.setObjectName("wh_frameback_height")
        self.gridLayout_3.addWidget(self.wh_frameback_height, 4, 3, 1, 1)
        self.wh_set = QtWidgets.QPushButton(self.wh)
        self.wh_set.setObjectName("wh_set")
        self.gridLayout_3.addWidget(self.wh_set, 5, 4, 1, 1)
        self.tabWidget.addTab(self.wh, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(mainUI)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainUI)
        mainUI.setTabOrder(self.uniform_camera, self.uniform_overscan)
        mainUI.setTabOrder(self.uniform_overscan, self.uniform_width)
        mainUI.setTabOrder(self.uniform_width, self.uniform_height)
        mainUI.setTabOrder(self.uniform_height, self.unifrom_getres)
        mainUI.setTabOrder(self.unifrom_getres, self.uniform_set)
        mainUI.setTabOrder(self.uniform_set, self.wh_camera)
        mainUI.setTabOrder(self.wh_camera, self.wh_horz)
        mainUI.setTabOrder(self.wh_horz, self.wh_vert)
        mainUI.setTabOrder(self.wh_vert, self.wh_width)
        mainUI.setTabOrder(self.wh_width, self.wh_height)
        mainUI.setTabOrder(self.wh_height, self.wh_getres)
        mainUI.setTabOrder(self.wh_getres, self.wh_frameback_width)
        mainUI.setTabOrder(self.wh_frameback_width, self.wh_frameback_height)
        mainUI.setTabOrder(self.wh_frameback_height, self.wh_getframeback)
        mainUI.setTabOrder(self.wh_getframeback, self.wh_set)
        mainUI.setTabOrder(self.wh_set, self.tabWidget)

    def retranslateUi(self, mainUI):
        mainUI.setWindowTitle(QtWidgets.QApplication.translate("mainUI", "Set Overscan", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("mainUI", "Frame Width / Height:", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("mainUI", "Camera:", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("mainUI", "Overscan:", None, -1))
        self.unifrom_getres.setText(QtWidgets.QApplication.translate("mainUI", "Get From Scene", None, -1))
        self.uniform_set.setText(QtWidgets.QApplication.translate("mainUI", "Set Overscan", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.uniform), QtWidgets.QApplication.translate("mainUI", "Uniform", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("mainUI", "Camera:", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("mainUI", "Horizontal Pixels:", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("mainUI", "Vertical Pixels:", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("mainUI", "Frame Width / Height:", None, -1))
        self.wh_getres.setText(QtWidgets.QApplication.translate("mainUI", "Get From Scene", None, -1))
        self.label_10.setText(QtWidgets.QApplication.translate("mainUI", "Film Back Width / Height:", None, -1))
        self.wh_getframeback.setText(QtWidgets.QApplication.translate("mainUI", "Get From Camera", None, -1))
        self.wh_set.setText(QtWidgets.QApplication.translate("mainUI", "Set Overscan", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.wh), QtWidgets.QApplication.translate("mainUI", "Width / Height", None, -1))

