from sklearn.cluster import DBSCAN
import numpy as np
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from sklearn.datasets import make_blobs
from random import randint

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
    db = DBSCAN(eps=1, min_samples= 6).fit(points)

   
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


    for i in range(len(data)):
        

        if labels[i] != lastLabel:
            centreX, centreY = centre_point(groupX, groupY)
            groupCentreX.append(centreX)
            groupCentreY.append(centreY)
            groupX.clear()
            groupY.clear()

    unique_labels = set(labels)
    colors = [(255/(5+i),200/(3+i),255/(1+i)) for i in range(len(unique_labels))]
    print(colors)
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = (255, 0, 0)
        
        class_member_mask = labels == k

        groupX.append(x[class_member_mask & core_samples_mask])
        groupY.append(y[class_member_mask & ~core_samples_mask])
        if k != last_k:
            centreX, centreY = centre_point(groupX, groupY)
            groupCentreX.append(centreX)
            groupCentreY.append(centreY)
            groupX.clear()
            groupY.clear()

        xy = points[class_member_mask & core_samples_mask]
        plot.plot(xy[:,0],xy[:,1], pen=None, symbol="o",
                symbolPen=None, symbolBrush=tuple(col))

        xy = points[class_member_mask & ~core_samples_mask]
        plot.plot(xy[:,0],xy[:,1], pen=None, symbol="x",
                symbolPen=None, symbolBrush=tuple(col))

        last_k = k

    if lastLabel == 0:
        groupX.append(x[i])
        groupY.append(y[i])
        centreX, centreY = centre_point(groupX, groupY)
        groupCentreX.append(centreX)
        groupCentreY.append(centreY)

    out = "Estimated Locations:"
    plot.addItem(pg.TextItem(out, (0,0,0,255), anchor = (0,15)))

    for i in range(n_clusters_):

        print (n_clusters_)

        out = '(' + str(round(groupCentreX[i])) + ', ' + str(round(groupCentreY[i])) + ')'
        
        plot.addItem(pg.TextItem(out, (0,0,0,255), anchor = (-2.5, -i + 14)))
        plot.plot([1.1],[ -i + 13.15], pen=None, symbol="o",
                    symbolPen=None, symbolBrush=(255/(i+5),200/(i+3),255/(i+1)))

    return groupCentreX, groupCentreY, n_clusters_


def centre_point(xList, yList):
    (x, y) = (float(sum(xList)) / len(xList), float(sum(yList)) / len(yList))
    return x, y
