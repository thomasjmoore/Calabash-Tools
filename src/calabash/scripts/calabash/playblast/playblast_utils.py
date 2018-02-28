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


class Playblaster(object):
    green = False
    clean_vp = True
    hud = True
    custom_hud_chk = False
    custom_hud_text = ""
    w = 960
    h = 540
    modelPanel = ""
    default_color = [0,1,0]
    overwrite = True
    editname = False


    # viewportSettings


    def __init__(self):
        self.proj = self.get_project()
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

    def framecount_hud(self):
        if cmds.headsUpDisplay("HUDFrameCount", exists=True):
            cmds.headsUpDisplay("HUDFrameCount", remove=True)
        cmds.headsUpDisplay("HUDFrameCount", section=5, block=2, blockSize="small", dfs="large", l="frame",
                            command="cmds.currentTime(q=True)", atr=True)

    def custom_hud(self, text=""):
        if cmds.headsUpDisplay("HUDCustom", exists=True):
            cmds.headsUpDisplay("HUDCustom", remove=True)
        cmds.headsUpDisplay("HUDCustom", section=5, block=3, blockSize="small", dfs="large", label=text)

    def get_project(self):
        projpath = cmds.workspace(q=True, sn=True)
        proj = os.path.basename(projpath)
        return proj

    def add_hud(self):
        self.scene_name_hud()
        self.framecount_hud()

    def remove_hud(self):
        if cmds.headsUpDisplay("HUDSceneName", exists=True):
            cmds.headsUpDisplay("HUDSceneName", remove=True)

        if cmds.headsUpDisplay("HUDFrameCount", exists=True):
            cmds.headsUpDisplay("HUDFrameCount", remove=True)

        if cmds.headsUpDisplay("HUDCustom", exists=True):
            cmds.headsUpDisplay("HUDCustom", remove=True)

    def get_active_viewport(self):
        active_panel = pmui.ModelEditor(pm.getPanel(withFocus=True))
        model_editor_list = pm.lsUI(editors=True)

        for myModelPanel in model_editor_list:
            if myModelPanel.find(active_panel) != -1:
                model_editor = myModelPanel

        if pm.getPanel(to=active_panel) == "modelPanel":
            self.modelPanel = model_editor
            return model_editor
        else:
            self.modelPanel = ""
            pm.displayWarning("No viewport active.")
            return None

    def reset_viewports(self):
        pmui.ModelEditor(self.modelPanel).setNurbsCurves(self.vp_curves)
        pmui.ModelEditor(self.modelPanel).setNurbsSurfaces(self.vp_nurbs)
        pmui.ModelEditor(self.modelPanel).setControlVertices(self.vp_cvs)
        pmui.ModelEditor(self.modelPanel).setHulls(self.vp_hulls)
        pmui.ModelEditor(self.modelPanel).setPolymeshes(self.vp_polys)
        pmui.ModelEditor(self.modelPanel).setSubdivSurfaces(self.vp_subdivs)
        pmui.ModelEditor(self.modelPanel).setPlanes(self.vp_planes)
        pmui.ModelEditor(self.modelPanel).setLights(self.vp_lights)
        pmui.ModelEditor(self.modelPanel).setCameras(self.vp_cameras)
        pmui.ModelEditor(self.modelPanel).setImagePlane(self.vp_imageplanes)
        pmui.ModelEditor(self.modelPanel).setJoints(self.vp_joints)
        pmui.ModelEditor(self.modelPanel).setIkHandles(self.vp_iks)
        pmui.ModelEditor(self.modelPanel).setDeformers(self.vp_deformers)
        pmui.ModelEditor(self.modelPanel).setDynamics(self.vp_dynamics)
        cmds.modelEditor(self.modelPanel, particleInstancers=self.vp_instancers, e=True)
        pmui.ModelEditor(self.modelPanel).setFluids(self.vp_fluids)
        pmui.ModelEditor(self.modelPanel).setHairSystems(self.vp_hair)
        pmui.ModelEditor(self.modelPanel).setFollicles(self.vp_follicles)
        pmui.ModelEditor(self.modelPanel).setNCloths(self.vp_nCloths)
        pmui.ModelEditor(self.modelPanel).setNParticles(self.vp_nParticles)
        pmui.ModelEditor(self.modelPanel).setNRigids(self.vp_nRigids)
        pmui.ModelEditor(self.modelPanel).setDynamicConstraints(self.vp_dynconstraints)
        pmui.ModelEditor(self.modelPanel).setLocators(self.vp_locators)
        pmui.ModelEditor(self.modelPanel).setDimensions(self.vp_dimensions)
        pmui.ModelEditor(self.modelPanel).setPivots(self.vp_pivots)
        pmui.ModelEditor(self.modelPanel).setHandles(self.vp_handles)
        pmui.ModelEditor(self.modelPanel).setTextures(self.vp_textureplacements)
        pmui.ModelEditor(self.modelPanel).setStrokes(self.vp_strokes)
        pmui.ModelEditor(self.modelPanel).setMotionTrails(self.vp_motiontrails)
        #pmui.ModelEditor(self.modelPanel).pluginShapes(self.vp_pluginshapes)
        cmds.modelEditor(self.modelPanel, clipGhosts=self.vp_clipghosts, e=True)
        cmds.modelEditor(self.modelPanel, greasePencils=self.vp_greasepencil, e=True)
        #self.vp_gpucache = cmds.modelEditor(self.modelPanel, queryPluginObjects="gpuCacheDisplayFilter", q=True)

        pmui.ModelEditor(self.modelPanel).setManipulators(self.vp_manipulators)
        pmui.ModelEditor(self.modelPanel).setGrid(self.vp_grid)
        pmui.ModelEditor(self.modelPanel).setHeadsUpDisplay(self.vp_hud)
        cmds.modelEditor(self.modelPanel, hos=self.vp_holdouts, e=True)
        pmui.ModelEditor(self.modelPanel).setSelectionHiliteDisplay(self.vp_selectionhighlighting)


    def set_cameras(self):
        cams = pm.ls(type="camera")
        for cam in cams:
            cam.displayFilmGate.set(0)
            cam.displaySafeAction.set(0)
            cam.displaySafeTitle.set(0)

    def set_viewports(self):

        hrg = pm.PyNode("hardwareRenderingGlobals")
        hrg.multiSampleEnable.set(1)

        pmui.ModelEditor(self.modelPanel).setNurbsCurves(False)
        pmui.ModelEditor(self.modelPanel).setNurbsSurfaces(False)
        pmui.ModelEditor(self.modelPanel).setControlVertices(False)
        pmui.ModelEditor(self.modelPanel).setHulls(False)
        pmui.ModelEditor(self.modelPanel).setPolymeshes(True)
        pmui.ModelEditor(self.modelPanel).setSubdivSurfaces(False)
        pmui.ModelEditor(self.modelPanel).setPlanes(False)
        pmui.ModelEditor(self.modelPanel).setLights(False)
        pmui.ModelEditor(self.modelPanel).setCameras(False)
        pmui.ModelEditor(self.modelPanel).setImagePlane(False)
        pmui.ModelEditor(self.modelPanel).setJoints(False)
        pmui.ModelEditor(self.modelPanel).setIkHandles(False)
        pmui.ModelEditor(self.modelPanel).setDeformers(False)
        pmui.ModelEditor(self.modelPanel).setDynamics(False)
        cmds.modelEditor(self.modelPanel, particleInstancers=False, e=True)
        pmui.ModelEditor(self.modelPanel).setFluids(False)
        pmui.ModelEditor(self.modelPanel).setHairSystems(False)
        pmui.ModelEditor(self.modelPanel).setFollicles(False)
        pmui.ModelEditor(self.modelPanel).setNCloths(False)
        pmui.ModelEditor(self.modelPanel).setNParticles(False)
        pmui.ModelEditor(self.modelPanel).setNRigids(False)
        pmui.ModelEditor(self.modelPanel).setDynamicConstraints(False)
        pmui.ModelEditor(self.modelPanel).setLocators(False)
        pmui.ModelEditor(self.modelPanel).setDimensions(False)
        pmui.ModelEditor(self.modelPanel).setPivots(False)
        pmui.ModelEditor(self.modelPanel).setHandles(False)
        pmui.ModelEditor(self.modelPanel).setTextures(False)
        pmui.ModelEditor(self.modelPanel).setStrokes(False)
        pmui.ModelEditor(self.modelPanel).setMotionTrails(False)
        #pmui.ModelEditor(self.modelPanel).pluginShapes(False)
        cmds.modelEditor(self.modelPanel, clipGhosts=False, e=True)
        cmds.modelEditor(self.modelPanel, greasePencils=False, e=True)
        #self.vp_gpucache = cmds.modelEditor(self.modelPanel, queryPluginObjects="gpuCacheDisplayFilter", q=True)

        pmui.ModelEditor(self.modelPanel).setManipulators(False)
        pmui.ModelEditor(self.modelPanel).setGrid(False)
        pmui.ModelEditor(self.modelPanel).setHeadsUpDisplay(not self.green)
        cmds.modelEditor(self.modelPanel, hos=False, e=True)
        pmui.ModelEditor(self.modelPanel).setSelectionHiliteDisplay(False)

        #if self.green:
        #    pmui.ModelEditor(self.modelPanel).setHeadsUpDisplay(False)
        #else:
        #    pmui.ModelEditor(self.modelPanel).setHeadsUpDisplay(True)

    def get_veiwport_settings(self):
        self.vp_curves = pmui.ModelEditor(self.modelPanel).getNurbsCurves()
        self.vp_nurbs = pmui.ModelEditor(self.modelPanel).getNurbsSurfaces()
        self.vp_cvs = pmui.ModelEditor(self.modelPanel).getControlVertices()
        self.vp_hulls = pmui.ModelEditor(self.modelPanel).getHulls()
        self.vp_polys = pmui.ModelEditor(self.modelPanel).getPolymeshes()
        self.vp_subdivs = pmui.ModelEditor(self.modelPanel).getSubdivSurfaces()
        self.vp_planes = pmui.ModelEditor(self.modelPanel).getPlanes()
        self.vp_lights = pmui.ModelEditor(self.modelPanel).getLights()
        self.vp_cameras = pmui.ModelEditor(self.modelPanel).getCameras()
        self.vp_imageplanes = pmui.ModelEditor(self.modelPanel).getImagePlane()
        self.vp_joints = pmui.ModelEditor(self.modelPanel).getJoints()
        self.vp_iks = pmui.ModelEditor(self.modelPanel).getIkHandles()
        self.vp_deformers = pmui.ModelEditor(self.modelPanel).getDeformers()
        self.vp_dynamics = pmui.ModelEditor(self.modelPanel).getDynamics()
        self.vp_instancers = cmds.modelEditor(self.modelPanel, particleInstancers=True, q=True)
        self.vp_fluids = pmui.ModelEditor(self.modelPanel).getFluids()
        self.vp_hair = pmui.ModelEditor(self.modelPanel).getHairSystems()
        self.vp_follicles = pmui.ModelEditor(self.modelPanel).getFollicles()
        self.vp_nCloths = pmui.ModelEditor(self.modelPanel).getNCloths()
        self.vp_nParticles = pmui.ModelEditor(self.modelPanel).getNParticles()
        self.vp_nRigids = pmui.ModelEditor(self.modelPanel).getNRigids()
        self.vp_dynconstraints = pmui.ModelEditor(self.modelPanel).getDynamicConstraints()
        self.vp_locators = pmui.ModelEditor(self.modelPanel).getLocators()
        self.vp_dimensions = pmui.ModelEditor(self.modelPanel).getDimensions()
        self.vp_pivots = pmui.ModelEditor(self.modelPanel).getPivots()
        self.vp_handles = pmui.ModelEditor(self.modelPanel).getHandles()
        self.vp_textureplacements = pmui.ModelEditor(self.modelPanel).getTextures()
        self.vp_strokes = pmui.ModelEditor(self.modelPanel).getStrokes()
        self.vp_motiontrails = pmui.ModelEditor(self.modelPanel).getMotionTrails()
        self.vp_pluginshapes = pmui.ModelEditor(self.modelPanel).pluginShapes()
        self.vp_clipghosts = cmds.modelEditor(self.modelPanel, clipGhosts=True, q=True)
        self.vp_greasepencil = cmds.modelEditor(self.modelPanel, greasePencils=True, q=True)
        self.vp_gpucache = cmds.modelEditor(self.modelPanel, queryPluginObjects="gpuCacheDisplayFilter", q=True)

        self.vp_manipulators = pmui.ModelEditor(self.modelPanel).getManipulators()
        self.vp_grid = pmui.ModelEditor(self.modelPanel).getGrid()
        self.vp_hud = pmui.ModelEditor(self.modelPanel).getHeadsUpDisplay()
        self.vp_holdouts = cmds.modelEditor(self.modelPanel, hos=True, q=True)
        self.vp_selectionhighlighting = pmui.ModelEditor(self.modelPanel).getSelectionHiliteDisplay()

    def render_resolution(self):

        w = str(cmds.getAttr("defaultResolution.width"))
        h = str(cmds.getAttr("defaultResolution.height"))
        return w, h

    def pb_filename(self):
        mayafile = cmds.file(q=True, sn=True, shn=True)
        if not mayafile:
            mayafile = "untitled"
        splitname = os.path.splitext(mayafile)
        self.filename = os.path.join("movies", splitname[0])
        if self.green:
            self.filename = self.filename + ".green"
        self.filename = self.filename + ".mov"
        return self.filename

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
        self.get_active_viewport()
        if not self.modelPanel:
            return

        if not self.overwrite:
            proj = cmds.workspace(q=True, fullName=True)
            if os.path.exists(os.path.join(proj, self.filename)):
                if cmds.file(modified=True, q=True):
                    overwrite = cmds.confirmDialog(title="Playblasts Exists",
                                              message="Overwrite Existing Playblast?",
                                              button=["Overwrite", "Cancel"],
                                              defaultButton="Overwrite",
                                              cancelButton="Cancel",
                                              dismissString="Cancel")
                    if not overwrite == "Overwrite":
                        cmds.warning("Action canceled")
                        return

        self.get_veiwport_settings()

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

            cmds.displayRGBColor("background", *self.default_color)
            cmds.displayRGBColor("backgroundTop", *self.default_color)
            cmds.displayRGBColor("backgroundBottom", *self.default_color)
            print "green triggered"
            self.remove_hud()

        gPlayBackSlider = pm.melGlobals['gPlayBackSlider']
        audio = cmds.timeControl(gPlayBackSlider, q=True, sound=True)

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
                       fo=True,
                       sound=audio
                       )

        if self.clean_vp or self.green:
            self.reset_viewports()

        if self.green:
            cmds.displayRGBColor("background", r, g, b)
            cmds.displayRGBColor("backgroundTop", rt, gt, bt)
            cmds.displayRGBColor("backgroundBottom", rb, gb, bb)

        self.remove_hud()
        return self.filename