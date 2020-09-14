from panda3d.core import Point3

__author__ = 'nezx'


def getSize(cNP):
    minLimit, maxLimit = cNP.getTightBounds()
    return Point3(maxLimit - minLimit)

