from ..lib.Qt import QtCore, QtGui, QtWidgets
from . import hotShot_ui as customUI
from . import hotShot_core
import os

try:
    from shiboken import wrapInstance
except:
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

reload(hotShot_core)
reload(customUI)

__all__ = [
    'launch',
    ]

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class ControlMainWindow(QtWidgets.QDialog):
    version = "1.0"

    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.hotShot = hotShot_core.hotShot()
        self.setWindowFlags(QtCore.Qt.Tool)
        self.ui = customUI.Ui_hotShot_dlg()
        self.ui.setupUi(self)

        self.hotShot.read_shot_file()

        self.populate()

        self.ui.project_le.textChanged.connect(self.update_project)

        self.ui.project_le.setText(r"C:\Users\Thomas\Dropbox\Calabash\Airstream\Airstream")


    def populate(self):

        print self.hotShot.shots
        row = 0
        for key, value in sorted(self.hotShot.shots.items()):
            #print(key, value)
            start = str(value["start"])
            end = str(value["end"])
            self.ui.shotList_tbl.insertRow(row)
            self.ui.shotList_tbl.setItem(row, 0, QtWidgets.QTableWidgetItem(key))
            self.ui.shotList_tbl.setItem(row, 1, QtWidgets.QTableWidgetItem(start))
            self.ui.shotList_tbl.setItem(row, 2, QtWidgets.QTableWidgetItem(end))
            #self.ui.shotList_tbl.item(0,row).setText(key)
            row += 1


    def update_project(self):
        text = self.ui.project_le.text()
        shots_file = "%s%sshots.json" % (text, os.path.sep)
        self.hotShot.shot_file = shots_file
        self.hotShot.read_shot_file()
        self.populate()

#############################################################################################################


def launch():
    global dialog
    #if dialog is None:
    #    dialog = ControlMainWindow(parent=maya_main_window())

    #dialog.show()
    try:
        if dialog:
            delete()
    except:
        pass
    dialog = ControlMainWindow(parent=maya_main_window())
    dialog.show()

def delete():
    global dialog
    if dialog is None:
        return
    dialog.deleteLater()
    dialog = None
