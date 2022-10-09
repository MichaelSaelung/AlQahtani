from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.callbacks import CSVLogger

import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split

from res.values import constan, path as dir 

def createModel(featureShape, classShape):
    
    model = Sequential()
    model.add(Conv2D(64, 3, input_shape = featureShape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(2))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(2))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(32))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))

    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))

    model.add(Dense(classShape))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
    #if summary : model.summary()
    model.summary(print_fn=myprint)
    model.save(f'{dir.MODEL_FOLDER}')
    
def fitModel(X_train, y_train, X_test, y_test):
    model = load_model(f'{dir.MODEL_FOLDER}')
    csv_logger = CSVLogger(f'{dir.PICKLE_FOLDER}{constan.LOSS_ACCURACY}.csv')
    model.fit(X_train,y_train,epochs=constan.EPOCHS, verbose = 1, validation_data=(X_test, y_test), callbacks=[csv_logger])
    if False:
        plt.plot(history.history['accuracy'], label='accuracy')
        plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.ylim([0.5, 1])
        plt.legend(loc='lower right')
        plt.show()

def evaluateModel(X_test, y_test):
    model = load_model(f'{dir.MODEL_FOLDER}')
    test_loss, test_acc = model.evaluate(X_test,y_test,verbose = True)
    print('Test lost{0} Test Accuracy {1}'.format(test_loss, test_acc))   

    with open(f'{dir.PICKLE_FOLDER}{constan.LOSS_ACCURACY}.pickle', "wb") as f:
        pickle.dump([test_loss, test_acc], f)

def executeModels():
    
    with open(f'{dir.PICKLE_FOLDER}{constan.TRAIN_TEST}.pickle','rb') as f:
        features, labels = pickle.load(f)
        
        # Membagi dataset ke train dan test dataset
        X_train, X_test, y_train, y_test  = train_test_split(features, labels, test_size=0.3,random_state=42)
        featureShape, classShape = X_train.shape[1:], y_train[0].shape[0]

        createModel(featureShape, classShape)
        fitModel(X_train, y_train, X_test, y_test)
        evaluateModel(X_test, y_test)

def myprint(s):
    with open(f'{dir.PICKLE_FOLDER}{constan.MODEL_SUMMARY}.txt','a') as f:
        print(s, file=f)

# =======================================================================================
# Test Function
# =======================================================================================
#executeModels()


