# modulos
from mobfacelib.centroidtracker_teste import CentroidTracker
from mobfacelib.trackableobject import TrackableObject
#from imutils.video import VideoStream
import numpy as np
import imutils
import dlib
import cv2


###############
### FUNCOES ###
###############

def objDetection(net, imagem, confidenceLimit):

	# parametros iniciais
	rects = []
	(H, W) = imagem.shape[:2]

	# deteccao de objeto usando a rede neural
	blob = cv2.dnn.blobFromImage(imagem, 0.007843, (W, H), 127.5)
	net.setInput(blob)
	detections = net.forward()

	# loop sobre as deteccoes
	for i in np.arange(0, detections.shape[2]):
		# extraindo o intervalo de confianca da deteccao
		confidence = detections[0, 0, i, 2]

		if confidence > confidenceLimit:
			# extraindo index da class de objeto
			idx = int(detections[0, 0, i, 1])

			### trabalhando somente com pessoas por enquanto
			#if CLASSES[idx] not in entity:
			#	continue

			# coordenadas do box para a deteccao atual
			box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
			(startX, startY, endX, endY) = box.astype("int")

			# construindo output - primeiro elemento = coords; segundo elemento = indice do label
			rects.append([(startX, startY, endX, endY), idx])

	return rects

def getTrackers(rects, rgb):

	# inicializando parametros locais
	trackers = []

	# controlando dados de entrada
	if not isinstance(rects, list):
		return print("'rects' needs to be a list.")

	# loop sobre os rects dos objetos
	for i in range(len(rects)):
		# unpacking das coords 
		startX = rects[i][0]
		startY = rects[i][1]
		endX = rects[i][2]
		endY = rects[i][3]

		# inicializando o dlib correlation tracker
		tracker = dlib.correlation_tracker()
		rect = dlib.rectangle(startX, startY, endX, endY)
		tracker.start_track(rgb, rect)

		# lista dos objetos detectados
		trackers.append(tracker)

	return trackers


def objTracking(trackers, rgb):

	# inicializando lista para o output
	rects = []

	# loop sobre o trackers
	for tracker in trackers:

		# atualizando tracker e pegando posicao atual
		tracker.update(rgb)
		pos = tracker.get_position()

		# unpack das coordenadas
		startX = int(pos.left())
		startY = int(pos.top())
		endX = int(pos.right())
		endY = int(pos.bottom())

		# lista dos rects para output
		rects.append((startX, startY, endX, endY))

	return rects

#####################
#### FIM FUNCOES ####
#####################

#videoPath = '/home/anderson/Downloads/people-counting-opencv/videos/example_01.mp4' #experimento 1-A
#videoPath = '/home/anderson/Downloads/people-counting-opencv/videos/example_02.mp4' #experimento 1-B
#videoPath = '/home/anderson/Vídeos/pedestres2.mp4' #experimento 2
#videoPath = '/home/anderson/Vídeos/pedestres.mp4' #experimento 3
#videoPath = '/home/anderson/Vídeos/carros01.mp4' #experimento 4 - A
videoPath = '/home/anderson/Vídeos/carros02.mp4' #experimento 4 - B
#videoPath = '/home/anderson/Vídeos/carros03.mp4' #experimento 4 - C

#videoPath = 'rtsp://admin:WCAwell72@tijuca03.dvrdns.org:554/Streaming/Channels/102'
#videoPath = 'rtsp://frankarts.dvrdns.org:562/user=admin&password=&channel=4&stream=0.sdp' #mais movimentado

prototxt = '/home/anderson/Downloads/people-counting-opencv/mobilenet_ssd/MobileNetSSD_deploy.prototxt'
model = '/home/anderson/Downloads/people-counting-opencv/mobilenet_ssd/MobileNetSSD_deploy.caffemodel'
skip_frames = 4
confidenceLimit = 0.5
entity = 'car' #['car', 'bus']

# lista das classes da MobileNet SSD
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# carregando modelo
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# carregando video
vs = cv2.VideoCapture(videoPath)

# instanciando o centroid tracker
ct = CentroidTracker(maxDisappeared=2, maxDistance=500)
trackableObjects = {}

# inicializando contadores
totalFrames = 0
totalDown = 0
totalUp = 0
total = 0

# loop sobre os frames do video
while True:
	# pegando o frame
	frame = vs.read()[1]

	# fechando o loop se nao ha frame
	if frame is None:
		break

	# resize do frame e conversão de BGR para RGB (dlib)
	frame = imutils.resize(frame, width=900)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# rodando deteccao de objetos e trackin6
	if totalFrames % skip_frames == 0:
		objList =  objDetection(net, frame, confidenceLimit)
		rects = [objList[i][0] for i in range(len(objList))]
		trackersList = getTrackers(rects, rgb)
		idxs = [objList[i][1] for i in range(len(objList))]

	else:
		rects = objTracking(trackersList, rgb)

	# atualizando os centroides dos objetos
	objects = ct.update(rects, idxs)

	# linha horizontal
	(H, W) = frame.shape[:2]
	#cv2.line(frame, (0, H // 2), (W, H // 2), (0, 255, 255), 2)

	# loop sobre os objetos 'trackeados'
	for (objectID, objData) in objects.items():

		centroid = objData[0]
		idx = objData[2]
		rect = objData[1]
		startX = rect[0]
		startY = rect[1]
		endX = rect[2]
		endY = rect[3]

		### trabalhando somente com pessoas por enquanto
		if CLASSES[idx] not in entity:
			continue

		# checagem de objeto
		to = trackableObjects.get(objectID, None)

		# se e novo na cena, criar um ID pegar seu centroide
		if to is None:
			to = TrackableObject(objectID, centroid)

		# se nao e novo na cena, calcular seu deslocamento
		else:
			y = [c[1] for c in to.centroids]
			direction = centroid[1] - np.mean(y)
			to.centroids.append(centroid)

			# checar se ja foi contado e calcular - contador simples
			#if not to.counted:
				#if direction < 0 and centroid[1] <= H // 2:
				#	totalUp += 1
				#	total += 1
				#	to.counted = True

				#elif direction > 0 and centroid[1] >= H // 2:
				#	totalDown += 1
				#	total += 1
				#	to.counted = True

		# guardar/atualizar objeto
		trackableObjects[objectID] = to

		# imprimindo informacoes do objeto no frame
		#if to.counted and centroid[1] > H // 2:
		#text = "{} ID{}".format(CLASSES[idx], objectID)
		text = "{}".format(CLASSES[idx])
		cv2.putText(frame, text, (startX - 5, startY - 5),      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1) #obj info
		
		#cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1) #obj centroide

		cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 1) #obj box

	# checar se ja foi contado e calcular - censo no frame
	objvec = np.array([CLASSES[i] == entity for i in idxs]).astype(int)
	total = sum(objvec)

	# imprimindo informacoes gerais no frame
	info = [
		("Up", totalUp),
		("Down", totalDown),
		("Total", total),
	]

	# loop sobre as info
	for (i, (k, v)) in enumerate(info):
		textInfo = "{}: {}".format(k, v)
		cv2.putText(frame, textInfo, (10, H - ((i * 20) + 20)),
			cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

	# output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# tecla 'q' para interromper reproducao
	if key == ord("q"):
		break

	# incrementar frames processados
	totalFrames += 1

print("TOTAL: {} | Up: {} | Down: {}".format(total, totalUp, totalDown))

# release do video
vs.release()

# fechar janelas
cv2.destroyAllWindows()