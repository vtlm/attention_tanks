from direct.interval.LerpInterval import LerpHprInterval, LerpPosHprInterval, LerpPosInterval, LerpFunc
from panda3d.core import Vec3, NodePath, Point3
import mover

__author__ = 'nezx'

from random import randint, choice, random


class CamCtrl(object):
    def __init__(self,baseApp):
        self.baseApp=baseApp

        self.baseNP=NodePath('camBaseNP')
        self.camNP=self.baseNP.attachNewNode('camNP')

        self.timeInterv=10
        self.explTimeInterv=4
        self.rSpd=360/self.timeInterv

        self.free=True

        # print(dir(self))

        # self.switch()

    def setRotateAround(self):
        board=choice(self.baseApp.targetsNP.getChildren())
        #baseNP=NodePath('base')
        self.baseNP.reparentTo(board.modNP)
        #camNP=baseNP.attachNewNode('camNP')
        self.camNP.setPos(0,-20,1)
        self.baseApp.cam.reparentTo(self.camNP)
        self.baseApp.cam.setPos(0,0,0)
        self.baseApp.cam.setHpr(self.baseNP,Vec3(0,0,0))
        startAng=randint(0,360)
        endAng=startAng+randint(-360,360)
        self.int=LerpHprInterval(self.baseNP,8,Vec3(endAng,0,0),startHpr=Vec3(startAng,0,0))
        self.int.start()

    def setRotateAroundandMove(self):
        self.board=choice(self.baseApp.targetsNP.getChildren())
        # baseNP=NodePath('base')
        self.baseNP.reparentTo(self.board)
        self.baseNP.setPos(0,0,0)
        self.baseNP.setHpr(0,0,0)
        # camNP=baseNP.attachNewNode('camNP')
        self.camNP.setPos(0,-20,13)
        self.camNP.setHpr(0,0,0)
        self.baseApp.cam.reparentTo(self.camNP)
        self.baseApp.cam.setPos(0,0,0)
        self.baseApp.cam.setHpr(self.baseNP,Vec3(0,0,0))
        startAng=randint(0,360)
        endAng=startAng+randint(-360,360)
        startDist=randint(0,30)
        endDist=randint(0,30)

        h=0.05
        self.int=LerpHprInterval(self.baseNP,8,Vec3(endAng,0,0),startHpr=Vec3(startAng,0,0))
        self.int.start()
        self.intM=LerpPosInterval(self.camNP,8,Point3(0,-endDist,h),startPos=Point3(0,-startDist,h))
        self.intM.start()

    def flyAlong(self):
        board=choice(self.baseApp.targetsNP.getChildren())
        self.baseNP.reparentTo(board.modNP)
        # self.baseNP.setPos(0,0,0)
        # self.camNP.setPos(0,-20,1)
        self.baseApp.cam.reparentTo(self.camNP)
        self.baseApp.cam.setPos(0,0,0)
        # self.baseApp.cam.setHpr(self.baseNP,Vec3(0,0,0))
        self.baseApp.cam.setHpr(Vec3(0,0,0))
        # startAng=randint(0,360)
        # endAng=startAng+randint(-360,360)
        startDist=randint(20,50)
        endDist=randint(-50,-20)
        sideShift=randint(-10,10)
        h=2

        camNP=self.camNP
        baseNP=self.baseNP
        # self.int=LerpHprInterval(baseNP,8,Vec3(endAng,0,0),startHpr=Vec3(startAng,0,0))
        # self.int.start()
        self.intM=LerpPosInterval(self.camNP,8,Point3(sideShift,-endDist,h),startPos=Point3(sideShift,-startDist,h))
        self.intM.start()

        def setView(t):
            # print(t)
            # camNP.lookAt(baseNP,Point3(0,0,0))
            self.camNP.lookAt(self.baseNP,Point3(0,0,0))

        self.intF=LerpFunc(setView,fromData=0,toData=1,duration=8)
        self.intF.start()

    def track(self):
        board=choice(self.baseApp.targetsNP.getChildren())
        lastLane=board.currDiscrSpline[-1]
        lastPt=Vec3(lastLane[0])+Vec3(lastLane[1])*10
        self.baseApp.cam.reparentTo(self.baseApp.render)
        self.baseApp.cam.setPos(lastPt+Vec3(0,0,2))

        def setView(t):
            # print(t)
            # camNP.lookAt(baseNP,Point3(0,0,0))
            self.baseApp.cam.lookAt(self.baseApp.render,board.modNP.getPos())

        self.intF=LerpFunc(setView,fromData=0,toData=1,duration=8)
        self.intF.start()

    def follow(self):
        board=choice(self.baseApp.targetsNP.getChildren())
        self.baseNP.reparentTo(board.modNP)
        self.baseApp.cam.reparentTo(self.camNP)
        self.baseApp.cam.setPos(Vec3(0,0,0))
        self.baseApp.cam.setHpr(Vec3(0,0,0))
        sideShift=randint(-3,3)
        alongShift=randint(-10,-3)
        heightShift=0.2+random()
        pathLength=randint(-15,15)

        self.intM=LerpPosInterval(self.baseNP,8,Point3(sideShift,alongShift+pathLength,heightShift),
                                  startPos=Point3(sideShift,alongShift,heightShift))
        self.intM.start()



    def lookAtExplode(self):
        q=self.camNP.getQuat(self.baseApp.worldNP)
        dir=q.getForward()
        newHpr=self.baseNP.getHpr(self.baseApp.worldNP)
        self.baseNP.reparentTo(self.baseApp.worldNP)
        # self.baseNP.setPosHpr(self.board.getPos(),self.board.getHpr())
        self.baseNP.setPosHpr(self.board.getPos(self.baseApp.worldNP),newHpr)
        # self.baseNP.setPos(self.board.getPos())
        # self.camNP.setPos(0,-40,30)
        # self.camNP.lookAt(self.baseNP.getPos(),Vec3(0,0,1))
        self.int.pause()
        self.intM.pause()
        # self.int.finish()
        # self.intM.finish()
        self.baseApp.taskMgr.remove('camSwitch')
        self.baseApp.taskMgr.doMethodLater(self.explTimeInterv,self.switch,'camSwitch',extraArgs=[])


    def lookAtExplodeWithRotateAndMove(self):

        self.baseApp.taskMgr.remove('camSwitch')

        q=self.camNP.getQuat(self.baseApp.worldNP)
        dir=q.getForward()
        newHpr=self.baseNP.getHpr(self.baseApp.worldNP)
        self.baseNP.reparentTo(self.baseApp.worldNP)
        # self.baseNP.setPosHpr(self.board.getPos(),self.board.getHpr())
        self.baseNP.setPosHpr(self.board.getPos(self.baseApp.worldNP),newHpr)
        # self.baseNP.setPos(self.board.getPos())
        # self.camNP.setPos(0,-40,30)
        # self.camNP.lookAt(self.baseNP.getPos(),Vec3(0,0,1))
        if hasattr(self,'int'):
            self.int.pause()
        if hasattr(self,'intM'):
            self.intM.pause()
        if hasattr(self,'intF'):
            self.intF.pause()

        hpr=self.baseNP.getHpr()
        pos=self.camNP.getPos()
        hpr+=Vec3(randint(-180,180),0,0)
        pos+=Vec3(0,randint(-40,-10),randint(10,50))

        expIntTime=4
        if hasattr(self,'int'):
            self.int.finish()
        if hasattr(self,'intM'):
            self.intM.finish()
        if hasattr(self,'intF'):
            self.intF.finish()

        self.int=LerpHprInterval(self.baseNP,4,hpr)
        self.int.start()
        self.intM=LerpPosInterval(self.camNP,4,pos)
        self.intM.start()

        def setView(t):
            # print(t)
            # camNP.lookAt(baseNP,Point3(0,0,0))
            self.baseApp.cam.lookAt(self.baseApp.render,self.baseNP.getPos())

        self.intF=LerpFunc(setView,fromData=0,toData=1,duration=4)
        self.intF.start()

        self.baseApp.taskMgr.doMethodLater(self.explTimeInterv,self.switch,'camSwitch',extraArgs=[])


    def checkSqrDiatance(self):
        if not self.rocket.done:
            dist=self.rocket.getDistanceToTarget()
            print(dist)
            if dist != None:
                if  dist < 100:
                    print('near')
                else:
                    self.baseApp.taskMgr.doMethodLater(0.2,self.checkSqrDiatance,'distCheck',extraArgs=[])
            else:
                self.free=True
        else:
            self.free=True


    def setOnRocket(self,rocket):
        self.rocket=rocket
        self.baseNP.reparentTo(rocket.modNP)
        self.baseNP.setPosHpr(0,0,0,0,0,0)
        self.camNP.setPosHpr(0,-5,1,0,0,0)
        self.baseApp.cam.reparentTo(self.camNP)
        self.baseApp.cam.setPos(Vec3(0,0,0))
        self.baseApp.cam.setHpr(Vec3(0,0,0))

        self.baseApp.taskMgr.doMethodLater(0.2,self.checkSqrDiatance,'distCheck',extraArgs=[])



    def lookOnRocket(self):
        boards=self.baseApp.targetsNP.getChildren()
        nodes=[board.node() for board in boards]
        objs=mover.getObjectsForNodes(nodes)

        # obj=next((objx for objx in objs if len(objx.attackers) > 0),None)
        obj=next((objx for objx in objs if objx.isNearestAttackerFarthestThan(20000)),None)
        if obj:
            obj.updateAttackers()
            if hasattr(self,'int'):
                self.int.finish()
            if hasattr(self,'intM'):
                self.intM.finish()
            if hasattr(self,'intF'):
                self.intF.finish()
            # print (list(obj.attackers))
            dists=[att.getDistanceToTarget() for att in obj.attackers]
            # print(dists)
            self.targ=obj
            self.board=obj.modNP
            self.rocket=obj.distAttacks[0][1]
            self.baseNP.reparentTo(self.targ.modNP)
            self.baseNP.setPos(0,0,0)
            self.camNP.setPos(0,-20,5)
            # print('pos:',self.baseNP.getPos(self.board),self.camNP.getPos(self.board))
            self.baseApp.cam.reparentTo(self.camNP)
            self.baseApp.cam.setPos(Vec3(0,0,0))
            self.baseApp.cam.setHpr(Vec3(0,0,0))
            # print('pos:',self.baseApp.cam.getPos(self.baseNP))
        # else:
            def setView(t):
                if not self.rocket.done and not self.targ.done:
                    # base=self.targ.modNP
                    # hpr=self.rocket.modNP.getHpr(base)
                    # self.baseNP.setHpr(hpr)
                    self.baseNP.lookAt(self.baseApp.worldNP,self.rocket.modNP.getPos())
                    self.baseApp.cam.lookAt(self.baseApp.worldNP,self.rocket.modNP.getPos())

            self.intF=LerpFunc(setView,fromData=0,toData=1,duration=4)
            self.intF.start()
        else:
            self.baseApp.taskMgr.doMethodLater(0.5,self.lookOnRocket,'lk',extraArgs=[])


    def switch(self):
        def setRandomPos():
            '''
            set cam at random pos in range rangeW, looks to center
            :return:
            '''
            rangeW=100
            minZ=20
            self.baseApp.cam.setPos(randint(-rangeW,rangeW),randint(-rangeW,rangeW),minZ+randint(0,rangeW))
            self.baseApp.cam.lookAt(self.baseApp.c)

        def setOnBoard():
            '''
            fix cam on some random board
            :return:
            '''
            rangeXB=1
            minY=30
            rangeYB=20
            minZ=1
            rangeYZ=1
            board=choice(self.baseApp.targetsNP.getChildren())
            self.baseApp.cam.reparentTo(board.modNP)
            self.baseApp.cam.setPos(randint(-rangeXB,rangeXB),-minY+randint(0,rangeYB),minZ+randint(0,rangeYZ))


        # setRandomPos()
        # setOnBoard()
        # self.setRotateAround()
        self.setRotateAroundandMove()
        # self.flyAlong()
        # self.track()
        # self.follow()
        # self.lookOnRocket()
        self.baseApp.taskMgr.doMethodLater(self.timeInterv,self.switch,'camSwitch',extraArgs=[])
