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
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev  libswscale-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
sudo apt-get install libopencv-dev

#5 - obtendo a imagem positiva para o exemplo deste tutorial:
'''
import urllib

pos_images_link = "https://upload.wikimedia.org/wikipedia/commons/6/69/Face_of_SpooSpa.jpg"
urllib.urlretrieve(pos_images_link, "pos_img.jpg")

'''
#6 - auxilio para obter imagens negativas (i.e., background): 
funcao para baixar imagens por URL (URLs da imageNET, neste exemplo) - salvo como 
arquivo dowload-image-by-link.py.
'''

#import urllib.request
import urllib2
import urllib
import cv2
import numpy as np
import os

def store_raw_images():
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n04081281'   
    #neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    neg_image_urls = urllib2.urlopen(urllib2.Request(neg_images_link)).read()
    pic_num = 1
    
    if not os.path.exists('neg'):
        os.makedirs('neg')
        
    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            #urllib.request.urlretrieve(i, "neg/"+str(pic_num)+".jpg")
            urllib.urlretrieve(i, "neg/"+str(pic_num)+".jpg")
            img = cv2.imread("neg/"+str(pic_num)+".jpg",cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite("neg/"+str(pic_num)+".jpg",resized_image)
            pic_num += 1
            
        except Exception as e:
            print(str(e))  

store_raw_images() #chamando a  funcao (para executa-la)

'''
#7 - arquivo com a descricao das imagens negativas
'''
def create_pos_n_neg():
    for file_type in ['neg']:
        
        for img in os.listdir(file_type):

            if file_type == 'pos':
                line = file_type+'/'+img+' 1 0 0 50 50\n'
                with open('info.dat','a') as f:
                    f.write(line)
            elif file_type == 'neg':
                line = file_type+'/'+img+'\n'
                with open('bg.txt','a') as f:
                    f.write(line)

create_pos_n_neg() #chamando a  funcao (para executa-la)

'''
#8 - criar um diretorio para as coisas da imagem positiva
$ mkdir info 

#9 - criar amostras da imagem positiva:
opencv_createsamples -img minhaImagemPositiva.jpg -bg bg.txt -info info/info.lst -pngoutput info -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num 1950
opencv_createsamples -info info/info.lst -num 1950 -w 20 -h 20 -vec positives.vec

#10 - criar diretorio para dados de treinemanto
$ mkdir data

#11 - treinar o classificador cascade:
opencv_traincascade -data data -vec positives.vec -bg bg.txt -numPos 1800 -numNeg 900 -numStages 10 -w 20 -h 20

#12 - rodar o classificador (na camera, aqui):
'''

import numpy as np
import cv2

#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#this is the cascade we just made. Call what you want
watch_cascade = cv2.CascadeClassifier('/home/anderson/Bravo Mob/FaceDetection/EyesTracker/cascades/haarcascade_frontalface_default.xml')


cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # add this
    # image, reject levels level weights.
    watches = watch_cascade.detectMultiScale(gray, 50, 50)
    
    # add this
    for (x,y,w,h) in watches:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)

    #for (x,y,w,h) in faces:
    #    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        #eyes = eye_cascade.detectMultiScale(roi_gray)
        #for (ex,ey,ew,eh) in eyes:
        #    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

