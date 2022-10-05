from glob import glob
from matplotlib import projections, pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.semi_supervised import LabelSpreading
from sklearn_porter import Porter

from CSV import getCsvData
from ML import Random_Forest, getMLperformance, KNN, Naive_Bayesian, SVM, Decision_Tree, Logistic_Regression, prepareDataset
from plots import plotLDA, plotPCA
from utility import mirrorData, motionFeature, quat2cosHeight
from globalVariables import sampleRate


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

      feature = motionFeature(data, subSample)
      dataSample = np.r_[labelID, feature]
      if len(allData) < 1:
        allData = dataSample
      else:
        allData = np.c_[allData, dataSample]

  df = pd.DataFrame(data=allData.T)
  return df.rename(columns={0: 'Motion Type'})


def unlabelledMotionTrainer(filePaths, subSample=5):
  timeLen = 3
  timeSample = 1
  windowLen = round(timeLen * sampleRate / subSample)
  windowSample = round(timeSample * sampleRate / subSample)
    
  allData = np.array([])
  labelID = -1
  for filePath in filePaths:
    fileData = getCsvData(filePath)
    fileData = fileData[np.arange(0, len(fileData), subSample), :]

    for timeID in range(0, len(fileData)-windowLen, windowSample):
      data = fileData[timeID:timeID + windowLen,:]
      for even in range(2):
        if even == 1:
          data = mirrorData(data)

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

  df_labelled = cleanMotionTrainer(filePaths, labels, subSample=5)

  #plotPCA(df_labelled, labels)
  #plotLDA(df_labelled, labels)
  #print(quat2cosHeight(np.array( [[1,0,0,10],[0,1,0,10],[0,0,1,10],[1,1,1,10]] )).T)
  getMLperformance(df_labelled, labels, Naive_Bayesian, 100)


def generateClassifierCode(clf, df, lang='js', dst='./'):
  X_train, X_test, y_train, y_test = prepareDataset(df, test_size=0.001)
  clf.fit(X_train, y_train)

  porter = Porter(clf, language=lang)
  classifierCode = porter.export(embed_data=False)

  if lang == 'js':
    classifierCode = 'export ' + classifierCode

  classifierFile = open(dst + clf.__class__.__name__ + '.' + lang, 'w')
  classifierFile.write(classifierCode)






if __name__ == "__main__":
  supervisedMotionDetection()

  '''
  filePaths = glob('./Clean Motion Data/*/*/*.csv')
  labels = []
  for dir in glob('./Clean Motion Data/*/*'):
    label = dir.split('/')[-1]
    labels.append(label)
  labels = np.array(labels)
  #labels = labels[3::]
  #labels[0] = labels[0].split(' ')[0]
  #labels = ['Fall', 'Non-Fall']

  df_labelled = cleanMotionTrainer(filePaths, labels, subSample=5)
  
  dummy, clf = SVM(df_labelled)
  dst = './src/visualiser/machineLearning/'
  generateClassifierCode(clf, df_labelled, lang='js', dst=dst)
  '''

  '''
  filePaths = glob('./Raw Motion Data/*/*/*.csv')
  df_unlabelled = unlabelledMotionTrainer(filePaths, subSample=5)
  print(df_unlabelled)

  X_train, X_test, y_train, y_test = prepareDataset(df_labelled, test_size=0.50)
  df_labelled = pd.DataFrame(data=np.c_[y_train, X_train])
  df_labelled = df_labelled.rename(columns={0: 'Motion Type'})
  df_unlabelled = pd.concat([df_labelled, df_unlabelled], ignore_index=True)
  print(df_unlabelled)

  X_train, dummy1, y_train, dummy2 = prepareDataset(df_unlabelled, test_size=0.001)
  df_unlabelled = pd.DataFrame(data=np.c_[y_train, X_train]).sample(frac=1)
  df_unlabelled = df_unlabelled.rename(columns={0: 'Motion Type'})
  print(df_unlabelled)

  label_spread = LabelSpreading(kernel='knn', alpha=0.02, max_iter=50, gamma=0.25)
  label_spread.fit(df_unlabelled.iloc[:, 1::].values, df_unlabelled.iloc[:, 0].values)
  df_unlabelled.values[:, 0] = label_spread.transduction_
  X_train, dummy1, y_train, dummy2 = prepareDataset(df_unlabelled, test_size=0.001)
  print(df_unlabelled)



  plotLDA(df_unlabelled, labels)
  plt.show()
  #'''

  '''
  classifier = GaussianNB()
  classifier.fit(X_train, y_train)
  y_predict = classifier.predict(X_test)
  confusionMatrix = confusion_matrix(y_test, y_predict)
  
  confusionMatrix = confusionMatrix / np.sum(confusionMatrix)
  accuracy = 100 * np.trace(confusionMatrix)
  precision = 100 * confusionMatrix.diagonal() / np.sum(confusionMatrix, axis=1)
  recall = 100 * confusionMatrix.diagonal() / np.sum(confusionMatrix, axis=0)

  plt.figure(figsize=(12, 6))
  plt.title('Naive_Bayesian average confusion matrix for "' +
            df_unlabelled.columns[0] + '" detection')

  accuracyText = ' accuracy: {accuracy: .2f}%, Precision: {precision: .2f}%, Recall: {recall: .2f}%'.format(
      accuracy=accuracy, precision=np.average(precision), recall=np.average(recall))
  plt.figtext(0.45, 0.03, accuracyText, ha="center", fontsize=12,
              bbox={"facecolor": "orange", "alpha": 0.5, "pad": 5})

  df_cm = pd.DataFrame(confusionMatrix, labels, labels)
  sns.heatmap(df_cm, annot=True, fmt=".3%", cmap=sns.color_palette(
      "Spectral", as_cmap=True), norm=LogNorm(), linewidths=1, linecolor='grey')
  plt.show()
  #'''
