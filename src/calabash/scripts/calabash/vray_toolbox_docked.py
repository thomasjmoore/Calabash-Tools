'''
Template class for docking a Qt widget to maya 2017+.
Author: Lior ben horin
12-1-2017
'''

import weakref

import maya.cmds as cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import logging as logger
from . import vrayUtils
from . import vray_toolboxUI

from .lib.Qt import QtGui, QtWidgets, QtCore  # https://github.com/mottosso/Qt.py by Marcus Ottosson

btns = []

def dock_window(dialog_class):
    try:
        cmds.deleteUI(dialog_class.CONTROL_NAME)
        logger.info('removed workspace {}'.format(dialog_class.CONTROL_NAME))

    except:
        pass

    # building the workspace control with maya.cmds
    main_control = cmds.workspaceControl(dialog_class.CONTROL_NAME, ttc=["AttributeEditor", -1], iw=dialog_class.WIDTH, mw=1,
                                         wp='preferred', label=dialog_class.DOCK_LABEL_NAME)

    # now lets get a C++ pointer to it using OpenMaya
    control_widget = omui.MQtUtil.findControl(dialog_class.CONTROL_NAME)
    # convert the C++ pointer to Qt object we can use
    control_wrap = wrapInstance(long(control_widget), QtWidgets.QWidget)

    # control_wrap is the widget of the docking window and now we can start working with it:
    control_wrap.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    win = dialog_class(control_wrap)

    # after maya is ready we should restore the window since it may not be visible
    cmds.evalDeferred(lambda *args: cmds.workspaceControl(main_control, e=True, rs=True))

    # will return the class of the dock content.
    return win.run()


class MyDockingUI(QtWidgets.QWidget):
    instances = list()
    CONTROL_NAME = 'Vray Toolbox'
    DOCK_LABEL_NAME = 'Vray Toolbox'
    WIDTH = 400

    def __init__(self, parent=None):
        super(MyDockingUI, self).__init__(parent)

        # let's keep track of our docks so we only have one at a time.
        MyDockingUI.delete_instances()
        self.__class__.instances.append(weakref.proxy(self))

        self.window_name = self.CONTROL_NAME
        self.ui = parent
        self.main_layout = parent.layout()
        self.main_layout.setContentsMargins(2, 2, 2, 2)

        # here we can start coding our UI
        self.title = QtWidgets.QLabel(self.CONTROL_NAME)

        self.main_layout.addWidget(self.title)
        vray_toolbox = QtWidgets.QWidget()
        self.main_layout.addWidget(vray_toolbox)

        vray_toolbox.setObjectName("vray_toolbox")
        vray_toolbox.resize(400, 472)
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

        QtCore.QMetaObject.connectSlotsByName(vray_toolbox)

        vray_toolbox.setWindowTitle(QtWidgets.QApplication.translate("vray_toolbox", "windowTitle", None, -1))
        self.vrayAttr_lbl.setText(QtWidgets.QApplication.translate("vray_toolbox", "Vray Attributes", None, -1))
        self.applyTo_lbl.setText(QtWidgets.QApplication.translate("vray_toolbox", "Apply to:", None, -1))
        self.selection_rbtn.setText(QtWidgets.QApplication.translate("vray_toolbox", "Selection", None, -1))
        self.hierarchy_rbtn.setText(QtWidgets.QApplication.translate("vray_toolbox", "Hierarchy", None, -1))
        self.addTo_lbl.setText(QtWidgets.QApplication.translate("vray_toolbox", "Add to:", None, -1))
        self.transforms_rbtn.setText(QtWidgets.QApplication.translate("vray_toolbox", "Transforms", None, -1))
        self.shapes_rbtn.setText(QtWidgets.QApplication.translate("vray_toolbox", "Shapes", None, -1))
        self.attributes_lbl.setText(QtWidgets.QApplication.translate("vray_toolbox", "Attributes:", None, -1))
        self.subd_chk.setText(QtWidgets.QApplication.translate("vray_toolbox", "Subdivision", None, -1))
        self.subdDisp_chk.setText(
            QtWidgets.QApplication.translate("vray_toolbox", "Subdivision and Displacement Quality", None, -1))
        self.objID_chk.setText(QtWidgets.QApplication.translate("vray_toolbox", "Object IDs", None, -1))
        self.openSubdiv_chk.setText(QtWidgets.QApplication.translate("vray_toolbox", "Open SubDiv", None, -1))
        self.disp_chk.setText(QtWidgets.QApplication.translate("vray_toolbox", "Displacement Control", None, -1))
        self.add_btn.setText(QtWidgets.QApplication.translate("vray_toolbox", "Add", None, -1))
        self.rem_bt.setText(QtWidgets.QApplication.translate("vray_toolbox", "Remove", None, -1))

        self.applyTo_btngrp = QtWidgets.QButtonGroup(self.main_layout)
        self.applyTo_btngrp.addButton(self.transforms_rbtn)
        self.applyTo_btngrp.addButton(self.shapes_rbtn)
        self.selection_rbtn.setChecked(True)
        self.shapes_rbtn.setChecked(True)

        self.add_btn.clicked.connect(self.add_btn_clicked)
        self.rem_bt.clicked.connect(self.remove_btn_clicked)

        self.transforms_rbtn.clicked.connect(self.transforms_clicked)
        self.shapes_rbtn.clicked.connect(self.transforms_clicked)

    def check_ui(self):
        selected = self.selection_rbtn.isChecked()
        shapes = self.shapes_rbtn.isChecked()

        commands = []
        if self.subd_chk.isChecked():
            commands.append("vray_subdivision")
        if self.subdDisp_chk.isChecked():
            commands.append("vray_subquality")
        if self.disp_chk.isChecked():
            commands.append("vray_displacement")
        if self.objID_chk.isChecked():
            commands.append("vray_objectID")
        if self.openSubdiv_chk.isChecked():
            commands.append("vray_opensubdiv")

        return selected, shapes, commands

    def add_btn_clicked(self):
        selected, shapes, commands = self.check_ui()

        if not commands:
            return

        for c in commands:
            vrayUtils.vray_attributes(selected=selected, shapes=shapes, add=True, command=c)

    def remove_btn_clicked(self):
        selected, shapes, commands = self.check_ui()

        if not commands:
            return

        for c in commands:
            vrayUtils.vray_attributes(selected=selected, shapes=shapes, add=False, command=c)

    def transforms_clicked(self):
        is_checked = self.transforms_rbtn.isChecked()
        if is_checked:
            self.subd_chk.setDisabled(True)
            self.subdDisp_chk.setDisabled(True)
            self.disp_chk.setDisabled(True)
            self.openSubdiv_chk.setDisabled(True)
            self.subd_chk.setChecked(False)
            self.subdDisp_chk.setChecked(False)
            self.disp_chk.setChecked(False)
            self.openSubdiv_chk.setChecked(False)
        else:
            self.subd_chk.setEnabled(True)
            self.subdDisp_chk.setEnabled(True)
            self.disp_chk.setEnabled(True)
            self.openSubdiv_chk.setEnabled(True)

    @staticmethod
    def delete_instances():
        for ins in MyDockingUI.instances:
            logger.info('Delete {}'.format(ins))
            try:
                ins.setParent(None)
                ins.deleteLater()
            except:
                # ignore the fact that the actual parent has already been deleted by Maya...
                pass

            MyDockingUI.instances.remove(ins)
            del ins

    def run(self):
        return self


# this is where we call the window
#my_dock = dock_window(MyDockingUI)