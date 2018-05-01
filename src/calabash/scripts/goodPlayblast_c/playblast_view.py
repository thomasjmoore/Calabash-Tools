from Qt import QtCore, QtGui, QtWidgets
import goodPlayblast_ui as customUI
from . import playblast_utils
from maya import cmds
import pymel.core as pm
import os

try:
    from shiboken import wrapInstance
except:
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

reload(playblast_utils)
reload(customUI)

__all__ = [
    'launch',
    ]

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class ControlMainWindow(QtWidgets.QDialog):
    version = "2.0"

    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.playblaster = playblast_utils.Playblaster()
        self.setWindowFlags(QtCore.Qt.Tool)
        self.ui = customUI.Ui_playblast_dlg()
        self.ui.setupUi(self)

        #
        # Setup GUI values
        bold = "font-weight:bold; color:#DDDDDD"
        title = self.ui.title_lbl.text()
        self.ui.title_lbl.setStyleSheet(bold)
        self.ui.title_lbl.setText("%s V%s --" % (title, self.version))
        self.format_list()

        # DISPLAY
        self.ui.viewportOverride_chk.setChecked(self.playblaster.override_vp)
        self.ui.overrideviewport_lbl.setStyleSheet(bold)
        self.ui.onlyPolygons_chk.setChecked(self.playblaster.only_polygons)
        self.ui.gates_chk.setChecked(self.playblaster.gates)
        self.ui.bgcolor_chk.setChecked(self.playblaster.green)
        self.set_button_color()

        # HUD
        self.ui.hudOverride_chk.setChecked(self.playblaster.override_hud)
        self.ui.overridehud_lbl.setStyleSheet(bold)
        self.ui.displayhud_chk.setChecked(self.playblaster.display_hud)
        self.ui.hud_chk.setChecked(self.playblaster.hud) # project
        self.ui.frameHud_chk.setChecked(self.playblaster.hud_frame_chk)
        self.ui.scenehud_chk.setChecked(self.playblaster.scene_hud)
        self.ui.camerahud_chk.setChecked(self.playblaster.camera_hud)
        self.ui.cstmHud_chk.setChecked(self.playblaster.custom_hud_chk)

        # FORMAT

        findex = self.ui.encoding_cmb.findText(self.playblaster.pb_format[1], QtCore.Qt.MatchFixedString)
        if findex >= 0:
            self.ui.encoding_cmb.setCurrentIndex(findex)
        self.format()
        self.ui.quality_sld.setMinimum(0)
        self.ui.quality_sld.setMaximum(100)
        self.ui.scale_sld.setMinimum(0)
        self.ui.scale_sld.setMaximum(100)
        self.ui.quality_le.setText(str(self.playblaster.quality))
        self.ui.scale_le.setText(str(self.playblaster.scale))
        self.ui.start_le.setText(str(self.playblaster.start))
        self.ui.end_le.setText(str(self.playblaster.end))
        self.ui.width_le.setText(str(self.playblaster.w))
        self.ui.height_le.setText(str(self.playblaster.h))
        self.ui.customresolution_chk.setChecked(self.playblaster.custom_resolution)

        # SAVE
        self.ui.view_chk.setChecked(self.playblaster.view)
        self.ui.overwrite_chk.setChecked(self.playblaster.overwrite)
        self.ui.offscreen_chk.setChecked(self.playblaster.offscreen)
        self.ui.filename_le.setText(self.playblaster.filename)
        self.ui.usescenename_chk.setChecked(self.playblaster.usescenename_chk)
        self.ui.saveDir_le.setText(self.playblaster.save_directory)
        self.filename()
        self.filename_preview()
        self.use_scenename_chk()

        #
        # Connect UI
        # DISPLAY
        self.ui.viewportOverride_chk.clicked.connect(self.override_vp)
        self.ui.onlyPolygons_chk.clicked.connect(self.only_polygons)
        self.ui.gates_chk.clicked.connect(self.gates)
        self.ui.bgcolor_chk.clicked.connect(self.green)
        self.ui.color_btn.clicked.connect(self.set_color)

        # HUD
        self.ui.hudOverride_chk.clicked.connect(self.override_scene_hud)
        self.ui.displayhud_chk.clicked.connect(self.displayhud)
        self.ui.hud_chk.clicked.connect(self.hud)
        self.ui.scenehud_chk.clicked.connect(self.scenehud)
        self.ui.frameHud_chk.clicked.connect(self.frameHud)
        self.ui.camerahud_chk.clicked.connect(self.camerahud)
        self.ui.cstmHud_chk.clicked.connect(self.custom_hud)
        self.ui.cstmHud_le.textChanged.connect(self.custom_hud_text)
        self.displayhud()

        # FORMAT
        self.ui.format_cmb.currentIndexChanged.connect(self.format)
        self.ui.encoding_cmb.currentIndexChanged.connect(self.encoding)
        self.ui.quality_sld.valueChanged.connect(self.quality_slider)
        self.ui.quality_le.textChanged.connect(self.quality_lineedit)
        self.ui.scale_sld.valueChanged.connect(self.scale_slider)
        self.ui.scale_le.textChanged.connect(self.scale_lineedit)
        self.quality_lineedit()
        self.scale_lineedit()
        self.ui.customresolution_chk.clicked.connect(self.renderresolution)
        self.renderresolution()
        self.ui.width_le.textChanged.connect(self.width)
        self.ui.height_le.textChanged.connect(self.height)
        self.ui.start_le.textChanged.connect(self.start)
        self.ui.end_le.textChanged.connect(self.end)
        self.ui.loadRenderFrameRange_btn.clicked.connect(self.load_renderFrameRange)
        self.ui.offscreen_chk.clicked.connect(self.offscreen)

        # SAVING
        self.ui.view_chk.clicked.connect(self.view)
        self.ui.filename_le.textChanged.connect(self.filename)
        self.ui.overwrite_chk.clicked.connect(self.overwrite)
        self.ui.browse_btn.clicked.connect(self.browse)
        self.ui.saveDir_le.textChanged.connect(self.filename_preview)
        self.ui.filename_le.textChanged.connect(self.filename_preview)
        self.ui.usescenename_chk.clicked.connect(self.use_scenename_chk)

        self.ui.playblast_btn.clicked.connect(self.playblast)
        self.ui.save_btn.clicked.connect(self.save_settings)
        self.ui.reset_btn.clicked.connect(self.reset)


        self.get_custom_hud_text()

        # STYLING

        button_style = "background-color:#3A6C4E"
        self.ui.playblast_btn.setStyleSheet(button_style)
        #self.ui.reset_btn.setStyleSheet(button_style)

    def playblast(self):
        self.save_settings()
        self.playblaster.playblast()

    # DISPLAY
    def override_vp(self):
        isChecked = self.ui.viewportOverride_chk.checkState()
        if isChecked:
            self.playblaster.override_vp = True
            self.ui.onlyPolygons_chk.setEnabled(True)
            self.ui.onlyPolygons_lbl.setEnabled(True)
            self.ui.gates_chk.setEnabled(True)
            self.ui.gates_lbl.setEnabled(True)
            #self.ui.ornaments_chk.setEnabled(True)
            #self.ui.ornaments_lbl.setEnabled(True)
            self.ui.bgcolor_chk.setEnabled(True)
            self.ui.bgcolor_lbl.setEnabled(True)
            self.ui.color_btn.setEnabled(True)
        else:
            self.playblaster.override_vp = False
            self.ui.onlyPolygons_chk.setEnabled(False)
            self.ui.onlyPolygons_lbl.setEnabled(False)
            self.ui.gates_chk.setEnabled(False)
            self.ui.gates_lbl.setEnabled(False)
            #self.ui.ornaments_chk.setEnabled(False)
            #self.ui.ornaments_lbl.setEnabled(False)
            self.ui.bgcolor_chk.setEnabled(False)
            self.ui.bgcolor_lbl.setEnabled(False)
            self.ui.color_btn.setEnabled(False)

    def only_polygons(self):
        self.playblaster.only_polygons = self.ui.onlyPolygons_chk.checkState()

    def gates(self):
        isChecked = self.ui.gates_chk.checkState()
        if isChecked:
            self.playblaster.gates = True
        else:
            self.playblaster.gates = False

    def green(self):
        self.playblaster.green = self.ui.bgcolor_chk.checkState()

    def set_button_color(self, color=None):
        # This function sets the color on the color picker button

        if not color:
            color = self.playblaster.default_color
        else:
            self.playblaster.default_color = color

        assert len(color) == 3, "You must provide a list of 3 colors"

        # Qt expects it in integer values from 0 to 255
        r, g, b = [c * 255 for c in color]

        self.ui.color_btn.setStyleSheet('background-color: rgba(%s, %s, %s, 1.0);' % (r, g, b))

    def set_color(self):

        color = self.playblaster.default_color

        # Then we provide this to the maya's color editor which gives us back the color the user specified
        new_color = pm.colorEditor(rgbValue=color)

        # Annoyingly, it gives us back a string instead of a list of numbers.
        # So we split the string, and then convert it to floats
        r, g, b, a = [float(c) for c in new_color.split()]

        # We then use the r,g,b to set the colors on the light and the button
        if a:
            color = (r, g, b)

        self.set_button_color(color)

    # HUD

    def override_scene_hud(self):
        is_checked = self.ui.hudOverride_chk.checkState()
        self.playblaster.override_hud = self.ui.hudOverride_chk.checkState()
        if is_checked:
            self.ui.displayhud_chk.setEnabled(True)
            self.ui.displayhud_lbl.setEnabled(True)
            self.ui.hud_chk.setEnabled(True)
            self.ui.sceneinfohud_chk.setEnabled(True)
            self.ui.namehud_lbl.setEnabled(True)
            self.ui.scenehud_chk.setEnabled(True)
            self.ui.frameHud_chk.setEnabled(True)
            self.ui.camerahud_chk.setEnabled(True)
            self.ui.cstmHud_chk.setEnabled(True)
            self.ui.cstmHud_le.setEnabled(True)
        else:
            self.ui.displayhud_chk.setEnabled(False)
            self.ui.displayhud_lbl.setEnabled(False)
            self.ui.hud_chk.setEnabled(False)
            self.ui.sceneinfohud_chk.setEnabled(False)
            self.ui.namehud_lbl.setEnabled(False)
            self.ui.scenehud_chk.setEnabled(False)
            self.ui.frameHud_chk.setEnabled(False)
            self.ui.camerahud_chk.setEnabled(False)
            self.ui.cstmHud_chk.setEnabled(False)
            self.ui.cstmHud_le.setEnabled(False)

    def displayhud(self):
        self.playblaster.display_hud = self.ui.displayhud_chk.checkState()
        is_checked = self.ui.displayhud_chk.checkState()

        if is_checked:
            self.ui.hud_chk.setEnabled(True)
            self.ui.sceneinfohud_chk.setEnabled(True)
            self.ui.namehud_lbl.setEnabled(True)
            self.ui.scenehud_chk.setEnabled(True)
            self.ui.frameHud_chk.setEnabled(True)
            self.ui.camerahud_chk.setEnabled(True)
            self.ui.cstmHud_chk.setEnabled(True)
            self.ui.cstmHud_le.setEnabled(True)
        else:
            self.ui.hud_chk.setEnabled(False)
            self.ui.sceneinfohud_chk.setEnabled(False)
            self.ui.namehud_lbl.setEnabled(False)
            self.ui.scenehud_chk.setEnabled(False)
            self.ui.frameHud_chk.setEnabled(False)
            self.ui.camerahud_chk.setEnabled(False)
            self.ui.cstmHud_chk.setEnabled(False)
            self.ui.cstmHud_le.setEnabled(False)


    def hud(self):
        self.playblaster.hud = self.ui.hud_chk.checkState()

    def scenehud(self):
        self.playblaster.scene_hud = self.ui.scenehud_chk.checkState()

    def camerahud(self):
        self.playblaster.camera_hud = self.ui.camerahud_chk.checkState()

    def frameHud(self):
        self.playblaster.hud_frame_chk = self.ui.frameHud_chk.checkState()

    def custom_hud(self):
        self.playblaster.custom_hud_chk = self.ui.cstmHud_chk.checkState()

    def get_custom_hud_text(self):
        if cmds.optionVar(exists="gp_username_le"):
            self.playblaster.custom_hud_text = cmds.optionVar(q="gp_username_le")
        self.ui.cstmHud_le.setText(self.playblaster.custom_hud_text)

    def custom_hud_text(self):
        self.playblaster.custom_hud_text = self.ui.cstmHud_le.text()

    # FORMAT

    def format_list(self):
        formats = cmds.playblast(q=True, format=True)
        for format in formats:
            self.ui.format_cmb.addItem(format)


    def format(self):
        self.playblaster.pb_format[0] = self.ui.format_cmb.currentIndex()
        self.playblaster.pb_format[1] = self.ui.format_cmb.currentText()

        self.encoding_list()

    def encoding_list(self):
        self.ui.encoding_cmb.clear()
        format = self.playblaster.pb_format

        encodings = pm.mel.eval('playblast -format "{0}" -q -compression;'.format(format[1]))

        for encoding in encodings:
            self.ui.encoding_cmb.addItem(encoding)
        if cmds.optionVar(exists="gp_encoding_cmb"):
            encoding_pref = cmds.optionVar(q="gp_encoding_cmb")
        else:
            encoding_pref = ""
        index = 0
        if format[1] == "qt":
            if encoding_pref:
                index = self.ui.encoding_cmb.findText(encoding_pref, QtCore.Qt.MatchFixedString)
            if index <= 0:
                index = self.ui.encoding_cmb.findText("H.264", QtCore.Qt.MatchFixedString)

            if index >= 0:
                self.ui.encoding_cmb.setCurrentIndex(index)

        if format[1] == "avi":
            if encoding_pref:
                index = self.ui.encoding_cmb.findText(encoding_pref, QtCore.Qt.MatchFixedString)
            if index <= 0:
                index = self.ui.encoding_cmb.findText("None", QtCore.Qt.MatchFixedString)

            if index >= 0:
                self.ui.encoding_cmb.setCurrentIndex(index)

        if format[1] == "image":
            if encoding_pref:
                index = self.ui.encoding_cmb.findText(encoding_pref, QtCore.Qt.MatchFixedString)
            if index <= 0:
                index = self.ui.encoding_cmb.findText("PNG", QtCore.Qt.MatchFixedString)

            if index >= 0:
                self.ui.encoding_cmb.setCurrentIndex(index)
        self.filename_preview()

    def encoding(self):
        self.playblaster.encoding = self.ui.encoding_cmb.currentText()

    def quality_slider(self):
        self.ui.quality_le.setText(str(self.ui.quality_sld.value()))

    def scale_slider(self):
        scale = self.ui.scale_sld.value() / 100.0
        self.ui.scale_le.setText(str(scale))

    def quality_lineedit(self):
        text = self.ui.quality_le.text()
        if text.isnumeric():
            self.ui.quality_sld.setValue(int(text))
            self.playblaster.quality = self.ui.quality_sld.value()

    def scale_lineedit(self):
        text = self.ui.scale_le.text()
        try:
            float(text)
        except ValueError:
            return False

        value = float(text) * 100
        self.ui.scale_sld.setValue(value)
        self.playblaster.scale = (self.ui.scale_sld.value())

    def renderresolution(self):
        if self.ui.customresolution_chk.isChecked():
            self.ui.width_le.setEnabled(True)
            self.ui.height_le.setEnabled(True)
            self.height()
            self.width()

        else:
            self.ui.width_le.setEnabled(False)
            self.ui.height_le.setEnabled(False)
            self.playblaster.w = int(self.playblaster.render_resolution()[0])
            self.playblaster.h = int(self.playblaster.render_resolution()[1])


    def load_renderResolution(self):
        pass
        w, h = self.playblaster.render_resolution()
        self.ui.width_le.setText(w)
        self.ui.height_le.setText(h)
        return w, h

    def load_renderFrameRange(self):
        s, e = self.playblaster.render_frameRange()
        self.ui.start_le.setText(s)
        self.ui.end_le.setText(e)

    def height(self):
        self.playblaster.h = int(self.ui.height_le.text())

    def width(self):
        self.playblaster.w = int(self.ui.width_le.text())

    def start(self):
        self.playblaster.start = int(self.ui.start_le.text())

    def end(self):
        self.playblaster.end = int(self.ui.end_le.text())

    def offscreen(self):
        isChecked = self.ui.offscreen_chk.checkState()
        if isChecked:
            self.playblaster.offscreen = True
        else:
            self.playblaster.offscreen = False

    # SAVING
    def filename(self):
        filetype = "mov"
        savedir = self.ui.saveDir_le.text()
        #self.playblaster.save_directory = savedir


        if not self.ui.usescenename_chk.isChecked():
            savefile = self.ui.filename_le.text()
        else:
            savefile = cmds.file(q=True, sn=True, shn=True)
            savefile = os.path.splitext(savefile)[0]

            if not savefile:
                savefile = "untitled"
        #combined = os.path.join("%s.%s" % (savefile))
        self.playblaster.filename = savefile

    def view(self):
        self.playblaster.view = self.ui.view_chk.isChecked()

    def overwrite(self):
        self.playblaster.overwrite = self.ui.overwrite_chk.checkState()

    def browse(self):
        curpath = self.ui.saveDir_le.text()
        path = cmds.fileDialog2(fileMode=3, okc="Select", dir=curpath)
        self.ui.saveDir_le.setText(path[0])

    def filename_preview(self):
        savedir = self.ui.saveDir_le.text()
        if savedir:
            self.playblaster.save_directory = savedir

        if self.playblaster.pb_format[1] == "qt":
            filetype = "mov"
        elif self.playblaster.pb_format[1] =="avi":
            filetype = "avi"
        else:
            filetype = "ext"

        dir = self.ui.saveDir_le.text()
        if not self.ui.usescenename_chk.isChecked():
            savefile = self.ui.filename_le.text()
        else:
            savefile = cmds.file(q=True, sn=True, shn=True)
            savefile = os.path.splitext(savefile)[0]
            if not savefile:
                savefile = "untitled"

        combined = os.path.join(dir, savefile).replace("\\","/")
        if len(combined) > 25:
            combined = "...%s.%s" % (combined[-55:], filetype)
        self.ui.filenamepreview_lbl.setText(combined)

    def reset(self):
        cmds.optionVar(remove="gp_overrideviewport_chk")
        cmds.optionVar(remove="gp_onlypolygons_chk")
        cmds.optionVar(remove="gp_gates_chk")
        cmds.optionVar(remove="gp_bgcolor_chk")
        cmds.optionVar(remove="gp_bgcolorR")
        cmds.optionVar(remove="gp_bgcolorG")
        cmds.optionVar(remove="gp_bgcolorB")

        cmds.optionVar(remove="gp_overridehud_chk")
        cmds.optionVar(remove="gp_displayhud_chk")
        cmds.optionVar(remove="gp_projecthud_chk")
        cmds.optionVar(remove="gp_frameHud_chk")
        cmds.optionVar(remove="gp_camerahud_chk")
        cmds.optionVar(remove="gp_scenehud_chk")
        cmds.optionVar(remove="gp_username_le")
        cmds.optionVar(remove="gp_username_chk")

        cmds.optionVar(remove="gp_format_ind")
        cmds.optionVar(remove="gp_format_cmb")
        cmds.optionVar(remove="gp_encoding_cmb")
        cmds.optionVar(remove="gp_quality_le")
        cmds.optionVar(remove="gp_customresolution_chk")
        cmds.optionVar(remove="gp_height_le")
        cmds.optionVar(remove="gp_width_le")
        cmds.optionVar(remove="gp_scale_le")

        cmds.optionVar(remove="gp_offscreen_chk")
        cmds.optionVar(remove="gp_view_chk")
        cmds.optionVar(remove="gp_overwrite_chk")
        cmds.optionVar(remove="gp_usescenename_chk")
        cmds.optionVar(remove="gp_scenename_le")
        cmds.optionVar(remove="gp_savedir_le")

        launch()

    def save_settings(self):
        cmds.optionVar(iv=("gp_overrideviewport_chk", self.ui.viewportOverride_chk.isChecked()))
        cmds.optionVar(iv=("gp_onlypolygons_chk", self.ui.onlyPolygons_chk.isChecked()))
        cmds.optionVar(iv=("gp_gates_chk", self.ui.gates_chk.isChecked()))
        cmds.optionVar(iv=("gp_bgcolor_chk", self.ui.bgcolor_chk.isChecked()))
        cmds.optionVar(fv=("gp_bgcolorR", self.playblaster.default_color[0]))
        cmds.optionVar(fv=("gp_bgcolorG", self.playblaster.default_color[1]))
        cmds.optionVar(fv=("gp_bgcolorB", self.playblaster.default_color[2]))

        cmds.optionVar(iv=("gp_overridehud_chk", self.ui.hudOverride_chk.isChecked()))
        cmds.optionVar(iv=("gp_displayhud_chk", self.ui.displayhud_chk.isChecked()))
        cmds.optionVar(iv=("gp_projecthud_chk", self.ui.hud_chk.isChecked()))
        cmds.optionVar(iv=("gp_frameHud_chk", self.ui.frameHud_chk.isChecked()))
        cmds.optionVar(iv=("gp_camerahud_chk", self.ui.camerahud_chk.isChecked()))
        cmds.optionVar(iv=("gp_scenehud_chk", self.ui.scenehud_chk.isChecked()))
        cmds.optionVar(sv=("gp_username_le", self.ui.cstmHud_le.text()))
        cmds.optionVar(iv=("gp_username_chk", self.ui.cstmHud_chk.isChecked()))

        cmds.optionVar(sv=("gp_format_cmb", self.ui.format_cmb.currentText()))
        cmds.optionVar(iv=("gp_format_ind", self.ui.format_cmb.currentIndex()))
        cmds.optionVar(sv=("gp_encoding_cmb", self.ui.encoding_cmb.currentText()))
        cmds.optionVar(iv=("gp_quality_le", int(self.ui.quality_le.text())))
        cmds.optionVar(iv=("gp_customresolution_chk", self.ui.customresolution_chk.isChecked()))
        cmds.optionVar(iv=("gp_height_le", int(self.ui.height_le.text())))
        cmds.optionVar(iv=("gp_width_le", int(self.ui.width_le.text())))
        cmds.optionVar(fv=("gp_scale_le", float(self.ui.scale_sld.value())))

        cmds.optionVar(iv=("gp_offscreen_chk", self.ui.offscreen_chk.isChecked()))
        cmds.optionVar(iv=("gp_view_chk", self.ui.view_chk.isChecked()))
        cmds.optionVar(iv=("gp_overwrite_chk", self.ui.overwrite_chk.isChecked()))
        cmds.optionVar(iv=("gp_usescenename_chk", self.ui.usescenename_chk.isChecked()))
        cmds.optionVar(sv=("gp_scenename_le", self.ui.filename_le.text()))
        cmds.optionVar(sv=("gp_savedir_le", self.ui.saveDir_le.text()))

    def use_scenename_chk(self):
        self.filename_preview()
        self.filename()
        if self.ui.usescenename_chk.isChecked():
            self.ui.filename_le.setEnabled(False)
        else:
            self.ui.filename_le.setEnabled(True)
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

