import cv2
import numpy as np
from Seguidor import *
import time

# Creamos un objeto de seguimiento
seguimiento = Rastreador()

# Abrir el video
cap = cv2.VideoCapture("autos.mp4")

deteccion = cv2.createBackgroundSubtractorMOG2(history=10000, varThreshold=10)
# PARA VERIFICAR LA RESOLUCIÓN DEL VIDEO
# Verificar si el video se ha abierto correctamente
'''if not cap.isOpened():
    print("Error al abrir el video")
else:
    # Obtener la resolución del video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"La resolución del video es {width} x {height}")'''

# Verificar si el video se ha abierto correctamente
if not cap.isOpened():
    print("Error al abrir el video")
else:
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

    # Listas para tiempos
    carI = {}
    car0 = {}
    prueba = {}

    while True:
        
        # Leer un fotograma
        ret, resized_frame = cap.read()
        if not ret:
            break

        # Creamos una mascara
        mask = np.zeros((height, width), dtype=np.uint8)

        # Elegimos una zona de interes
        # Seleccionamos los puntos
        #pts = np.array([[esquina superior izquierda], [esquina superior derecha], [esquina inferior derecha], [esquina inferior izquierda]], dtype=np.int32)
        pts = np.array([[583, 285], [665, 285], [927, 627], [359, 627]], dtype=np.int32)

        # Redimensionar el fotograma al tamaño deseado
        resized_frame = cv2.resize(resized_frame, (width, height))

        # Envolver pts en otra lista para que sea una lista de listas
        pts = [pts]
        # Cramos el poligono con los puntos
        cv2.fillPoly(mask, pts, 255)
        # Elegimos lo que esté dentro de los puntos
        zona = cv2.bitwise_and(resized_frame, resized_frame, mask=mask)

        #Mostramos con lineas la zona de interes
        areag = [(583, 285), (650, 285), (1068, 725), (289, 725)]
        area3 = [(583, 285), (650, 285), (718, 358), (534, 358)]
        area2 = [(534, 358), (718, 358), (839, 487), (451, 487)]
        area1 = [(451, 487), (839, 487), (972, 627), (359, 627)]
        

        # Dibujamos
        # Area general
        cv2.polylines(resized_frame, [np.array(areag, np.int32)], True, (255, 255, 0), 2)
        # Area 3
        cv2.polylines(resized_frame, [np.array(area3, np.int32)], True, (0, 130, 255), 1)
        # Area 2
        cv2.polylines(resized_frame, [np.array(area2, np.int32)], True, (0, 0, 255), 1)
        # Area 1
        cv2.polylines(resized_frame, [np.array(area1, np.int32)], True, (0, 130, 255), 1)

        # Creamos una mascara
        mascara = deteccion.apply(zona)
        # aplicamos filtro gausseano para eliminar ruido
        filtro = cv2.GaussianBlur(mascara, (9, 9), 0)
        # umbralizamos para binarizar las imagenes
        _, umbral = cv2.threshold(filtro, 150, 255, cv2.THRESH_BINARY)
        # aplicamos la medíana para eliminar ruido
        mediana = cv2.medianBlur(umbral, 3)
        # dilatamos para eliminar partes de color negro dentro de las imagenes
        dila = cv2.dilate(mediana, np.ones((5, 5)))
        # obtenemos los contornos de los autos
        contornos, _ = cv2.findContours(dila, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detecciones = []  # Lista donde vamos a almacenar la info de los contornos

        # Eliminamos los contornos pequeños
        for cont in contornos:
            #extrae el área de todos los contonos que hayan
            area = cv2.contourArea(cont)
            if area > 300:#si el área es mayor a 1800 proceso
                cv2.drawContours(zona,[cont], -1, (255,255,0), 2)
                #toma las medidas de los objetos, los identifica como un rectángulo
                x, y, ancho, alto = cv2.boundingRect(cont)

                # Dibujamos el rectangulo
                # cv2.rectangle(zona, (x,y), (x + ancho, y +alto), (255,255,0), 3)

                # Almacenamos las medidas de los objetos
                detecciones.append([x, y, ancho, alto])

        # Seguimiento de los objetos usando las medidas detectadas
        info_id = seguimiento.rastreo(detecciones)

        #recorre los objetos identificados en info_id
        for inf in info_id:
            # Extraemos coordenadas
            x, y, ancho, alto, id = inf

            # Dibujamos el rectangulo
            cv2.rectangle(resized_frame, (x, y - 10), (x + ancho, y + alto), (0, 0, 255), 2)  # Dibujamos el rectangulo

            # Extraemos el centro para identificar en que área está
            cx = int(x + ancho / 2)
            cy = int(y + alto / 2)

            # Area de influencia, verifica si un punto se encuentra en determinada área
            a2 = cv2.pointPolygonTest(np.array(area2, np.int32), (cx, cy), False)

            # Si esta en el area de la mitad
            if a2 >= 0: #resultados de a2: -1 si no esta en área, 1 si está dentro de área, 0 si está en límite
                # Tomamos el tiempo en el que el carro entro i guardamos en diccionario
                carI[id] = time.process_time()

            # si hay algo en carI pasamos áreas 2
            if id in carI:
                # Mostramos el centro
                cv2.circle(resized_frame, (cx, cy), 3, (0, 0, 255), -1)

                # Preguntamos si entra al area 3
                a3 = cv2.pointPolygonTest(np.array(area3, np.int32), (cx, cy), False)

                # Si esta en el area mostramos resultados de velocidad
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

                        vel = 18.40 / car0[id]
                        vel = vel * 3.6
                    
                    # Mostramos el numero
                    cv2.rectangle(resized_frame, (x, y - 10), (x + 70, y - 50), (0, 0, 255), -1)
                    cv2.putText(resized_frame, str(int(vel)) + " KM / H", (x, y - 35), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 0),2)

                # Mostramos el numero
                cv2.putText(resized_frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)


        # Mostrar el fotograma redimensionado
        cv2.imshow("Video", resized_frame)
      
        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la captura de video y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()






