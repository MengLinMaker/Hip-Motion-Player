from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd


def prepareDataset(dataset, test_size=0.80):
  # Assign values to the X and y variables:
  X = dataset.iloc[:, 1:-1].values
  y = dataset.iloc[:, 0].values

  # Split dataset into random train and test subsets:
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

  # Standardize features by removing mean and scaling to unit variance:
  scaler = StandardScaler()
  scaler.fit(X_train)

  X_train = scaler.transform(X_train)
  X_test = scaler.transform(X_test)

  return X_train, X_test, y_train, y_test


def KNN(dataset):
  X_train, X_test, y_train, y_test = prepareDataset(dataset)

  # Use the KNN classifier to fit data:
  classifier = KNeighborsClassifier(n_neighbors=3)
  classifier.fit(X_train, y_train)

  # Predict y data with classifier:
  y_predict = classifier.predict(X_test)

  # Print results:
  #print(confusion_matrix(y_test, y_predict))
  print(classification_report(y_test, y_predict))
