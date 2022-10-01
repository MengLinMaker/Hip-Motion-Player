from glob import glob
from tkinter import NS
from matplotlib import projections, pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import pandas as pd
import seaborn as sns

from CSV import getCsvData
from ML import Random_Forest, getMLperformance, KNN, Naive_Bayesian, SVM, Decision_Tree, Logistic_Regression
from plots import plotPCA
from utility import mirrorData, motionFeature

from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
from mpl_toolkits import mplot3d
import plotly.express as px


def cleanMotionTrainer(filePaths, labels, subSample=5):
  allData = np.array([])
  for filePath in filePaths:
    for even in range(2):
      label = filePath.split('/')[-1].split(' (')[0]
      data = getCsvData(filePath)
      data = data[np.arange(0, len(data), subSample), :]
      if even == 1:
        data = mirrorData(data)
        if label == 'Fall Left': label = 'Fall Right'
        elif label == 'Fall Right': label = 'Fall Left'
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
  return df.rename(columns={0: 'Motion Type'})


def supervisedMotionDetection():
  filePaths = glob('./Clean Motion Data/*/*/*.csv')
  labels = []
  for dir in glob('./Clean Motion Data/*/*'):
    label = dir.split('/')[-1]
    labels.append(label)
  labels = np.array(labels)
  #labels = labels[3::]
  #labels[0] = labels[0].split(' ')[0]
  #labels = ['Fall', 'Non-Fall']

  df = cleanMotionTrainer(filePaths, labels, subSample=2)
  #plotPCA(df, labels)
  getMLperformance(df, labels, Naive_Bayesian, 1000)







if __name__ == "__main__":
  supervisedMotionDetection()