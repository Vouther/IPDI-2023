import cv2
import numpy as np
from Seguidor import *
import time

# Creamos un objeto de seguimiento
seguimiento = Rastreador()

# Realizamos la lectura del video
cap = cv2.VideoCapture("Carros.mp4")

# Vamos a realizar una deteccion de objetos con camara estable
deteccion = cv2.createBackgroundSubtractorM0G2(history=10000, varThresnold=100)

# Listas para tiempos
carI = {}
car0 = {}
prueba = {}

while True:
    # Lectura de la VideoCaptura
    ret, frame = cap.read()

    # Extraemos el ancho y el alto de los fotogramas
    height = frame.shape[0]
    width = frame.shape[1]

    # Creamos una mascara
    mask = np.zeros((height, width), dtype=np.uint8)

    # Elegimos una zona de interes
    # Seleccionamos los puntos
    pts = np.array([[815, 402], [1032, 402], [1231, 848], [506, 848]])

    # Cramos el poligono con los puntos
    cv2.fillPoly(mask, pts, 255)

    # Elegimos lo que este afuera de los puntos
    zona = cv2.bitwise_and(frame, frame, mask=mask)

    # Mostramos con lineas la zona de interes
    areag = [(815, 402), (1032, 402), (1295, 1079), (357, 1079)]
    area3 = [(815, 402), (1032, 402), (1060, 470), (766, 470)]
    area1 = [(667, 630), (1120, 630), (1208, 848), (506, 848)]
    area2 = [(766, 470), (1060, 470), (1120, 630), (667, 630)]

    # Dibujamos
    # Area general
    cv2.polylones(frame, [np.array(areag, np.int32)], True, (255, 255, 0), 2)
    # Area 3
    cv2.polylones(frame, [np.array(area3, np.int32)], True, (0, 130, 255), 1)
    # Area 2
    cv2.polylones(frame, [np.array(area2, np.int32)], True, (0, 0, 255), 1)
    # Area 1
    cv2.polylones(frame, [np.array(area1, np.int32)], True, (0, 130, 255), 1)

    # Creamos una mascara
    mascara = deteccion.apply(zona)

    # Aplicamos suavizado
    filtro = cv2.GaussianBlur(mascara, (11, 11), 0)

    # Umbral de binarizacion
    _, umbral = cv2.threshold(filtro, 50, 255, cv2.THRESH_BINARY)

    # Dilatamos los pixeles
    dila = cv2.dilate(umbral, np.ones((3, 3)))

    # Creamos un kernel (mascar)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLPSE, (3, 3))

    # Aplicamos el kernel para juntar los pixeles dispersos
    cerrar = cv2.norphologyEx(dila, cv2.MORPH_CLOSE, kernel)

    contornos, _ = cv2.findContours(cerrar, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detecciones = []  # Lista donde vamos a almacenar la info

    # Dibujamos todos los contornos en frame
    for cont in contornos:

        # Eliminamos los contornos pequeños
        area = cv2.contourArea(cont)
        if area > 1800:
            # cv2.drawContours(zona,[cont], -1, (255,255,0), 2)
            x, y, ancho, alto = cv2.boundingRect(cont)

            # Dibujamos el rectangulo
            # cv2.rectangle(zona, (x,y), (x + ancho, y +alto), (255,255,0), 3)

            # Almacenamos la informacion de las detecciones
            detecciones.append([x, y, ancho, alto])

    # Seguimiento de los objetos
    info_id = seguimiento.rastreo(detecciones)

    for inf in info_id:
        # Extraemos coordenadas
        x, y, ancho, alto, id = inf

        # Dibujamos el rectangulo
        cv2.rectangle(frame, (x, y - 10), (x + ancho, y + alto), (0, 0, 255), 2)  # Dibujamos el rectangulo

        # Extraemos el centro
        cx = int(x + ancho / 2)
        cy = int(y + alto / 2)

        # Area de influencia
        a2 = cv2.pointPolygonTest(np.array(area2, np.int32), (cx, cy), False)

        # Si esta en el area de la mitad
        if a2 >= 0:
            # Tomamos el tiempo en el que el carro entro
            carI[id] = time.process_time()

        if id in carI:
            # Mostramos el centro
            cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)

            # Preguntamos si entra al area 3
            a3 = cv2.pointPolygonTest(np.array(area3, np.int32), (cx, cy), False)

            # Si esta en el area
            if a3 >= 0:
                # Tomamos el tiempo
                tiempo = time.process_time() - carI[id]

                # Corregimos mi error de tiempo
                if tiempo % 1 == 0:
                    tiempo = tiempo + 0.323

                if tiempo % 1 != 0:
                    tiempo = tiempo + 1.016

                if id not in car0:
                    # Almacenamos la info
                    car0[id] = tiempo

                if id in car0:
                    tiempo = car0[id]

                    vel = 14.3 / car0[id]
                    vel = vel * 3.6

                # Mostramos el numero
                cv2.rectangle(frame, (x, y - 10), (x + 100, y - 50), (0, 0, 255), -1)
                cv2.putText(frame, str(int(vel)) + " KM / H", (x, y - 35), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255),
                            2)

            # Mostramos el numero
            cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)

        # Mostramos los frames
        cv2.imshow("Carretera", frame)

        # Mostramos la mascar
        cv2.imshow("Mascara", umbral)

        key = cv2.waitkey(5)
        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()