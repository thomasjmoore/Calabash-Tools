### missionCtrl - tool box for adjusting rig controls

from maya import OpenMaya, OpenMayaUI, OpenMayaAnim, cmds

__all__ = [
    'moveCtrlUI'
]

try:
    import shiboken
    from shiboken import wrapInstance

except:

    import shiboken2 as shiboken
    from shiboken2 import wrapInstance

import calabash.lib.Qt.QtCore as QtCore
import calabash.lib.Qt.QtWidgets as QtWidgets


from functools import partial

#connects to maya's main window(but not on mac)
pointer = long(OpenMayaUI.MQtUtil.mainWindow())

#does some c++ to pyside converting
maya_window = shiboken.wrapInstance(pointer, QtWidgets.QMainWindow)


class moveCtrl (QtWidgets.QDialog):
    
    #the default action of the class opens the window
    def __init__ (self, parent=maya_window): 
        super(moveCtrl, self).__init__(parent)
        object_name = "Mission Ctrl" 

        exist = parent.findChild(QtWidgets.QDialog, object_name)
        
        buttonWidth = 25
        #deletes the window if it exists
        if exist:
            shiboken.delete (exist) 
        
        #sets some basic window properties 
        self.setWindowTitle( "v0.5 Move Control" )
        self.setObjectName( object_name ) 
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint )
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint )
        self.resize(100,100)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(5,5,5,5)
        main_layout.setSpacing(5)

        mirrorWidget = QtWidgets.QWidget()
        mirrorLayout = QtWidgets.QHBoxLayout(mirrorWidget)
        mirrorLayout.setContentsMargins(0,5,0,0)
        mirrorLayout.setSpacing(0)

        mirrorLbl = QtWidgets.QLabel("Try to mirror on X: ")
        self.mirrorchk = QtWidgets.QCheckBox()
        self.mirrorchk.setCheckState(QtCore.Qt.Checked)

        mirrorLayout.addWidget(mirrorLbl)        
        mirrorLayout.addWidget(self.mirrorchk)


        translateWidget =  QtWidgets.QWidget()
        translateLayout = QtWidgets.QGridLayout(translateWidget)
        translateLayout.setContentsMargins(0,5,0,0)
        translateLayout.setSpacing(2)




        transLbl = QtWidgets.QLabel('TRANSLATE')
        transIncrementLbl = QtWidgets.QLabel('Increment: ')
        self.transIncrement = QtWidgets.QLineEdit('.25')
        tXPosbtn = QtWidgets.QPushButton('X +')
        tXNegbtn = QtWidgets.QPushButton('X -')

        tYPosbtn = QtWidgets.QPushButton('Y +')
        tYNegbtn = QtWidgets.QPushButton('Y -')

        tZPosbtn = QtWidgets.QPushButton('Z +')
        tZNegbtn = QtWidgets.QPushButton('Z -')

        #set button widths
        tXPosbtn.setMaximumWidth(buttonWidth)
        tXNegbtn.setMaximumWidth(buttonWidth)
        tYPosbtn.setMaximumWidth(buttonWidth)
        tYNegbtn.setMaximumWidth(buttonWidth)
        tZPosbtn.setMaximumWidth(buttonWidth)
        tZNegbtn.setMaximumWidth(buttonWidth)

        translateLayout.addWidget(transLbl, 0,0, 1, 2)
        translateLayout.addWidget(tXPosbtn, 0,2)
        translateLayout.addWidget(tXNegbtn, 0,3)
        translateLayout.addWidget(transIncrementLbl, 1,0, 1, 1)
        translateLayout.addWidget(self.transIncrement, 2,0, 1, 1)
        translateLayout.addWidget(tYPosbtn, 1,2)
        translateLayout.addWidget(tYNegbtn, 1,3)
        translateLayout.addWidget(tZPosbtn, 2,2)
        translateLayout.addWidget(tZNegbtn, 2,3)


        rotateWidget =  QtWidgets.QWidget()
        rotateLayout = QtWidgets.QGridLayout(rotateWidget)
        rotateLayout.setContentsMargins(0,5,0,0)
        rotateLayout.setSpacing(2)

        rotLbl = QtWidgets.QLabel('ROTATE')
        rotIncrementLbl = QtWidgets.QLabel('Increment: ')
        self.rotIncrement = QtWidgets.QLineEdit('10')
        rXPosbtn = QtWidgets.QPushButton('X +')
        rXNegbtn = QtWidgets.QPushButton('X -')

        rYPosbtn = QtWidgets.QPushButton('Y +')
        rYNegbtn = QtWidgets.QPushButton('Y -')

        rZPosbtn = QtWidgets.QPushButton('Z +')
        rZNegbtn = QtWidgets.QPushButton('Z -')


        #set button widths
        rXPosbtn.setMaximumWidth(buttonWidth)
        rXNegbtn.setMaximumWidth(buttonWidth)
        rYPosbtn.setMaximumWidth(buttonWidth)
        rYNegbtn.setMaximumWidth(buttonWidth)
        rZPosbtn.setMaximumWidth(buttonWidth)
        rZNegbtn.setMaximumWidth(buttonWidth)

        rotateLayout.addWidget(rotLbl, 0,0, 1, 2)
        rotateLayout.addWidget(rXPosbtn, 0,2)
        rotateLayout.addWidget(rXNegbtn, 0,3)
        rotateLayout.addWidget(rotIncrementLbl, 1,0, 1, 1)
        rotateLayout.addWidget(self.rotIncrement, 2,0, 1, 1)
        rotateLayout.addWidget(rYPosbtn, 1,2)
        rotateLayout.addWidget(rYNegbtn, 1,3)
        rotateLayout.addWidget(rZPosbtn, 2,2)
        rotateLayout.addWidget(rZNegbtn, 2,3)


        scaleWidget =  QtWidgets.QWidget()
        scaleLayout = QtWidgets.QGridLayout(scaleWidget)
        scaleLayout.setContentsMargins(0,5,0,0)
        scaleLayout.setSpacing(2)

        scaleLbl = QtWidgets.QLabel('SCALE')
        scaleIncrementLbl = QtWidgets.QLabel('Increment: ')
        self.scaleIncrement = QtWidgets.QLineEdit('1.1')
        sXPosbtn = QtWidgets.QPushButton('X')
        sXNegbtn = QtWidgets.QPushButton('X -')

        sYPosbtn = QtWidgets.QPushButton('Y')
        sYNegbtn = QtWidgets.QPushButton('Y -')

        sZPosbtn = QtWidgets.QPushButton('Z')
        sZNegbtn = QtWidgets.QPushButton('Z -')

        sUniBtn = QtWidgets.QPushButton('Uni')
        sInvBtn = QtWidgets.QPushButton('Inv')


        #set button widths
        sXPosbtn.setMaximumWidth(buttonWidth)
        sYPosbtn.setMaximumWidth(buttonWidth)
        sZPosbtn.setMaximumWidth(buttonWidth)
        sXNegbtn.setMaximumWidth(buttonWidth)
        sYNegbtn.setMaximumWidth(buttonWidth)
        sZNegbtn.setMaximumWidth(buttonWidth)
        sUniBtn.setMaximumWidth(buttonWidth)
        sInvBtn.setMaximumWidth(buttonWidth)

        scaleLayout.addWidget(scaleLbl, 0,0, 1, 2)
        scaleLayout.addWidget(sUniBtn, 3,3, 1, 1)
        scaleLayout.addWidget(sInvBtn, 3,2, 1, 1)

        scaleLayout.addWidget(sXPosbtn, 0,3, 1 ,1)
        scaleLayout.addWidget(sXNegbtn, 0,2, 1 ,1)

        scaleLayout.addWidget(scaleIncrementLbl, 1,0, 1, 1)
        scaleLayout.addWidget(self.scaleIncrement, 2,0, 1, 1)
        scaleLayout.addWidget(sYPosbtn, 1,3, 1 ,1)
        scaleLayout.addWidget(sYNegbtn, 1,2, 1 ,1)


        scaleLayout.addWidget(sZPosbtn, 2,3, 1 ,1)
        scaleLayout.addWidget(sZNegbtn, 2,2, 1 ,1)

        main_layout.addWidget(mirrorWidget)
        main_layout.addWidget(translateWidget)
        main_layout.addWidget(rotateWidget)
        main_layout.addWidget(scaleWidget)

        tXPosbtn.clicked.connect(self.tPosXButton)
        tXNegbtn.clicked.connect(self.tNegXButton)
        tYPosbtn.clicked.connect(self.tPosYButton)
        tYNegbtn.clicked.connect(self.tNegYButton)
        tZPosbtn.clicked.connect(self.tPosZButton)
        tZNegbtn.clicked.connect(self.tNegZButton)

        rXPosbtn.clicked.connect(self.rPosXButton)
        rXNegbtn.clicked.connect(self.rNegXButton)
        rYPosbtn.clicked.connect(self.rPosYButton)
        rYNegbtn.clicked.connect(self.rNegYButton)
        rZPosbtn.clicked.connect(self.rPosZButton)
        rZNegbtn.clicked.connect(self.rNegZButton)

        sXPosbtn.clicked.connect(self.sPosXButton)
        sYPosbtn.clicked.connect(self.sPosYButton)
        sZPosbtn.clicked.connect(self.sPosZButton)
        sUniBtn.clicked.connect(self.sUniButton)
        sXNegbtn.clicked.connect(self.sNegXButton)
        sYNegbtn.clicked.connect(self.sNegYButton)
        sZNegbtn.clicked.connect(self.sNegZButton)
        sInvBtn.clicked.connect(self.sInvButton)

        stylesheet1 = "QPushButton{background-color: rgb(200,80,80);}"
        stylesheet2 = "QPushButton{background-color: rgb(30,120,50);}"
        stylesheet3 = "QPushButton{background-color: rgb(30,100,200);}"

        #set background color
        #translateWidget.setAutoFillBackground(True)
        translateWidget.setStyleSheet(stylesheet1)
        rotateWidget.setStyleSheet(stylesheet2)
        scaleWidget.setStyleSheet(stylesheet3)


    def chkMirror(self):
        if self.mirrorchk.checkState():
            mirror = True
        else:
            mirror = False
        return mirror


    def tPosXButton(self):
        inc = self.transIncrement.text()
        moveControl('translate', inc, 0, 0, self.chkMirror())

    def tNegXButton(self):
        inc = self.transIncrement.text()
        valid = validation(inc)
        if not valid:
            return
        inc = (float(inc))*-1
        moveControl('translate', inc, 0, 0, self.chkMirror())

    def tPosYButton(self):
        inc = self.transIncrement.text()
        moveControl('translate', 0, inc, 0, False)

    def tNegYButton(self):
        inc = self.transIncrement.text()
        valid = validation(inc)
        if not valid:
            return
        inc = (float(inc))*-1
        moveControl('translate', 0, inc, 0, False)

    def tPosZButton(self):
        inc = self.transIncrement.text()
        moveControl('translate', 0, 0, inc, False)

    def tNegZButton(self):
        inc = self.transIncrement.text()
        valid = validation(inc)
        if not valid:
            return
        inc = (float(inc))*-1
        moveControl('translate', 0, 0, inc, False)


    def rPosXButton(self):
        inc = self.rotIncrement.text()
        moveControl('rotate', inc, 0, 0, self.chkMirror())

    def rNegXButton(self):
        inc = self.rotIncrement.text()
        valid = validation(inc)
        if not valid:
            return
        inc = (float(inc))*-1
        moveControl('rotate', inc, 0, 0, self.chkMirror())

    def rPosYButton(self):
        inc = self.rotIncrement.text()
        moveControl('rotate', 0, inc, 0, self.chkMirror())

    def rNegYButton(self):
        inc = self.rotIncrement.text()
        valid = validation(inc)
        if not valid:
            return
        inc = (float(inc))*-1
        moveControl('rotate', 0, inc, 0, self.chkMirror())

    def rPosZButton(self):
        inc = self.rotIncrement.text()
        moveControl('rotate', 0, 0, inc, self.chkMirror())

    def rNegZButton(self):
        inc = self.rotIncrement.text()
        valid = validation(inc)
        if not valid:
            return
        inc = (float(inc))*-1
        moveControl('rotate', 0, 0, inc, self.chkMirror())



    def sPosXButton(self):
        inc = self.scaleIncrement.text()
        moveControl('scale', inc, 1, 1)

    def sPosYButton(self):
        inc = self.scaleIncrement.text()
        moveControl('scale', 1, inc, 1)

    def sPosZButton(self):
        inc = self.scaleIncrement.text()
        moveControl('scale', 1, 1, inc)

    def sUniButton(self):
        inc = self.scaleIncrement.text()
        moveControl('scale', inc, inc, inc)

    def sNegXButton(self):
        inc = self.scaleIncrement.text()
        valid = validation(inc)
        if not valid:
            return
        if float(inc) == 0:
            return
        inv = 1/float(inc)

        moveControl('scale', inv, 1, 1)

    def sNegYButton(self):
        inc = self.scaleIncrement.text()
        valid = validation(inc)
        if not valid:
            return
        if float(inc) == 0:
            return
        inv = 1/float(inc)
        moveControl('scale', 1, inv, 1)

    def sNegZButton(self):
        inc = self.scaleIncrement.text()
        valid = validation(inc)
        if not valid:
            return
        if float(inc) == 0:
            return
        inv = 1/float(inc)
        moveControl('scale', 1, 1, inv)

    def sInvButton(self):
        inc = self.scaleIncrement.text()
        valid = validation(inc)
        if not valid:
            return
        if float(inc) == 0:
            return
        inv = 1/float(inc)
        moveControl('scale', inv, inv, inv)

def validation(user_Input):
    valid=True
    try:
        val = float(user_Input)
    except ValueError:
        print(user_Input,' not an number!')
        valid = False
    return valid


def moveControl(operation, x=0, y=0, z=0, mirror=False):
    list = cmds.ls(sl=1)

    # make sure something is selected
    if not list:
        print "Nothing Selected"
        pass

    valid = validation(x)
    if not valid:
        return
    valid = validation(y)
    if not valid:
        return
    valid = validation(z)
    if not valid:
        return

    print x, y, z
    #open under chunk so we can under all movements with single undo
    cmds.undoInfo(openChunk = True)

    # iterate through each control that is selected
    for item in list :
        # clear any previous selections
        cmds.select(clear=True)




        # check to see if RT is in object name, and if mirror option is enabled, otherwise act normally

        if not item.find("RT") == -1 and mirror:
            rtCtrl = True

        else:
            rtCtrl = False


        #find all the shape nodes for the current control
        shapes = cmds.listRelatives(item, s = True,type='nurbsCurve')

        #if no valid shapes selected, close undo chunk
        if not shapes:
            cmds.undoInfo(closeChunk = True)
            print "not Shape"
            pass


        # find the center of object in order to scale
        bbox = cmds.exactWorldBoundingBox(shapes)
        xCtr = (bbox[0]+bbox[3])/2
        yCtr = (bbox[1]+bbox[4])/2
        zCtr = (bbox[2]+bbox[5])/2



        for shape in shapes :
            if cmds.objectType(shape) == 'nurbsCurve' :
                cmds.select(shape + '.cv[0:]', add = True)
            elif cmds.objectType(shape) == 'mesh' :
                cmds.select(shape + '.vtx[0:]', add = True)
        listPoints = cmds.ls(sl=True)

        #if no points selected, close undo chunk
        if not listPoints:
            cmds.undoInfo(closeChunk = True)
            break


        if operation == "translate":

            controlTranslate(x, y, z, rtCtrl)
        if operation == "rotate":
            controlRotate(x, y, z,  xCtr, yCtr, zCtr, rtCtrl)
        if operation =="scale":
            controlScale(x, y, z, xCtr, yCtr, zCtr)


    cmds.select(list)
    #close undo chunk
    cmds.undoInfo(closeChunk = True)



def controlScale(sX, sY, sZ, xPiv, yPiv, zPiv):
    cmds.scale(float(sX), float(sY), float(sZ), r = True, pivot = [xPiv, yPiv, zPiv])

def controlTranslate(tX, tY, tZ, rtCtrl):
    # mirror the x value
    tXOut = tX
    if rtCtrl:
        tXOut = (float(tX)) * -1
    else:
        tXOut = tX
    cmds.move(tXOut, tY, tZ, r = True, worldSpace = True)

def controlRotate(rX, rY, rZ,  xPiv, yPiv, zPiv, rtCtrl):

    # mirror the rotation values
    if rtCtrl:
        rXOut = float(rX)
        rYOut = float(rY) * -1
        rZOut = float(rZ) * -1
    else:
        rXOut = float(rX)
        rYOut = float(rY)
        rZOut = float(rZ)

    cmds.rotate(rXOut, rYOut, rZOut, objectCenterPivot = True, worldSpace = True,  pivot = [xPiv, yPiv, zPiv])

def controlScaleAll(sX, sY, sZ):
    pass

def moveCtrlUI ():
    w=moveCtrl()
    w.show()
    
if __name__ == "__main__":
    moveCtrlUI()
    

