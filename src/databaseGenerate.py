
import os
from res.values.constan import screen as scr
from PIL import Image
from res.values import constan, path as dir
from os import walk,path

FILE_NAME = 'coor{0}-{1}-umur{2}{3}'


def generate():
        for x in range(len(constan.CROP_COORDINATE)):
                for (dirPath, _,fileNames) in walk(dir.DATABASE_FOLDER):
                        umur = dirPath.split('/')[-1]
                        createNewPath = path.join(dir.DATA_FOLDER, umur)

                        if not os.path.exists(createNewPath):os.makedirs(createNewPath) 
                                
                        for fileName in fileNames:
                                crop = fileName.split('.')[0]

                                if fileName.endswith(constan.IMAGE_TYPE):
                                        CropImageOpended = Image.open(path.join(dirPath, fileName))
                                        CropImageResize = CropImageOpended.resize((scr.WIDTH, scr.height_70p))

                                        CropImageResize = CropImageResize.rotate(constan.CROP_COORDINATE[x][0])
                                        cropImage = CropImageResize.crop(constan.CROP_COORDINATE[x][1])

                                        saveCropPath = path.join(createNewPath, FILE_NAME.format(x, crop, umur, constan.IMAGE_TYPE))
                                        cropImage.save(saveCropPath)


