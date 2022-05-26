from sklearn.cluster import DBSCAN
import numpy as np
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

labels_true = 1

def scanner(s,x,y):
    radius = 0
    centre = [0,0]
    data = []
    if len(x) == len(y):
        for i in range(len(x)):
            data.append([x[i],y[i]])

        points = np.array(data)
    else:
        print('Uneven number of x an y')

    db = DBSCAN(eps= 0.3, min_samples=5).fit(points)

    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print("Estimated number of clusters: %d" % n_clusters_)
    print("Estimated number of noise points: %d" % n_noise_)
    
    lastLabel =- 1
    colorInd = 0

    scatter = pg.ScatterPlotItem(pxMode = False)
    spots = []

    for i in range(len(data)):
        if labels[i] != lastLabel:
            colorInd += 1
            lastLabel = labels[i]
        
        spot_dic = {'pos': (x[i],y[i]), 'size': .4,
                    'pen': {'color': 'w', 'width': 0.1},
                    'brush': pg.intColor(colorInd * 2, 100)}
        spots.append(spot_dic)
    
    scatter.addPoints(spots)

    return scatter, x, y