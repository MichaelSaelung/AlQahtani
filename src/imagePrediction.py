import pickle
import test as t
import time

import cv2 as cv
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model

from res.values import constan
from res.values import path as dir
from src import dataset as dst

class_array = dst.classLabel()
model = load_model(f'{dir.MODEL_FOLDER}{constan.MODEL_FILE_NAME}')

def imagePrediction():

    imageCropPath = f'{dir.DRAWABLE_FOLDER}{constan.CROP_FILE_NAME}{constan.IMAGE_TYPE}'
    feature = cv.imread(imageCropPath)
    feature = cv.resize(feature, (constan.IMAGE_SIZE, constan.IMAGE_SIZE))    
    features = np.array(feature) / 255.0
    features = features.reshape(-1, constan.IMAGE_SIZE, constan.IMAGE_SIZE, constan.DIMENTION)
    
    with open(f'{dir.PICKLE_FOLDER}{constan.LOSS_ACCURACY}.pickle', "rb") as f:
        loss, accuracy = pickle.load(f)
    try:
        
        start_time = time.time()
        arr_y_pred = model.predict(features)
        #arr_y_pred = model(imageCrop)
        timeExecution = (time.time() - start_time)   
        
        y_pred = np.argmax(arr_y_pred[0, :])
        y_pred = class_array[y_pred]

    except: print('Terjadi kesalahan Pada Saat Memprediksi Gambar.. ')

    return y_pred, timeExecution, accuracy, loss, np.asarray(arr_y_pred), class_array[0]

def test():

    with open(f'{dir.PICKLE_FOLDER}{constan.TRAIN_TEST}.pickle','rb') as f:
        features, labels = pickle.load(f)
        _, X_val, _, y_val  = train_test_split(features, labels, test_size=0.3,random_state=42)
        y_preds, y_trues  = [], []
    try:
        start_time = time.time()
        arr_y_pred = model.predict(X_val)           
        #arr_y_pred = model(imageCrop)
        timeExecution = (time.time() - start_time)   

        for x in range(len(arr_y_pred)):
            y_pred = np.argmax(arr_y_pred[x, :])
            y_pred = class_array[y_pred]
            y_preds.append(y_pred)

            y_true = np.argmax(y_val[x, :])
            y_true = class_array[y_true]
            y_trues.append(y_true)

    except: print('Terjadi kesalahan Pada Saat Memprediksi Gambar.. ')
    with open(f'{dir.PICKLE_FOLDER}{constan.YTRUE_YPRED}.pickle', "wb") as f:
        pickle.dump((y_trues, y_preds), f) 
    
