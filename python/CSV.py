import numpy as np
import csv


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


def parsePoseFile(fileSrcPath, fileDstPath, ID):
  pathString = fileSrcPath.split('%')

  data = []
  for i in range(1, 20+1):
    fileSrcPath = pathString[0] + str(i) + pathString[1]
    dataPoint = getCsvData(fileSrcPath)[ID, :]
    data.append(dataPoint)
  data = np.array(data)
  saveCsvData(fileDstPath, data)
