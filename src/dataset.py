
import pickle
from os import path, walk

import cv2 as cv
import numpy as np
import tensorflow.keras.utils as utl

from res.values import constan
from res.values import path as dir


def loadDataset():
    labels, features = [], []
    firstClassLabel = classLabel()[0]
    # load semua file yang ada di folder dataset
    for (dirPath, _,fileNames) in walk(dir.DATA_FOLDER):
        for fileName in fileNames:
            # cek file type
            if fileName.endswith(constan.IMAGE_TYPE):
                # mengubah Paht ke Kelas Image
                feature = cv.imread(path.join(dirPath, fileName))
                feature = cv.resize(feature, (constan.IMAGE_SIZE, constan.IMAGE_SIZE))
                
                label = int(dirPath.split('/')[-1]) - firstClassLabel

                labels.append(label)
                features.append(feature)
     
    features = np.array(features) / 255.0
    features = features.reshape(-1, constan.IMAGE_SIZE, constan.IMAGE_SIZE, constan.DIMENTION)
    
    labels = utl.to_categorical(np.array(labels))

    with open(f'{dir.PICKLE_FOLDER}{constan.TRAIN_TEST}.pickle', "wb") as f:
        pickle.dump([features, labels], f) 
        
def classLabel():
    class_array = []
    for (dirPath, _,fileNames) in walk(dir.DATA_FOLDER):
        if dirPath.split('/')[-1] != '' : class_array.append(int(dirPath.split('/')[-1]))
    class_array = np.sort(class_array)
    return class_array