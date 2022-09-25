import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn import svm


def getMLperformance(df, header, classifier, numTests=1000):
  numClass = len(df[df.columns[0]].unique())
  confusionMatrix = np.zeros((numClass, numClass))

  for i in range(0, numTests):
    testConfusion = classifier(df)
    if len(testConfusion) == len(confusionMatrix):
      confusionMatrix = confusionMatrix + testConfusion

  confusionMatrix = confusionMatrix / np.sum(confusionMatrix)
  accuracy = 100 * np.trace(confusionMatrix)
  precision = 100 * confusionMatrix.diagonal() / np.sum(confusionMatrix, axis=1)
  recall = 100 * confusionMatrix.diagonal() / np.sum(confusionMatrix, axis=0)

  plt.figure(figsize=(12, 6))
  plt.title(classifier.__name__ + ' average confusion matrix for "' + df.columns[0] + '" detection')
  
  accuracyText = ' accuracy: {accuracy: .2f}%, Precision: {precision: .2f}%, Recall: {recall: .2f}%'.format(
    accuracy=accuracy, precision=np.average(precision), recall=np.average(recall))
  plt.figtext(0.45, 0.03, accuracyText, ha="center", fontsize=12, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

  df_cm = pd.DataFrame(confusionMatrix, header, header)
  sns.heatmap(df_cm, annot=True, fmt=".2%")

  plt.show()


def prepareDataset(df, test_size=0.20):
  # Assign values to the X and y variables:
  X = df.iloc[:, 1::].values
  y = df.iloc[:, 0].values

  # Split dataframe into random train and test subsets:
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
  return X_train, X_test, y_train, y_test


'''
Machine Learning algorithms below
'''

def KNN(df, n_neighbors=1):
  X_train, X_test, y_train, y_test = prepareDataset(df)
  classifier = KNeighborsClassifier(n_neighbors=n_neighbors)
  classifier.fit(X_train, y_train)
  y_predict = classifier.predict(X_test)
  return confusion_matrix(y_test, y_predict)


def Naive_Bayesian(df):
  X_train, X_test, y_train, y_test = prepareDataset(df)
  classifier = GaussianNB()
  classifier.fit(X_train, y_train)
  y_predict = classifier.predict(X_test)
  return confusion_matrix(y_test, y_predict)


def SVM(df):
  X_train, X_test, y_train, y_test = prepareDataset(df)
  classifier = svm.SVC(kernel='rbf')
  classifier.fit(X_train, y_train)
  y_predict = classifier.predict(X_test)
  return confusion_matrix(y_test, y_predict)


def Random_Forest(df):
  X_train, X_test, y_train, y_test = prepareDataset(df)
  classifier = RandomForestClassifier(n_estimators=10)
  classifier.fit(X_train, y_train)
  y_predict = classifier.predict(X_test)
  return confusion_matrix(y_test, y_predict)


def Decision_Tree(df):
  X_train, X_test, y_train, y_test = prepareDataset(df)
  classifier = DecisionTreeClassifier()
  classifier.fit(X_train, y_train)
  y_predict = classifier.predict(X_test)
  return confusion_matrix(y_test, y_predict)


def LDA(df):
  X_train, X_test, y_train, y_test = prepareDataset(df)
  classifier = LinearDiscriminantAnalysis()
  classifier.fit(X_train, y_train)
  y_predict = classifier.predict(X_test)
  return confusion_matrix(y_test, y_predict)


def Logistic_Regression(df):
  X_train, X_test, y_train, y_test = prepareDataset(df)
  classifier = LogisticRegression()
  classifier.fit(X_train, y_train)
  y_predict = classifier.predict(X_test)
  return confusion_matrix(y_test, y_predict)