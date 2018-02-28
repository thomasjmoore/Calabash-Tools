import maya.cmds as cmds
import os

calabash_menu = None




def calabash_menu():
    global calabash_menu
    if cmds.menu('calabash_m', exists=True):
        cmds.deleteUI('calabash_m')

    ###############################################################################

    calabash_menu = cmds.menu('calabash_m', p='MayaWindow', label='Calabash', tearOff=True)

    ###############################################################################

    general_submenu = cmds.menuItem('general_sub', p=calabash_menu, subMenu=True, label='General', tearOff=True)
    ani_submenu = cmds.menuItem('ani_sub', p=calabash_menu, subMenu=True, label='Animation', tearOff=True)
    rigging_submenu = cmds.menuItem('rigging_sub', p=calabash_menu, subMenu=True, label='Rigging', tearOff=True)
    Rendering_submenu = cmds.menuItem('rendering_sub', p=calabash_menu, subMenu=True, label='Render', tearOff=True)
    xgen_submenu = cmds.menuItem('xgen_sub', p=calabash_menu, subMenu=True, label='XGen', tearOff=True)
    hatch_submenu = cmds.menuItem('hatch_sub', p=calabash_menu, subMenu=True, label='Hatchimals', tearOff=True)

    ###############################################################################

    # Vray Submenu
    cmds.menuItem(p=Rendering_submenu, label='Submit to Smedge', c='from maya import mel; mel.eval("smedgeRender");')

    cmds.menuItem(p=Rendering_submenu, divider=True, dividerLabel='Vray Attributes', itl=True)

    cmds.menuItem(p=Rendering_submenu, label='Add Subdivision Attributes', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.makeVraySubdAttr()')
    cmds.menuItem(p=Rendering_submenu, label='Add Object ID Attributes', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.makeVrayObjId()')
    cmds.menuItem(p=Rendering_submenu, label='Add Material ID Attributes (Beta)', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.makeVrayMatId()')
    cmds.menuItem(p=Rendering_submenu, label='Add Displacement Control', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.displacementControl()')

    cmds.menuItem(p=Rendering_submenu, divider=True, dividerLabel='Vray Object Properties', itl=True)

    cmds.menuItem(p=Rendering_submenu, label='Apply single object properties node to selection', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.single_vop()')
    cmds.menuItem(p=Rendering_submenu, label='Primary Vis Off', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.primVis()')
    cmds.menuItem(p=Rendering_submenu, label='Matte Surface', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.matteSurface()')

    cmds.menuItem(p=Rendering_submenu, divider=True, dividerLabel='Render Settings', itl=True)

    cmds.menuItem(p=Rendering_submenu, label='Apply Final Render Settings', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.renderSettings()')
    cmds.menuItem(p=Rendering_submenu, label='Apply Final Render GI Settings', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.giSettings()')
    cmds.menuItem(p=Rendering_submenu, label='Render Elements for Selected Lights', c='from maya import mel;mel.eval("vrLightPass;")')



    ###############################################################################


    # General Submenu
    cmds.menuItem(p=general_submenu, label='Increase File Version', c='from calabash import increaseVersion;reload(increaseVersion);increaseVersion.versionUp()')
    cmds.menuItem(p=general_submenu, label='Check For Updates...', c='from calabash import update;reload(update);update.check()')


    ###############################################################################

    # Rigging Submenu
    cmds.menuItem(p=rigging_submenu, label='Publish Selected Rig', c='from calabash import fileUtils;reload(fileUtils);fileUtils.publishCurrentFile()')
    cmds.menuItem(p=rigging_submenu, label='Publish Vray Rig', c='from calabash import fileUtils;reload(fileUtils);fileUtils.publish_vray_rig()')
    cmds.menuItem(p=rigging_submenu, label='Publish Groom Rig', c='from calabash import fileUtils;reload(fileUtils);fileUtils.publish_groom_rig()',version="2017")
    cmds.menuItem(p=rigging_submenu, label='MoveCtrl', c='from calabash import moveControl;reload(moveControl);moveControl.moveCtrlUI()')
    cmds.menuItem(p=rigging_submenu, label='Hide Joints', c='from calabash import rigUtils;reload(rigUtils);rigUtils.jointDisplay()')
    cmds.menuItem(p=rigging_submenu, label='Show Joints', c='from calabash import rigUtils  ;reload(rigUtils);rigUtils.jointDisplay(show=True)')

    #cmds.menuItem(p=general_submenu, label='Publish and Package', c='from calabash import fileUtils;reload(fileUtils);fileUtils.publishCurrentFile(send=True)')


    ###############################################################################

    # Animation Submenu

    #cmds.menuItem(p=ani_submenu, label='Playblast', c='from calabash import playblast_utils;reload(playblast_utils);playblast_utils.make_playblast()')
    #cmds.menuItem(p=ani_submenu, label='Playblast Green Screen', c='from calabash import playblast_utils;reload(playblast_utils);playblast_utils.make_playblast(green=True)')
    cmds.menuItem(p=ani_submenu, label='Playblast-O-Scope', c='from calabash import playblast;reload(playblast);playblast.launch()')


    ###############################################################################

    # XGen Submenu


    cmds.menuItem(p=xgen_submenu, label='Cache Descriptions', c='from calabash import xgen_utils;reload(xgen_utils);xgen_utils.cache_groomableSplines()')
    cmds.menuItem(p=xgen_submenu, label='Repath Caches', c='from calabash import xgen_utils;reload(xgen_utils);xgen_utils.repath_caches()')


    ###############################################################################

    # Hatchimal Submenu

    cmds.menuItem(p=hatch_submenu, label='Publish Season2 Rig', c='from calabash import oldHatchUtils;reload(oldHatchUtils);oldHatchUtils.ohPublishCurrentFile()')
    cmds.menuItem(p=hatch_submenu, label='Publish Season2 No Vray Rig', c='from calabash import oldHatchUtils;reload(oldHatchUtils);oldHatchUtils.ohPublish_mayaMat_rig()')
    cmds.menuItem(p=hatch_submenu, label='Rename New Hatch Rigs', c='from calabash import fileUtils;reload(fileUtils);fileUtils.rename_hatch_rigs()')

calabash_menu()