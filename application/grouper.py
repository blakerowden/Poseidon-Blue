from sklearn.cluster import DBSCAN
import numpy as np
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

labels_true = 1


def scanner(s, x, y, last_clusters, plot, iteration):
    radius = 0
    centre = [0, 0]
    data = []
    groupX = []
    groupY = []
    groupCentreX = []
    groupCentreY = []
    plot.clear()

    

    if len(x) == len(y):
        for i in range(len(x)):
            data.append([x[i], y[i]])
    
    for xpoint, ypoint in data:
        points = np.array(data)
    else:
        print("Uneven number of x an y")
    if last_clusters == 0:
        last_clusters = 1
    db = DBSCAN(eps=0.6, min_samples=int(len(x)/(3 * last_clusters))).fit(points)

   
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print("Estimated number of clusters: %d" % n_clusters_)
    print("Estimated number of noise points: %d" % n_noise_)

    lastLabel = 0
    colorInd = 0

    scatter = pg.ScatterPlotItem(pxMode=False)
    ellipseList = []

    for i in range(len(data)):
        groupX.append(x[i])
        groupY.append(y[i])

        if labels[i] != lastLabel:
            colorInd += 1
            lastLabel = labels[i]
            centreX, centreY = centre_point(groupX, groupY)
            groupCentreX.append(centreX)
            groupCentreY.append(centreY)
            plot.addItem(pg.QtGui.QGraphicsEllipseItem(centreX, centreY, 0.1, 0.1))
            groupX.clear()
            groupY.clear()

        

        

    if lastLabel == 0:
        groupX.append(x[i])
        groupY.append(y[i])
        centreX, centreY = centre_point(groupX, groupY)
        plot.addItem(pg.QtGui.QGraphicsEllipseItem(centreX, centreY, 0.1, 0.1))
        groupCentreX.append(centreX)
        groupCentreY.append(centreY)
        

    for ellipse in ellipseList:
        plot.addItem(ellipse)

    for item in ellipseList:
        print(item)
    
    return groupCentreX, groupCentreY, n_clusters_


def centre_point(xList, yList):
    (x, y) = (float(sum(xList)) / len(xList), float(sum(yList)) / len(yList))
    return x, y
