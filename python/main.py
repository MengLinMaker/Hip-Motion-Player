import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import glob
from ML import Random_Forest, getMLperformance, KNN, Naive_Bayesian, SVM, Decision_Tree, Logistic_Regression

from utility import VIF, butterIIR, generateDataFrame, motionFeature, norm, poseFeature
from CSV import getCsvData, parsePoseFile
from plots import plotTimeGraphs, generateWindowedSamples
from globalVariables import sampleRate

import tsfel
#from tsfresh.feature_extraction import ComprehensiveFCParameters, extract_features
#from tsfresh import select_features
#from tsfresh.utilities.dataframe_functions import impute


if __name__ == "__main__":
  #generateWindowedSamples()

  '''
  fileSrcPath = './Clean Motion Data/Non Fall/Walk (%).csv'
  fileDstPath = './Clean Motion Data/Pose/Stand.csv'
  parsePoseFile(fileSrcPath, fileDstPath, -1)
  #'''

  '''
  filePaths = glob.glob('./Pose/*.csv')
  headers = ['Pose', 'Waist X', 'Waist Y', 'Waist Z',
             'Right X', 'Right Y', 'Right Z',
             'Left X', 'Left Y', 'Left Z']
  df = generateDataFrame(filePaths, poseFeature, headers)

  #sns.pairplot(df, hue='Pose', palette='Set2')

  #sns.heatmap(df.corr(), annot=True, vmin=-1, vmax=1)
  
  X = df[['Pose','Waist X', 'Waist Z',
          'Right Y', 'Right Z',
          'Left Y', 'Left Z']]
  
  categories = []
  for filePath in filePaths:
    categories.append( filePath.split('/')[-1].split('.')[0] )
  #getMLperformance(df, categories, Random_Forest, 1000)
  #'''


  #sns.heatmap(df.corr(), annot=True, vmin=-1, vmax=1)
  #sns.pairplot(df, hue='Pose', palette='tab10')
  #plt.subplots_adjust(bottom=0.12, top=0.88)
  #plt.show()

  #print(VIF(X))

  #'''
  filePath = './Raw Motion Data/Fall Data/Fall Front/Fall Front (1).csv'
  #filePath = './Raw Motion Data/Non-Fall Data/Walk/Walk (20).csv'
  #filePath = './Raw Motion Data/Non-Fall Data/Run/Run (20).csv'
  #filePath = './Raw Motion Data/Non-Fall Data/Stair/Stair (20).csv'
  #filePath = './Raw Motion Data/Fall Data/Fall Right/Fall Right (20).csv'

  
  
  filePaths = glob.glob('./Clean Motion Data/*/*/*.csv')
  labels = []
  for dir in glob.glob('./Clean Motion Data/*/*'):
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

    orientationFeature = poseFeature(data)
    dataHigh = butterIIR(data.T, 1, sampleRate/subSample, 2).T
    waistAccNorm = norm(dataHigh[:, 3:6])
    rightAccNorm = norm(dataHigh[:, 13:16])
    leftAccNorm = norm(dataHigh[:, 23:26])


    #df_file = pd.read_csv(filePath)
    #df_file = pd.DataFrame(data=np.c_[orientationFeature, waistAccNorm, leftAccNorm, rightAccNorm])
    #cfg = tsfel.get_features_by_domain("temporal")
    #X = tsfel.time_series_features_extractor(cfg, df_file)

    feature = motionFeature(data, subSample)
    dataSample = np.r_[labelID, feature]#, X.to_numpy()[0]]
    if len(allData) < 1:
      allData = dataSample
    else:
      allData = np.c_[allData, dataSample]

  df = pd.DataFrame(data=allData.T)
  df = df.rename(columns = {0: 'Motion Type'})

  #sns.heatmap(df.corr(), vmin=-1, vmax=1)
  #print(VIF(df))
  getMLperformance(df, labels, Naive_Bayesian, 1000)
  #'''
