
NO_IMAGES_FILE_NAME = 'No Images'
NO_IMAGE_FILE_NAME  = 'No Image'
IMAGE_TYPE          = '.jpg'

DEVIATION           = 0.3 #Dalam Tahun
CROP_FILE_NAME      = 'Crop'
TO_RGB              = 'RGB'

IMAGE_SIZE = 64
EPOCHS = 100
DATASET_PICKLE_NAME = 'dataset'
TRAIN_TEST          = 'features_labels'
LOSS_ACCURACY       = 'loss_accuracy'
MODEL_SUMMARY       = 'model_summary'
FLOAT_POINT = '{:.3}'

class tab():
    tabMain        = 'Main'
    tabInformation = 'Information'
    tabProfile     = 'Profile'
    # Show/Hide TabMenu
    hideFrameStatus      = False
    hideFrameInformation = False
    hideFrameProfile     = True

class label():
    COPY_RIGHT    = 'Copyright © 2022 Michael Saelung Sinambela'
    accuracy      = 'akurasi        : {} %'
    timeExecution = 'Waktu eksekusi : {} s'
    deviation     = 'Deviasi        : '
    maxDeviasion  = 'Max Preddict'
    minDeviasion  = 'Min Preddict'
    title         = 'Al Qahtani Clasification'
    predictStatus = 'Estimate Status : '
    loadStatus    = 'Path Status     : '
    cropStatus    = 'Crop Status     : '
    predict       = '0'
    tahun         = 'tahun'
    selectedCoor  = 'Selected Coordinate '
    btnPress      = 'Button Press'
    btnMove       = 'Button Move CurX = {0}, CurY = {1}'
    btnRelease    = 'Button Release'
    predictingSts = 'Predicting'
    predictFinish = 'Prediction Finish'
    selectArea    = 'Select Area'

class buttonLabel():
    LOAD_IMAGE     = 'Load Image'
    CROP_IMAGE     = 'Crop'
    SELECT_REGION  = 'Pilih Gigi'
    PREDICT        = 'Predict'
    RESET_IMAGE    = 'Reset'
    BUILD_DATASET  = 'Build Datsets'
    TRAIN_MODEL    = 'Train Models'

class fontDecoration():
    arial10bold = 'arial 10'
    arial07     = 'arial 7'
    arial40bold = 'arial 40 bold'

class screen():
    WIDTH      = 1000
    HEIGHT     = 800

    height_5p  = int(HEIGHT * 0.05)
    height_10p = int(HEIGHT * 0.1)
    height_15p = int(HEIGHT * 0.15)
    height_30p = int(HEIGHT * 0.3)
    height_70p = int(HEIGHT * 0.7)

    width_5p   = int(WIDTH * 0.05)
    width_20p  = int(WIDTH * 0.2)
    width_25p  = int(WIDTH * 0.25)
    width_30p  = int(WIDTH * 0.3)
    width_50p  = int(WIDTH * 0.5)
    width_70p  = int(WIDTH * 0.7) 

class message():
    keterangan1  = 'Hasil prediksi region 1 \ndan region 2:'
    coorSelected = 'startX {0}, startY {1}),(endX {2}, endY {3}'
    coorTerminal = 'StartX = {0}, StartY = {1}, CurX = {2}, CurY = {3}'
    test = 'umur {0}\numut {1}\numur {2}\numur {0}\numut {1}\numur {2}umur {0}\numut {1}\numur {2}\numur {0}\numut {1}\numur {2}'
    PROFILE      = """Nama         : Michael Saelung Sinambela
Alamat       :
Fakultas     :
Bidang Studi :"""