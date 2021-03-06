# -*- coding: utf-8 -*-
"""
Firstly , we will download the dataset.
"""

! wget https://archive.ics.uci.edu/ml/machine-learning-databases/00240/UCI%20HAR%20Dataset.zip

#unzip it
!unzip "UCI HAR Dataset.zip"

#moving it into our current working directory
!mv "UCI HAR Dataset" HARDataset/

from numpy import std
from numpy import dstack
from pandas import read_csv

"""Here we will try to load a group of files, such as all of the body acceleration data files as a single group.

"""

# load a single file as a numpy array
def load_file(filepath):
	dataframe = read_csv(filepath, header=None, delim_whitespace=True)
	return dataframe.values
 
# load a list of files, such as x, y, z data for a given variable
def load_group(filenames, prefix=''):
	loaded = list()
	for name in filenames:
		data = load_file(prefix + name)
		loaded.append(data)
	# stack group so that features are the 3rd dimension
	loaded = dstack(loaded)
	return loaded
 
# load the total acc data
filenames = ['total_acc_x_train.txt', 'total_acc_y_train.txt', 'total_acc_z_train.txt']
total_acc = load_group(filenames, prefix='HARDataset/train/Inertial Signals/')
print(total_acc.shape)

# load a single file as a numpy array
def load_file(filepath):
	dataframe = read_csv(filepath, header=None, delim_whitespace=True)
	return dataframe.values
 
# load a list of files, such as x, y, z data for a given variable
def load_group(filenames, prefix=''):
	loaded = list()
	for name in filenames:
		data = load_file(prefix + name)
		loaded.append(data)
	# stack group so that features are the 3rd dimension
	loaded = dstack(loaded)
	return loaded
 
# load a dataset group, such as train or test
def load_dataset(group, prefix=''):
	filepath = prefix + group + '/Inertial Signals/'
	# load all 9 files as a single array
	filenames = list()
	# total acceleration
	filenames += ['total_acc_x_'+group+'.txt', 'total_acc_y_'+group+'.txt', 'total_acc_z_'+group+'.txt']
	# body acceleration
	filenames += ['body_acc_x_'+group+'.txt', 'body_acc_y_'+group+'.txt', 'body_acc_z_'+group+'.txt']
	# body gyroscope
	filenames += ['body_gyro_x_'+group+'.txt', 'body_gyro_y_'+group+'.txt', 'body_gyro_z_'+group+'.txt']
	# load input data
	X = load_group(filenames, filepath)
	# load class output
	y = load_file(prefix + group + '/y_'+group+'.txt')
	return X, y

# load all train
trainX, trainy = load_dataset('train', 'HARDataset/')
print(trainX.shape, trainy.shape)
# load all test
testX, testy = load_dataset('test', 'HARDataset/')
print(testX.shape, testy.shape)

testr = testy
trainr = trainy

testr = testr-1

from keras.utils import np_utils

# zero-offset class values
testy = testy - 1
trainy = trainy - 1

#one hot encoding
testy = np_utils.to_categorical(testy)
testy.shape

#one hot encoding
trainy = np_utils.to_categorical(trainy)
trainy.shape

from keras.models import Sequential
from keras.layers import Dense,Flatten

import matplotlib.pyplot as plt
from mlxtend.plotting import plot_confusion_matrix
from sklearn.metrics import confusion_matrix

import numpy as np

"""# **RNN model**

"""

from keras.layers import SimpleRNN

#building a RNN 
#model creation
modelrnn = Sequential()
modelrnn.add(SimpleRNN(units = 128,input_shape=(128,9)))
modelrnn.add(Dense(units = 64, activation='relu'))
modelrnn.add(Dense(units = 6 , activation='sigmoid'))

modelrnn.summary()

#compile model
modelrnn.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])

#fitting model
history=modelrnn.fit(trainX,trainy,epochs=20,validation_data=(testX,testy))

modelrnn.evaluate(testX, testy)

r_pred = modelrnn.predict_classes(testX)

"""# Confusion Matrix"""

mat = confusion_matrix(testr , r_pred)
plot_confusion_matrix(conf_mat = mat, show_normed=False , figsize=(10,8))

"""# Plotting Curves for Accuracy and Loss"""

plt.figure(figsize=(6, 4))
plt.plot(history.history['accuracy'],'r', label='Accuracy of training data')
plt.plot(history.history['val_accuracy'],'g', label='Accuracy of validation data')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.show()

plt.figure(figsize=(6, 4))
plt.plot(history.history['loss'],'r', label='Loss of training data')
plt.plot(history.history['val_loss'],'g', label='Loss of validation data')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend(loc='upper right')
plt.show()

"""# Classification Report"""

from sklearn.metrics import classification_report
y_pred = modelrnn.predict(testX)
y_pred_classes = [np.argmax(element) for element in y_pred]
print('\nClassification Report\n')
print(classification_report(testr, y_pred_classes, target_names=["WALKING", "WALKING_UPSTAIRS", "WALKING_DOWNSTAIRS", "SITTING", "STANDING", "LAYING"]))
#here we needed testr not testy

"""## We can see RNN model gives an accuracy of 71%

# **LSTM model**
"""

from keras.layers import LSTM

#building a LSTM
#model creation
modellstm = Sequential()
modellstm.add(LSTM(units = 128,input_shape=(trainX.shape[1:]),return_sequences=True))
modellstm.add(LSTM(units = 64))
modellstm.add(Dense(units = 64, activation='relu'))
modellstm.add(Dense(units = 6 , activation='sigmoid'))

modellstm.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])

modellstm.summary()

historyy=modellstm.fit(trainX,trainy,epochs=20,validation_data=(testX,testy))

modellstm.evaluate(testX, testy)

r_pred = modellstm.predict_classes(testX)

"""# Confusion Matrix"""

mat = confusion_matrix(testr , r_pred)
plot_confusion_matrix(conf_mat = mat, show_normed=False , figsize=(10,8))

"""
# Plotting Curves for Accuracy and Loss"""

plt.figure(figsize=(6, 4))
plt.plot(historyy.history['accuracy'],'r', label='Accuracy of training data')
plt.plot(historyy.history['val_accuracy'],'g', label='Accuracy of validation data')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.show()

plt.figure(figsize=(6, 4))
plt.plot(historyy.history['loss'],'r', label='Loss of training data')
plt.plot(historyy.history['val_loss'],'g', label='Loss of validation data')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend(loc='upper right')
plt.show()

"""# Classification Report"""

from sklearn.metrics import classification_report
y_pred = modellstm.predict(testX)
y_pred_classes = [np.argmax(element) for element in y_pred]
print('\nClassification Report\n')
print(classification_report(testr, y_pred_classes, target_names=["WALKING", "WALKING_UPSTAIRS", "WALKING_DOWNSTAIRS", "SITTING", "STANDING", "LAYING"]))
#here we needed testr not testy

"""# We can see LSTM model gives an accuracy of 92%
Therefore we can say LSTM works well on time-series data.

# **GRU Model**
"""

from keras.layers import GRU

#building a GRU
#model creation
modelgru = Sequential()
modelgru.add(GRU(units = 128,input_shape=(trainX.shape[1:]),return_sequences=True))
modelgru.add(GRU(units = 64))
modelgru.add(Dense(units = 64, activation='relu'))
modelgru.add(Dense(units = 6 , activation='sigmoid'))

modelgru.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])

modelgru.summary()

history=modelgru.fit(trainX,trainy,epochs=20,validation_data=(testX,testy))

modelgru.evaluate(testX, testy)

r_pred = modelgru.predict_classes(testX)

"""# Confusion Matrix"""

mat = confusion_matrix(testr , r_pred)
plot_confusion_matrix(conf_mat = mat, show_normed=False , figsize=(10,8))

"""# Plotting Curves for Accuracy and Loss"""

plt.figure(figsize=(6, 4))
plt.plot(history.history['accuracy'],'r', label='Accuracy of training data')
plt.plot(history.history['val_accuracy'],'g', label='Accuracy of validation data')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.show()

plt.figure(figsize=(6, 4))
plt.plot(history.history['loss'],'r', label='Loss of training data')
plt.plot(history.history['val_loss'],'g', label='Loss of validation data')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend(loc='upper right')
plt.show()

"""# Classification Report"""

from sklearn.metrics import classification_report
y_pred = modelgru.predict(testX)
y_pred_classes = [np.argmax(element) for element in y_pred]
print('\nClassification Report\n')
print(classification_report(testr, y_pred_classes, target_names=["WALKING", "WALKING_UPSTAIRS", "WALKING_DOWNSTAIRS", "SITTING", "STANDING", "LAYING"]))
#here we needed testr not testy

"""# GRU model gives an accuracy of 90%"""
