# Importamos las librerias
import cv2
import numpy as np
import pytesseract
from PIL import Image

# Realizamos la ViedoCaptura
cap = cv2.VideoCapture("Placas.mp4")

# Dimensiones deseadas para mostrar el video
desired_width = 1298
desired_height = 727

#Aqui almacenamos los caracteres de las placas
Ctexto = ''

# Creamos nuestro while true
while True:
    # Relizamos la lectura de la VideoCaptura
    ret, frame = cap.read()

    if ret == False:
        break

    # Redimensionamos el fotograma al tamaño deseado
    frame = cv2.resize(frame, (desired_width, desired_height))

    # Dibujamos un rectangulo
    cv2.rectangle(frame, (682, 565), (920, 634), (0, 0, 0), cv2.FILLED)
    #Ctexto se configura como un arreglo de acuerdo a la cantidad de caracteres verdaderos
    cv2.putText(frame, Ctexto[0:9], (698, 612), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Extraemos el ancho y el alto de los fotogramas
    al, an, c = frame.shape

    #************** REGION DE INTERES *******************************
    # Tomar el centro de la imagen
    # En x:
    x1 = int(200)
    x2 = int(1000)

    # En y:
    y1 = int(248)
    y2 = int(477)

    #print('Primer punto: ',x1,y1)
    #print('Segundo punto: ',x2,y2)
    # ****************************************************************

    # Texto
    cv2.rectangle(frame, (337, 566), (650, 631), (0, 0, 0), cv2.FILLED)
    cv2.putText(frame, 'Procesando Placa', (351, 612), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Ubicamos el rectangulo en las zonas extraidas (EN COLOR VERDE)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Realizamos un recorte a nuestra zona de interes
    # Se extraen los pixeles que pertenecen al rectagulo (interior)
    recorte = frame[y1:y2, x1:x2]

    # Preprocesamiento de la zona de interes, separamos los canales RGB
    mB = np.matrix(recorte[:, :, 0])
    mG = np.matrix(recorte[:, :, 1])
    mR = np.matrix(recorte[:, :, 2])

    # Convertir la imagen al espacio de color YUV
    yuv = cv2.cvtColor(recorte, cv2.COLOR_BGR2YUV)
    y_channel = yuv[:, :, 0]

    # Color de la patente, aquí se especifica cuál es
    Color = cv2.absdiff(mG, mB)  # Buscamos la diferencia entre G y B para destacar las regiones amarillas

    # Binarizamos la imagen
    _, umbral = cv2.threshold(Color, 40, 255, cv2.THRESH_BINARY)

    # Binarizar la imagen basándonos en el canal de luminancia
    #_, umbral = cv2.threshold(y_channel, 200, 255, cv2.THRESH_BINARY_INV)

    # Eliminación de ruido
    umbral = cv2.medianBlur(umbral, 5)

    # Extraemos los contornos de la zona seleccionada
    contornos, _ = cv2.findContours(umbral, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrado de contornos
    contornos = [contorno for contorno in contornos if
                 cv2.contourArea(contorno) > 500 and cv2.contourArea(contorno) < 5000]

    # Primero los ordenamos del mas grande al mas pequeño
    contornos = sorted(contornos, key=lambda x: cv2.contourArea(x), reverse=True)

    # Dibujamos los contornos extraidos
    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > 500 and area < 5000:
            # Detectamos la placa, para dibujar un rectangulo sobre la misma
            x, y, ancho, alto = cv2.boundingRect(contorno)

            # Extraemos las coordenadas
            xpi = x + x1  # Coordenadas de la placa en x inicial
            ypi = y + y1  # Coordenadas de la placa en y

            xpf = x + ancho + x1  # Coordenada de la placa en X final
            ypf = y + alto + y1  # Coordenada de la placa en Y inicial

            # Dibujamos el rectangulo
            cv2.rectangle(frame, (xpi, ypi), (xpf, ypf), (255, 255, 0), 2)

            # Extraemos los pixeles que pertenecen a la paca, con los colores originales en RGB
            placa = frame[ypi:ypf, xpi:xpf]

            # Extraemos el ancho y el alto de los fotogramas
            alt, anp, cp = placa.shape
            # print(alt, anp)

            # Procesamos los pixeles para extraer los valores de las placas
            Mva = np.zeros((alt, anp))

            # Normalizamos las Matrices, separacion de los canales
            nBp = np.matrix(placa[:, :, 0])
            nGp = np.matrix(placa[:, :, 1])
            nRp = np.matrix(placa[:, :, 2])

            # Creamos una mascara
            for col in range(0, alt):
                for fil in range(0, anp):
                    Max = max(nRp[col, fil], nGp[col, fil], nBp[col, fil])
                    Mva[col, fil] = 255 - Max #Se hace la diferencia para resaltar el color negro de los caracteres en la placa

            # Binarizamos la imagen con el fin de que solo me queden los caracteres
            _, bin = cv2.threshold(Mva, 150, 255, cv2.THRESH_BINARY)

            # Convertimos la matris en imagen, para poder procesarla en el reconocimiento de texto
            bin = bin.reshape(alt, anp)
            bin = Image.fromarray(bin)
            bin = bin.convert("L")

           # Nos aseguramos de tener un buen tamaño de placa
            if alt >= 36 and anp >= 82:

                # Declaramos la direccion de Pytesserect
                pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

                # Extraemos el texto
                config = "--psm 1"
                texto = pytesseract.image_to_string(bin, config=config)

                # If para no mostrar masura, es decir que se reconozcan todos los caracteres
                if len(texto) >= 9:
                    # print(texto[0:7])
                    Ctexto = texto

                # Mostramos los valores que nos interesan
                # cv2.putText(frame, Ctexto[0:7], (910, 810), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            break

        # Mostramos el recorte
        #cv2.imshow("Recorte", bin)

    # Mostramos al recorte en gris
    cv2.imshow("Vehiculos", frame)

    # Leemos una tecla
    t = cv2.waitKey(1)

    if t == 27:
        break

cap.release()
cv2.destroyAllWindows()