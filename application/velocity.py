from sklearn.cluster import DBSCAN
import numpy as np
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import datetime
import math


def velocity_calc(xList, yList):
    velList = []
    angList = []
    #print(xList, yList)
    if len(xList)%2 == 0:
        for i in range(int(len(xList)/2)):
            velocityX = abs((xList[i*2][0] - xList[i*2+1][0])*5)
            velocityY = abs((yList[i*2][0] - yList[i*2+1][0])*5)
            if velocityX > 4 or velocityY > 4:
                velocityY = 0
                velocityX = 0
            velList.append(math.sqrt(velocityX*velocityX+velocityY*velocityX))
            angList.append(math.atan2(velocityX, velocityY)*180/math.pi)
        return velList, angList
    else:
        return [0], [0]
