import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import spectrogram, cwt, ricker, morlet2, convolve, gausspulse

from CSV import getCsvData, saveCsvData
from utility import butterFilter, norm, quat2cosHeight, butterIIR, peakFilter
from globalVariables import sampleRate, samplePeriod


def plotTimeGraphs(filePath, subSample=1):
  fig, ax = plt.subplots(4, 1, figsize=(10, 12))
  plt.subplots_adjust(hspace=0.4, bottom=0.08, top=0.92)
  fig.suptitle('Preprocessed time series at {sampleRate: .2f} Hz. File: {file}'.
    format(sampleRate=sampleRate/subSample , file = filePath.split('/')[-1]))

  data = getCsvData(filePath)
  data = data[np.arange(0, len(data), subSample), :]
  timeStamp = np.linspace(0, len(data)*samplePeriod*subSample, len(data))

  '''
  freqMorlet = 2
  w = 5
  s = round(sampleRate/subSample*w/(2*np.pi)/freqMorlet)
  M = sampleRate/subSample
  wavelet = morlet2(M, s, w)
  #numSamples = w*sampleRate/freqMorlet
  #wavelet = np.sin(2*np.pi*np.arange(numSamples + 1)*freqMorlet/sampleRate)
  #wavelet2 = np.cos(2*np.pi*np.arange(numSamples + 1)*freqMorlet/sampleRate)
  #window = 0.5-0.5*np.cos(2*np.pi*np.arange(numSamples + 1)/(numSamples+1))
  #wavelet = window*wavelet
  #wavelet2= window*wavelet2

  plt.subplots(1, 1, figsize=(8, 4))
  plt.plot(range(len(wavelet)), wavelet)
  #plt.plot(range(len(wavelet2)), wavelet2)
  plt.plot(range(len(wavelet)), np.zeros(len(wavelet)))
  plt.show()

  data2 = []
  for col in data.T:
    #convSin = convolve(col, wavelet, mode='same')
    #convCos = convolve(col, wavelet2, mode='same')
    #data2.append( (convSin**2 + convCos**2)**0.5 )
    data2.append( abs(convolve(col, wavelet, mode='same')) )
  data2 = np.array(data2).T
  print(len(data))
  print(len(data2))
  #'''
  

  #data2 = peakFilter(data, 2, 2, fs=sampleRate/subSample)
  #data2 = peakFilter(data2, 2, 2, fs=sampleRate/subSample)
 
  #data2 = butterFilter(data.T, 1, fs=sampleRate/subSample, type='high', order=2).T
  data2 = butterIIR(data.T, 1, sampleRate/subSample, 2).T
  #data2 = butterFilter(data2.T, 2, fs=sampleRate/subSample, type='low', order=2).T


  #plotGyroNorm(data, timeStamp, ax[0])
  #ax[0].set_title('2nd order 20 Hz high pass Butterworth')
  
  plotCosHeight(data[:, [9, 6, 7, 8]], timeStamp, ax[0])
  ax[0].set_title('Waist global cosine height')

  plotCosHeight(data[:, [19, 16, 17, 18]], timeStamp, ax[1])
  ax[1].set_title('Right global cosine height')

  plotCosHeight(data[:, [29, 26, 27, 28]], timeStamp, ax[2])
  ax[2].set_title('Left global cosine height')

  plotAccNorm(data2, timeStamp, ax[3])
  ax[3].set_title('2nd order 20 Hz high pass Butterworth normalised acceleration')


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


def plotCosHeight(quat, timeStamp, ax=False):
  if ax == False:
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))

  cosHeight = quat2cosHeight(quat)

  ax.plot(timeStamp, cosHeight[0], 'r-', linewidth=0.5, label='X axis height')
  ax.plot(timeStamp, cosHeight[1], 'g-', linewidth=0.5, label='Y axis height')
  ax.plot(timeStamp, cosHeight[2], 'b-', linewidth=0.5, label='Z axis height')
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


def plotSpectrogram(data, fs):
  f, t, Sxx = spectrogram(data, fs, nfft=2**10, nperseg=2**5, noverlap=2**2)
  fig, ax = plt.subplots(1, 1, figsize=(8, 4))
  plt.pcolormesh(t, f, Sxx, shading='gouraud')
  plt.ylabel('Frequency [Hz]')
  plt.xlabel('Time [sec]')
  plt.show()


def plotCWT(data):
  widths = np.arange(1, 31)
  cwtmatr = cwt(data, ricker, widths)
  fig, ax = plt.subplots(1, 1, figsize=(8, 4))
  plt.imshow(cwtmatr, extent=[-1, 1, 31, 1], cmap='PRGn', aspect='auto',
            vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
  plt.show()


def generateWindowedSamples():
  for i in range(1, 20+1):
    filePath = './Raw Motion Data/Non-Fall Data/Unlabelled/Unlabelled ('+str(
        i)+').csv'

    plotTimeGraphs(filePath)
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
      plotTimeGraphs(filePath)
