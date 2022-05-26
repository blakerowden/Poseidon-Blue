from sklearn.cluster import DBSCAN
import numpy as np
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import datetime
import math

def center_point(xList, yList):
    if len(xList) == len(yList):
        (x, y) = (float(sum(xList)) / len(xList), float(sum(yList)) / len(yList))
        print(x, y)
        return x, y, datetime.now()
    else:
        print("Points not same dimensions")
        return 0,0

def velocity_calc(xList, yList, timeStamps):
    velocityX = (xList[-1] - xList[-2])/(timeStamps[-1] - timeStamps[-2])
    velocityY = (yList[-1] - yList[-2])/(timeStamps[-1] - timeStamps[-2])
    combinedVelocity = math.sqrt(velocityX*velocityX+velocityY*velocityX);
    angleInDegrees = math.atan2(velocityX,velocityY)*180/math.PI
    return combinedVelocity, angleInDegrees
    