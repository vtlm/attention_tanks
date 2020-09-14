from operator import itemgetter
from random import choice, randint
from direct.actor.Actor import Actor
from direct.interval.FunctionInterval import Func
from direct.interval.LerpInterval import LerpPosInterval, LerpHprInterval, LerpPosQuatInterval
from direct.interval.MetaInterval import Sequence, Parallel
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.bullet import BulletBoxShape, BulletGhostNode, BulletRigidBodyNode, BulletTriangleMesh, \
    BulletTriangleMeshShape
from panda3d.core import Vec3, Point3, BitMask32, NodePath
from helpers import getSize
from ParticlesWrapper import createParticlesEffect, ParticlesCtrl

__author__ = 'nezx'

# rocks=[]
movers=[]


def getObjectForNode(node):
    obj = next((x for x in movers if x.modNP.node() == node),None)
    return obj


def getObjectsForNodes(nodes):
    # print('search in:',list(movers))
    # print('search nodes:',list(nodes))
    objs=[getObjectForNode(n) for n in nodes]
    return objs


class MoverS(object):
    def __init__(self,base,world,modFileName,lanesList):
        self.base=base
        self.lanesList=lanesList
        self.world=base.world
        self.intLen=0.31
        self.cActors=[]

        self.worldNP=self.base.targetsNP#render.attachNewNode('worldNP')
        self.empNP=self.base.worldNP.attachNewNode('empNP')

        self.bm=self.base.loader.loadModel(modFileName)
        sz=getSize(self.bm)
        self.shape=BulletBoxShape(sz)
        # self.modNP=self.worldNP.attachNewNode(BulletRigidBodyNode('mod'))
        self.modNP=self.worldNP.attachNewNode(BulletGhostNode('modH'))
        self.modNP.node().addShape(self.shape)
        # self.modNP.node().setMass(20)
        # self.world.attachRigidBody(self.modNP.node())
        self.world.attach(self.modNP.node())
        self.bm.reparentTo(self.modNP)
        self.b=self.modNP

        whR=self.modNP.find('**/whR')

        # rw=self.loadWheelLayout()
        # rw.reparentTo(self.modNP)
        # lp=whR.getPos()
        # lp.setX(lp.getX() * -1)
        # rw.setPos(whR.getPos())
        # lw=self.loadWheelLayout()
        # lw.reparentTo(self.modNP)
        # lw.setPos(lp)

        # self.cActorW = Actor('qw.egg',
        #     {})
        # tb=getSize(self.cActorW).getY()

        # fw=self.bm.find('**/FirstWheel')
        # lw=self.bm.find('**/LastWheel')
        # fwPos=fw.getPos()
        # lwPos=lw.getPos()
        # vec3=fwPos-lwPos
        # dist=vec3.length()
        # whNumb=round(dist/tb)
        # gap=vec3/whNumb
        #
        # for i in range(0,whNumb+1):
        #     self.cActor = Actor('roadWheel',
        #         {})
        #     # self.cActor.setScale(4,4,4)
        #     self.cActor.reparentTo(self.modNP)
        #     self.cActor.setPos(fwPos-gap*i)
        #     self.myNodePath = self.cActor.controlJoint(None, "modelRoot", "Bone")
        #     # self.myNodePath1 = self.cActor.controlJoint(None, "modelRoot", "Bone.001")
        #     int=LerpHprInterval(self.myNodePath,1,Vec3(0,360,0))
        #     # int=LerpHprInterval(wheel,1,Vec3(0,360,0))
        #     # int=LerpHprInterval(wheel,1,Vec3(0,0,360))
        #     # int = LerpQuatInterval(wheel,1,Quat(3.14,Vec3(0,1,0)))
        #     int.loop()

        # wheels=self.bm.findAllMatches('**/wheel*')

        # self.ints=[]
        # for wheel in wheels:
        #     # int=LerpHprInterval(wheel,1,Vec3(360,0,0))
        #     # int=LerpHprInterval(wheel,1,Vec3(0,360,0))
        #     # int=LerpHprInterval(wheel,1,Vec3(0,0,360))
        #     int = LerpQuatInterval(wheel,1,Quat(3.14,Vec3(0,1,0)))
        #     int.loop()
        #     self.ints.append(int)

        # self.cActor = Actor('wheelBone',
        #     {})
        # # self.cActor.setScale(4,4,4)
        # self.cActor.reparentTo(self.modNP)
        # self.cActor.setPos(3, 0, 1)
        # print(self.cActor.listJoints())
        # self.turrNp = self.cActor.controlJoint(None, "root", "Bone")
        #
        # int=LerpHprInterval(self.turrNp,1,Vec3(0,360,0))
        # # int=LerpHprInterval(wheel,1,Vec3(0,360,0))
        # # int=LerpHprInterval(wheel,1,Vec3(0,0,360))
        # # int = LerpQuatInterval(wheel,1,Quat(3.14,Vec3(0,1,0)))
        # int.loop()

        # self.cActor = Actor('qw.egg',
        #     {})
        # # self.cActor.setScale(4,4,4)
        # self.cActor.reparentTo(self.modNP)
        # self.cActor.setPos(fw.getPos())
        # self.myNodePath = self.cActor.controlJoint(None, "modelRoot", "Bone")
        # # self.myNodePath1 = self.cActor.controlJoint(None, "modelRoot", "Bone.001")
        # int=LerpHprInterval(self.myNodePath,1,Vec3(0,180,0))
        # # int=LerpHprInterval(wheel,1,Vec3(0,360,0))
        # # int=LerpHprInterval(wheel,1,Vec3(0,0,360))
        # # int = LerpQuatInterval(wheel,1,Quat(3.14,Vec3(0,1,0)))
        # int.loop()

        # self.cActor = Actor('ca3.egg',
        #     {})
        # # self.cActor.setScale(4,4,4)
        # self.cActor.reparentTo(self.modNP)
        # self.cActor.setPos(3, 0, 0)
        # self.myNodePath = self.cActor.controlJoint(None, "modelRoot", "Bone")
        # self.myNodePath1 = self.cActor.controlJoint(None, "modelRoot", "Bone.001")
        # int=LerpHprInterval(self.myNodePath1,1,Vec3(0,360,0))
        # # int=LerpHprInterval(wheel,1,Vec3(0,360,0))
        # # int=LerpHprInterval(wheel,1,Vec3(0,0,360))
        # # int = LerpQuatInterval(wheel,1,Quat(3.14,Vec3(0,1,0)))
        # int.loop()

        self.currLane=choice(self.lanesList)
        self.destLane=choice(list(self.currLane.links))
        self.currDiscrSpline=self.currLane.linksDiscrSplines[self.destLane]

        self.initPos=self.currDiscrSpline[0][0]
        initHprT=self.currDiscrSpline[0][1]
        initHprV=Vec3(initHprT[0],initHprT[1],initHprT[2])
        self.initHpr=initHprV.getStandardizedHpr()
        self.b.setPos(Point3(self.initPos[0],self.initPos[1],self.initPos[2]))
        self.b.setHpr(self.initHpr)

        self.pInd=1
        self.destPosT=self.currDiscrSpline[self.pInd][0]
        initHprT=self.currDiscrSpline[self.pInd][1]
        initHprV=Vec3(initHprT[0],initHprT[1],initHprT[2])
        self.destHpr=initHprV.getStandardizedHpr()
        self.destPos=Point3(self.destPosT[0],self.destPosT[1],self.destPosT[2])
        self.pInd+=1

        # self.intrl=self.b.posInterval(self.intLen,Point3(self.destPos))
        # self.intrl=Sequence(LerpPosInterval(self.b,self.intLen,Point3(self.destPos),bakeInStart=0),
        # self.intrl=Sequence(LerpPosHprInterval(self.b,self.intLen,Point3(self.destPos),self.destHpr,bakeInStart=0),
        self.intrl=Sequence(LerpPosInterval(self.b,self.intLen,Point3(self.destPos),bakeInStart=0),
                            Func(self.intDone))

        self.intrl.start()
        self.done=False
        self.name='rem_'+str(id(self))
        # self.base.taskMgr.doMethodLater(3,self.makeShot,'shot',extraArgs=[])
        self.base.taskMgr.doMethodLater(randint(3,5),self.setDone,self.name,extraArgs=[])
        # self.base.taskMgr.doMethodLater(4,self.base.addToRemove,'rem',extraArgs=[self])

    def setDone(self):
        self.done=True

    def loadWheelLayout(self):
        layoutNP=self.base.loader.loadModel('wheelsLayout')

        self.cActorW = Actor('roadWheel',
            {})
        tb=getSize(self.cActorW).getY()

        fw=layoutNP.find('**/FirstWheel*')
        lw=layoutNP.find('**/LastWheel*')
        fwPos=fw.getPos()
        lwPos=lw.getPos()
        vec3=fwPos-lwPos
        dist=vec3.length()
        whNumb=round(dist/tb)
        gap=vec3/whNumb

        for i in range(0,whNumb+1):
            self.cActor = Actor('roadWheel',
                {})
            # self.cActor.setScale(4,4,4)
            self.cActor.reparentTo(layoutNP)
            self.cActor.setPos(fwPos-gap*i)
            # print(self.cActor.getPos())
            self.myNodePath = self.cActor.controlJoint(None, "modelRoot", "Bone")
            # self.myNodePath1 = self.cActor.controlJoint(None, "modelRoot", "Bone.001")
            int=LerpHprInterval(self.myNodePath,1,Vec3(0,-360,0))
            # int=LerpHprInterval(wheel,1,Vec3(0,360,0))
            # int=LerpHprInterval(wheel,1,Vec3(0,0,360))
            # int = LerpQuatInterval(wheel,1,Quat(3.14,Vec3(0,1,0)))
            int.loop()

        # cActorT=Actor('v2_001',{'run':'v2_001-Anim0'})
        # cActorT.reparentTo(layoutNP)
        # # self.cActorT.setX(2)
        # cActorT.loop('run')
        # self.cActors.append(cActorT)
        # c=cActorT.getAnimControl('run')
        # c.setPlayRate(-8)
        # # self.cActorT=Actor('t_004_005',{'run':'t_004_005-Anim0'})
        # # self.cActorT.reparentTo(self.modNP)
        # # self.cActorT.setX(2)
        # # self.cActorT.loop('run')
        cActorT=Actor('tr',{'run':'tr-Anim0'})
        cActorT.reparentTo(layoutNP)
        # self.cActorT.setX(2)
        cActorT.loop('run')
        self.cActors.append(cActorT)
        c=cActorT.getAnimControl('run')
        c.setPlayRate(8)

        cActorTB=Actor('btr',{'run':'btr-Anim0'})
        cActorTB.reparentTo(layoutNP)
        # self.cActorT.setX(2)
        cActorTB.loop('run')
        self.cActors.append(cActorTB)
        c=cActorTB.getAnimControl('run')
        c.setPlayRate(8)

        cActorTM=Actor('tr_mid',{'run':'tr_mid-Anim0'})
        cActorTM.reparentTo(layoutNP)
        # self.cActorT.setX(2)
        cActorTM.loop('run')
        self.cActors.append(cActorTM)
        c=cActorTM.getAnimControl('run')
        c.setPlayRate(8)
        # self.cActorT=Actor('t_004_005',{'run':'t_004_005-Anim0'})
        # self.cActorT.reparentTo(self.modNP)
        # self.cActorT.setX(2)
        # self.cActorT.loop('run')

        return layoutNP

    def removeFromWorlds(self):
        # self.tms.disable()
        # self.tms=None
        self.done=True
        self.intrl.clearIntervals()
        self.intrl.finish()
        self.world.remove(self.modNP.node())
        self.modNP.detachNode()
        # self.modNP.removeNode()

    def intDone(self):
        # print("posInt done!",self,self.destLane,id(self.lanesList))
        self.intrl.finish()
        if self.pInd == len(self.currDiscrSpline):
            #reload
            # print("reload")
            self.currLane=self.destLane
            self.destLane=choice(list(self.currLane.links))
            self.currDiscrSpline=self.currLane.linksDiscrSplines[self.destLane]

            # self.initPos=self.currDiscrSpline[0][0]
            # self.b.setPos(Point3(self.initPos[0],self.initPos[1],self.initPos[2]))
            self.pInd=1
            self.destPosT=self.currDiscrSpline[self.pInd][0]
            initHprT=self.currDiscrSpline[self.pInd][1]
            initHprV=Vec3(initHprT[0],initHprT[1],initHprT[2])
            self.destHpr=initHprV.getStandardizedHpr()
            self.pInd+=1
            self.destPos=Point3(self.destPosT[0],self.destPosT[1],self.destPosT[2])

            self.empNP.setPos(self.modNP.getPos())
            self.empNP.lookAt(self.destPos)
            q=self.empNP.getQuat()
            # self.intrl=Sequence(LerpPosInterval(self.b,self.intLen,Point3(self.destPos),bakeInStart=0),
            # self.intrl=Sequence(LerpPosHprInterval(self.b,self.intLen,Point3(self.destPos),self.destHpr,bakeInStart=0),
            self.intrl=Sequence(LerpPosInterval(self.b,self.intLen,Point3(self.destPos),bakeInStart=0),
                            Func(self.intDone))
            # self.b.lookAt(self.destPos)
            # self.b.setH(self.b.getH()+180)
            self.intrl.start()
        else:
            # print("continue",self.pInd)
            self.destPosT=self.currDiscrSpline[self.pInd][0]
            initHprT=self.currDiscrSpline[self.pInd][1]
            initHprV=Vec3(initHprT[0],initHprT[1],initHprT[2])
            self.destHpr=initHprV.getStandardizedHpr()
            self.pInd+=1
            self.destPos=Point3(self.destPosT[0],self.destPosT[1],self.destPosT[2])
            # print(self.destHpr)

            self.empNP.setPos(self.modNP.getPos())
            self.empNP.lookAt(self.destPos)
            self.q=self.empNP.getQuat()
            # self.intrl=self.b.posInterval(self.intLen,Point3(self.destPos))
            # self.intrl=Sequence(LerpPosInterval(self.b,self.intLen,Point3(self.destPos),bakeInStart=0),
            # self.intrl=Sequence(LerpPosHprInterval(self.b,self.intLen,Point3(self.destPos),self.destHpr,bakeInStart=0),
            # self.intrl=Sequence(LerpPosInterval(self.b,self.intLen,Point3(self.destPos),bakeInStart=0),
            #                 Func(self.intDone))
            self.intrl=Sequence(LerpPosQuatInterval(self.b,self.intLen,Point3(self.destPos),self.q,bakeInStart=0),
                            Func(self.intDone))

            # self.b.lookAt(self.destPos)
            # self.b.setH(self.b.getH()+180)
            self.intrl.start()


    # def addShooterCtrl(self,targets):
    #     self.tms=tmrAct(self.base,self.makeShot,3)
    #     # self.targets=targets

    def makeShot(self):

        if self.done:
            return

        targets=self.worldNP.getChildren()

        # for t in targs:
        #     print(t.getPos())
        # return

        #panda collision version
        # cs=CollisionSegment()
        # cs.setPointA(self.b.getPos()+Vec3(0,0,3))
        # fromObject=self.base.render.attachNewNode(CollisionNode(''))
        # fromObject.node().addSolid(cs)
        #
        # for t in self.targets:
        #     cs.setPointB(t.getPos())
        #     queue = CollisionHandlerQueue()
        #     traverser = CollisionTraverser('')
        #     traverser.addCollider(fromObject, queue)
        #     traverser.traverse(self.base.render)
        #     print(queue.getNumEntries())
        pFrom=self.b.getPos()+Vec3(0,0,3)
        for target in targets:
            if target != self.b:
                pTo=target.getPos()
                result = self.world.rayTestClosest(pFrom, pTo)
                # print (result.hasHit(),
                #       # result.getHitFraction(),
                #       result.getNode().getName(),
                #       # result.getHitPos(),
                #       result.getHitNormal())

                if result.hasHit() and result.getNode().getName() == 'modH':
                    # print('Shot!')
                    # target=choice(self.targets)
                    r=MoverR(self.base,'models/rocket',self.b.getPos()+Vec3(0,0,8),target)
                    movers.append(r)
                    break
                    #todo sel target from avail by dist,angle,power,damage, etc.

        self.base.taskMgr.doMethodLater(3,self.makeShot,'shot',extraArgs=[])

def createBNode(visNP,worldNP,world):
    sz=getSize(visNP)
    shape=BulletBoxShape(sz/2)
    # self.modNP=self.worldNP.attachNewNode(BulletRigidBodyNode('mod'))
    modNP=worldNP.attachNewNode(BulletGhostNode('modH'))
    modNP.node().addShape(shape)
    modNP.setCollideMask(BitMask32.bit(1))
    # self.modNP.node().setMass(20)
    world.attach(modNP.node())
    visNP.reparentTo(modNP)
    return modNP


class TankModelCtrl(object):
    def __init__(self,base,modFileName,ctrls):
        self.cActors=[]
        self.attackers=[]

        self.base=base
        self.worldNP=self.base.targetsNP#render.attachNewNode('worldNP')
        self.world=base.world

        self.visNP=Actor(modFileName,{})#,flattenable=False)
        hullJointNP = self.visNP.exposeJoint(None,"modelRoot","Bone")
        turretJointNP = self.visNP.exposeJoint(None,"modelRoot","turret")

        hullNP=self.loadHull()
        # hullNP.setColor(1,0,0,1)
        # hullNP.setColorScale(1,0,0,1)
        hullNP.reparentTo(hullJointNP)

        turretNP=self.base.loader.loadModel('turr')
        turretNP.reparentTo(turretJointNP)
        self.turrNp = self.visNP.controlJoint(None, "modelRoot", "turret")
        self.gunNp = self.visNP.controlJoint(None, "modelRoot", "mainGun")
        self.gunNpCoax = self.visNP.controlJoint(None, "modelRoot", "mainGunCoax")

        # self.int1=self.turrNp.hprInterval(3,Vec3(360,0,0))
        # self.int1.loop()
        # self.turrNp.setR(90)

        mainGunJointNP = self.visNP.exposeJoint(None,"modelRoot","mainGunCoax")
        # print(self.visNP.ls())
        mainGunNP=self.base.loader.loadModel('mainGun')
        mainGunNP.reparentTo(mainGunJointNP)
        self.fireNode=mainGunNP.find('**/fireNode*')
        self.smokeNode=mainGunNP.find('**/smokeNode*')

        # self.int=self.gunNp.hprInterval(3,Vec3(0,360,0))
        # self.int.loop()

        self.modNP=createBNode(self.visNP,self.worldNP,self.world)
        self.b=self.modNP

        self.targPointerNP=self.modNP.attachNewNode('targPtr')
        # mod=self.base.loader.loadModel('arrow')
        # mod.reparentTo(self.targPointerNP)
        # mod.setZ(3)
        # mod.setScale(2)


        self.mySound = self.base.audio3d.loadSfx('engS2.ogg')
        self.fireSound = self.base.audio3d.loadSfx('tank_firing_001.ogg')
        self.base.audio3d.attachSoundToObject(self.mySound, self.modNP)
        self.mySound.setLoop(True)
        self.mySound.play()

        self.done=False
        self.name='rem_'+str(id(self))

        self.int3=self.gunNpCoax.posInterval(0.1,Vec3(0,-1,0))
        self.int4=self.gunNpCoax.posInterval(0.6,Vec3(0,0,0))

        if 'shootsEnable' in ctrls:
            self.base.taskMgr.doMethodLater(3,self.makeShot,'shot'+self.name,extraArgs=[])
        # self.base.taskMgr.doMethodLater(randint(3,5),self.setDone,self.name,extraArgs=[])
        # self.base.taskMgr.doMethodLater(4,self.base.addToRemove,'rem',extraArgs=[self])

        if TankMover in ctrls:
            self.moveCtrl=TankMover(base,self.b)

        # self.cActorW = Actor('qw.egg',
        #     {})
        # tb=getSize(self.cActorW).getY()

        # fw=self.bm.find('**/FirstWheel')
        # lw=self.bm.find('**/LastWheel')
        # fwPos=fw.getPos()
        # lwPos=lw.getPos()
        # vec3=fwPos-lwPos
        # dist=vec3.length()
        # whNumb=round(dist/tb)
        # gap=vec3/whNumb
        #
        # for i in range(0,whNumb+1):
        #     self.cActor = Actor('roadWheel',
        #         {})
        #     # self.cActor.setScale(4,4,4)
        #     self.cActor.reparentTo(self.modNP)
        #     self.cActor.setPos(fwPos-gap*i)
        #     self.myNodePath = self.cActor.controlJoint(None, "modelRoot", "Bone")
        #     # self.myNodePath1 = self.cActor.controlJoint(None, "modelRoot", "Bone.001")
        #     int=LerpHprInterval(self.myNodePath,1,Vec3(0,360,0))
        #     # int=LerpHprInterval(wheel,1,Vec3(0,360,0))
        #     # int=LerpHprInterval(wheel,1,Vec3(0,0,360))
        #     # int = LerpQuatInterval(wheel,1,Quat(3.14,Vec3(0,1,0)))
        #     int.loop()

        # wheels=self.bm.findAllMatches('**/wheel*')

        # self.ints=[]
        # for wheel in wheels:
        #     # int=LerpHprInterval(wheel,1,Vec3(360,0,0))
        #     # int=LerpHprInterval(wheel,1,Vec3(0,360,0))
        #     # int=LerpHprInterval(wheel,1,Vec3(0,0,360))
        #     int = LerpQuatInterval(wheel,1,Quat(3.14,Vec3(0,1,0)))
        #     int.loop()
        #     self.ints.append(int)

        # self.cActor = Actor('wheelBone',
        #     {})
        # # self.cActor.setScale(4,4,4)
        # self.cActor.reparentTo(self.modNP)
        # self.cActor.setPos(3, 0, 1)
        # print(self.cActor.listJoints())
        # self.turrNp = self.cActor.controlJoint(None, "root", "Bone")
        #
        # int=LerpHprInterval(self.turrNp,1,Vec3(0,360,0))
        # # int=LerpHprInterval(wheel,1,Vec3(0,360,0))
        # # int=LerpHprInterval(wheel,1,Vec3(0,0,360))
        # # int = LerpQuatInterval(wheel,1,Quat(3.14,Vec3(0,1,0)))
        # int.loop()

        # self.cActor = Actor('qw.egg',
        #     {})
        # # self.cActor.setScale(4,4,4)
        # self.cActor.reparentTo(self.modNP)
        # self.cActor.setPos(fw.getPos())
        # self.myNodePath = self.cActor.controlJoint(None, "modelRoot", "Bone")
        # # self.myNodePath1 = self.cActor.controlJoint(None, "modelRoot", "Bone.001")
        # int=LerpHprInterval(self.myNodePath,1,Vec3(0,180,0))
        # # int=LerpHprInterval(wheel,1,Vec3(0,360,0))
        # # int=LerpHprInterval(wheel,1,Vec3(0,0,360))
        # # int = LerpQuatInterval(wheel,1,Quat(3.14,Vec3(0,1,0)))
        # int.loop()

        # self.cActor = Actor('ca3.egg',
        #     {})
        # # self.cActor.setScale(4,4,4)
        # self.cActor.reparentTo(self.modNP)
        # self.cActor.setPos(3, 0, 0)
        # self.myNodePath = self.cActor.controlJoint(None, "modelRoot", "Bone")
        # self.myNodePath1 = self.cActor.controlJoint(None, "modelRoot", "Bone.001")
        # int=LerpHprInterval(self.myNodePath1,1,Vec3(0,360,0))
        # # int=LerpHprInterval(wheel,1,Vec3(0,360,0))
        # # int=LerpHprInterval(wheel,1,Vec3(0,0,360))
        # # int = LerpQuatInterval(wheel,1,Quat(3.14,Vec3(0,1,0)))
        # int.loop()

    def loadHull(self):
        hullNP=self.base.loader.loadModel('hull')
        # print(hullNP.ls())
        modNP=createBNode(hullNP,self.worldNP,self.world)

        whR=hullNP.find('**/whR*')

        rw=self.loadWheelLayout()
        rw.reparentTo(hullNP)
        lp=whR.getPos()
        lp.setX(lp.getX() * -1)
        rw.setPos(whR.getPos())
        lw=self.loadWheelLayout()
        lw.reparentTo(hullNP)
        lw.setPos(lp)

        return modNP

    def loadWheelLayout(self):
        layoutNP=self.base.loader.loadModel('wheelsLayout')

        self.cActorW = Actor('roadWheel',
            {})
        tb=getSize(self.cActorW).getY()

        fw=layoutNP.find('**/FirstWheel*')
        lw=layoutNP.find('**/LastWheel*')
        fwPos=fw.getPos()
        lwPos=lw.getPos()
        vec3=fwPos-lwPos
        dist=vec3.length()
        whNumb=round(dist/tb)
        gap=vec3/whNumb

        for i in range(0,whNumb+1):
            self.cActor = Actor('roadWheel',
                {})
            # self.cActor.setScale(4,4,4)
            self.cActor.reparentTo(layoutNP)
            self.cActor.setPos(fwPos-gap*i)
            self.cActor.setShaderAuto()
            # print(self.cActor.getPos())
            self.myNodePath = self.cActor.controlJoint(None, "modelRoot", "Bone")
            self.myNodePath.setP(randint(-180,180))
            # self.myNodePath1 = self.cActor.controlJoint(None, "modelRoot", "Bone.001")
            int=LerpHprInterval(self.myNodePath,1,Vec3(0,-360,0))
            # int=LerpHprInterval(wheel,1,Vec3(0,360,0))
            # int=LerpHprInterval(wheel,1,Vec3(0,0,360))
            # int = LerpQuatInterval(wheel,1,Quat(3.14,Vec3(0,1,0)))
            int.loop()

        # cActorT=Actor('v2_001',{'run':'v2_001-Anim0'})
        # cActorT.reparentTo(layoutNP)
        # # self.cActorT.setX(2)
        # cActorT.loop('run')
        # self.cActors.append(cActorT)
        # c=cActorT.getAnimControl('run')
        # c.setPlayRate(-8)
        # # self.cActorT=Actor('t_004_005',{'run':'t_004_005-Anim0'})
        # # self.cActorT.reparentTo(self.modNP)
        # # self.cActorT.setX(2)
        # # self.cActorT.loop('run')
        cActorT=Actor('tr',{'run':'tr-Anim0'})
        cActorT.reparentTo(layoutNP)
        # self.cActorT.setX(2)
        cActorT.loop('run')
        self.cActors.append(cActorT)
        c=cActorT.getAnimControl('run')
        c.setPlayRate(8)

        cActorTB=Actor('btr',{'run':'btr-Anim0'})
        cActorTB.reparentTo(layoutNP)
        # self.cActorT.setX(2)
        cActorTB.loop('run')
        self.cActors.append(cActorTB)
        c=cActorTB.getAnimControl('run')
        c.setPlayRate(8)

        cActorTM=Actor('tr_mid',{'run':'tr_mid-Anim0'})
        cActorTM.reparentTo(layoutNP)
        # self.cActorT.setX(2)
        cActorTM.loop('run')
        self.cActors.append(cActorTM)
        c=cActorTM.getAnimControl('run')
        c.setPlayRate(8)
        # self.cActorT=Actor('t_004_005',{'run':'t_004_005-Anim0'})
        # self.cActorT.reparentTo(self.modNP)
        # self.cActorT.setX(2)
        # self.cActorT.loop('run')

        # p=createParticlesEffect(self.base)
        # p.reparentTo(layoutNP)

        return layoutNP

    def setDone(self):
        self.done=True

    def getTarget(self):
        targets=self.worldNP.getChildren()
            #todo sel target from avail by dist,angle,power,damage, etc.
        # for t in targs:
        #     print(t.getPos())
        # return

        #panda collision version
        # cs=CollisionSegment()
        # cs.setPointA(self.b.getPos()+Vec3(0,0,3))
        # fromObject=self.base.render.attachNewNode(CollisionNode(''))
        # fromObject.node().addSolid(cs)
        #
        # for t in self.targets:
        #     cs.setPointB(t.getPos())
        #     queue = CollisionHandlerQueue()
        #     traverser = CollisionTraverser('')
        #     traverser.addCollider(fromObject, queue)
        #     traverser.traverse(self.base.render)
        #     print(queue.getNumEntries())
        pFrom=self.b.getPos()+Vec3(0,0,3)
        for target in targets:
            if target != self.b:
                pTo=target.getPos()
                result = self.world.rayTestClosest(pFrom, pTo)
                # print (result.hasHit(),
                #       # result.getHitFraction(),
                #       result.getNode().getName(),
                #       # result.getHitPos(),
                #       result.getHitNormal())
                # print(result.getNode().getName())
                # print(self.b.getPos(),pTo)

                if result.hasHit() and result.getNode().getName() == 'modH':
                    return target

        return None

    def doAim(self,target,shotEnable=True):
        if isinstance(target,NodePath):
            pTo=target.getPos()
        elif isinstance(target,Point3):
            pTo=target

        # print('Shot!')
        # target=choice(self.targets)

        # c=self.base.loader.loadModel('c')
        # c.reparentTo(self.base.worldNP)
        # c.setPos(pTo)

        self.targPointerNP.lookAt(self.base.worldNP,pTo,Vec3(0,0,1))
        # self.base.taskMgr.doMethodLater(0.3,self.makeShot,'shot',extraArgs=[])
        # return

        # self.moveDirEmpNP.setPos(self.b.getPos())
        # self.moveDirEmpNP.lookAt(self.base.worldNP,pTo,Vec3(0,0,1))
        hc=self.turrNp.getH(self.base.worldNP)
        # hc=self.modNP.getH(self.base.worldNP)
        # h=self.moveDirEmpNP.getH()
        #
        # #dbg
        # # self.turrNp.setH(self.base.worldNP,h)
        # # print(hc)
        # dh=h-hc
        # newH=hc+dh
        newH=self.targPointerNP.getH()
        dh=newH-hc
        # self.turrNp.setH(self.targPointerNP.getH())
        grPerSec=130
        hTime=abs(dh)/grPerSec
        # p=self.moveDirEmpNP.getP()
        p=self.targPointerNP.getP()
        # self.turrNp.setH(self.moveDirEmpNP.getH())
        int=self.turrNp.hprInterval(hTime,Vec3(newH,0,0),blendType='easeInOut')# setH(self.moveDirEmpNP.getH())
        # int.start()
        int2=self.gunNp.hprInterval(0.7,Vec3(0,p,0))# setH(self.moveDirEmpNP.getH())
        # int2.start()
        p=Parallel(int,int2)
        # self.sec4.start()

        # self.shotSeq=Sequence(p,Func(self.doShot,target),self.int3,self.int4)
        self.shotSeq=Sequence(p,Func(self.doShot,target),self.int3,self.int4)
        self.shotSeq.start()


    def doShot(self,target):

        if isinstance(target,NodePath) and target.node():
            if isinstance(target.node(),BulletGhostNode):
                obj=getObjectForNode(target.node())
        elif isinstance(target,Point3):
            obj=target
        else:
            obj=None
        if obj:
            startPos=self.fireNode.getPos(self.base.worldNP)
            startPosS=self.smokeNode.getPos(self.base.worldNP)
            # r=MoverR(self.base,'models/rocket',self.b.getPos()+Vec3(0,0,8),obj)
            r=MoverR(self.base,'models/rocket',startPos,obj)
            movers.append(r)
            if isinstance(obj,TankModelCtrl):
                obj.attackers.append(r)
            self.fireSound.play()
            # ParticlesCtrl(self.base,pos=startPosS)
            # self.int3=self.gunNpCoax.posInterval(0.1,Vec3(0,-1,0))
            # self.int4=self.gunNpCoax.posInterval(0.6,Vec3(0,0,0))
            # self.shotBack=Sequence(self.int3,self.int4,'shotBack')
            # self.shotBack.start()

            if hasattr(self.base,'cc') and self.base.cc.free:
                print('New launch:')
                self.base.cc.setOnRocket(r)
                self.base.cc.free=False


    def makeShot(self):

        if self.done:
            return

        target=self.getTarget()

        if target:
            self.doAim(target)

        self.base.taskMgr.doMethodLater(3.3,self.makeShot,'shot',extraArgs=[])

    def updateAttackers(self):
        self.dists=[attack.getDistanceToTarget() for attack in self.attackers]
        self.distAttacks=zip(self.dists,self.attackers)
        self.distAttacks=sorted(self.distAttacks,key=itemgetter(0))

    def getNearestAttackerDistance(self):
        self.updateAttackers()
        return self.distAttacks[0][0]

    def isNearestAttackerFarthestThan(self,dist):
        if not self.attackers:
            return False
        return self.getNearestAttackerDistance() > dist

    def removeFromWorlds(self):
        # self.tms.disable()
        # self.tms=None
        self.done=True
        if hasattr(self,'shotSeq'):
            self.shotSeq.finish()
        self.base.audio3d.detachSound(self.mySound)
        self.moveCtrl.retire()
        # self.wr.remove()
        self.world.remove(self.modNP.node())
        # self.modNP.detachNode()
        self.modNP.removeNode()


class TankMover(object):
    def __init__(self,base,nodePath):
        self.base=base
        self.lanesList=base.roadLanesSections

        self.intLen=0.31

        self.worldNP=self.base.targetsNP#render.attachNewNode('worldNP')
        self.world=base.world

        # self.tm=TankModelCtrl(base,modFileName)
        self.b=nodePath

        self.moveDirEmpNP=self.base.worldNP.attachNewNode('empNP')
        # self.audNP=self.base.worldNP.attachNewNode('audNP')
        # self.visNP1=self.base.loader.loadModel(modFileName)

        self.currLane=choice(self.lanesList)
        self.destLane=choice(list(self.currLane.links))
        self.currDiscrSpline=self.currLane.linksDiscrSplines[self.destLane]

        self.initPos=self.currDiscrSpline[0][0]
        initHprT=self.currDiscrSpline[0][1]
        initHprV=Vec3(initHprT[0],initHprT[1],initHprT[2])
        self.initHpr=initHprV.getStandardizedHpr()
        self.b.setPos(Point3(self.initPos[0],self.initPos[1],self.initPos[2]))
        self.b.setHpr(self.initHpr)

        self.pInd=1
        self.destPosT=self.currDiscrSpline[self.pInd][0]
        initHprT=self.currDiscrSpline[self.pInd][1]
        initHprV=Vec3(initHprT[0],initHprT[1],initHprT[2])
        self.destHpr=initHprV.getStandardizedHpr()
        self.destPos=Point3(self.destPosT[0],self.destPosT[1],self.destPosT[2])
        self.pInd+=1

        # self.intrl=self.b.posInterval(self.intLen,Point3(self.destPos))
        # self.intrl=Sequence(LerpPosInterval(self.b,self.intLen,Point3(self.destPos),bakeInStart=0),
        # self.intrl=Sequence(LerpPosHprInterval(self.b,self.intLen,Point3(self.destPos),self.destHpr,bakeInStart=0),
        self.intrl=Sequence(LerpPosInterval(self.b,self.intLen,Point3(self.destPos),bakeInStart=0),
                            Func(self.intDone))

        self.intrl.start()

    def intDone(self):
        # print("posInt done!",self,self.destLane,id(self.lanesList))
        self.intrl.finish()
        if self.pInd == len(self.currDiscrSpline):
            #reload
            # print("reload")
            self.currLane=self.destLane
            self.destLane=choice(list(self.currLane.links))
            self.currDiscrSpline=self.currLane.linksDiscrSplines[self.destLane]

            # self.initPos=self.currDiscrSpline[0][0]
            # self.b.setPos(Point3(self.initPos[0],self.initPos[1],self.initPos[2]))
            self.pInd=1
            self.destPosT=self.currDiscrSpline[self.pInd][0]
            initHprT=self.currDiscrSpline[self.pInd][1]
            initHprV=Vec3(initHprT[0],initHprT[1],initHprT[2])
            self.destHpr=initHprV.getStandardizedHpr()
            self.pInd+=1
            self.destPos=Point3(self.destPosT[0],self.destPosT[1],self.destPosT[2])

            self.moveDirEmpNP.setPos(self.b.getPos())
            self.moveDirEmpNP.lookAt(self.destPos)
            q=self.moveDirEmpNP.getQuat()
            # self.intrl=Sequence(LerpPosInterval(self.b,self.intLen,Point3(self.destPos),bakeInStart=0),
            # self.intrl=Sequence(LerpPosHprInterval(self.b,self.intLen,Point3(self.destPos),self.destHpr,bakeInStart=0),
            self.intrl=Sequence(LerpPosInterval(self.b,self.intLen,Point3(self.destPos),bakeInStart=0),
                            Func(self.intDone))
            # self.b.lookAt(self.destPos)
            # self.b.setH(self.b.getH()+180)
            self.intrl.start()
        else:
            # print("continue",self.pInd)
            self.destPosT=self.currDiscrSpline[self.pInd][0]
            initHprT=self.currDiscrSpline[self.pInd][1]
            initHprV=Vec3(initHprT[0],initHprT[1],initHprT[2])
            self.destHpr=initHprV.getStandardizedHpr()
            self.pInd+=1
            self.destPos=Point3(self.destPosT[0],self.destPosT[1],self.destPosT[2])
            # print(self.destHpr)

            self.moveDirEmpNP.setPos(self.b.getPos())
            self.moveDirEmpNP.lookAt(self.destPos)
            self.q=self.moveDirEmpNP.getQuat()
            # self.intrl=self.b.posInterval(self.intLen,Point3(self.destPos))
            # self.intrl=Sequence(LerpPosInterval(self.b,self.intLen,Point3(self.destPos),bakeInStart=0),
            # self.intrl=Sequence(LerpPosHprInterval(self.b,self.intLen,Point3(self.destPos),self.destHpr,bakeInStart=0),
            # self.intrl=Sequence(LerpPosInterval(self.b,self.intLen,Point3(self.destPos),bakeInStart=0),
            #                 Func(self.intDone))
            self.intrl=Sequence(LerpPosQuatInterval(self.b,self.intLen,Point3(self.destPos),self.q,bakeInStart=0),
                            Func(self.intDone))

            # self.b.lookAt(self.destPos)
            # self.b.setH(self.b.getH()+180)
            self.intrl.start()

            # self.audNP.setPos(self.modNP.getPos())


    # def addShooterCtrl(self,targets):
    #     self.tms=tmrAct(self.base,self.makeShot,3)
    #     # self.targets=targets
    def retire(self):
        self.intrl.clearIntervals()
        self.intrl.finish()


class MoverC(object):
    def __init__(self,base,b):
        self.base=base
        self.b=b
        self.cmove()

    def cmove(self):
        r=100
        newPos=Point3(randint(-r,r),randint(-r,r),randint(-r,r))
        self.s=Sequence(LerpPosInterval(self.b,5,newPos),
                   Func(self.cmove))
        self.s.start()


class MoverR(object):
    def __init__(self,base,modFileName,srcPos,targetObj):
        self.base=base
        # self.b=self.base.loader.loadModel(modFileName)
        # self.b.reparentTo(self.base.render)
        # self.b.setPos(srcPos)
        self.targetObj=targetObj

        if isinstance(self.targetObj,TankModelCtrl):
            self.target=targetObj.b
        elif isinstance(self.targetObj,Point3):
            self.target=targetObj

        self.bm=self.base.loader.loadModel(modFileName)
        sz=getSize(self.bm)
        self.shape=BulletBoxShape(sz/8)#Vec3(sz,sz,sz))
        # self.modNP=self.worldNP.attachNewNode(BulletRigidBodyNode('mod'))
        # self.modNP=self.base.worldNP.attachNewNode(BulletGhostNode('Rock'))
        self.modNP=self.base.worldNP.attachNewNode(BulletRigidBodyNode('Rock'))
        self.modNP.node().addShape(self.shape)
        self.modNP.setCollideMask(BitMask32.bit(1))

        # self.modNP.node().setMass(20)
        # self.world.attachRigidBody(self.modNP.node())
        # self.base.world.attachGhost(self.modNP.node())
        self.base.world.attach(self.modNP.node())
        self.bm.reparentTo(self.modNP)
        self.b=self.modNP
        # p=createParticlesEffect(self.base)
        # p.reparentTo(self.modNP)
        self.b.setPos(srcPos)

        self.done=False

        # self.tms=tmrAct(self.base,self.removeFromWorlds,4)
        self.name='rem_'+str(id(self))
        # print(name)

        self.base.taskMgr.doMethodLater(6,self.setDone,self.name,extraArgs=['timeout'])
        # self.base.taskMgr.doMethodLater(4,self.base.addToRemove,'rem',extraArgs=[self])

        self.cmove()

    def getTargetPos(self):
        if isinstance(self.targetObj,TankModelCtrl):
            return self.targetObj.b.getPos()
        elif isinstance(self.targetObj,Point3):
            return self.targetObj

    def setDone(self,mess='hit'):
        # print(mess)
        self.done=True

    def getDistanceToTarget(self):
        if self.target:
            targPos=self.getTargetPos()#target.getPos()
            cPos=self.b.getPos()
            dlt=cPos-targPos
            return cPos.lengthSquared()
        else:
            return None

    def removeFromWorlds(self):
        # self.tms.disable()
        # self.tms=None
        if self.modNP:
            if isinstance(self.targetObj,TankModelCtrl):
                self.targetObj.attackers.remove(self)
            if self.modNP.find('camBaseNP'):
                self.base.cc.free=True
            self.base.taskMgr.remove(self.name)
            # movers.remove(self)
            self.s.clearIntervals()
            self.s.finish()
            self.base.world.remove(self.modNP.node())
            self.modNP.removeNode()
        else:
            print('already remd')

    def cmove(self):
        cPos=self.b.getPos()
        if self.target:
            targPos=self.getTargetPos()#self.target.getPos()
            self.dir=targPos-cPos
            self.dir.normalize()
        newPos=cPos+self.dir*10
        self.b.lookAt(newPos)
        self.s=Sequence(LerpPosInterval(self.b,0.1,newPos),
                   Func(self.cmove))
        self.s.start()

    def checkForRemove(self,toRem):
        # lg=self.base.world.getGhosts()
        exists = self.modNP.node() in toRem
        if exists:
            # self.s.clearIntervals()
            # self.s.finish()
            # self.modNP.removeNode()
            # self.removeFromWorlds()
            return True
        return False
        # return self.modNP.node()#getNumChildren()


class MoverT(object):
    def __init__(self,base,modFileName,srcPos,target):
        self.base=base
        # self.b=self.base.loader.loadModel(modFileName)
        # self.b.reparentTo(self.base.render)
        # self.b.setPos(srcPos)
        self.target=target

        self.visNP=self.base.loader.loadModel(modFileName)

        self.wr=BulletNodeWrapper(base,self.visNP)


        # sz=getSize(self.bm)
        # self.shape=BulletBoxShape(sz)#Vec3(sz,sz,sz))
        # # self.modNP=self.worldNP.attachNewNode(BulletRigidBodyNode('mod'))
        # self.modNP=self.base.worldNP.attachNewNode(BulletGhostNode('Rock'))
        # self.modNP.node().addShape(self.shape)
        # # self.modNP.node().setMass(20)
        # # self.world.attachRigidBody(self.modNP.node())
        # self.base.world.attachGhost(self.modNP.node())
        # self.bm.reparentTo(self.modNP)
        # self.b=self.modNP

        self.wr.modNP.setPos(srcPos)

        self.done=False

        # self.tms=tmrAct(self.base,self.removeFromWorlds,4)
        self.name='rem_'+str(id(self))
        # print(name)

        # print(self.base)
        # self.base.doMethodLater(3,self.setDone,self.name,extraArgs=[])
        # self.base.doMethodLater(4,self.base.addToRemove,'rem',extraArgs=[self])

        # self.cmove()

    def setDone(self):
        self.done=True

    def removeFromWorlds(self):
        self.wr.remove()


    def cmove(self):
        cPos=self.b.getPos()
        if self.target:
            targPos=self.target.getPos()
            self.dir=targPos-cPos
            self.dir.normalize()
        newPos=cPos+self.dir*10
        self.b.lookAt(newPos)
        self.s=Sequence(LerpPosInterval(self.b,0.5,newPos),
                   Func(self.cmove))
        self.s.start()

    def checkForRemove(self,toRem):
        # lg=self.base.world.getGhosts()
        exists = self.modNP.node() in toRem
        if exists:
            # self.s.clearIntervals()
            # self.s.finish()
            # self.modNP.removeNode()
            # self.removeFromWorlds()
            return True
        return False
        # return self.modNP.node()#getNumChildren()


# class tmrAct(object):
#     def __init__(self,base,func,time):
#         self.base=base
#         self.func=func
#         self.time=time
#         self.goingTime=0
#         self.disabled=False
#
#         self.base.taskMgr.add(self.update, 'updateWorld')
#
#     def update(self,task):
#         if not self.disabled:
#             self.goingTime += globalClock.getDt()
#             if self.goingTime > self.time:
#                 # print('upd',self)
#                 self.goingTime=0
#                 self.func()
#             return task.again
#
#     def disable(self):
#         self.disabled=True


class BulletNodeWrapper(object):
    def __init__(self,base,visNP,initPos=None,startVel=None,particleEffectConfig=None,lifeTime=None):
        self.base=base
        self.visNP=visNP

        sz=getSize(self.visNP)
        sz=sz/2
        self.shape=BulletBoxShape(sz)
        self.modNP=self.base.worldNP.attachNewNode(BulletRigidBodyNode('mod'))
        self.modNP.setCollideMask(BitMask32.bit(2))

        # print(visNP.getPos(base.render))
        # self.modNP.setPos(visNP.getPos())
        # visNP.setPos(0,0,0)

        # self.modNP=self.base.worldNP.attachNewNode(BulletGhostNode('modH'))
        self.modNP.node().addShape(self.shape)
        self.modNP.node().setMass(200)
        # self.world.attachRigidBody(self.modNP.node())
        self.base.world.attach(self.modNP.node())
        self.visNP.reparentTo(self.modNP)

        if initPos:
            self.modNP.setPos(initPos)

        if startVel:
            self.modNP.node().setLinearVelocity(startVel)
            self.modNP.node().applyTorqueImpulse(startVel)

        # if particleEffectConfig:
        #     p = createParticlesEffect(self.base)
        #     p.reparentTo(self.modNP)

        if lifeTime:
            name='rem_'+str(id(self))
            # print(name)
            self.base.taskMgr.doMethodLater(lifeTime,self.remove,name,extraArgs=[])

    def remove(self):
        self.base.world.remove(self.modNP.node())
        self.modNP.removeNode()
        #todo add remove visNP


class BulletNodeMeshWrapper(object):
    def __init__(self,base,visNP,initPos=None,startVel=None,particleEffectConfig=None,lifeTime=None):
        self.base=base
        self.bm=visNP
        # sz=getSize(self.bm)
        # self.shape=BulletBoxShape(sz)
        # print(visNP.getName())
        self.modNP=self.base.worldNP.attachNewNode(BulletRigidBodyNode(visNP.getName()))

        geom = visNP.node().getGeom(0)
        mesh = BulletTriangleMesh()
        mesh.addGeom(geom)
        self.shape = BulletTriangleMeshShape(mesh, dynamic=False)

        # print(visNP.getPos(base.render))
        # self.modNP.setPos(visNP.getPos())
        # visNP.setPos(0,0,0)

        # self.modNP=self.base.worldNP.attachNewNode(BulletGhostNode('modH'))
        self.modNP.node().addShape(self.shape)
        # self.modNP.node().setMass(20)
        # self.world.attachRigidBody(self.modNP.node())
        self.base.world.attach(self.modNP.node())
        self.bm.reparentTo(self.modNP)

        if initPos:
            self.modNP.setPos(initPos)

        if startVel:
            self.modNP.node().setLinearVelocity(startVel)
            self.modNP.node().applyTorqueImpulse(startVel)

        if particleEffectConfig:
            p = ParticleEffect()
            p.loadConfig(particleEffectConfig)
            p.reparentTo(self.modNP)
            p.start()

        if lifeTime:
            self.base.taskMgr.doMethodLater(lifeTime,self.remove,'rem',extraArgs=[])

    def remove(self):
        self.base.world.remove(self.modNP.node())
        self.modNP.removeNode()
        #todo add remove visNP