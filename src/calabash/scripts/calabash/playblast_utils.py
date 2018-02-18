'''
A set of utilities to aid in easy and consistent playblasts
'''

from maya import cmds
import pymel.core as pm
import pymel.core.uitypes as pmui
import os
from maya import mel
import maya.OpenMayaAnim as oma


def clean_hud():
    hud_menu = pm.melGlobals['gHeadsUpDisplayMenu']
    menuitems = cmds.menu(hud_menu, q=True, itemArray=True)
    print menuitems



def playblast(filename="", green=False, h=960, w=540, start="", end="", clean_vp=True, hud=True, custom_hud_text=""):
    #
    # Things to improve:
    # -restore settings after playblast
    # -turn off action/title safe
    # -better file name detection/stop if no name is detected
    #
    if not filename:
        raise Exception("Filename not provided")

    if clean_vp:
        set_cameras()
        set_viewports(green)

    if hud:
        add_hud()
    print custom_hud_text
    if custom_hud_text:
        custom_hud(custom_hud_text)

    if green:
        r, g, b = cmds.displayRGBColor("background", q=True)
        rt, gt, bt = cmds.displayRGBColor("backgroundTop", q=True)
        rb, gb, bb = cmds.displayRGBColor("backgroundBottom", q=True)

        cmds.displayRGBColor("background", 0, 1, 0)
        cmds.displayRGBColor("backgroundTop", 0, 1, 0)
        cmds.displayRGBColor("backgroundBottom", 0, 1, 0)

        remove_hud()

    cmds.playblast(format = "qt",
                   filename=filename,
                   sequenceTime=False,
                   clearCache=True,
                   viewer=True,
                   showOrnaments=True,
                   offScreen=False,
                   compression="H.264",
                   quality=100,
                   widthHeight=[w,h],
                   st=start,
                   et=end,
                   percent=100,
                   fo=True
                   )

    if clean_vp:
        reset_viewports()

    if green:
        cmds.displayRGBColor("background", r, g, b)
        cmds.displayRGBColor("backgroundTop", rt, gt, bt)
        cmds.displayRGBColor("backgroundBottom", rb, gb, bb)

    remove_hud()
    return filename


class Playblaster(object):
    green = False
    clean_vp = True
    hud = True
    custom_hud_chk = False
    custom_hud_text = ""
    w = 960
    h = 540

    def __init__(self):
        self.proj = get_project()
        self.start, self.end = self.start_end()
        self.filename = self.pb_filename()
        # get viewport settings

        # make playblast

        # return viewport settings

    def scene_name_hud(self):
        if cmds.headsUpDisplay("HUDSceneName", exists=True):
            cmds.headsUpDisplay("HUDSceneName", remove=True)

        cmds.headsUpDisplay("HUDSceneName", section=5, block=1, blockSize="small", dfs="small", l=self.proj,
                            command="cmds.file(q=True, sn=True, shn=True)")

    @staticmethod
    def framecount_hud(self):
        if cmds.headsUpDisplay("HUDFrameCount", exists=True):
            cmds.headsUpDisplay("HUDFrameCount", remove=True)
        cmds.headsUpDisplay("HUDFrameCount", section=5, block=2, blockSize="small", dfs="large", l="frame",
                            command="cmds.currentTime(q=True)", atr=True)

    def custom_hud(self, text=""):
        if cmds.headsUpDisplay("HUDCustom", exists=True):
            cmds.headsUpDisplay("HUDCustom", remove=True)
        cmds.headsUpDisplay("HUDCustom", section=5, block=3, blockSize="small", dfs="large", label=text)

    @staticmethod
    def get_project(self):
        projpath = cmds.workspace(q=True, sn=True)
        proj = os.path.basename(projpath)
        return proj

    def add_hud(self):
        scene_name_hud()
        framecount_hud()

    def remove_hud(self):
        if cmds.headsUpDisplay("HUDSceneName", exists=True):
            cmds.headsUpDisplay("HUDSceneName", remove=True)

        if cmds.headsUpDisplay("HUDFrameCount", exists=True):
            cmds.headsUpDisplay("HUDFrameCount", remove=True)

        if cmds.headsUpDisplay("HUDCustom", exists=True):
            cmds.headsUpDisplay("HUDCustom", remove=True)

    def reset_viewports(self):
        modelPanelList = []
        modelEditorList = pm.lsUI(editors=True)
        for myModelPanel in modelEditorList:
            if myModelPanel.find('modelPanel') != -1:
                modelPanelList.append(myModelPanel)

        for modelPanel in modelPanelList:
            pmui.ModelEditor(modelPanel).setAllObjects(True)
            # pmui.ModelEditor(modelPanel).setGrid(True)
            pmui.ModelEditor(modelPanel).setSelectionHiliteDisplay(True)

    def set_cameras(self):
        cams = pm.ls(type="camera")
        for cam in cams:
            cam.displayFilmGate.set(0)
            cam.displaySafeAction.set(0)
            cam.displaySafeTitle.set(0)

    def set_viewports(self):
        hrg = pm.PyNode("hardwareRenderingGlobals")
        hrg.multiSampleEnable.set(1)

        modelPanelList = []
        modelEditorList = pm.lsUI(editors=True)
        for myModelPanel in modelEditorList:
            if myModelPanel.find('modelPanel') != -1:
                modelPanelList.append(myModelPanel)

        for modelPanel in modelPanelList:
            pmui.ModelEditor(modelPanel).setAllObjects(False)
            pmui.ModelEditor(modelPanel).setNurbsSurfaces(True)
            pmui.ModelEditor(modelPanel).setPolymeshes(True)
            pmui.ModelEditor(modelPanel).setControlVertices(False)
            pmui.ModelEditor(modelPanel).setGrid(False)
            pmui.ModelEditor(modelPanel).setSelectionHiliteDisplay(False)

            if self.green:
                pmui.ModelEditor(modelPanel).setHeadsUpDisplay(False)
            else:
                pmui.ModelEditor(modelPanel).setHeadsUpDisplay(True)

    def pb_filename(self):
        mayafile = cmds.file(q=True, sn=True, shn=True)
        if not mayafile:
            mayafile = "untitled"
        splitname = os.path.splitext(mayafile)
        filename = "movies/%s" % splitname[0]
        if self.green:
            filename = filename + ".green"
        filename = filename + ".mov"
        return filename

    def start_end(self):
        self.start = int(oma.MAnimControl.minTime().value())
        self.end = int(oma.MAnimControl.maxTime().value())
        return self.start, self.end

    def playblast(self):
        #
        # Things to improve:
        # -restore viewport and camera settings after playblast
        # -better file name detection/stop if no name is detected
        # -make green alter current filename, not overwrite
        # -save name to option var
        # -add resolution presets dropdown, 960, HD, render globals, custom


        if self.clean_vp or self.green:
            self.set_cameras()
            self.set_viewports()

        if self.hud:
            self.add_hud()

        if self.custom_hud_chk and self.hud:
            self.custom_hud(self.custom_hud_text)

        if self.green:
            r, g, b = cmds.displayRGBColor("background", q=True)
            rt, gt, bt = cmds.displayRGBColor("backgroundTop", q=True)
            rb, gb, bb = cmds.displayRGBColor("backgroundBottom", q=True)

            cmds.displayRGBColor("background", 0, 1, 0)
            cmds.displayRGBColor("backgroundTop", 0, 1, 0)
            cmds.displayRGBColor("backgroundBottom", 0, 1, 0)

            self.remove_hud()

        cmds.playblast(format="qt",
                       filename=self.filename,
                       sequenceTime=False,
                       clearCache=True,
                       viewer=True,
                       showOrnaments=True,
                       offScreen=False,
                       compression="H.264",
                       quality=100,
                       widthHeight=[self.w, self.h],
                       st=self.start,
                       et=self.end,
                       percent=100,
                       fo=True
                       )

        if self.clean_vp:
            self.reset_viewports()

        if self.green:
            cmds.displayRGBColor("background", r, g, b)
            cmds.displayRGBColor("backgroundTop", rt, gt, bt)
            cmds.displayRGBColor("backgroundBottom", rb, gb, bb)

        remove_hud()
        return self.filename