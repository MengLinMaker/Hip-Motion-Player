import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from glob import glob
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
  fileSrcPath = './Clean Motion Data/Non Fall/Walk/Walk (1).csv'
  fileDstPath = './Clean Motion Data/Pose/Stand.csv'
  parsePoseFile(fileSrcPath, fileDstPath, -1)
  #'''

  '''
  filePaths = glob('./Pose/*.csv')
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
  #filePath = './Raw Motion Data/Fall Data/Fall Front/Fall Front (1).csv'
  filePath = './Raw Motion Data/Non-Fall Data/Walk/Walk (20).csv'
  #filePath = './Raw Motion Data/Non-Fall Data/Run/Run (20).csv'
  #filePath = './Raw Motion Data/Non-Fall Data/Stair/Stair (20).csv'
  #filePath = './Raw Motion Data/Fall Data/Fall Right/Fall Right (20).csv'
  plotTimeGraphs(filePath, 5)
  plt.show()

  

  #'''
