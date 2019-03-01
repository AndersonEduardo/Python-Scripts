'''
Tutorial basico para criar um harr cascade classifier (do zero) usando 
imagens baixadas no imageNet.
FONTE: https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/

#1 - atualizar  
$ sudo apt-get update
$ sudo apt-get upgrade

#2 - criar o diretorio de trabalho
$ mkdir opencv_workspace
$ cd opencv_workspace

#3 - 'instalar' o openCV
sudo apt-get install git
git clone https://github.com/Itseez/opencv.git

#4 - algumas outras coisas importantes (atencao com a quebra de linha!)
sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev 
libswscale-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev 
libtiff-dev libjasper-dev libdc1394-22-dev
sudo apt-get install libopencv-dev

#5 - auxilio para obter imagens negativas (i.e., background): 
funcao para baixar imagens por URL (URLs da imageNET, neste exemplo)
'''

import urllib.request
import cv2
import numpy as np
import os

def store_raw_images():
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n04081281'   
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 1
    
    if not os.path.exists('neg'):
        os.makedirs('neg')
        
    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, "neg/"+str(pic_num)+".jpg")
            img = cv2.imread("neg/"+str(pic_num)+".jpg",cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite("neg/"+str(pic_num)+".jpg",resized_image)
            pic_num += 1
            
        except Exception as e:
            print(str(e))  



'''

#funcao para baixando imagens 'negativas' no imageNet 
# (i.e., construir um tipo de background dataset)
import urllib.request
import cv2
import numpy as np
import os
def store_raw_images():
    neg_images_link = 'copy the link to the URls containing the images from image-net'   
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 2393
    
    if not os.path.exists('neg'):
        os.makedirs('neg')
        
    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, "neg/"+str(pic_num)+".jpg")
                        img = cv2.imread("neg/"+str(pic_num)+".jpg",cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (200, 200))
            cv2.imwrite("neg/"+str(pic_num)+".jpg",resized_image)
            pic_num += 1   
        except Exception as e:
            print(str(e)) 
store_raw_images()

#no terminal, fazer as instalacoes necessarias
'''
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install git
    git clone https://github.com/Itseez/opencv.git
    sudo apt-get install build-essential
    sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
    sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
    sudo apt-get install libopencv-dev
'''

#treinando o HaarCascade - terminal
'''
opencv_createsamples -img watch5050.jpg -bg bg.txt -info info/info.lst -pngoutput info -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num 1950
opencv_createsamples -info info/info.lst -num 1950 -w 20 -h 20 -vec positives.vec
opencv_traincascade -data data -vec positives.vec -bg bg.txt -numPos 1800 -numNeg 900 -numStages 10 -w 20 -h 20
'''