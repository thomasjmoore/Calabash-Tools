# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\mayaTools\calabash\src\calabash\scripts\calabash\vray_toolbox.ui'
#
# Created: Sat Sep 22 14:15:02 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_vray_toolbox(object):
    def setupUi(self, vray_toolbox):
        vray_toolbox.setObjectName("vray_toolbox")
        vray_toolbox.resize(400, 279)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(vray_toolbox.sizePolicy().hasHeightForWidth())
        vray_toolbox.setSizePolicy(sizePolicy)
        vray_toolbox.setMinimumSize(QtCore.QSize(400, 0))
        vray_toolbox.setMaximumSize(QtCore.QSize(400, 16777215))
        self.form_vLyt = QtWidgets.QVBoxLayout(vray_toolbox)
        self.form_vLyt.setObjectName("form_vLyt")
        self.line = QtWidgets.QFrame(vray_toolbox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.form_vLyt.addWidget(self.line)
        self.vrayAttr_lbl = QtWidgets.QLabel(vray_toolbox)
        self.vrayAttr_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.vrayAttr_lbl.setObjectName("vrayAttr_lbl")
        self.form_vLyt.addWidget(self.vrayAttr_lbl)
        self.vray_form = QtWidgets.QFormLayout()
        self.vray_form.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.vray_form.setContentsMargins(-1, 10, -1, -1)
        self.vray_form.setObjectName("vray_form")
        self.applyTo_lbl = QtWidgets.QLabel(vray_toolbox)
        self.applyTo_lbl.setObjectName("applyTo_lbl")
        self.vray_form.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.applyTo_lbl)
        self.applyTo_hlyt = QtWidgets.QHBoxLayout()
        self.applyTo_hlyt.setObjectName("applyTo_hlyt")
        self.selection_rbtn = QtWidgets.QRadioButton(vray_toolbox)
        self.selection_rbtn.setObjectName("selection_rbtn")
        self.applyTo_hlyt.addWidget(self.selection_rbtn)
        self.hierarchy_rbtn = QtWidgets.QRadioButton(vray_toolbox)
        self.hierarchy_rbtn.setObjectName("hierarchy_rbtn")
        self.applyTo_hlyt.addWidget(self.hierarchy_rbtn)
        self.vray_form.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.applyTo_hlyt)
        self.addTo_lbl = QtWidgets.QLabel(vray_toolbox)
        self.addTo_lbl.setObjectName("addTo_lbl")
        self.vray_form.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.addTo_lbl)
        self.addTo_hlyt = QtWidgets.QHBoxLayout()
        self.addTo_hlyt.setObjectName("addTo_hlyt")
        self.transforms_rbtn = QtWidgets.QRadioButton(vray_toolbox)
        self.transforms_rbtn.setObjectName("transforms_rbtn")
        self.addTo_hlyt.addWidget(self.transforms_rbtn)
        self.shapes_rbtn = QtWidgets.QRadioButton(vray_toolbox)
        self.shapes_rbtn.setObjectName("shapes_rbtn")
        self.addTo_hlyt.addWidget(self.shapes_rbtn)
        self.vray_form.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.addTo_hlyt)
        self.attributes_lbl = QtWidgets.QLabel(vray_toolbox)
        self.attributes_lbl.setObjectName("attributes_lbl")
        self.vray_form.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.attributes_lbl)
        self.subd_chk = QtWidgets.QCheckBox(vray_toolbox)
        self.subd_chk.setObjectName("subd_chk")
        self.vray_form.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.subd_chk)
        self.subdDisp_chk = QtWidgets.QCheckBox(vray_toolbox)
        self.subdDisp_chk.setObjectName("subdDisp_chk")
        self.vray_form.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.subdDisp_chk)
        self.objID_chk = QtWidgets.QCheckBox(vray_toolbox)
        self.objID_chk.setObjectName("objID_chk")
        self.vray_form.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.objID_chk)
        self.openSubdiv_chk = QtWidgets.QCheckBox(vray_toolbox)
        self.openSubdiv_chk.setObjectName("openSubdiv_chk")
        self.vray_form.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.openSubdiv_chk)
        self.disp_chk = QtWidgets.QCheckBox(vray_toolbox)
        self.disp_chk.setObjectName("disp_chk")
        self.vray_form.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.disp_chk)
        self.form_vLyt.addLayout(self.vray_form)
        self.attrBut_hlyt = QtWidgets.QHBoxLayout()
        self.attrBut_hlyt.setContentsMargins(-1, 10, -1, -1)
        self.attrBut_hlyt.setObjectName("attrBut_hlyt")
        self.add_btn = QtWidgets.QPushButton(vray_toolbox)
        self.add_btn.setObjectName("add_btn")
        self.attrBut_hlyt.addWidget(self.add_btn)
        self.rem_bt = QtWidgets.QPushButton(vray_toolbox)
        self.rem_bt.setObjectName("rem_bt")
        self.attrBut_hlyt.addWidget(self.rem_bt)
        self.form_vLyt.addLayout(self.attrBut_hlyt)
        self.line_2 = QtWidgets.QFrame(vray_toolbox)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.form_vLyt.addWidget(self.line_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.form_vLyt.addItem(spacerItem)

        self.retranslateUi(vray_toolbox)
        QtCore.QMetaObject.connectSlotsByName(vray_toolbox)

    def retranslateUi(self, vray_toolbox):
        vray_toolbox.setWindowTitle(QtWidgets.QApplication.translate("vray_toolbox", "VRAY TOOLBOX", None, -1))
        self.vrayAttr_lbl.setText(QtWidgets.QApplication.translate("vray_toolbox", "Vray Attributes", None, -1))
        self.applyTo_lbl.setText(QtWidgets.QApplication.translate("vray_toolbox", "Apply to:", None, -1))
        self.selection_rbtn.setText(QtWidgets.QApplication.translate("vray_toolbox", "Selection", None, -1))
        self.hierarchy_rbtn.setText(QtWidgets.QApplication.translate("vray_toolbox", "Hierarchy", None, -1))
        self.addTo_lbl.setText(QtWidgets.QApplication.translate("vray_toolbox", "Add to:", None, -1))
        self.transforms_rbtn.setText(QtWidgets.QApplication.translate("vray_toolbox", "Transforms", None, -1))
        self.shapes_rbtn.setText(QtWidgets.QApplication.translate("vray_toolbox", "Shapes", None, -1))
        self.attributes_lbl.setText(QtWidgets.QApplication.translate("vray_toolbox", "Attributes:", None, -1))
        self.subd_chk.setText(QtWidgets.QApplication.translate("vray_toolbox", "Subdivision", None, -1))
        self.subdDisp_chk.setText(QtWidgets.QApplication.translate("vray_toolbox", "Subdivision and Displacement Quality", None, -1))
        self.objID_chk.setText(QtWidgets.QApplication.translate("vray_toolbox", "Object IDs", None, -1))
        self.openSubdiv_chk.setText(QtWidgets.QApplication.translate("vray_toolbox", "Open SubDiv", None, -1))
        self.disp_chk.setText(QtWidgets.QApplication.translate("vray_toolbox", "Displacement Control", None, -1))
        self.add_btn.setText(QtWidgets.QApplication.translate("vray_toolbox", "Add", None, -1))
        self.rem_bt.setText(QtWidgets.QApplication.translate("vray_toolbox", "Remove", None, -1))

