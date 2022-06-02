from sklearn.cluster import DBSCAN
import numpy as np
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import datetime
import math
from math import floor


def velocity_calc(xList, yList):
    velList = []
    angList = []
    for i in range(floor(len(xList)/2) - 1):
        velocityX = abs((xList[i*2][0] - xList[i*2+1][0]))
        velocityY = abs((yList[i*2][0] - yList[i*2+1][0]))
        if velocityX > 4 or velocityY > 4:
            velocityY = 0
            velocityX = 0
        velList.append(math.sqrt(velocityX*velocityX+velocityY*velocityX))
        angList.append(math.atan2(velocityX, velocityY)*180/math.pi)
    return velList, angList
