import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import glob
from ML import Random_Forest, getMLperformance, KNN, Naive_Bayesian, SVM, Decision_Tree, Logistic_Regression

from utility import VIF, generateDataFrame, motionFeature, poseFeature
from CSV import getCsvData, parsePoseFile
from plots import plotTimeGraphs, generateWindowedSamples
from globalVariables import sampleRate


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
  print(labels)

  allData = np.array([])
  for filePath in filePaths:
    data = getCsvData(filePath)
    label = filePath.split('/')[-1].split(' (')[0]
    labelID = np.float64(np.where(labels == label)[0])

    feature = motionFeature(data)
    dataSample = np.r_[labelID , feature]
    if len(allData) < 1:
      allData = dataSample
    else:
      allData = np.c_[allData, dataSample]
  
  headers = np.arange(len(allData)-1)
  headers = np.r_[['Motion Type'], headers]
  df = pd.DataFrame(data=allData.T, columns=headers)
  getMLperformance(df, labels, KNN, 1000)
  #'''
