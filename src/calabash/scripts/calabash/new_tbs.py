from pymel import core as pm

# TBS for the modern era



def tbs():
    particles = check_selection()
    if not particles: return

    for p in particles:
        # check to see if particles are already TBS
        if pm.objExists("{}.isBig".format(p)):
            pm.displayWarning("{} is already TBS".format(p))
            continue

        transform = p.getParent()

        if not pm.objExists("{}.radiusPP".format(p)):
            pm.addAttr(p, ln="radiusPP", dt="doubleArray")
            pm.addAttr(p, ln="radiusPP0", dt="doubleArray")

        if not pm.objExists("{}.RGBPP".format(p)):
            pm.addAttr(p, ln="rgbPP", dt="vectorArray")
            pm.addAttr(p, ln="rgbPP0", dt="vectorArray")

        # add attributes
        pm.addAttr(p, ln = "isBig", dt = "doubleArray")
        pm.addAttr(p, ln = "isBig0", dt = "doubleArray")
        pm.addAttr(p, ln = "noiseMod", dt = "doubleArray")
        pm.addAttr(p, ln = "noiseMod0", dt = "doubleArray")
        pm.addAttr(p, ln = "isChild", dt = "doubleArray")
        pm.addAttr(p, ln = "isChild0", dt = "doubleArray")

        transform.addAttr("lifespanBig", at = "double", min = 0, dv = 2, k = True)
        transform.addAttr("lifespanBigRand", at = "double", min = 0, dv = 1, k = True)
        transform.addAttr("lifespanSmall", at = "double", min = 0, dv = .75, k = True)
        transform.addAttr("lifespanSmallRand", at = "double", min = 0, dv = .37, k = True)
        transform.addAttr("percentBig", at = "double", min = 0, max = 100, dv = 20, k = True)
        transform.addAttr("twinkle", at = "double", min = 0, max = 1, dv = .5, k = True)
        transform.addAttr("twinkleSpeed", at = "double", min = 0, dv = 4, k = True)

        p.addAttr("lifespanBig", at = "double", min = 0, dv = 2, k = True)
        p.addAttr("lifespanBigRand", at = "double", min = 0, dv = 1, k = True)
        p.addAttr("lifespanSmall", at = "double", min = 0, dv = .75, k = True)
        p.addAttr("lifespanSmallRand", at = "double", min = 0, dv = .37, k = True)
        p.addAttr("percentBig", at = "double", min = 0, max = 100, dv = 20, k = True)
        p.addAttr("twinkle", at = "double", min = 0, max = 1, dv = .5, k = True)
        p.addAttr("twinkleSpeed", at = "double", min = 0, dv = 4, k = True)

        #connect the attrs on transform to the attrs on the shape
        transform.lifespanBig.connect(p.lifespanBig)
        transform.lifespanBigRand.connect(p.lifespanBigRand)
        transform.lifespanSmall.connect(p.lifespanSmall)
        transform.lifespanSmallRand.connect(p.lifespanSmallRand)
        transform.percentBig.connect(p.percentBig)
        transform.twinkle.connect(p.twinkle)
        transform.twinkleSpeed.connect(p.twinkleSpeed)

        # set attributes
        p.particleRenderType.set(4)
        p.lifespanMode.set(3)
        p.radiusScaleInput.set(2)
        pm.setAttr("%s.radius"%p, .05)
        p.radiusScale[0].radiusScale_Position.set(.85)
        p.radiusScale[1].radiusScale_Position.set(1)
        p.radiusScale[1].radiusScale_FloatValue.set(0)
        p.radiusScaleRandomize.set(.25)

        # expression
        pm.dynExpression(p,
                         s=".noiseMod = rand(2);\nseed(.particleId);\nfloat $twinkle = ((noise(.age * .twinkleSpeed * .noiseMod) + 1) * .twinkle) / 2;\n\nif (.percentBig && .particleId % floor(100/.percentBig) == 0 && !.isChild)\n{\n    .isBig = 1;\n    .lifespanPP = .lifespanBig + rand(0 - .lifespanBigRand,.lifespanBigRand);\n    .rgbPP = <<1 - $twinkle, 0, 0 >>;\n}\nelse\n{\n   .isBig = 0;\n   .lifespanPP = .lifespanSmall + rand(0 - .lifespanSmallRand,.lifespanSmallRand);\n   .rgbPP = <<0, 0, 1 - $twinkle >>;\n}",
                         c=True)
        pm.dynExpression(p,
                         s="seed(.particleId);\nfloat $twinkle = ((noise(.age * .twinkleSpeed * .noiseMod) + 1) * .twinkle) / 2;\n\nif (.isBig){\n    .rgbPP = <<1 - $twinkle, 0, 0 >>;\n}\nelse {\n    .rgbPP = <<0, 0, 1 - $twinkle>>;\n}" ,
                         rbd=True)


def check_selection():
    # Check to make sure at least one nParticle system is selected
    sel = pm.ls(sl=True)

    if not sel:
        pm.displayWarning("Select a nParticle system to make TBS")
        return
    particles = []

    for s in sel:
        shapes = s.listRelatives(shapes=True)

        for shape in shapes:
            if shape.nodeType() == "nParticle":
                particles.append(shape)

    if not particles:
        pm.displayWarning("Select a nParticle system to make TBS")
        return

    return particles