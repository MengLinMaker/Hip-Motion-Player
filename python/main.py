import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import glob
from ML import KNN, getMLperformance

from utility import VIF, generateDataFrame, poseFeature
from CSV import parsePoseFile
from plots import plotTimeGraphs
from globalVariables import sampleRate


if __name__ == "__main__":
  #generateWindowedSamples()

  '''
  fileSrcPath = './Clean Motion Data/Non Fall/Walk (%).csv'
  fileDstPath = './Clean Motion Data/Pose/Stand.csv'
  parsePoseFile(fileSrcPath, fileDstPath, -1)
  #'''

  #'''
  filePaths = glob.glob('./Clean Motion Data/Pose/*.csv')
  headers = ['Pose', 'Waist X', 'Waist Y', 'Waist Z',
             'Right X', 'Right Y', 'Right Z',
             'Left X', 'Left Y', 'Left Z']
  df = generateDataFrame(filePaths, poseFeature, headers)

  plt.figure(figsize=(20, 10))
  plt.title('Scatter plot matrix of features for "' + df.columns[0] + '" detection')
  sns.pairplot(df, hue='Pose', palette='Tab10')


  #sns.heatmap(df.corr(), annot=True, vmin=-1, vmax=1)
  
  X = df[['Pose','Waist X', 'Waist Z',
          'Right Y', 'Right Z',
          'Left Y', 'Left Z']]
  
  categories = []
  for filePath in filePaths:
    categories.append( filePath.split('/')[-1].split('.')[0] )
  #getMLperformance(df, categories, KNN)
  #'''


  #sns.heatmap(df.corr(), annot=True, vmin=-1, vmax=1)
  #sns.pairplot(df, hue='Pose', palette='tab10')
  #plt.subplots_adjust(bottom=0.12, top=0.88)
  #plt.show()

  #print(VIF(X))

  '''
  filePath = './Raw Motion Data/Fall Data/Fall Back/Fall Back (2).csv'
  plotTimeGraphs(filePath)
  plt.show()
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
