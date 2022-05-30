from sklearn.cluster import DBSCAN
import numpy as np
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

labels_true = 1


def scanner(s, x, y, last_clusters):
    radius = 0
    centre = [0, 0]
    data = []
    groupX = []
    groupY = []
    groupCentreX = []
    groupCentreY = []

    if len(x) == len(y):
        for i in range(len(x)):
            data.append([x[i], y[i]])

        points = np.array(data)
    else:
        print("Uneven number of x an y")

    db = DBSCAN(eps=1, min_samples=int(len(x)/(last_clusters + 1))).fit(points)

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
        if labels[i] != lastLabel:
            colorInd += 1
            lastLabel = labels[i]
            if i > 0:
                centreX, centreY = centre_point(groupX, groupY)
                groupCentreX.append(centreX)
                groupCentreY.append(centreY)

                p_ellipse = pg.QtGui.QGraphicsEllipseItem(centreX, centreY, 0.02, 0.02)

                ellipseList.append(p_ellipse)
                groupX.clear()
                groupY.clear()

        groupX.append(x[i])
        groupY.append(y[i])

    if lastLabel == 0:
        centreX, centreY = centre_point(groupX, groupY)
        p_ellipse = pg.QtGui.QGraphicsEllipseItem(centreX, centreY, 0.02, 0.02)
        ellipseList.append(p_ellipse)
        groupCentreX.append(centreX)
        groupCentreY.append(centreY)

    return ellipseList, groupCentreX, groupCentreY, n_clusters_


def centre_point(xList, yList):
    (x, y) = (float(sum(xList)) / len(xList), float(sum(yList)) / len(yList))
    return x, y
