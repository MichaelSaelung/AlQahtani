from tensorflow.keras.models import load_model
import numpy as np
from os import walk
import time
import pickle

from src import dataset as dst
from res.values import constan, path as dir 

#dst.loadDataset()
#dst.selectionFearture()
#mdl.executeModels()

def imagePrediction():
    class_array = []
    for (dirPath, _,fileNames) in walk(dir.DATA_FOLDER):
        if dirPath.split('/')[-1] != '' : class_array.append(int(dirPath.split('/')[-1]))
    class_array = np.sort(class_array)

    imageCropPath = f'{dir.DRAWABLE_FOLDER}{constan.CROP_FILE_NAME}{constan.IMAGE_TYPE}'
    imageCropPath = dst.convertNewImage(imageCropPath)
    model = load_model(f'{dir.MODEL_FOLDER}')
    #model.summary()

    with open(f'{dir.PICKLE_FOLDER}{constan.LOSS_ACCURACY}.pickle', "rb") as f:
        loss, accuracy = pickle.load(f)

    start_time = time.time()
    try:
        #arr_y_pred = model.predict(imageCropPath)
        arr_y_pred = model(imageCropPath)
        y_pred = np.argmax(arr_y_pred[0, :])
        agePrediction = class_array[y_pred]
        print(arr_y_pred)
    except: print('Terjadi kesalahan Pada Saat Memprediksi Gambar.. ')
    timeExecution = (time.time() - start_time)
    
    return agePrediction, timeExecution, accuracy, loss, np.asarray(arr_y_pred)


#imagePrediction()