
import cv2 as cv
from os import walk, path
import pickle
import numpy as np
from random import shuffle
from sklearn.preprocessing import LabelEncoder,OneHotEncoder

from res.values import constan, path as dir 

#import matplotlib.pyplot as plt

def loadDataset(IMAGE_SIZE = constan.IMAGE_SIZE):
    dataset = []
    # load semua file yang ada di folder dataset
    for (dirPath, _,fileNames) in walk(dir.DATA_FOLDER):
        for fileName in fileNames:
            # cek file type
            if fileName.endswith(constan.IMAGE_TYPE):
                try:
                    object_array = cv.imread(path.join(dirPath, fileName),-1)
                    # resize image 
                    object_array = cv.resize(object_array, (IMAGE_SIZE,IMAGE_SIZE))
                    # mengubah Paht ke Kelas Image
                    class_array = dirPath.split('/')[-1]
                    # Mengabungkan Dependent Dan Independet Variable, atau features dari image dam Kelas dari image tersebut
                    dataset.append([object_array, class_array])
                    #print(dataset)
                except: print('Terjadi kesalahan Pada Saat Generate Dataset.. ')
    shuffle(dataset)

    # simpan dataset dalam pickle format
    with open(f'{dir.PICKLE_FOLDER}{constan.DATASET_PICKLE_NAME}.pickle', "wb") as f:
        pickle.dump(dataset, f)
    
def selectionFeature():
        features = []
        labels = []
        try:
            for feature, label in pickle.load(open(f'{dir.PICKLE_FOLDER}{constan.DATASET_PICKLE_NAME}.pickle','rb')):
                features.append(feature)
                labels.append(label)
            
            # integer encode
            labels = np.array(labels)
            label_encoder = LabelEncoder()
            integer_encoded = label_encoder.fit_transform(labels)

            # binarry encode, onehotencode merubah class ke binnary
            onehot_encoder = OneHotEncoder(sparse=False)
            integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
            labels = onehot_encoder.fit_transform(integer_encoded)

            #digunakna untuk inverted(membalikan lagi one hot encoding ke bentuk klas awal)
            #inverted = label_encoder.inverse_transform([argmax(labels[0, :])])


            features = np.array(features) / 255.0

            with open(f'{dir.PICKLE_FOLDER}{constan.TRAIN_TEST}.pickle', "wb") as f:
                pickle.dump([features,labels], f)

        except: print('Terjadi kesalahan Pada Saat merescale dari 0-255 menjadi 0-1.. ')
        
def convertNewImage(imgPath, IMAGE_SIZE = constan.IMAGE_SIZE):
    object_array = cv.imread(imgPath)
    object_array = cv.resize(object_array, (IMAGE_SIZE,IMAGE_SIZE))

    object_array = np.array(object_array).reshape(-1,IMAGE_SIZE,IMAGE_SIZE,3)
    #print(object_array.shape)
    newImg = object_array / 255.0
    
    return newImg

# =======================================================================================
# Test Function
# =======================================================================================
#newImg = convertNewImage(img path)
#print(newImg.shape)
#loadDataset()
#selectionFeature()
