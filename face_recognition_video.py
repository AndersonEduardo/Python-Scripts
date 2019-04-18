## FONTE: https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py
## virtual env: faceRecVideo

import face_recognition
import cv2


# inicializando captura de imagem usando a webcam
video_capture = cv2.VideoCapture(0)

# abrindo imagens para teste
anderson_image = face_recognition.load_image_file("/home/anderson/Imagens/photo_0.jpg")
morpheus_image = face_recognition.load_image_file("/home/anderson/Imagens/morpheus.jpg")

# computando as metricas das faces
anderson_face_encoding = face_recognition.face_encodings(anderson_image)[0]
morpheus_face_encoding = face_recognition.face_encodings(morpheus_image)[0]

# arrays dos encodings e dos respectivos nomes
known_face_encodings = [
    anderson_face_encoding,
    morpheus_face_encoding
]
known_face_names = [
    "Mr. Anderson",
    "Morpheus"
]

# variaveis auxiliares
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:

    # capturando um frame do video
    ret, frame = video_capture.read()

    # diminuindo o tamanho para facilitar o processamento
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # convertendo de BGR (formato do OpenCV) para RGB (formato do dlib)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:

        # encontrar faces no frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # trabalhando com cada uma das faces encontradas na imagem
        face_names = []
        for face_encoding in face_encodings:
            # comparar face do video com os dados 
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # se a face do video existe nos dados, imprimir nome
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display dos resultados
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # voltando a escala original
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # desenhar box da face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # desenhar a label da face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # landmarks
        face_landmarks_list = face_recognition.face_landmarks(frame)

        for face_landmarks in face_landmarks_list:
            # for (x, y) in face_landmarks['right_eyebrow']:
            #     cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)
            # for (x, y) in face_landmarks['left_eyebrow']:
            #     cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)
            for (x, y) in face_landmarks['right_eye']:
                cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)
            for (x, y) in face_landmarks['left_eye']:
                cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)
            for (x, y) in face_landmarks['chin']:
                cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)
            for (x, y) in face_landmarks['nose_bridge']:
                cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)
            #for (x, y) in face_landmarks['nose_tip']:
            #    cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)
            # for (x, y) in face_landmarks['top_lip']:
            #     cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)
            # for (x, y) in face_landmarks['bottom_lip']:
            #     cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)
              

    # display final da imagem
    cv2.imshow('Bem vindo a matrix!! : )', frame)

    # apertar a tecla 'q' pra sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# finalização da captura pela webcam
video_capture.release()
cv2.destroyAllWindows()
