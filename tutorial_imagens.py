import os as os
import cv2
import glob

os.getcwd() #mostra o diretorio atual

pathImgs = '/home/anderson/keras-tutorial/images'

os.chdir(pathImgs) #muda o diretorio atual

os.listdir('.') #lista dos arquivos no diretorio

pathImgsComplete = [os.path.abspath(file) for file in os.listdir('.')] #pega o caminho completo de cada imagem

imgs = [cv2.imread(file) for file in pathImgsComplete] #abre todas as imagens da pasta

##visualizaxao
## referencia para opencv: https://docs.opencv.org/3.1.0/dc/d2e/tutorial_py_image_display.html
cv2.imshow('teste',imgs[0])
cv2.waitKey(0)
cv2.destroyAllWindows()
