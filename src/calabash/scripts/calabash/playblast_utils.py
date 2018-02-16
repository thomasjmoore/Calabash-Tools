'''
A set of utilities to aid in easy and consistent playblasts
'''

from maya import cmds
import pymel.core as pm
import pymel.core.uitypes as pmui
import os
from maya import mel
import maya.OpenMayaAnim as oma

# HUD Utils

def scene_name_hud():
    if cmds.headsUpDisplay("HUDSceneName", exists=True):
        cmds.headsUpDisplay("HUDSceneName", remove=True)
    proj = get_project()
    cmds.headsUpDisplay("HUDSceneName", section=5, block=1, blockSize="small", dfs="small", l=proj, command="cmds.file(q=True, sn=True, shn=True)")


def framecount_hud():
    if cmds.headsUpDisplay("HUDFrameCount", exists=True):
        cmds.headsUpDisplay("HUDFrameCount", remove=True)
    cmds.headsUpDisplay("HUDFrameCount", section=5, block=2, blockSize="small", dfs="large", l="frame", command="cmds.currentTime(q=True)", atr=True)


def custom_hud(text=""):
    if cmds.headsUpDisplay("HUDCustom", exists=True):
        cmds.headsUpDisplay("HUDCustom", remove=True)
    cmds.headsUpDisplay("HUDCustom", section=5, block=3, blockSize="small", dfs="large", label=text)

'''
def custom_hud_input():
    result = cmds.promptDialog(
        title='HUD Label',
        message='Enter Label:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')

    if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)
    else:
        text = ""
    return text
'''

def get_project():
    projpath = cmds.workspace(q=True, sn=True)
    proj =os.path.basename(projpath)
    return proj


def add_hud():
    scene_name_hud()
    framecount_hud()


def remove_hud():
    if cmds.headsUpDisplay("HUDSceneName", exists=True):
        cmds.headsUpDisplay("HUDSceneName", remove=True)

    if cmds.headsUpDisplay("HUDFrameCount", exists=True):
        cmds.headsUpDisplay("HUDFrameCount", remove=True)

    if cmds.headsUpDisplay("HUDCustom", exists=True):
        cmds.headsUpDisplay("HUDCustom", remove=True)


def make_playblast(filename="", green=False):
    #
    # Things to improve:
    # -restore settings after playblast
    # -turn off action/title safe
    # -better file name detection/stop if no name is detected
    #
    if not filename:
        filename = pb_filename()
    set_cameras()
    set_viewports(green)
    add_hud()

    if green:
        r, g, b = cmds.displayRGBColor("background", q=True)
        rt, gt, bt = cmds.displayRGBColor("backgroundTop", q=True)
        rb, gb, bb = cmds.displayRGBColor("backgroundBottom", q=True)

        cmds.displayRGBColor("background", 0, 1, 0)
        cmds.displayRGBColor("backgroundTop", 0, 1, 0)
        cmds.displayRGBColor("backgroundBottom", 0, 1, 0)
        greenname = splitname[0]+ ".green"
        splitname = (greenname, splitname[1])

        remove_hud()

    cmds.playblast(format = "qt",
                   filename=filename,
                   sequenceTime=False,
                   clearCache=True,
                   viewer=True,
                   showOrnaments=True,
                   offScreen=False,
                   compression = "H.264",
                   quality=100,
                   widthHeight=[1920,1080],
                   percent=100,
                   fo=True
                   )
    reset_viewports()

    if green:
        cmds.displayRGBColor("background", r, g, b)
        cmds.displayRGBColor("backgroundTop", rt, gt, bt)
        cmds.displayRGBColor("backgroundBottom", rb, gb, bb)

    remove_hud()
    return filename

def set_cameras():
    cams = pm.ls(type="camera")
    for cam in cams:
        cam.displayFilmGate.set(0)
        cam.displaySafeAction.set(0)
        cam.displaySafeTitle.set(0)


def set_viewports(green=False):
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

        if green:
            pmui.ModelEditor(modelPanel).setHeadsUpDisplay(False)



def clean_hud():
    hud_menu = pm.melGlobals['gHeadsUpDisplayMenu']
    menuitems = cmds.menu(hud_menu, q=True, itemArray=True)
    print menuitems


def reset_viewports():
    modelPanelList = []
    modelEditorList = pm.lsUI(editors=True)
    for myModelPanel in modelEditorList:
        if myModelPanel.find('modelPanel') != -1:
            modelPanelList.append(myModelPanel)

    for modelPanel in modelPanelList:
        pmui.ModelEditor(modelPanel).setAllObjects(True)
        #pmui.ModelEditor(modelPanel).setGrid(True)
        pmui.ModelEditor(modelPanel).setSelectionHiliteDisplay(True)


def pb_filename():
    mayafile = cmds.file(q=True, sn=True, shn=True)
    if not mayafile:
        mayafile = "untitled"
    splitname = os.path.splitext(mayafile)
    filename = "movies/%s" % splitname[0]
    return filename

def start_end():
    start = oma.MAnimControl.minTime().value()

    end = oma.MAnimControl.maxTime().value()
    return start, end


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
        filename = filename + ".green"
        #splitname = (greenname, splitname[1])

        remove_hud()

    cmds.playblast(format = "qt",
                   filename=filename,
                   sequenceTime=False,
                   clearCache=True,
                   viewer=True,
                   showOrnaments=True,
                   offScreen=False,
                   compression = "H.264",
                   quality=100,
                   widthHeight=[w,h],
                   st = start,
                   et = end,
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