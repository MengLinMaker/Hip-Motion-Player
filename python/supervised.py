from glob import glob
import numpy as np
import pandas as pd


from CSV import getCsvData
from ML import Naive_Bayesian, getMLperformance
from utility import motionFeature


def supervisedMotionDetection():
  filePaths = glob('./Clean Motion Data/*/*/*.csv')
  labels = []
  for dir in glob('./Clean Motion Data/*/*'):
    label = dir.split('/')[-1]
    labels.append(label)
  labels = np.array(labels)
  #labels = labels[3::]
  #labels[0] = labels[0].split(' ')[0]
  #labels = [labels[0].split(' ')[0], 'Non-Fall']

  allData = np.array([])
  subSample = 5
  for filePath in filePaths:
    data = getCsvData(filePath)
    data = data[np.arange(0, len(data), subSample), :]
    label = filePath.split('/')[-1].split(' (')[0]
    #labelID = 1
    #if label == labels[0]: labelID = 0
    labelID = np.float64(np.where(labels == label)[0])

    '''
    orientationFeature = poseFeature(data)
    dataHigh = butterIIR(data.T, 1, sampleRate/subSample, 2).T
    waistAccNorm = norm(dataHigh[:, 3:6])
    rightAccNorm = norm(dataHigh[:, 13:16])
    leftAccNorm = norm(dataHigh[:, 23:26])
    df_file = pd.read_csv(filePath)
    df_file = pd.DataFrame(data=np.c_[orientationFeature, waistAccNorm, leftAccNorm, rightAccNorm])
    cfg = tsfel.get_features_by_domain("temporal")
    X = tsfel.time_series_features_extractor(cfg, df_file).to_numpy()[0]
    #'''

    feature = motionFeature(data, subSample)
    dataSample = np.r_[labelID, feature]
    if len(allData) < 1:
      allData = dataSample
    else:
      allData = np.c_[allData, dataSample]

  df = pd.DataFrame(data=allData.T)
  df = df.rename(columns = {0: 'Motion Type'})

  #sns.heatmap(df.corr(), vmin=-1, vmax=1, cmap=sns.color_palette("icefire",as_cmap=True))
  #print(VIF(df).to_numpy())
  getMLperformance(df, labels, Naive_Bayesian, 1000)


if __name__ == "__main__":
  supervisedMotionDetection()