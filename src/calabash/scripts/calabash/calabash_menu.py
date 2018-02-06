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

    vray_tools_submenu = cmds.menuItem('vray_tools_sub', p=calabash_menu, subMenu=True, label='Vray Tools', tearOff=True)
    #general_submenu = cmds.menuItem('general_sub', p=calabash_menu, subMenu=True, label='General', tearOff=True)
    ani_submenu = cmds.menuItem('ani_sub', p=calabash_menu, subMenu=True, label='Animation', tearOff=True)

    ###############################################################################

    # Vray Submenu
    cmds.menuItem(p=vray_tools_submenu, divider=True, dividerLabel='Vray Attributes', itl=True)

    cmds.menuItem(p=vray_tools_submenu, label='Add Subdivision Attributes', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.makeVraySubdAttr()')
    cmds.menuItem(p=vray_tools_submenu, label='Add Object ID Attributes', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.makeVrayObjId()')
    cmds.menuItem(p=vray_tools_submenu, label='Add Material ID Attributes (Beta)', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.makeVrayMatId()')
    cmds.menuItem(p=vray_tools_submenu, label='Add Displacement Control', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.displacementControl()')

    cmds.menuItem(p=vray_tools_submenu, divider=True, dividerLabel='Vray Object Properties', itl=True)

    cmds.menuItem(p=vray_tools_submenu, label='Apply single object properties node to selection', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.single_vop()')
    cmds.menuItem(p=vray_tools_submenu, label='Primary Vis Off', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.primVis()')
    cmds.menuItem(p=vray_tools_submenu, label='Matte Surface', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.matteSurface()')

    cmds.menuItem(p=vray_tools_submenu, divider=True, dividerLabel='Render Settings', itl=True)

    cmds.menuItem(p=vray_tools_submenu, label='Apply Final Render Settings', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.renderSettings()')
    cmds.menuItem(p=vray_tools_submenu, label='Apply Final Render GI Settings', c='from calabash import vrayUtils;reload(vrayUtils);vrayUtils.giSettings()')



    ###############################################################################


    # General Submenu

    #cmds.menuItem(p=general_submenu, label='Rename New Hatch Rigs', c='from calabash import fileUtils;reload(fileUtils);fileUtils.rename_hatch_rigs()')
    #cmds.menuItem(p=general_submenu, label='Publish Current File', c='from calabash import fileUtils;reload(fileUtils);fileUtils.publishCurrentFile()')
    #cmds.menuItem(p=general_submenu, label='Publish and Package', c='from calabash import fileUtils;reload(fileUtils);fileUtils.publishCurrentFile(send=True)')


    ###############################################################################

    cmds.menuItem(p=ani_submenu, label='Playblast', c='from calabash import playblast_utils;reload(playblast_utils);playblast_utils.make_playblast()')
    cmds.menuItem(p=ani_submenu, label='Playblast Green Screen', c='from calabash import playblast_utils;reload(playblast_utils);playblast_utils.make_playblast(green=True)')


calabash_menu()