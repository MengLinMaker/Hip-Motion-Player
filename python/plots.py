import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.transform import Rotation as R

from utility import norm


def plotGyroNorm(data, timeStamp, ax=False):
  if ax==False:
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
  
  waistGyroNorm = norm(data[:, 0:3])
  rightGyroNorm = norm(data[:, 10:13])
  leftGyroNorm = norm(data[:, 20:23])
  ax.plot(timeStamp, waistGyroNorm, 'b-', linewidth=0.5, label='Waist')
  ax.plot(timeStamp, rightGyroNorm, 'g-', linewidth=0.5, label='Right Thigh')
  ax.plot(timeStamp, leftGyroNorm, 'r-', linewidth=0.5, label='Left Thigh')
  ax.legend(loc="upper left")
  ax.set_xlabel('Time (s)')
  ax.set_ylabel('Ang vel (rad/s)')
  ax.axis([0, timeStamp[-1], 0, 7])
  ax.xaxis.set_ticks(np.arange(0, timeStamp[-1], 1))
  ax.grid()


def plotAccNorm(data, timeStamp, ax=False):
  if ax==False:
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
  
  waistAccNorm = norm(data[:, 3:6])
  rightAccNorm = norm(data[:, 13:16])
  leftAccNorm = norm(data[:, 23:26])
  ax.plot(timeStamp, waistAccNorm, 'b-', linewidth=0.5, label='Waist')
  ax.plot(timeStamp, rightAccNorm, 'g-', linewidth=0.5, label='Right Thigh')
  ax.plot(timeStamp, leftAccNorm, 'r-', linewidth=0.5, label='Left Thigh')
  ax.legend(loc="upper left")
  ax.set_xlabel('Time (s)')
  ax.xaxis.set_label_coords(1, -.2)
  ax.xaxis.set_ticks(np.arange(0, timeStamp[-1], 1))
  ax.set_ylabel('Acc (m/s^2)')
  ax.axis([0, timeStamp[-1], 0, 15])
  ax.grid()


def plotCosineHeight(quat, timeStamp, ax=False):
  if ax == False:
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))

  waistRot = R.from_quat(quat)
  # Calculate waist vector relative to earth
  cosWaistX = waistRot.apply([1, 0, 0])[:, 2]
  ax.plot(timeStamp, cosWaistX, 'r-', linewidth=0.5, label='X axis height')
  cosWaistY = waistRot.apply([0, 1, 0])[:, 2]
  ax.plot(timeStamp, cosWaistY, 'g-', linewidth=0.5, label='Y axis height')
  cosWaistZ = waistRot.apply([0, 0, -1])[:, 2]
  ax.plot(timeStamp, cosWaistZ, 'b-', linewidth=0.5, label='Z axis height')
  ax.set_ylim([-1, 1])
  ax.legend(loc="upper left")
  ax.set_xlabel('Time (s)')
  ax.xaxis.set_label_coords(1,-.2)
  ax.xaxis.set_ticks(np.arange(0, timeStamp[-1], 1))
  ax.set_ylabel('Cosine height (unitless)')
  ax.axis([0, timeStamp[-1], -1, 1])
  ax.grid()


def densityPlot(data, bins=100):
  plt.figure(figsize=(5, 5))
  sns.distplot(data, bins=bins)