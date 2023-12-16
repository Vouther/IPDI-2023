# Importamos las librerias
import cv2
import numpy as np
from PIL import Image
from Reconocimiento import LPR

# Realizamos la ViedoCaptura
cap = cv2.VideoCapture("Placas.mp4")

# Establecemos la velocidad de reproducción deseada (por ejemplo, 30 fotogramas por segundo)
# Comentar si no es necesario y controlar el ingreso de teclas
desired_fps = 30
cap.set(cv2.CAP_PROP_FPS, desired_fps)

# No seria necesario ***********************************
# Obtener la resolución original del video
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Resolución deseada para mostrar en la pantalla (puedes ajustarla según tu pantalla)
# Extraemos el ancho y el alto de los fotogramas
height = 727
width = 1298

# Crear una ventana para mostrar el video
cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Video", width, height)
#*********************************************************

# Dimensiones deseadas para mostrar el video
desired_width = 1298
desired_height = 727

# Creamos una instancia de la clase LPR
lpr = LPR()

# Variable para controlar el estado de reproducción (True para reproducción, False para pausa)
playing = True

# Creamos nuestro while true
while True:

    # Si estamos en estado de reproducción, leemos el siguiente fotograma
    if playing:
        # Relizamos la lectura de la VideoCaptura
        ret, frame = cap.read()

        if ret == False:
            break

        # Redimensionamos el fotograma al tamaño deseado
        frame = cv2.resize(frame, (desired_width, desired_height))

        # Texto de referencia
        cv2.rectangle(frame, (337, 566), (650, 631), (0, 0, 0), cv2.FILLED)
        cv2.putText(frame, 'Procesando Placa', (351, 612), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # ************** REGION DE INTERES *******************************
        # Tomar el centro de la imagen
        # En x:
        x1 = int(200)
        x2 = int(1000)

        # En y:
        y1 = int(248)
        y2 = int(477)
        # ****************************************************************

        # Ubicamos el rectangulo de las zonas extraidas (EN COLOR AZUL)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # Dibujamos un rectángulo para visualizar la lectura
        cv2.rectangle(frame, (682, 565), (920, 634), (0, 0, 0), cv2.FILLED)

        # Recortamos la región de interés
        roi = frame[y1:y2, x1:x2]

        # Leemos la placa usando la clase LPR
        plate_text = lpr.read_license(roi)

        # Configuramos Ctexto con el texto de la placa
        if plate_text == "NoReading":
            Ctexto = plate_text
        else:
            # Adaptamos al formato de la patente
            Ctexto = plate_text[:2]+' '+plate_text[2:5]+' '+plate_text[5:]

        # Mostramos la placa en el fotograma
        cv2.putText(frame, Ctexto[0:9], (698, 612), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Mostramos el fotograma
        cv2.imshow("Video", frame)

    # Para la reproduccion sin una velocidad de reproduccion establecida descomentar
    # Leemos una tecla
    #key = cv2.waitKey(1)

    # Para la reproduccion con una velocidad de reproduccion establecida descomentar
    # Leemos una tecla
    key = cv2.waitKey(1000 // desired_fps)  # Espera según la velocidad de reproducción deseada

    # Manejo de eventos de teclado
    if key == 27:  # Tecla 'ESC' para salir
        break
    elif key == ord('p'):  # Tecla 'p' para pausar/continuar
        playing = not playing

cap.release()
cv2.destroyAllWindows()