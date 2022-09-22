import matplotlib.pyplot as plt
import numpy as np

from utility import getCsvData, butterFilter, saveCsvData, norm
from plots import plotCosineHeight, plotAccNorm, plotGyroNorm, densityPlot


def analyse(filePath):
  data = getCsvData(filePath)
  sampleRate = 50
  samplePeriod = 1/sampleRate
  timeStamp = np.linspace(0, len(data)*samplePeriod, len(data))

  data2 = butterFilter(data.T, cutoff=20, fs=sampleRate, type='high', order=2).T

  plt.ion()
  fig, ax = plt.subplots(4, 1, figsize=(20, 8))
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
  for i in range(1,6):
    filePath = './Raw Motion Data/Fall Data/Fall Front/Fall Front ('+str(i)+').csv'
    analyse(filePath)
    data = getCsvData(filePath)
    
    #saveCsvData('test ('+str(i)+').csv',data[100:300,:])
    #analyse('test ('+str(i)+').csv')
    
  #'''
  typed = input("Press [enter] to finish.")
  print(typed)
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
