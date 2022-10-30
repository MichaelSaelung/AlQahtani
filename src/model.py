import pickle

from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import CSVLogger
from tensorflow.keras.layers import Conv2D, Dense, Flatten, MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import SGD

from res.values import constan
from res.values import path as dir


def myprint(s):
    with open(f'{dir.PICKLE_FOLDER}{constan.MODEL_SUMMARY}.txt','a') as f:
        print(s, file=f)

def createModel(features, labels,):

    # Membagi dataset ke train dan test dataset
    X_train, X_val, y_train, y_val  = train_test_split(features, labels, test_size=0.3,random_state=42)

    inputShape = X_train.shape[1:]
    units = y_train[0].shape[0]

    # ===================
    # Add Sequential Model
    # ===================
    model = Sequential()
    model.add(Conv2D(filters=64, kernel_size=(3,3), padding= 'Same', activation='relu',input_shape=inputShape))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(filters=128, kernel_size=(3,3), padding= 'Same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(filters=128, kernel_size=3, padding= 'Same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(filters=256, kernel_size=3, padding= 'Same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(filters=256, kernel_size=3, padding= 'Same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(filters=512, kernel_size=3, padding= 'Same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Flatten())
    model.add(Dense(1024, activation = "relu"))
    model.add(Dense(512, activation = "relu"))
    model.add(Dense(units, activation = "softmax"))

    # ===================
    # Compile Model
    # ===================
    optimizer = SGD(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer="adam",metrics=['accuracy'])
    model.summary(print_fn=myprint)
    
    # ===================
    # Fit Model
    # ===================
    csv_logger = CSVLogger(f'{dir.PICKLE_FOLDER}{constan.LOSS_ACCURACY}.csv')
    model.fit(X_train,y_train,epochs=constan.EPOCHS, verbose = 1, validation_data=(X_val, y_val), callbacks=[csv_logger])
  
    # ===================
    # Evaluate Model
    # ===================
    test_loss, test_acc = model.evaluate(X_val, y_val)
    with open(f'{dir.PICKLE_FOLDER}{constan.LOSS_ACCURACY}.pickle', "wb") as f:
        pickle.dump([test_loss, test_acc], f)

    # ===================
    # Save Model
    # ===================
    model.save(f'{dir.MODEL_FOLDER}{constan.MODEL_FILE_NAME}')

    return model

def executeModels():  
    with open(f'{dir.PICKLE_FOLDER}{constan.TRAIN_TEST}.pickle','rb') as f:
        features, labels = pickle.load(f)
        createModel(features, labels)