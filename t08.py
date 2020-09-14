'''
todo
fix turret straight
remove box target aim
separate shot
+add reverse movement
add track target
set rockets to follow targets or far than target
'''
from random import random, randint, randrange, uniform, choice
import pickle
from direct.actor.Actor import Actor
from direct.filter.CommonFilters import CommonFilters
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.showbase import Audio3DManager
from direct.showbase.InputStateGlobal import inputState

from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld, BulletRigidBodyNode, BulletConvexHullShape, BulletDebugNode, BulletBoxShape, \
    BulletVehicle, ZUp
from panda3d.core import Vec3, BitMask32, AmbientLight, Vec4, DirectionalLight, Point3, TextureStage, Fog, \
    TransformState, TransparencyAttrib
import sys
from CamCtrl import CamCtrl
import llf
import mover

from mover import MoverS, movers, BulletNodeWrapper, BulletNodeMeshWrapper, MoverT, TankMover, MoverR

#tmp stub
sys.path.append('/media/50G/v/src/py/City_Py_OCC')

camAuto=True
bulletDebugDisplay=False


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.toRemove=[]
        self.toExpl=[]

        # self.forwardMovement=True
        self.speedSign=1
        self.deltaX=0
        self.deltaY=0
        self.mouseLookSpeed = [0.1, 0.1]
        self.targetWin=self.win

        # filters = CommonFilters(self.win, self.cam)
        # filters.setBloom(blend=(0, 0, 0, 1), desat=-0.5, intensity=3.0, size="small")

        self.roadLanesSections=self.loadPaths()

        self.setup()
        self.setupBulletVehicle()

        # self.m = self.loader.loadModel('skyBox')
        # scale=14000
        # self.m.setScale(scale,scale,scale)
        # self.m.reparentTo(self.render)

        # Input
        self.accept('escape', self.doExit)
        # self.accept('r', self.doReset)
        # self.accept('v', self.doViewReset)
        # self.accept('f1', self.toggleWireframe)
        # self.accept('f2', self.toggleTexture)
        # self.accept('f3', self.toggleDebug)
        # self.accept('f5', self.doScreenshot)

        self.accept("wheel_up", self.moveCamera, extraArgs = [Vec3(0, 1, 0)])
        self.accept("wheel_down", self.moveCamera, extraArgs = [Vec3(0, -1, 0)])

        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('turnLeft', 'q')
        inputState.watchWithModifiers('turnRight', 'e')
        inputState.watchWithModifiers('backward', 'r')

        self.accept("mouse1",self.mouseTask1)
        self.accept("mouse3",self.mouseTask3)
        # Task
        self.taskMgr.add(self.update, 'updateWorld')

        # self.testExpl()
        self.addMachine()

        if camAuto:
            self.cc=CamCtrl(self)
            self.cc.free=False
            # self.cc.lookOnRocket()
            self.cc.switch()

    def doExit(self):
        # self.cleanup()
        sys.exit(1)

    def moveCamera(self, vector):
        self.cam.setPos(self.cam, vector * 2)

    def getRandomPlace(self):
        self.currLane=choice(self.roadLanesSections)
        self.destLane=choice(list(self.currLane.links))
        self.currDiscrSpline=self.currLane.linksDiscrSplines[self.destLane]

        self.initPos=self.currDiscrSpline[0][0]
        # initHprT=self.currDiscrSpline[0][1]
        # initHprV=Vec3(initHprT[0],initHprT[1],initHprT[2])
        # self.initHpr=initHprV.getStandardizedHpr()
        # self.b.setPos(Point3(self.initPos[0],self.initPos[1],self.initPos[2]))
        return Point3(self.initPos[0],self.initPos[1],self.initPos[2])
        # self.b.setHpr(self.initHpr)

    def setup(self):
        # self.setBackgroundColor(0.1, 0.1, 0.8, 1)
        self.setFrameRateMeter(True)

        self.setupBaseLighting()

        self.worldNP = self.render.attachNewNode('World')
        self.targetsNP = self.worldNP.attachNewNode('targets')

        # World
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        #bullet debug display
        if bulletDebugDisplay:
            self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
            self.debugNP.show()
            self.debugNP.node().showWireframe(True)
            self.debugNP.node().showConstraints(True)
            self.debugNP.node().showBoundingBoxes(False)
            self.debugNP.node().showNormals(True)

            #self.debugNP.showTightBounds()
            #self.debugNP.showBounds()

            self.world.setDebugNode(self.debugNP.node())

        self.enableParticles()

        ct=self.loader.loadModel('ct')
        ct.reparentTo(self.worldNP)
        # print(ct.ls())
        l,h=ct.getTightBounds()
        dl=h-l
        self.c=l+dl/2

        hs=ct.findAllMatches('**/house*')
        for h in hs:
            # print(h.getPos(self.worldNP))
            h.detachNode()
            BulletNodeMeshWrapper(self,h)

            alight = AmbientLight('ambientLight')
            alight.setColor(Vec4(random(), random(), random(), 1))
            alnp = h.attachNewNode(alight)
            h.setLight(alnp)

        self.addToPhysWorld(ct,['road','Joint','bordersVertical','bordersHorizontal','trottoirs'])

        #fog
        colour = (0.2,0.5,0.2)
        expfog = Fog("Scene-wide exponential Fog object")
        expfog.setColor(*colour)
        expfog.setExpDensity(0.005)
        self.render.setFog(expfog)
        self.setBackgroundColor(*colour)

# from direct.showbase import Audio3DManager
        self.audio3d = Audio3DManager.Audio3DManager(self.sfxManagerList[0], self.camera)
        self.audio3d.setDropOffFactor(0)
        mySound = self.audio3d.loadSfx('ph.ogg')
        self.audio3d.attachSoundToObject(mySound, self.worldNP)
        mySound.setLoop(True)
        mySound.setVolume(0.1)
        mySound.play()

        self.xpldSounds=[]
        for i in range(1,9):
            sfname='expl_00'+str(i)+'.ogg'
            xplSound = self.audio3d.loadSfx(sfname)
            self.audio3d.attachSoundToObject(xplSound, self.worldNP)
            self.xpldSounds.append(xplSound)

        self.soundNames=['no_target','target_locked_001']
        self.soundMess={}
        for sn in self.soundNames:
            snd=self.audio3d.loadSfx('as/'+sn+'.ogg')
            self.soundMess[sn]=snd
            self.audio3d.attachSoundToObject(snd,self.worldNP)

        # self.xplSound = self.audio3d.loadSfx('expl_003.ogg')
        # self.audio3d.attachSoundToObject(self.xplSound, self.worldNP)

        # filters = CommonFilters(self.win, self.cam)
        # filters.setBloom(blend=(0, 0, 0, 1), desat=-0.5, intensity=3.0, size="small")
        self.target = OnscreenImage(image = "ag/crossHair_002.png", pos = (0, 0, 0))
        self.target.setTransparency(TransparencyAttrib.MAlpha)
        self.target.setScale(0.5)
        self.target.setSa(0.5)

        self.textObject = OnscreenText(text = 'my text string', pos = (-1, -1), fg=(1,1,1,1), scale = 0.3)
        self.textObject.setText('R')
        # textObject.setColor((1,1,1,1))
        self.textObject.setColorScale((0.1,0.4,0.1,0.5))

    def playSound(self,name):
        snd=self.soundMess.get(name)
        snd.play()

    def setupBaseLighting(self):
        # Light
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.1, 0.1, 0.1, 1))
        alightNP = self.render.attachNewNode(alight)

        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(1, 1, -1))
        dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        dlightNP = self.render.attachNewNode(dlight)

        dlight2 = DirectionalLight('directionalLight')
        dlight2.setDirection(Vec3(1, -1, 1))
        dlight2.setColor(Vec4(0.7, 0.7, 0.7, 1))
        dlight2NP = self.render.attachNewNode(dlight2)

        self.render.clearLight()
        self.render.setLight(alightNP)
        self.render.setLight(dlightNP)
        self.render.setLight(dlight2NP)

    def addToPhysWorld(self,nodePath,keyNames):

        def addToPhysWorld(nodePath,keyName):
            hs=nodePath.findAllMatches('**/'+keyName+'*')
            for h in hs:
                h.detachNode()
                BulletNodeMeshWrapper(self,h)

        for keyName in keyNames:
            addToPhysWorld(nodePath,keyName)

    def setupBulletVehicle(self):

        def addWheel(vehicle, pos, front, np):
            wheel = vehicle.createWheel()

            wheel.setNode(np.node())
            wheel.setChassisConnectionPointCs(pos)
            wheel.setFrontWheel(front)

            wheel.setWheelDirectionCs(Vec3(0, 0, -1))
            wheel.setWheelAxleCs(Vec3(1, 0, 0))
            wheel.setWheelRadius(0.25)
            wheel.setMaxSuspensionTravelCm(40.0)

            wheel.setSuspensionStiffness(40.0)
            wheel.setWheelsDampingRelaxation(2.3)
            wheel.setWheelsDampingCompression(4.4)
            wheel.setFrictionSlip(100.0);
            wheel.setRollInfluence(0.1)

        # Chassis
        shape = BulletBoxShape(Vec3(0.6, 1.4, 0.5))
        ts = TransformState.makePos(Point3(0, 0, 0.5))

        np = self.worldNP.attachNewNode(BulletRigidBodyNode('Vehicle'))
        self.car=np
        np.node().addShape(shape, ts)
        np.setPos(self.getRandomPlace()+Vec3(0,0,2))
        np.node().setMass(800.0)
        np.node().setDeactivationEnabled(False)

        self.world.attachRigidBody(np.node())

        # self.arr=loader.loadModel('turret')
        # self.arr.setPos(0,0,1.2)
        # self.arr.reparentTo(np)
        #
        # self.gun=loader.loadModel('gun')
        # self.gun.setPos(0,2,1)
        # self.gun.reparentTo(self.arr)

        # self.cActor = Actor('ag/turret_arm',
        #     {})
        # # self.cActor.setScale(4,4,4)
        # self.cActor.reparentTo(np)
        # self.cActor.setPos(0, 0, 1)
        # self.turrNp = self.cActor.controlJoint(None, "modelRoot", "turrBone")
        # self.gunNp = self.cActor.controlJoint(None, "modelRoot", "gunBone")

        self.empN=np.attachNewNode('empN')
        self.empN.setPos(0,0,1.2)
        # self.empN.reparentTo(np)

        self.mod=mover.TankModelCtrl(self,'t_004_012',[])
        self.mod.b.reparentTo(np)

        self.camNp=np.attachNewNode('camNp')
        # self.empN.reparentTo(np)
        self.cam.setPos(0, -9, 4)
        self.cam.lookAt(0, 0, 0)
        self.cam.reparentTo(self.camNp)

        #np.node().setCcdSweptSphereRadius(1.0)
        #np.node().setCcdMotionThreshold(1e-7)

        # Vehicle
        self.vehicle = BulletVehicle(self.world, np.node())
        self.vehicle.setCoordinateSystem(ZUp)
        self.world.attachVehicle(self.vehicle)

        self.yugoNP = self.loader.loadModel('ag/yugo/yugo.egg')
        self.yugoNP.reparentTo(np)
        # assert isinstance(np, object)
        # self.mainNP = np
        # self.camNP = self.mainNP.attachNewNode('CamNode')
        # self.camNP.setPos(0, -10, 4)

        # Right front wheel
        np = self.loader.loadModel('ag/yugo/yugotireR.egg')
        np.reparentTo(self.worldNP)
        addWheel(self.vehicle,Point3(0.70, 1.05, 0.3), True, np)

        # Left front wheel
        np = self.loader.loadModel('ag/yugo/yugotireL.egg')
        np.reparentTo(self.worldNP)
        addWheel(self.vehicle,Point3(-0.70, 1.05, 0.3), True, np)

        # Right rear wheel
        np = self.loader.loadModel('ag/yugo/yugotireR.egg')
        np.reparentTo(self.worldNP)
        addWheel(self.vehicle,Point3(0.70, -1.05, 0.3), False, np)

        # Left rear wheel
        np = self.loader.loadModel('ag/yugo/yugotireL.egg')
        np.reparentTo(self.worldNP)
        addWheel(self.vehicle,Point3(-0.70, -1.05, 0.3), False, np)

        # Steering info
        self.steering = 0.0  # degree
        self.steeringClamp = 45.0  # degree
        self.steeringIncrement = 120.0  # degree per second

    def mouseTask1(self):

        # c=ShooterControl(self.mainMap,render)
        # c.targetsList.append(self.cActor)

        # check if we have access to the mouse
        if self.mouseWatcherNode.hasMouse():

            # # get the mouse position
            # mpos = base.mouseWatcherNode.getMouse()
            # print mpos
            #
            # # self.ball = loader.loadModel("c")
            # # self.ball.reparentTo(render)
            # # self.ball.setPos(self.weap.getPos(render))
            #
            # pMouse = base.mouseWatcherNode.getMouse()
            # pFrom = Point3()
            # pTo = Point3()
            # base.camLens.extrude(pMouse, pFrom, pTo)
            # print 'FT:', pFrom, pTo
            #
            # # pFrom = render.getRelativePoint(base.cam, pFrom)
            # # pTo = render.getRelativePoint(base.cam, pTo)
            # d=pTo-pFrom
            # d.normalize()
            # tP=pTo#+d.normalize()*100
            # print 'tP=', d,tP

            # setup the projectile interval
            # self.trajectory = ProjectileInterval(self.ball,
            #                                      startPos = Point3(-100,100,10),
            #                                      endPos = Point3(100,100,10), duration=5)
            # self.trajectory = ProjectileInterval(self.ball,
            #                                      startPos = self.weap.getPos(render),
            #                                      endPos = Point3(-100,10000,100), duration=4)
            # self.trajectory.loop()

            # set the position of the ray based on the mouse position
            # self.pickerRay.setFromLens(base.camNode,mpos.getX(),mpos.getY())
            rDir=self.targPt-self.gunNp.getPos(render)
            rDir.normalize()

            # print 'rDir=',rDir
            # self.ptr.setPos(self.gunNp.getPos(render))
            # self.ptr.lookAt(self.gunNp.getPos(render)+rDir*20)
            # self.pickerRay.setOrigin(self.gunNp.getPos(render))
            # self.pickerRay.setDirection(rDir)
            # self.picker.traverse(render)
            # # if we have hit something sort the hits so that the closest is first and highlight the node
            # if self.pq.getNumEntries() > 0:
            #     self.pq.sortEntries()
            #     pickedObj = self.pq.getEntry(0).getIntoNodePath()
            #     print ('click on '+pickedObj.getName())
            #     # pickedObj.detachNode()
            #     np=render.attachNewNode('S')
            #     # print self.pq.getEntry(0).getContactPos(render)
            #     print self.pq.getEntry(0).getSurfacePoint(render)
            #     print self.pq.getEntry(0).getSurfaceNormal(render)
            # else:
            #     print 'no hits'

                # box1 = self.loader.loadModel("c")
                # box1.reparentTo(render)
                # box1.setPos(self.pq.getEntry(0).getSurfacePoint(render))
                # box1.setCollideMask(BitMask32.bit(1))
            cfg.launchRocket(self.gunNp.getPos(render)+rDir*20, self.targPt)

    def mouseTask3(self):

        # check if we have access to the mouse
        if self.mouseWatcherNode.hasMouse():

            dir=self.cam.getQuat(self.render).getForward()
            pFrom=self.cam.getPos(self.render)
            pTo=pFrom+dir*1200

            result = self.world.rayTestClosest(pFrom, pTo)
            # print (result.hasHit(),
            #       # result.getHitFraction(),
            #       result.getNode().getName(),
            #       # result.getHitPos(),
            #       result.getHitNormal())
            # print(result.getNode().getName())
            # print(self.b.getPos(),pTo)

            if result.hasHit() and result.getNode().getName() == 'modH':
                hp=result.getHitPos()

                # ball = self.loader.loadModel("ag/c")
                # ball.reparentTo(self.render)
                # ball.setPos(hp)

                self.targPt=hp

                self.mod.doAim(hp)
            else:
                self.playSound('no_target')

    def processInput(self, dt):

        if not inputState.isSet('backward'):
            self.chgEnable=True
        if inputState.isSet('backward') and self.chgEnable:
            self.speedSign *= -1
            self.chgEnable=False
            if self.speedSign < 0:
                self.textObject.setColorScale((0.9,0.4,0.1,0.9))
            else:
                self.textObject.setColorScale((0.1,0.4,0.1,0.5))


        engineForce = 0.0
        brakeForce = 0.0
        # self.steering=0

        if inputState.isSet('forward'):
            engineForce = 1000.0*self.speedSign
            brakeForce = 0.0

        if inputState.isSet('reverse'):
            engineForce = 0.0
            brakeForce = 100.0

        if not inputState.isSet('turnLeft') and not inputState.isSet('turnRight'):
            dt=self.steering/8
            self.steering -= dt
            if abs(self.steering) < abs(dt):
                self.steering=0
        else:
            if inputState.isSet('turnLeft'):
                self.steering += dt * self.steeringIncrement
                self.steering = min(self.steering, self.steeringClamp)

            if inputState.isSet('turnRight'):
                self.steering -= dt * self.steeringIncrement
                self.steering = max(self.steering, -self.steeringClamp)

        # Apply steering to front wheels
        self.vehicle.setSteeringValue(self.steering, 0);
        self.vehicle.setSteeringValue(self.steering, 1);

        # Apply engine and brake to rear wheels
        self.vehicle.applyEngineForce(engineForce, 2);
        self.vehicle.applyEngineForce(engineForce, 3);
        self.vehicle.setBrake(brakeForce, 2);
        self.vehicle.setBrake(brakeForce, 3);

    def updateMouse(self):
        winSizeX = self.targetWin.getXSize()/2
        winSizeY = self.targetWin.getYSize()/2

        mouse = self.targetWin.getPointer(0)

        self.deltaX -= (mouse.getX() - winSizeX) * self.mouseLookSpeed[0]
        self.deltaY -= (mouse.getY() - winSizeY) * self.mouseLookSpeed[1]

        self.targetWin.movePointer(0, int(winSizeX), int(winSizeY))

        # p = self.targetCamera.getP(render) - deltaY
        # h = self.targetCamera.getH(render) - deltaX
        # if abs(p) > 90:
        #     p = 90 * cmp(p, 0)

        # print self.deltaX, self.deltaY
        # base.cam.setP(self.deltaY)
        self.cam.setP(self.deltaY)
        self.camNp.setH(self.deltaX)
        # self.targetCamera.setP(p)
        # self.targetCamera.setH(h)

    def update(self, task):
        dt = globalClock.getDt()
        # self.world.doPhysics(dt)
        self.world.doPhysics(dt, 5, 1.0/180.0)
        if not camAuto:
            self.updateMouse()
        self.processInput(dt)

        # print(self.world.getNumManifolds())
        mfs=self.world.getManifolds()
        # print(list())
        for mf in mfs:
            # print(mf.getNode0().getName(),mf.getNode1())
            if mf.getNumManifoldPoints()>0:
                mfNodes=[mf.getNode0(),mf.getNode1()]
                rNode=next((x for x in mfNodes if x.getName() == 'Rock'),None)
                if rNode:
                    print('rocket collided',mf.getNumManifoldPoints())
                    # print(list(movers))
                    for n in mfNodes:
                        print(n.getName())
                    othNode=next((x for x in mfNodes if x != rNode),None)
                    rObj=mover.getObjectForNode(rNode)
                    othObj=mover.getObjectForNode(othNode)
                    rObj.setDone()
                    if isinstance(othObj, mover.TankModelCtrl):
                        othObj.setDone()

        self.rem()

        if self.targetsNP.getNumChildren() < 5:
            self.addMachine()

        return task.cont

        for m in movers:
            if isinstance(m,MoverR):
                if m.modNP.node().getNumOverlappingNodes()>0:

                    # if m.modNP.find('camBaseNP'):
                    #     self.cc.free=True

                    # print('hit!')
                    overlNodes=m.modNP.node().getOverlappingNodes()
                    print(list(overlNodes))
                    objs=mover.getObjectsForNodes(m.modNP.node().getOverlappingNodes())
                    # print(list(objs))
                    for obj in objs:
                        if isinstance(obj, mover.TankModelCtrl):
                            obj.setDone()
                            # if self.cc.free and obj.modNP.find('camBaseNP'):
                            if obj.modNP.find('camBaseNP'):
                                self.cc.lookAtExplodeWithRotateAndMove()
                                # print('switch')
                                # pos=obj.modNP.getPos()
                                # hpr=obj.modNP.getHpr()
                                # a=self.loader.loadModel('arrow')
                                # a.reparentTo(self.worldNP)
                                # a.setPosHpr(pos+Vec3(0,0,2),hpr)
                    m.setDone()
                    # a=self.loader.loadModel('arrow')
                    # a.reparentTo(self.worldNP)
                    # a.setPosHpr(m.b.getPos()+Vec3(0,0,0),m.b.getHpr())

        if self.targetsNP.getNumChildren() < 3:
            self.addMachine()
            # cd=BulletNodeWrapper(self,self.loader.loadModel('t_004_003'))
            r=50
            # cd.modNP.setPos(randint(-r,r),randint(-r,r),randint(-r,r))
            # cd.modNP.node().setLinearVelocity(Vec3(randint(-r,r),randint(-r,r),randint(-r,r)))
            # self.taskMgr.doMethodLater(3,cd.remove,'rem',extraArgs=[])

            # BulletNodeWrapper(self,self.loader.loadModel('t_004_003'),initPos=(randint(-r,r),randint(-r,r),randint(-r,r)),
            #                   startVel=Vec3(randint(-r,r),randint(-r,r),randint(-r,r)),particleEffectConfig='dust.ptf',
            #                   lifeTime=3)

        # if len(self.mcs) < 8:
        #     mod=self.loader.loadModel('t_004_005')
        #     mod.reparentTo(self.worldNP)
        #     self.mcs.append(mod)
        #
        # if random() > 0.5:
        #     toe=choice(self.mcs)
        #     self.mcs.remove(toe)
        #     toe.detachNode()
        #     self.xpld(toe)
        # self.processInput(dt)

        # if len(self.mcs) < 8:
        #     mod=BulletNodeWrapper(self,self.loader.loadModel('t_004_005'))
        #     # mod.reparentTo(self.worldNP)
        #     self.mcs.append(mod)
        #
        # if random() > 0.5:
        #     toe=choice(self.mcs)
        #     self.mcs.remove(toe)
        #     ne=toe.bm
        #     toe.remove()
        #     self.xpld(ne)

        # self.processInput(dt)

        # for m in rocks:
        #     n=m.modNP.node().getNumOverlappingNodes()
        #     if n:
        #         print('hit!')
        #         # toRem=[]
        #         for nd in m.modNP.node().getOverlappingNodes():
        #             print(nd.getName())
        #             if nd.getName() == 'modH':
        #                 # toRem.append(nd)
        #                 self.addToRemove(nd)
        #                 self.addToRemove(m.modNP.node())

        # for m in self.ms:
        #     n=m.modNP.node().getNumOverlappingNodes()
        #     if n:
        #         toRem=[]
        #         for nd in m.modNP.node().getOverlappingNodes():
        #             if nd.getName() == 'Rock':
        #                 toRem.append(nd)
        #         if toRem:
        #             self.checkRocks(toRem)
        #             self.targets.remove(m.b)
        #             # self.xplodeNodePath(m.b)
        #             mn=m.bm
        #             print('expl ',mn)
        #             m.removeFromWorlds()
        #             # self.xpld(mn)
        #             self.ms.remove(m)
                    # return task.cont
            # if n:
            #     # m.modNP.node().removeAllChildren()
            #     toRem=[]
            #     for nd in m.modNP.node().getOverlappingNodes():
            #         if nd.getName() == 'Rock':
            #             toRem.append(nd)
            #         # self.world.remove(n)
            #         # print(n,n.getParent(1))
            #     if toRem:
            #         self.checkRocks(toRem)
            #         self.targets.remove(m.b)
            #         # self.xplodeNodePath(m.b)
            #         m.removeFromWorlds()
            #         self.ms.remove(m)
            #         return task.cont
        while len(self.toExpl):
            e=self.toExpl.pop()
            print('try expl',e)
            # self.xpld(e)

        # self.remove()
        self.rem()

        return task.cont

    def doMethodLater(self, delay, func, name, extraArgs):
        print(func,name)
        self.taskMgr.doMethodLater(delay,func,name,extraArgs=extraArgs)

    def addMachine(self):
        # m=MoverT(self,'t_004_005',Point3(llf.randomFormRange(100)),None)
        m= mover.TankModelCtrl(self,'t_004_012',[TankMover,'shootsEnable'])
        # m= mover.TankModelCtrl(self,'t_004_012',[TankMover])
        movers.append(m)
        # self.taskMgr.doMethodLater(3,m.setDone,'name',extraArgs=[])

    # def addToRemove(self,obj):
    #     if obj not in self.toRemove:
    #         self.toRemove.append(obj)

    def checkForRem(self,arr,nd):
        for el in arr:
            if el.modNP.node() == nd:
                el.removeFromWorlds()
                arr.remove(el)

    def rem(self):
        for m in movers:
            if m.done:
                if isinstance(m, mover.TankModelCtrl):
                    vis=m.visNP
                    self.xpld(vis)
                m.removeFromWorlds()
                movers.remove(m)

    def remove(self):

        toRem=[]
        for obj in movers:
            if obj.done:
                toRem.append(obj)
            else:
                n=obj.modNP.node().getNumOverlappingNodes()
                if n >0:
                    toRem.append(obj)

        en=None
        for obj in toRem:
            if isinstance(obj,MoverS):
                en=obj.bm
            if en:
                self.toExpl.append(en)
            obj.removeFromWorlds()
            if obj in movers:
                movers.remove(obj)
                # print(n)
                # obj.removeFromWorlds()
                # if obj in movers:
                #     movers.remove(obj)
        # for obj in self.toRemove:
        #     if isinstance(obj,MoverR):
        #         obj.removeFromWorlds()
        # toRem=set(self.toRemove)
        # # if toRem:
        #     # print(toRem)
        #     # print(self.toRemove)
        # self.toRemove.clear()
        # while toRem:
        #     obj=toRem.pop()
        #     self.checkForRem()
        #     # ifself.targets.remove(obj)
        #     # rocks.remove(obj)
        #     # # if isinstance(obj,MoverR):
        #     # obj.removeFromWorlds()

    # def checkRocks(self,toRem):
    #     for r in rocks:
    #         if r.checkForRemove(toRem):
    #             #pass#
    #             self.addToRemove(r)
    #             # rocks.remove(r)


    def loadPaths(self):
        ps=pickle.load(open('nmss.bin','rb'))
        # for p in ps:
            # print(p)
            # for l in p.linksSplines.values():
            #     # print(l)
            #     pts=[tuple_to_gp_Pnt(li) for li in l]
            #     spl=dbgMakeSpline(pts)
            #     self.displayCurve(spl.Curve())

            # for splD in p.linksDiscrSplines.values():
            #     for loc in splD:
            #         b=self.loader.loadModel('box')
            #         b.reparentTo(self.render)
            #         pos=loc[0]
            #         b.setPos(Point3(loc[0][0],loc[0][1],loc[0][2]))#pnt.X(),pnt.Y(),pnt.Z())
            #         # b.setPos(Point3(pos[0],pos[1],pos[2]))#pnt.X(),pnt.Y(),pnt.Z())
            #         b.setScale(0.5,0.5,0.2)

        return ps


    def xpld(self,modNP):
        vs=modNP.findAllMatches('**/+GeomNode')
        # geom = visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
        # print (vs)
        choice(self.xpldSounds).play()
        # self.xpldSounds[-1].play()

        # pos=modNP.getPos(self.render)
        # hpr=modNP.getHpr(self.render)
        #
        # modNP.reparentTo(self.worldNP)
        # modNP.setPosHpr(pos,hpr)
        # return

        pos=modNP.getPos(self.render)
        np=vs.getNumPaths()

        c=0
        for visNP in vs:
            r=4
            r2=0.12
            # c+=1
            # if c >12:
            #     return
            c=BulletNodeWrapper(self,visNP,initPos=pos+Vec3(randint(-r,r),randint(-r,r),randint(-r,r)),
                              startVel=Vec3(uniform(-r2,r2),uniform(-r2,r2),uniform(-r2,r2)),particleEffectConfig='dust.ptf')
                              # startVel=Vec3(uniform(-r2,r2),uniform(-r2,r2),uniform(-r2,r2)))
                # ,
                #               lifeTime=5)
            self.taskMgr.doMethodLater(3,c.remove,'name',extraArgs=[])


    def testExpl(self):
        mod=self.loader.loadModel('t_004_005')
        self.xpld(mod)

        self.taskMgr.doMethodLater(1,self.testExpl,'expl',extraArgs=[])

    def xplodeNodePath(self,nodePath):
        print ('geoms:')
        vs=nodePath.findAllMatches('**/+GeomNode')
        # geom = visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
        print (vs)

        for visNP in vs:
            geom = visNP.node().getGeom(0)
            print (geom.getBounds(),type(geom))

            # mesh = BulletTriangleMesh()
            # mesh.addGeom(geom)
            # shape = BulletTriangleMeshShape(mesh, dynamic=False)
            shape = BulletConvexHullShape()
            shape.addGeom(geom)

            body = BulletRigidBodyNode(visNP.getName())
            bodyNP = self.worldNP.attachNewNode(body)
            bodyNP.node().addShape(shape)
            bodyNP.node().setMass(1.0)
            bodyNP.node().setDeactivationEnabled(False)
            # bodyNP.setPos(0, 0, 2)
            bodyNP.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(bodyNP.node())

            visNP.reparentTo(bodyNP)

            # p = ParticleEffect()
            # p.loadConfig('models/dust.ptf')
            # p.start()
            # p.reparentTo(bodyNP)
            #
            bodyNP.node().setLinearVelocity(Vec3(0,0,randrange(5,30)))


app = MyApp()
app.run()
