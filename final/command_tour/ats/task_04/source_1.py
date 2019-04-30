import dlib
import os
import cv2
import xml.etree.ElementTree as pars


#адрес к датасету
dir=r"C:\Users\DFCZ\PycharmProjects\DetektionWithLabelImage\AllPeople"
images=[]
annots=[]

ImgNameList = os.listdir(dir + "\images")
print (ImgNameList)


# перебираем изображения по одному, каждому изображению ставим в 
# соответствие аннотации (координаты светофора на изображении)
for FileName in ImgNameList:
    image=cv2.imread(dir+"/images/"+FileName)
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    OnlyFileName=FileName.split(".")[0]
    print (OnlyFileName)
    e = pars.parse(dir+"/annotations/xmls/"+OnlyFileName+".xml")
    root=e.getroot()

    #object=root.find("object")
    for object in root.findall("object"):
        object=object.find("bndbox")

        x=int(object.find("xmin").text)
        y = int(object.find("ymin").text)
        x2 = int(object.find("xmax").text)
        y2 = int(object.find("ymax").text)

        if (x2 - x) / (y2 - y) < 0.7:
            images.append(image)
            annots.append([dlib.rectangle(left=x, top=y, right=x2, bottom=y2)])


# сформированные масивы с изображениями и аннотациями подаём на вход 
# функции обучения детектора. Обученный детектор сохраняем в файл

options = dlib.simple_object_detector_training_options()
options.be_verbose=True
detector = dlib.train_simple_object_detector(images, annots, options)

detector.save("tld.svm")
print ("Detector Saved")