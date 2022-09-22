import numpy as np
import csv
from scipy.signal import butter, lfilter



def getCsvData(filePath):
  file = open(filePath)
  csvreader = csv.reader(file)
  data = []

  for row in csvreader:
    row = np.array(row).astype(np.float)
    data.append(row)

  file.close()
  return np.array(data)


def saveCsvData(filePath, data):
  f = open(filePath, 'w')
  writer = csv.writer(f)

  for row in data:
    writer.writerow(row)

  f.close()



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