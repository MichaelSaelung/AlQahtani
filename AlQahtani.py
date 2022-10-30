import test as t
from tkinter import *
from tkinter import filedialog, ttk

from PIL import Image, ImageTk

from res.values import constan, path
from res.values.constan import buttonLabel as btnLbl
from res.values.constan import fontDecoration as fd
from res.values.constan import label as lbl
from res.values.constan import message as msg
from res.values.constan import screen as scr
from res.values.constan import tab
from src import databaseGenerate as dgt
from src import dataset as dst
from src import imagePrediction as imgPredict
from src import model as mdl

WIDTH, HEIGHT = scr.WIDTH, scr.HEIGHT

root = Tk()
root.title(lbl.title)
root.geometry(f'{WIDTH}x{HEIGHT}')
v = IntVar()
v.set(1)

def updateStatus(lblStatus=None,     lblStatusCrop=None,     lblStatusPredict=None, 
                 lblAccuracy = None, lblTimeExecution= None, lblPrediction=None, lblKeterangan1=None,
                 buttonRestImg=None, buttonCropImg=None, buttonPrediksiImg=None):

    if lblStatus         is not None : lbl_status.config(        text = f'{lbl.loadStatus}{lblStatus}')
    if lblStatusCrop     is not None : lbl_status_crop.config(   text = f'{lbl.cropStatus}{lblStatusCrop}')
    if lblStatusPredict  is not None : lbl_status_predict.config(text = f'{lbl.predictStatus}{lblStatusPredict}')
    if lblAccuracy       is not None : lbl_accuracy.config(      text = lbl.accuracy.format(lblAccuracy))
    if lblTimeExecution  is not None : lbl_time_execution.config(text = lbl.timeExecution.format(lblTimeExecution))
    if lblPrediction     is not None : lbl_predict.config(       text = f'{lblPrediction}')
    if lblKeterangan1    is not None : lbl_keterangan1.config(   text = f'{lblKeterangan1}')

    if buttonRestImg     is not None : btn_reset_image.config(   state = buttonRestImg)
    if buttonCropImg     is not None : btn_crop_image.config(    state = buttonCropImg)
    if buttonPrediksiImg is not None : btn_prediksi_image.config(state = buttonPrediksiImg)

def openAndPut():
    newImagePath = filedialog.askopenfilename()
    openImage(newImagePath)

def resetImage():
    global defaultImagePath
    #openImage(defaultImagePath)
    updateStatus(lblStatus='', lblStatusCrop='', lblStatusPredict='', 
                 lblAccuracy = '0', lblTimeExecution= '0',
                 buttonPrediksiImg='disabled')
    updateCropImage(constan.NO_IMAGE_FILE_NAME)
    selectAreaStop()

def openImage(path):
    global imgOriginal, CropImageResize
    width, height = WIDTH, scr.height_70p
    if path:
        #update Original for Crop imgae
        CropImageOpended = Image.open(path)
        CropImageResize = CropImageOpended.resize((width, height), Image.ANTIALIAS)
        #update original image
        imageOpended = Image.open(path)
        imageResize = imageOpended.resize((width, height), Image.ANTIALIAS)
        imgOriginal = ImageTk.PhotoImage(imageResize)
        Frameb.create_image(0, 0, image=imgOriginal, anchor='nw')
        updateStatus(lblStatus=path,buttonRestImg='normal',buttonCropImg='normal',buttonPrediksiImg='disabled')
        selectAreaStop()

def saveImage(st=False):
    if st : coor = constan.DEFAULT_COORDINATE
    else:
        if   (start_x > curX and start_y > curY): coor = (curX, curY,start_x, start_y)  
        elif (start_x > curX and start_y < curY): coor = (curX, start_y,start_x, curY)  
        elif (start_x < curX and start_y > curY): coor = (start_x, curY,curX, start_y)  
        else:                                     coor = (start_x, start_y, curX, curY)

    cropImage = CropImageResize.crop(coor)
    startX, startY, endX, endY = coor
    _str = msg.coorSelected.format(startX, startY, endX, endY)

    saveCropPath = f'{path.DRAWABLE_FOLDER}{constan.CROP_FILE_NAME}{constan.IMAGE_TYPE}'
    cropImage = cropImage.convert(constan.TO_RGB)
    cropImage.save(saveCropPath)
    #openImage.show()
    updateStatus(lblStatus = saveCropPath, lblStatusCrop=lbl.selectedCoor + _str, 
                buttonPrediksiImg='normal')

def updateCropImage(filename = constan.CROP_FILE_NAME):
    global imgCrop
    imgss = Image.open(f'{path.DRAWABLE_FOLDER}{filename}{constan.IMAGE_TYPE}')
    imgRegion = imgss.resize((scr.width_30p, scr.height_30p), Image.ANTIALIAS)
    imgCrop = ImageTk.PhotoImage(imgRegion)
    FrameAKi.create_image(0, 0, image=imgCrop, anchor='nw')

def buttonPress(event):
    # simpan mouse drag posisi awal
    global start_x, start_y, rect
    start_x = Frameb.canvasx(event.x)
    start_y = Frameb.canvasy(event.y)
    # buat kotak seleksi warna merah
    rect = Frameb.create_rectangle(0, 0, 1, 1, outline='red')

    updateStatus(lblStatusCrop=lbl.btnPress)

def buttonMove(event):
    global curX, curY
    curX = Frameb.canvasx(event.x)
    curY = Frameb.canvasy(event.y)
    # buat kotak selama di drag
    print(msg.coorTerminal.format(start_x,start_y,curX,curY))
    Frameb.coords(rect, start_x, start_y, curX, curY)    

    updateStatus(lblStatusCrop=lbl.btnMove.format(curX,curY))

def buttonRelease(event):
    updateStatus(lblStatusCrop=lbl.btnRelease)
    saveImage()    
    Frameb.delete(rect)
    updateCropImage()    

def ctrlName(event):
    try:
        if event.keysym == 'd':
            FrameAKa.forget(FrameAKaTI)
        elif event.keysym == 's':
            FrameAKaTI.pack()
            FrameAKa.add(FrameAKaTI, text=tab.tabInformation)
        elif event.keysym == 'c':
            saveImage(TRUE)    
            updateCropImage()         
        elif event.keysym == 'p':
            root.config(cursor="watch")
            root.update()
            #imgPredict.test()
            openNewWindow()
            root.config(cursor="")

    except : pass

def selectArea(): 
    Frameb.bind('<ButtonPress-1>', buttonPress)
    Frameb.bind('<B1-Motion>', buttonMove)
    Frameb.bind('<ButtonRelease-1>', buttonRelease)
    updateStatus(lblStatusCrop=lbl.selectArea,buttonPrediksiImg='disabled', lblStatusPredict='')

def selectAreaStop():
    Frameb.bind('<ButtonPress-1>', '')
    Frameb.bind('<B1-Motion>', '')
    Frameb.bind('<ButtonRelease-1>', '')

def prediksi():
    updateStatus(lblStatusPredict=lbl.predictingSts)
    root.config(cursor="watch")
    root.update()

    agePrediction, timeExecution, accuracy, loss, PredictionClass, firstFolder = imgPredict.imagePrediction()
    
    PredictionClass = PredictionClass[0]
    str =''
    for x in range(len(PredictionClass)):
        str = str + msg.allPredict.format(constan.FLOAT_POINT.format(PredictionClass[x]*100), (firstFolder + x))
    allPred.config(text = str)

    min = f'{(agePrediction - constan.DEVIATION)}'
    max = f'{(agePrediction + constan.DEVIATION)}'

    updateStatus(lblAccuracy= (accuracy * 100),
                lblTimeExecution= (timeExecution / 1000),
                lblStatusPredict=lbl.predictFinish, 
                lblKeterangan1= msg.keterangan1.format(min,max),
                lblPrediction= agePrediction)

    root.config(cursor="")

def trainModel():
    root.config(cursor="watch")
    root.update()
    mdl.executeModels()
    root.config(cursor="")

def buildDataset():
    root.config(cursor="watch")
    root.update()
    dst.loadDataset()
    root.config(cursor="")

def databaseGenerate():
    root.config(cursor="watch")
    root.update()
    dgt.generate()
    root.config(cursor="")

def openNewWindow():
     
    t.abc(root)

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------


#=======================================================================
#   Membuat Frame bagian atas 
#   FrameA = Frame Atas
#   Membuat Frame Bagian bawah untuk gambar original 
#   Frameb = Frame Bawah
#=======================================================================
FrameA = ttk.Notebook(root, width= WIDTH, height= scr.height_30p)
FrameA.grid(row=0, column=0, sticky='nsew')
FrameA.grid_propagate(False)

Frameb = Canvas(root, bg='white', width= WIDTH, height= scr.height_70p, highlightbackground='black')
Frameb.grid(row=1, column=0, sticky='nsew')
Frameb.grid_propagate(False)
#=======================================================================
#   Membuat Frame sebelah atas kanan untuk mem
# buat tab frame 
#   FrameAKa = Frame Atas Kanan 
#   Membuat Frame yang atas sebelah kiri kotak gambar crop 
#   FrameAKi = Frame Atas Kiri
#=======================================================================
FrameAKa = ttk.Notebook(FrameA, width= scr.width_70p, height= scr.height_30p)
FrameAKa.grid(row=0, column=1, sticky='nsew')
FrameAKa.grid_propagate(False)

FrameAKi = Canvas(FrameA, bg='white', width= scr.width_30p, height= scr.height_30p, highlightbackground='black')
FrameAKi.grid(row=0, column=0, sticky='nsew')
FrameAKi.grid_propagate(False)
#=======================================================================
#   Membuat Frame Tab 
#   FrameAKaTU = Frame Atas Kamam Tab Menu Utama
#   FrameAKaTI = Frame Atas Kamam Tab Informasi
#   FrameAKaTP = Frame Atas Kamam Tab Profile
#=======================================================================
FrameAKaTU = ttk.Frame(FrameAKa,width= scr.width_70p, height= scr.height_30p)
FrameAKaTI = ttk.Frame(FrameAKa,width= scr.width_70p, height= scr.height_30p)
FrameAKaTP = ttk.Frame(FrameAKa,width= scr.width_70p, height= scr.height_30p)
FrameAKaTU.pack(fill='both', expand=True)
FrameAKaTI.pack(fill='both', expand=True)
FrameAKaTP.pack(fill='both', expand=True)
FrameAKa.add(FrameAKaTU, text=tab.tabMain)
FrameAKa.add(FrameAKaTI, text=tab.tabInformation)
FrameAKa.add(FrameAKaTP, text=tab.tabProfile)
#=======================================================================
#   Membagi frame tab bagian tab menu utama menjadi 3 frame secara horizontal

#   FrameAKaTUA     = Frame Atas Kanan Tab Menu Utama Bagian Atas

#   FrameAKaTUAKi   = Frame Atas Kanan Tab Menu Utama Bagian Atas bagian Kiri
#   FrameAKaTUAKiA  = Frame Atas Kanan Tab Menu Utama Bagian Atas bagian Kiri Atas (load, reset button)
#   FrameAKaTUATe   = Frame Atas Kanan Tab Menu Utama Bagian Atas Bagian Tengah (accuracy, time excecution label)
#   FrameAKaTUAKa   = Frame Atas Kanan Tab Menu Utama Bagian Atas Bagian Kanan (accuracy, time excecution label)

#   FrameAKaTUTe  = Frame Atas Kanan Tab Menu Utama Bagian Kiri Tengah (load, crop, dan predict label)
#   FrameAKaTUB   = Frame Atas Kanan Tab Menu Utama Bagian Kiri Bawah (copyright)

#   FrameAKaTUKa    = Frame Atas Kanan Tab Menu Utama Bagian Kanan
#=======================================================================

FrameAKaTUA = Frame(FrameAKaTU,width= scr.width_70p, height= scr.height_15p)
FrameAKaTUA.grid(row=0, column=0, sticky='nsew')
FrameAKaTUA.grid_propagate(False)

FrameAKaTUAKi = Frame(FrameAKaTUA,width= scr.width_25p, height= scr.height_15p)
FrameAKaTUAKi.grid(row=0, column=0, sticky='nsew')
FrameAKaTUAKi.grid_propagate(False)
FrameAKaTUAKiA = Frame(FrameAKaTUAKi, width= 20)
FrameAKaTUAKiA.grid(row=0, column=0, sticky='nsew', padx=30, pady=(20,1))

FrameAKaTUATe = Frame(FrameAKaTUA,width= scr.width_25p, height= scr.height_15p)
FrameAKaTUATe.grid(row=0, column=1, sticky='nsew')
FrameAKaTUATe.grid_propagate(False)

FrameAKaTUAKa = Frame(FrameAKaTUA,width= scr.width_20p, height= scr.height_15p)
FrameAKaTUAKa.grid(row=0, column=2, sticky='nsew')
FrameAKaTUAKa.grid_propagate(False)


FrameAKaTUTe = Frame(FrameAKaTU,width= scr.width_70p, height= scr.height_10p)
FrameAKaTUTe.grid(row=1, column=0, sticky='nsew')
FrameAKaTUTe.grid_propagate(False)
FrameAKaTUB = Frame(FrameAKaTU,width= scr.width_70p, height= scr.height_5p)
FrameAKaTUB.grid(row=2, column=0, sticky='nsew')
FrameAKaTUB.grid_propagate(False)


#=======================================================================
#   fame tab bagian tab Informasi

#   FrameAKaTIKi    = Frame Atas Kanan Tab Informasi Bagian Kiri
#=======================================================================

FrameAKaTIKi = Frame(FrameAKaTI,width= scr.width_50p, height= scr.height_30p)
FrameAKaTIKi.grid(row=0, column=0, sticky='nsew')
FrameAKaTIKi.grid_propagate(False)

FrameAKaTIKiKi = Frame(FrameAKaTIKi,width= scr.width_25p, height= scr.height_30p)
FrameAKaTIKiKi.grid(row=0, column=0, sticky='nsew')
FrameAKaTIKiKi.grid_propagate(False)
FrameAKaTIKiKa = Frame(FrameAKaTIKi,width= scr.width_25p, height= scr.height_30p)
FrameAKaTIKiKa.grid(row=0, column=1, sticky='nsew')
FrameAKaTIKiKa.grid_propagate(False)
#=======================================================================
#   frame tab bagian Profile

#   FrameAKaTPKi    = Frame Atas Kanan Tab Profile Bagian Kiri
#=======================================================================

FrameAKaTPKi = Frame(FrameAKaTP,width= scr.width_50p, height= scr.height_30p)
FrameAKaTPKi.grid(row=0, column=0, sticky='nsew')
FrameAKaTPKi.grid_propagate(False)

#=======================================================================
#   Membuat Button Pada Tab Menu
#=======================================================================
btn_load_image = Button(FrameAKaTUAKiA,  width=10, text=btnLbl.LOAD_IMAGE, font=fd.arial10bold,command = openAndPut)
btn_load_image.grid(row=0, column=0, sticky='nsew')
btn_reset_image = Button(FrameAKaTUAKiA, width= 10, text=btnLbl.RESET_IMAGE, font=fd.arial10bold, command = resetImage)
btn_reset_image.grid(row=0,column=1, sticky='nsew')
btn_reset_image.config(state = 'disabled')

btn_crop_image = Button(FrameAKaTUAKi, width= 20, text=btnLbl.CROP_IMAGE, font=fd.arial10bold, command = selectArea)
btn_crop_image.grid(row=1,column=0,sticky='nsew', padx=30, pady=1)
btn_crop_image.config(state = 'disabled')
btn_prediksi_image = Button(FrameAKaTUAKi, width= 20, text=btnLbl.PREDICT, font=fd.arial10bold, command = prediksi)
btn_prediksi_image.grid(row=2,column=0,sticky='nsew', padx=30, pady=1)
btn_prediksi_image.config(state = 'disabled')
#=======================================================================
#   Membuat Label Pada Teb Menu
#=======================================================================
lbl_accuracy = Label(FrameAKaTUATe, text=lbl.accuracy.format(0.0), font=fd.arial10bold,highlightthickness=2)
lbl_accuracy.grid(row=0, column=1, sticky=W, padx=5,pady=(20,1))
lbl_time_execution= Label(FrameAKaTUATe, text=lbl.timeExecution.format(0.0), font=fd.arial10bold,highlightthickness=2)
lbl_time_execution.grid(row=1, column=1, sticky=W, padx=5,pady=1)
lbl_deviation = Label(FrameAKaTUATe, text=lbl.deviation, font=fd.arial10bold,highlightthickness=2)
lbl_deviation.grid(row=2, column=1, sticky=W, padx=5,pady=1)
lbl_deviation.destroy()

lbl_predict = Label(FrameAKaTUAKa, text=lbl.predict, font=fd.arial40bold)
lbl_predict.grid(row=0, column=0, sticky=W, pady=(20,2))
lbl_tahun = Label(FrameAKaTUAKa, text=lbl.tahun, font=fd.arial10bold)
lbl_tahun.grid(row=0, column=0, sticky=W,padx = 80, pady=(40,2))
lbl_keterangan1 = Label(FrameAKaTUAKa, text=msg.keterangan1.format(0,0),justify='left', font=fd.arial10bold)
lbl_keterangan1.grid(row=1, column=0, sticky=W, pady=(5,2))

lbl_status = Label(FrameAKaTUTe, text=lbl.loadStatus, font=fd.arial10bold,highlightthickness=2)
lbl_status.grid(row=3, column=0, sticky=W, padx=(30,2),pady=1)
lbl_status_crop = Label(FrameAKaTUTe, text=lbl.cropStatus, font=fd.arial10bold,highlightthickness=2)
lbl_status_crop.grid(row=4, column=0, sticky=W, padx=30,pady=1)
lbl_status_predict = Label(FrameAKaTUTe, text=lbl.predictStatus, font=fd.arial10bold,highlightthickness=2)
lbl_status_predict.grid(row=5, column=0, sticky=W, padx=30,pady=1)

lbl_copyright = Label(FrameAKaTUB, text=lbl.COPY_RIGHT, font=fd.arial07,highlightthickness=2)
lbl_copyright.grid(row=6, column=0, sticky=W, pady=5)
#=======================================================================
#   Membuat Label Pada Teb Informasi
#=======================================================================
databaseGenerate = Button(FrameAKaTIKiKi,  width=15, text=btnLbl.DATABASE_GENERATE, font=fd.arial10bold,command=databaseGenerate)
databaseGenerate.grid(row=0, column=0, sticky=W, padx=30,pady=(20,20))
buildDataset = Button(FrameAKaTIKiKi,  width=15, text=btnLbl.BUILD_DATASET, font=fd.arial10bold,command=buildDataset)
buildDataset.grid(row=1, column=0, sticky=W, padx=30,pady=1)
trainModel = Button(FrameAKaTIKiKi,  width=15, text=btnLbl.TRAIN_MODEL, font=fd.arial10bold,command=trainModel)
trainModel.grid(row=2, column=0, sticky=W, padx=30,pady=1)
allPred = Label(FrameAKaTIKiKa,  width=20, text='', justify='left' ,font=fd.arial10bold)
allPred.grid(row=1, column=2, sticky=W, padx=5,pady=(20,2))
#=======================================================================
#   Membuat Label Pada Teb Profile
#=======================================================================
lbl_profile = Label(FrameAKaTPKi, text=msg.PROFILE,justify='left', font=fd.arial10bold,highlightthickness=2)
lbl_profile.grid(row=0, column=0, sticky=W, padx=30,pady=(20))
#=======================================================================
#   Load 
#=======================================================================

defaultImagePath = f'{path.DRAWABLE_FOLDER}{constan.NO_IMAGES_FILE_NAME}{constan.IMAGE_TYPE}'
imgs = Image.open(defaultImagePath)
imgs = ImageTk.PhotoImage(imgs)
Frameb.create_image(WIDTH/2,scr.height_70p/2 ,anchor=CENTER, image=imgs)

imgss = Image.open(f'{path.DRAWABLE_FOLDER}{constan.NO_IMAGE_FILE_NAME}{constan.IMAGE_TYPE}')
imgRegion = imgss.resize((int(scr.width_30p), int(scr.height_30p)), Image.ANTIALIAS)
imgss = ImageTk.PhotoImage(imgRegion)
FrameAKi.create_image(scr.width_30p/2,scr.height_30p/2,anchor=CENTER, image=imgss)

FrameAKa.forget(FrameAKaTI)

root.bind('<Control-d>', ctrlName)
root.bind('<Control-s>', ctrlName)
root.bind('<Control-c>', ctrlName)
root.bind('<Control-p>', ctrlName)
root.eval('tk::PlaceWindow . center')
root.resizable(False, False)
root.mainloop()





