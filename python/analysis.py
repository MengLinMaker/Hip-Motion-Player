import matplotlib.pyplot as plt
import numpy as np

from utility import getCsvData, butterFilter, saveCsvData, norm
from plots import plotCosineHeight, plotAccNorm, plotGyroNorm, densityPlot


# Global variables
sampleRate = 50
samplePeriod = 1/sampleRate


def analyse(filePath):
  data = getCsvData(filePath)
  timeStamp = np.linspace(0, len(data)*samplePeriod, len(data))

  data2 = butterFilter(data.T, cutoff=20, fs=sampleRate, type='high', order=2).T

  plt.ion()
  fig, ax = plt.subplots(4, 1, figsize=(10, 8))
  plt.subplots_adjust(hspace=0.35)

  #plotGyroNorm(data, timeStamp, ax[0])
  #ax[0].set_title('2nd order 20 Hz high pass Butterworth')
  
  plotCosineHeight(data[:, [9, 6, 7, 8]], timeStamp, ax[0])
  ax[0].set_title('Waist global cosine height')

  plotCosineHeight(data[:, [19, 16, 17, 18]], timeStamp, ax[1])
  ax[1].set_title('Right global cosine height')

  plotCosineHeight(data[:, [29, 26, 27, 28]], timeStamp, ax[2])
  ax[2].set_title('Left global cosine height')

  #plotAccNorm(data, timeStamp, ax[0])
  #ax[0].set_title('No filter normalised acceleration')

  plotAccNorm(data2, timeStamp, ax[3])
  ax[3].set_title('2nd order 20 Hz high pass Butterworth normalised acceleration')

  #densityPlot(data[:, 3])
  #densityPlot(data[:, 4])
  #densityPlot(data[:, 5])

  fig.suptitle(filePath.split('/')[-1])


if __name__ == "__main__":
  #'''
  for i in range(11,20+1):
    filePath = './Raw Motion Data/Fall Data/Fall Right/Fall Right ('+str(i)+').csv'
    analyse(filePath)
    data = getCsvData(filePath)

    startTime = input("Start time: ")
    #endTime = input("End time: ")
    endTime = float(startTime)+3
    print('')
    
    filePath = './Clean Motion Data/Fall/Fall Right ('+str(i)+').csv'
    if (startTime != '' and endTime != ''):
      startID = int(np.floor(sampleRate*float(startTime)))
      endID = int(np.floor(sampleRate*float(endTime)))
      saveCsvData(filePath, data[startID:endID, :])
      analyse(filePath)
    
  #'''
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
