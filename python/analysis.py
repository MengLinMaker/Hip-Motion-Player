from os import pathsep
import matplotlib.pyplot as plt
import numpy as np

from utility import getCsvData, butterFilter, saveCsvData, norm
from plots import plotCosineHeight, plotAccNorm, plotGyroNorm, densityPlot


# Global variables
sampleRate = 50
samplePeriod = 1/sampleRate


def analyse(filePath):
  plt.ion()
  fig, ax = plt.subplots(4, 1, figsize=(10, 8))
  plt.subplots_adjust(hspace=0.35)
  fig.suptitle(filePath.split('/')[-1])

  data = getCsvData(filePath)
  timeStamp = np.linspace(0, len(data)*samplePeriod, len(data))
  data2 = butterFilter(data.T, cutoff=20, fs=sampleRate, type='high', order=2).T

  #plotGyroNorm(data, timeStamp, ax[0])
  #ax[0].set_title('2nd order 20 Hz high pass Butterworth')
  
  plotCosineHeight(data[:, [9, 6, 7, 8]], timeStamp, ax[0])
  ax[0].set_title('Waist global cosine height')

  plotCosineHeight(data[:, [19, 16, 17, 18]], timeStamp, ax[1])
  ax[1].set_title('Right global cosine height')

  plotCosineHeight(data[:, [29, 26, 27, 28]], timeStamp, ax[2])
  ax[2].set_title('Left global cosine height')

  plotAccNorm(data2, timeStamp, ax[3])
  ax[3].set_title('2nd order 20 Hz high pass Butterworth normalised acceleration')


def generateWindowedSamples():
  for i in range(1, 20+1):
    filePath = './Raw Motion Data/Non-Fall Data/Unlabelled/Unlabelled ('+str(i)+').csv'

    analyse(filePath)
    data = getCsvData(filePath)

    startTime = input("Start time: ")
    endTime = '1'
    #endTime = input("End time: ")
    print('')

    filePath = './Clean Motion Data/Unlabelled/Unlabelled ('+str(i)+').csv'
    if (startTime != '' and endTime != ''):
      startID = int(np.floor(sampleRate*float(startTime)))
      endTime = float(startTime)+3
      endID = int(np.floor(sampleRate*float(endTime)))
      saveCsvData(filePath, data[startID:endID, :])
      analyse(filePath)


def parsePoseFile(fileSrcPath, fileDstPath, ID):
  pathString = fileSrcPath.split('%')

  data = []
  for i in range(1, 20+1):
    fileSrcPath = pathString[0] + str(i) + pathString[1]
    dataPoint = getCsvData(fileSrcPath)[ID, :]
    data.append(dataPoint)
  data = np.array(data)
  #print(data)
  saveCsvData(fileDstPath, data)


if __name__ == "__main__":
  #generateWindowedSamples()
  fileSrcPath = './Clean Motion Data/Non Fall/Walk (%).csv'
  fileDstPath = './Clean Motion Data/Pose/Stand.csv'
  parsePoseFile(fileSrcPath, fileDstPath, -1)

  '''
  filePath = './Raw Motion Data/Fall Data/Fall Back/Fall Back (2).csv'
  analyse(filePath)
  filePath = './Raw Motion Data/Fall Data/Fall Right/Fall Right (2).csv'
  analyse(filePath)
  filePath = './Raw Motion Data/Fall Data/Fall Left/Fall Left (2).csv'
  analyse(filePath)
  filePath = './Raw Motion Data/Non-Fall Data/Stair/Stair (2).csv'
  analyse(filePath)
  filePath = './Raw Motion Data/Non-Fall Data/Run/Run (2).csv'
  analyse(filePath)
  filePath = './Raw Motion Data/Non-Fall Data/Jump/Jump (2).csv'
  analyse(filePath)
  filePath = './Raw Motion Data/Non-Fall Data/Sit/Sit (2).csv'
  analyse(filePath)
  #'''
