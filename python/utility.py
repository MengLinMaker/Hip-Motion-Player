import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R
from scipy.signal import butter, lfilter
from statsmodels.stats.outliers_influence import variance_inflation_factor

from CSV import getCsvData


def norm(vectorArray):
  normArray = []
  for row in vectorArray:
    normVal = np.linalg.norm(row)
    normArray.append(normVal)
  return np.array(normArray)


def butterFilter(data, cutoff, fs, type='low', order=2):
  b, a = butter(order, cutoff, fs=fs, btype=type, analog=False)
  y = lfilter(b, a, data)
  return y


def VIF(data):
  # the calculation of variance inflation requires a constant
  #data['intercept'] = 0

  # create dataframe to store vif values
  vif = pd.DataFrame()
  vif["Variable"] = data.columns
  vif["VIF"] = [variance_inflation_factor(
      data.values, i) for i in range(data.shape[1])]
  return vif[vif['Variable'] != 'intercept']



def quat2cosHeight(quat):
  # Calculate waist vector relative to earth
  rot = R.from_quat(quat)
  if quat.ndim == 2:
    cosHeightX = rot.apply([1, 0, 0])[:, 2]
    cosHeightY = rot.apply([0, 1, 0])[:, 2]
    cosHeightZ = rot.apply([0, 0, -1])[:, 2]
  elif quat.ndim == 1:
    cosHeightX = rot.apply([1, 0, 0])[2]
    cosHeightY = rot.apply([0, 1, 0])[2]
    cosHeightZ = rot.apply([0, 0, -1])[2]
  return np.array([cosHeightX, cosHeightY, cosHeightZ])



def poseFeature(data):
  orientationFeature = np.c_[
    quat2cosHeight(data[:, [9, 6, 7, 8]]).T,
    quat2cosHeight(data[:, [19, 16, 17, 18]]).T,
    quat2cosHeight(data[:, [29, 26, 27, 28]]).T
  ]
  return orientationFeature


def generateDataFrame(filePaths, getFeature, headers=False):
  allData = np.array([])
  label = 0
  for filePath in filePaths:
    data = getCsvData(filePath)
    #label = filePath.split('/')[-1].split('.')[0]
    label = label + 1
    feature = getFeature(data)
    labels = [label] * len(data)
    data = np.c_[labels, feature]
    if allData.ndim == 1: allData = data
    else: allData = np.r_[ allData, data ]

  if headers == False: return pd.DataFrame(allData)
  else: return pd.DataFrame(allData, columns=headers)