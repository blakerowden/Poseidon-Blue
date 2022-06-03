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
        velocityX = abs((xList[i*2][0] - xList[i*2+1][0]))/2
        velocityY = abs((yList[i*2][0] - yList[i*2+1][0]))/2
        if velocityX > 4 or velocityY > 4:
            velocityY = 0
            velocityX = 0
        velList.append(math.sqrt(velocityX*velocityX+velocityY*velocityX))
        angList.append(math.atan2(velocityX, velocityY)*180/math.pi)
    return velList, angList

def kalman_predict(self):
        """Calculate the predicted state and covariance"""
        self._x = self.A @ self._x  # Predicted (a priori) state estimate
        self._P = (
            self.A @ self._P @ self.A.transpose() + self.Q
        )  # Predicted (a priori) estimate covariance

def update(self, observation: np.array) -> None:
    """Update the state estimate based on the observation.
    Args:
        observation (np.array): The observation vector.
    """
    self.innovation_covariance = (
        self.H @ self._P @ self.H.transpose() + self.R
    )  # Innovation (or pre-fit residual) covariance
    self.observation_noise = (
        observation - self.H @ self._x
    )  # Innovation or measurement pre-fit residual
    self.kalman_gain = (
        self._P @ self.H.transpose() @ np.linalg.inv(self.innovation_covariance)
    )  # Optimal Kalman gain
    self._x = (
        self._x + self.kalman_gain @ self.observation_noise
    )  # Updated (a posteriori) state estimate
    self._P = (
        self._P
        - self.kalman_gain
        @ self.innovation_covariance
        @ self.kalman_gain.transpose()
    )  # Updated (a posteriori) estimate covariance