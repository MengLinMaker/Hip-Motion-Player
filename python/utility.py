import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R
from scipy.signal import butter, lfilter, iirpeak, iirfilter
from statsmodels.stats.outliers_influence import variance_inflation_factor
from globalVariables import sampleRate, samplePeriod, subSample
from scipy.stats import kurtosis

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


def butterIIR(data, cutoff, fs, order=1):
  Wn = cutoff / fs
  b, a = iirfilter(order, Wn, btype='highpass', ftype='butter')
  y = lfilter(b, a, data)
  return y


def peakFilter(data, cutoff, Q, fs):
  b, a = iirpeak(cutoff, Q, fs)
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
  if data.ndim == 2:
    feature = np.c_[
      quat2cosHeight(data[:, [9, 6, 7, 8]]).T,
      quat2cosHeight(data[:, [19, 16, 17, 18]]).T,
      quat2cosHeight(data[:, [29, 26, 27, 28]]).T
    ]
  else:
    feature = np.r_[
      quat2cosHeight(data[[9, 6, 7, 8]]).T,
      quat2cosHeight(data[[19, 16, 17, 18]]).T,
      quat2cosHeight(data[[29, 26, 27, 28]]).T
    ]
  return feature


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


def mirrorData(data):
  # Mirror about y axis
  #'''
  data[:, 1] = -data[:, 1]
  data[:, 4] = -data[:, 4]
  data[:, 7] = -data[:, 7]
  data[:, 9] = -data[:, 9]
  data[:, 11] = -data[:, 11]
  data[:, 14] = -data[:, 14]
  data[:, 17] = -data[:, 17]
  data[:, 19] = -data[:, 19]
  data[:, 21] = -data[:, 21]
  data[:, 24] = -data[:, 24]
  data[:, 27] = -data[:, 27]
  data[:, 29] = -data[:, 29]
  
  # Swap left and right leg
  #temp = data[:, 10:20]
  #data[:,10:20] = data[:,20:30]
  #data[:,20:30] = temp
  #'''
  return data


def motionFeature(data, subSample=1):
  dataHigh = butterIIR(data.T, 1, sampleRate/subSample, 2).T
  waistAccNorm = norm(dataHigh[:, 3:6])
  rightAccNorm = norm(dataHigh[:, 13:16])
  leftAccNorm = norm(dataHigh[:, 23:26])
  aveAccNorm = np.array([np.average(waistAccNorm), np.average(rightAccNorm), np.average(leftAccNorm)])
  aveAccEnergy = np.array([np.average(waistAccNorm**2), np.average(rightAccNorm**2), np.average(leftAccNorm**2)])

  orientationFeature = poseFeature(data)
  aveOrientationFeature = np.average(orientationFeature, axis=0)

  waistGyro = data[0:3, :]
  rightGyro = data[10:13, :]
  leftGyro = data[20:23, :]
  gyro = np.r_[ waistGyro, rightGyro, leftGyro]

  gyroNorm = np.r_[norm(waistGyro), norm(rightGyro), norm(leftGyro)]
  #waistAcc = data[:, [3, 4, 5]]
  #rightAcc = data[:, [13, 14, 15]]
  #leftAcc = data[:, [23, 24, 25]]

  #dataLength = len(data)
  feature = np.r_[
    orientationFeature[0,:],
    orientationFeature[-1,:],
    aveOrientationFeature,
    #np.max(orientationFeature, axis=0),
    np.min(orientationFeature, axis=0),
    aveAccNorm,
    #np.average(gyro, axis=0),
    #np.sum(aveAccEnergy),
    #np.average(gyroNorm, axis=0),
    #kurtosis(waistAccNorm),
    #kurtosis(rightAccNorm),
    #kurtosis(leftAccNorm),
  ]
  return feature