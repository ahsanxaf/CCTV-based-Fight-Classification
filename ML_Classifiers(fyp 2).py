# -*- coding: utf-8 -*-
"""Untitled1 (1) (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11yRgnksWpLHI62Uan0caLtfuEfd3jfmp
"""

import cv2 as cv
import numpy as np
import os
import imutils
import random
import matplotlib.pyplot as plt
from skimage.feature import hog
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm

directory = r'C:\\Users\\AHSAN FAROOQ\\OneDrive\\Desktop\\fight-detection-surv-dataset-master\\fight-detection-surv-dataset-master'
#directory = r'C:\Users\AHSAN FAROOQ\OneDrive\Desktop\Fight dataset'
CATEGORIES = ['fight', 'noFight']

orb_data = []
orb_X = []
orb_Y = []
count = 0

data, labels = [],[]
frame_size = 1200
for category in CATEGORIES:
    folder = os.path.join(directory, category)
    label = CATEGORIES.index(category)
    print(folder)
    for frame in os.listdir(folder):
        frm_path = os.path.join(folder, frame)
        cap = cv.VideoCapture(frm_path)
        video = []
        while cap.isOpened():
            ret, frames = cap.read()
            if ret == True:
                video.append(frames)
            else:
                break
        if len(video) > 30:
            for i in range(len(video)):
                video[i] = cv.resize(video[i], (120, 80))
        #              video[i] = cv.cvtColor(video[i], cv.COLOR_BGR2GRAY)
            rem = len(video) % 30
            video = video[int(rem/2): -(int(rem/2))]
            if len(video) % 2 != 0:
                video = video[1:]
            NumberOfSamples = int(len(video)/30)
            for i in range(NumberOfSamples):
                sample = np.array(video[i*30: ((i+1)*30)])   
                features = []
                for i in range(len(sample)):
                    orb = cv.ORB_create()
                    orbKeypoints, orbDescriptors = orb.detectAndCompute(sample[i], None)
                    frame_features = list(np.ravel(orbDescriptors))
                    if len(frame_features) >= frame_size:
                        frame_features = np.squeeze(frame_features[:frame_size])
                    else:
                        if len(frame_features) < 50:
                            frame_features = [0]*frame_size
                        else:
                            frame_features = pad_sequences(np.array(frame_features).reshape(1,-1), maxlen=frame_size, dtype="int32", padding = "pre", truncating = "pre", value = 0.0)
                    features.append(np.squeeze(frame_features))
                data.append(list(np.ravel(features)))
                labels.append(category)

data = np.array(data)
labels = np.array(labels)

print(data.shape)

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(labels)
labels = le.transform(labels)

X_train, X_test, Y_train, Y_test = train_test_split(data, labels, test_size=0.2, random_state=1)

"""## Decision Tree"""

tree_clf = DecisionTreeClassifier(criterion="entropy", max_depth=5000)
tree_clf.fit(X_train, Y_train)
y_pred = tree_clf.predict(X_test)

print(y_pred)

Accuracy = metrics.balanced_accuracy_score(y_pred, Y_test)

print(Accuracy)

metrics.plot_confusion_matrix(tree_clf, X_test, Y_test, display_labels=['Fight', 'NoFight'])

recall_sensitivity = metrics.recall_score(Y_test, y_pred, pos_label=0)
recall_specificity = metrics.recall_score(Y_test, y_pred, pos_label=1)
print(recall_sensitivity, recall_specificity)

"""## Random Forest"""

forest_clf = RandomForestClassifier(n_estimators=11, random_state=0)
forest_clf.fit(X_train, Y_train)
y_pred_forest = forest_clf.predict(X_test)

print(y_pred_forest)

Accuracy = metrics.accuracy_score(Y_test, y_pred_forest)

print(Accuracy)

trees = range(1, 51)
scores = []
for tree in trees:
    forest_clf1 = RandomForestClassifier(n_estimators=tree, random_state=1)
    forest_clf1.fit(X_train, Y_train)
    y_pred_forest = forest_clf1.predict(X_test)
    Accuracy = metrics.accuracy_score(Y_test, y_pred_forest)
    scores.append(Accuracy)

plt.plot(trees, scores)
plt.xlabel("No. of trees")
plt.ylabel("Testing Accuracy")

metrics.plot_confusion_matrix(forest_clf, X_test, Y_test, display_labels=['Fight', 'NoFight'])

confusion = metrics.confusion_matrix(Y_test, y_pred_forest)

print(confusion)

recall_sensitivity = metrics.recall_score(Y_test, y_pred_forest, pos_label=0)
recall_specificity = metrics.recall_score(Y_test, y_pred_forest, pos_label=1)
print(recall_sensitivity, recall_specificity)

"""## Naive Bayes"""

gnb = GaussianNB()
y_pred_gnb = gnb.fit(X_train, Y_train).predict(X_test)

print(y_pred_gnb)

Accuracy = metrics.accuracy_score(Y_test, y_pred_gnb)

print(Accuracy)

metrics.plot_confusion_matrix(gnb, X_test, Y_test, display_labels=['Fight', 'NoFight'])

recall_sensitivity = metrics.recall_score(Y_test, y_pred_gnb, pos_label=0)
recall_specificity = metrics.recall_score(Y_test, y_pred_gnb, pos_label=1)
print(recall_sensitivity, recall_specificity)

"""## KNN"""

knn = KNeighborsClassifier(n_neighbors=10)

knn.fit(X_train, Y_train)

y_pred_knn = knn.predict(X_test)

print(y_pred_knn)

Accuracy = metrics.accuracy_score(Y_test, y_pred_knn)

print(Accuracy)

k_range = range(1, 101)
scores = []
for k in k_range:
    knn1 = KNeighborsClassifier(n_neighbors=k)
    knn1.fit(X_train, Y_train)
    y_pred_knn1 = knn1.predict(X_test)
    Accuracy = metrics.accuracy_score(Y_test, y_pred_knn1)
    scores.append(Accuracy)

plt.plot(k_range, scores)
plt.xlabel("Value of K for KNN")
plt.ylabel("Testing Accuracy")

metrics.plot_confusion_matrix(knn, X_test, Y_test, display_labels=['Fight', 'NoFight'])

recall_sensitivity = metrics.recall_score(Y_test, y_pred_knn, pos_label=0)
recall_specificity = metrics.recall_score(Y_test, y_pred_knn, pos_label=1)
print(recall_sensitivity, recall_specificity)

