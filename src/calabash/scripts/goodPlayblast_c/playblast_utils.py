'''
A set of utilities to aid in easy and consistent playblasts
'''

from maya import cmds
import pymel.core as pm
import pymel.core.uitypes as pmui
import os
from maya import mel
import maya.OpenMayaAnim as oma
import glob

def clean_hud():
    hud_menu = pm.melGlobals['gHeadsUpDisplayMenu']
    menuitems = cmds.menu(hud_menu, q=True, itemArray=True)


class Playblaster(object):
    """

    """

    # Default settings
    override_vp=True
    green = False
    only_polygons = True
    override_hud = True
    display_hud = True
    hud = True
    scene_hud = True
    camera_hud = True
    custom_hud_chk = False
    hud_frame_chk = True
    custom_hud_text = ""
    w = 960
    h = 540
    modelPanel = ""
    default_color = [0,1,0]
    overwrite = False
    view = True
    offscreen = False
    camera = ""
    gates = False
    usescenename_chk = True
    pb_format = [0, "qt"]
    encoding = "H.264"
    quality = 70
    scale = 100
    custom_resolution = False
    save_directory = ""



    def __init__(self):

        self.proj = self.get_project()
        self.start, self.end = self.start_end()
        self.filename = self.pb_filename()
        self.load_option_vars()
        if not self.save_directory:
            self.save_directory = os.path.join(cmds.workspace(q=True, fn=True), "movies").replace("\\", "/")

    def load_option_vars(self):
        # check for preferences, and load them if they exist
        if cmds.optionVar(exists="gp_overrideviewport_chk"):
            self.override_vp = bool(cmds.optionVar(q="gp_overrideviewport_chk"))
        if cmds.optionVar(exists="gp_onlypolygons_chk"):
            self.only_polygons = bool(cmds.optionVar(q="gp_onlypolygons_chk"))
        if cmds.optionVar(exists="gp_gates_chk"):
            self.gates = bool(cmds.optionVar(q="gp_gates_chk"))
        if cmds.optionVar(exists="gp_bgcolor_chk"):
            self.green = bool(cmds.optionVar(q="gp_bgcolor_chk"))
        if cmds.optionVar(exists="gp_bgcolorR"):
            color =[]
            color.append(cmds.optionVar(q="gp_bgcolorR"))
            color.append(cmds.optionVar(q="gp_bgcolorG"))
            color.append(cmds.optionVar(q="gp_bgcolorB"))
            self.default_color = color

        if cmds.optionVar(exists="gp_overridehud_chk"):
            self.override_hud = bool(cmds.optionVar(q="gp_overridehud_chk"))
        if cmds.optionVar(exists="gp_displayhud_chk"):
            self.display_hud = bool(cmds.optionVar(q="gp_displayhud_chk"))
        if cmds.optionVar(exists="gp_projecthud_chk"):
            self.hud = bool(cmds.optionVar(q="gp_projecthud_chk"))
        if cmds.optionVar(exists="gp_frameHud_chk"):
            self.hud_frame_chk = bool(cmds.optionVar(q="gp_frameHud_chk"))
        if cmds.optionVar(exists="gp_camerahud_chk"):
            self.camera_hud = bool(cmds.optionVar(q="gp_camerahud_chk"))
        if cmds.optionVar(exists="gp_scenehud_chk"):
            self.scene_hud = bool(cmds.optionVar(q="gp_scenehud_chk"))
        if cmds.optionVar(exists="gp_username_chk"):
            self.custom_hud_chk = bool(cmds.optionVar(q="gp_username_chk"))

        if cmds.optionVar(exists="gp_format_ind"):
            self.pb_format[0] = int(cmds.optionVar(q="gp_format_ind"))
        if cmds.optionVar(exists="gp_format_cmb"):
            self.pb_format[1] = cmds.optionVar(q="gp_format_cmb")
        if cmds.optionVar(exists="gp_encoding_cmb"):
            self.encoding = cmds.optionVar(q="gp_encoding_cmb")
        if cmds.optionVar(exists="gp_quality_le"):
            self.quality = int(cmds.optionVar(q="gp_quality_le"))
        if cmds.optionVar(exists="gp_customresolution_chk"):
            self.custom_resolution = bool(cmds.optionVar(q="gp_customresolution_chk"))
        if cmds.optionVar(exists="gp_height_le") and self.custom_resolution:
            self.h = int(cmds.optionVar(q="gp_height_le"))
        if cmds.optionVar(exists="gp_width_le") and self.custom_resolution:
            self.w = int(cmds.optionVar(q="gp_width_le"))
        if cmds.optionVar(exists="gp_scale_le"):
            self.scale = float(cmds.optionVar(q="gp_scale_le"))

        if cmds.optionVar(exists="gp_offscreen_chk"):
            self.offscreen = bool(cmds.optionVar(q="gp_offscreen_chk"))
        if cmds.optionVar(exists="gp_view_chk"):
            self.view = bool(cmds.optionVar(q="gp_view_chk"))
        if cmds.optionVar(exists="gp_overwrite_chk"):
            self.overwrite = bool(cmds.optionVar(q="gp_overwrite_chk"))
        if cmds.optionVar(exists="gp_usescenename_chk"):
            self.usescenename_chk = bool(cmds.optionVar(q="gp_usescenename_chk"))
        if cmds.optionVar(exists="gp_scenename_le") and not self.usescenename_chk:
            self.filename = (cmds.optionVar(q="gp_scenename_le"))
        if cmds.optionVar(exists="gp_savedir_le"):
            self.save_directory = (cmds.optionVar(q="gp_savedir_le"))

    def get_project(self):
        projpath = cmds.workspace(q=True, sn=True)
        proj = os.path.basename(projpath)
        return proj

    def scene_name_hud(self):
        if cmds.headsUpDisplay("HUDSceneName", exists=True):
            cmds.headsUpDisplay("HUDSceneName", remove=True)

        scene = cmds.file(q=True, sn=True, shn=True)
        cmds.headsUpDisplay("HUDSceneName", section=5, block=2, blockSize="small", dfs="small", l=scene)

    def proj_name_hud(self):
        if cmds.headsUpDisplay("HUDProjName", exists=True):
            cmds.headsUpDisplay("HUDProjName", remove=True)

        cmds.headsUpDisplay("HUDProjName", section=5, block=3, blockSize="small", dfs="small", l=self.proj)

    def framecount_hud(self):
        if cmds.headsUpDisplay("HUDFrameCount", exists=True):
            cmds.headsUpDisplay("HUDFrameCount", remove=True)
        cmds.headsUpDisplay("HUDFrameCount", section=5, block=1, blockSize="small", dfs="large", l="frame",
                            command="cmds.currentTime(q=True)", atr=True)

    def custom_hud(self, text=""):
        if cmds.headsUpDisplay("HUDCustom", exists=True):
            cmds.headsUpDisplay("HUDCustom", remove=True)
        cmds.headsUpDisplay("HUDCustom", section=5, block=4, blockSize="small", dfs="large", label=text)

    def set_hud(self):
        self.cameraNamesVisibility = cmds.optionVar(q="cameraNamesVisibility")
        self.animationDetailsVisibility = cmds.optionVar(q="animationDetailsVisibility")
        self.capsLockVisibility = cmds.optionVar(q="capsLockVisibility")
        self.currentContainerVisibility = cmds.optionVar(q="currentContainerVisibility")
        self.capsLockVisibility = cmds.optionVar(q="capsLockVisibility")
        self.currentFrameVisibility = cmds.optionVar(q="currentFrameVisibility")
        self.focalLengthVisibility = cmds.optionVar(q="focalLengthVisibility")
        self.frameRateVisibility = cmds.optionVar(q="frameRateVisibility")
        self.hikDetailsVisibility = cmds.optionVar(q="hikDetailsVisibility")
        self.materialLoadingDetailsVisibility = cmds.optionVar(q="materialLoadingDetailsVisibility")
        self.objectDetailsVisibility = cmds.optionVar(q="objectDetailsVisibility")
        self.particleCountVisibility = cmds.optionVar(q="particleCountVisibility")
        self.polyCountVisibility = cmds.optionVar(q="polyCountVisibility")
        self.sceneTimecodeVisibility = cmds.optionVar(q="sceneTimecodeVisibility")
        self.selectDetailsVisibility = cmds.optionVar(q="selectDetailsVisibility")
        self.symmetryVisibility = cmds.optionVar(q="symmetryVisibility")
        self.viewAxisVisibility = cmds.optionVar(q="viewAxisVisibility")
        self.viewportRendererVisibility = cmds.optionVar(q="viewportRendererVisibility")

        self.evaluationManagerHUDVisibility = cmds.optionVar(q="evaluationVisibility")

        if cmds.pluginInfo("xgenToolkit", loaded=True, q=True):
            self.xgenHUDVisibility = cmds.optionVar(q="xgenHUDVisibility")


        self.originAxis = cmds.toggleAxis(o=True, q=True)
        if not self.override_hud:
            return

        mel.eval('setCameraNamesVisibility(0);')
        mel.eval('setAnimationDetailsVisibility(0)')
        mel.eval('setCapsLockVisibility(0)')
        mel.eval('setCurrentContainerVisibility(0)')
        mel.eval('setCapsLockVisibility(0)')
        mel.eval('setCurrentFrameVisibility(0)')
        mel.eval('setFocalLengthVisibility(0)')
        mel.eval('setFrameRateVisibility(0)')
        mel.eval('setHikDetailsVisibility(0)')
        mel.eval('ToggleMaterialLoadingDetailsHUDVisibility(0)')
        mel.eval('setObjectDetailsVisibility(0)')
        mel.eval('setParticleCountVisibility(0)')
        mel.eval('setPolyCountVisibility(0)')
        mel.eval('setSceneTimecodeVisibility(0)')
        mel.eval('setSelectDetailsVisibility(0)')
        mel.eval('setSymmetryVisibility(0)')
        mel.eval('setViewAxisVisibility(0)')
        mel.eval('setViewportRendererVisibility(0)')
        mel.eval('SetEvaluationManagerHUDVisibility(0)')
        mel.eval('viewManip - v(0);')
        mel.eval('toggleAxis - o(0);')
        if cmds.pluginInfo("xgenToolkit", loaded=True, q=True):
            mel.eval('setXGenHUDVisibility(0)')

        if not self.display_hud:
            return

        if self.hud:
            self.proj_name_hud()

        if self.scene_hud:
            self.scene_name_hud()

        if self.hud_frame_chk:
            self.framecount_hud()

        if self.custom_hud_chk:
            self.custom_hud(self.custom_hud_text)

        if self.camera_hud and self.override_hud:
            cam = 1
        else:
            cam = 0

        mel.eval('setCameraNamesVisibility(%s);' % cam)

    def reset_hud(self):
        if cmds.headsUpDisplay("HUDProjName", exists=True):
            cmds.headsUpDisplay("HUDProjName", remove=True)

        if cmds.headsUpDisplay("HUDSceneName", exists=True):
            cmds.headsUpDisplay("HUDSceneName", remove=True)

        if cmds.headsUpDisplay("HUDFrameCount", exists=True):
            cmds.headsUpDisplay("HUDFrameCount", remove=True)

        if cmds.headsUpDisplay("HUDCustom", exists=True):
            cmds.headsUpDisplay("HUDCustom", remove=True)

        mel.eval('setCameraNamesVisibility(%s);'% self.cameraNamesVisibility)
        mel.eval('setAnimationDetailsVisibility(%s);'% self.animationDetailsVisibility)
        mel.eval('setCapsLockVisibility(%s);'% self.capsLockVisibility)
        mel.eval('setCurrentContainerVisibility(%s);'% self.currentContainerVisibility)
        mel.eval('setCapsLockVisibility(%s);'% self.capsLockVisibility)
        mel.eval('setCurrentFrameVisibility(%s);'% self.currentFrameVisibility)
        mel.eval('setFocalLengthVisibility(%s);'% self.focalLengthVisibility)
        mel.eval('setFrameRateVisibility(%s);'% self.frameRateVisibility)
        mel.eval('setHikDetailsVisibility(%s);'% self.hikDetailsVisibility)
        mel.eval('ToggleMaterialLoadingDetailsHUDVisibility(%s);'% self.materialLoadingDetailsVisibility)
        mel.eval('setObjectDetailsVisibility(%s);'% self.objectDetailsVisibility)
        mel.eval('setParticleCountVisibility(%s);'% self.particleCountVisibility)
        mel.eval('setPolyCountVisibility(%s);'% self.polyCountVisibility)
        mel.eval('setSceneTimecodeVisibility(%s);'% self.sceneTimecodeVisibility)
        mel.eval('setSelectDetailsVisibility(%s);'% self.selectDetailsVisibility)
        mel.eval('setSymmetryVisibility(%s);'% self.symmetryVisibility)
        mel.eval('setViewAxisVisibility(%s);'% self.viewAxisVisibility)
        mel.eval('setViewportRendererVisibility(%s);'% self.viewportRendererVisibility)
        mel.eval('SetEvaluationManagerHUDVisibility(%s);'% self.evaluationManagerHUDVisibility)
        cmds.toggleAxis(o=self.originAxis)
        if cmds.pluginInfo("xgenToolkit", loaded=True, q=True):
            mel.eval('setXGenHUDVisibility(%s);' % self.xgenHUDVisibility)

    def get_active_viewport(self):
        active_panel = pmui.ModelEditor(pm.getPanel(withFocus=True))
        model_editor_list = pm.lsUI(editors=True)

        for myModelPanel in model_editor_list:
            if myModelPanel.find(active_panel) != -1:
                model_editor = myModelPanel

        if pm.getPanel(to=active_panel) == "modelPanel":
            self.modelPanel = model_editor
            self.camera = (pm.modelEditor(self.modelPanel, q=True, camera=True)).getShape()
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
        cmds.modelEditor(self.modelPanel, clipGhosts=self.vp_clipghosts, e=True)
        cmds.modelEditor(self.modelPanel, greasePencils=self.vp_greasepencil, e=True)

        pmui.ModelEditor(self.modelPanel).setManipulators(self.vp_manipulators)
        pmui.ModelEditor(self.modelPanel).setGrid(self.vp_grid)
        pmui.ModelEditor(self.modelPanel).setHeadsUpDisplay(self.vp_hud)
        cmds.modelEditor(self.modelPanel, hos=self.vp_holdouts, e=True)
        pmui.ModelEditor(self.modelPanel).setSelectionHiliteDisplay(self.vp_selectionhighlighting)

    def set_cameras(self):
        if not self.override_vp:
            return

        self.cam_dr = self.camera.displayResolution.get()
        self.cam_df = self.camera.displayFilmGate.get()
        self.cam_dsa = self.camera.displaySafeAction.get()
        self.cam_dst = self.camera.displaySafeTitle.get()

        if not self.gates:
            self.camera.displayResolution.set(0)
            self.camera.displayFilmGate.set(0)
            self.camera.displaySafeAction.set(0)
            self.camera.displaySafeTitle.set(0)

    def reset_cameras(self):
        self.camera.displayResolution.set(self.cam_dr)
        self.camera.displayFilmGate.set(self.cam_df)
        self.camera.displaySafeAction.set(self.cam_dsa)
        self.camera.displaySafeTitle.set(self.cam_dst)

    def set_viewports(self):
        if not self.override_vp:
            return
        self.get_veiwport_settings()

        if self.only_polygons:
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

            pmui.ModelEditor(self.modelPanel).setManipulators(False)
            pmui.ModelEditor(self.modelPanel).setGrid(False)
            pmui.ModelEditor(self.modelPanel).setHeadsUpDisplay(True)
            cmds.modelEditor(self.modelPanel, hos=False, e=True)
            pmui.ModelEditor(self.modelPanel).setSelectionHiliteDisplay(False)

    def get_veiwport_settings(self):
        # stores the pre-playblast viewport visilbity settings
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

    def render_frameRange(self):
        s = str(int(cmds.getAttr("defaultRenderGlobals.startFrame")))
        e = str(int(cmds.getAttr("defaultRenderGlobals.endFrame")))
        return s, e

    def pb_filename(self):
        # get the current scene name, remove the extension, and account for a scene without a name
        mayafile = cmds.file(q=True, sn=True, shn=True)
        if not mayafile:
            mayafile = "untitled"
        splitname = os.path.splitext(mayafile)
        self.filename = splitname[0]

        return self.filename

    def start_end(self):
        # get the selected timeline range, if it exists, otherwise use the visible timeline range
        slider = pm.melGlobals['gPlayBackSlider']
        if cmds.timeControl(slider, rangeVisible=True, q=True):
            range = cmds.timeControl(slider, range=True, q=True)
            s, e = range.split(":")
            self.start = s[1:]
            self.end = e[:-1]
        else:
            self.start = int(oma.MAnimControl.minTime().value())
            self.end = int(oma.MAnimControl.maxTime().value())
        return self.start, self.end

    def playblast(self):
        self.get_active_viewport()
        if not self.modelPanel:
            return

        self.filename = os.path.join(self.save_directory, self.filename)

        if not self.overwrite:
            # glob allows searching for the filename with a wildcard for the extension
            if glob.glob('%s.*' % self.filename):
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

        # save the viewport settings so we can revert them later
        self.get_veiwport_settings()
        # set everything up for playblast
        self.set_viewports()
        self.set_cameras()
        self.set_hud()

        if self.green and self.override_vp:
            r, g, b = cmds.displayRGBColor("background", q=True)
            rt, gt, bt = cmds.displayRGBColor("backgroundTop", q=True)
            rb, gb, bb = cmds.displayRGBColor("backgroundBottom", q=True)

            cmds.displayRGBColor("background", *self.default_color)
            cmds.displayRGBColor("backgroundTop", *self.default_color)
            cmds.displayRGBColor("backgroundBottom", *self.default_color)

        # Get active audio clip
        gPlayBackSlider = pm.melGlobals['gPlayBackSlider']
        audio = cmds.timeControl(gPlayBackSlider, q=True, sound=True)

        # Do Playblast
        cmds.playblast(
                       format=self.pb_format[1],
                       filename=self.filename,
                       sequenceTime=False,
                       clearCache=True,
                       viewer=self.view,
                       showOrnaments=True,
                       offScreen=self.offscreen,
                       compression=self.encoding,
                       quality=self.quality,
                       widthHeight=[self.w, self.h],
                       st=self.start,
                       et=self.end,
                       percent=(self.scale),
                       fo=True,
                       sound=audio
                       )

        # Reset everything
        self.reset_viewports()
        self.reset_cameras()
        if self.green and self.override_vp:
            cmds.displayRGBColor("background", r, g, b)
            cmds.displayRGBColor("backgroundTop", rt, gt, bt)
            cmds.displayRGBColor("backgroundBottom", rb, gb, bb)
        self.reset_hud()

        return self.filename