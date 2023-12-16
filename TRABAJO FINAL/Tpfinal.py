from PIL import Image as PILImage, ImageTk
from tkinter import *
from tkinter import filedialog, ttk
import cv2
import numpy as np
import time
from VELOCIDAD.Seguidor import *
from PATENTE.Reconocimiento import LPR
salir_del_bucle = False
pausar_bucle = True
btnCerrar = None 
btnPausar = None 

def limpiar_interfaz():
    # Restaurar la información del video
    lblInfoVideoPath.configure(text="Aún no ha seleccionado un video")

    # Deshabilitar el botón después de seleccionar una opción del ComboBox
    btnSelecionarVideo['state'] = 'disabled'
    # Limpiar el Canvas
    canvas.delete("all")
    lblVideo.configure(image=None)
    lblVideo.image = None
    # Ocultar el Label de video
    lblVideo.place_forget()
    btnCerrar.destroy()
 


def cerrar_reproduccion():
    global salir_del_bucle, cap
    salir_del_bucle = True  # Establece la variable para salir del bucle
    # Llamar a la función para limpiar la interfaz antes de cerrar
    limpiar_interfaz()

    # Actualizar la ventana de Tkinter para reflejar los cambios
    cap.release()
    root.update()
def pausar_reproduccion():
    # Variable para controlar el estado de reproducción (True para reproducción, False para pausa)
    global pausar_bucle
    pausar_bucle= not pausar_bucle

def visualizarVelocidad(video_path):
    
    global salir_del_bucle, btnCerrar
    salir_del_bucle = False
    # Creamos un objeto de seguimiento
    seguimiento = Rastreador()

    global cap  # Referenciar la variable global cap
    cap = cv2.VideoCapture(video_path)
    deteccion = cv2.createBackgroundSubtractorMOG2(history=10000, varThreshold=10)
    lblVideo.place(x=25, y=0)
    if not cap.isOpened():
        print("Error al abrir el video")
    else:

        height = 727
        width = 1298

        # Listas para tiempos
        carI = {}
        car0 = {}
        prueba = {}

        canvas.config(width=width, height=height)
        # Crear el botón de cierre fuera del bucle

        btnCerrar = Button(root, text="STOP", command=cerrar_reproduccion, bg="red", fg="white", font=("Arial", 12))
        btnCerrar_window = canvas.create_window(150, 50, anchor=NW, window=btnCerrar)
        while True:
            # Leer un fotograma
            ret, frame = cap.read()
            if not ret:
                break

            # Redimensionar el fotograma
            resized_frame = cv2.resize(frame, (width, height))

            #PROCESAMIENTO
            # Creamos una mascara
            mask = np.zeros((height, width), dtype=np.uint8)

            # Elegimos una zona de interes
            # Seleccionamos los puntos
            #pts = np.array([[esquina superior izquierda], [esquina superior derecha], [esquina inferior derecha], [esquina inferior izquierda]], dtype=np.int32)
            pts = np.array([[583, 285], [665, 285], [927, 627], [359, 627]], dtype=np.int32)

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

            # Verificar si se debe seguir procesando y actualizando el label
            img = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(PILImage.fromarray(img))

            lblVideo.configure(image=img)
            lblVideo.image = img
            
            root.update()
            
            # Salir del bucle si se presiona la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q') or salir_del_bucle:
                break
             
        # Liberar la captura de video
        cap.release()

def visualizarPatentes(video_path):
    global salir_del_bucle, btnCerrar, pausar_bucle
    salir_del_bucle = False

    global cap  # Referenciar la variable global cap
    cap = cv2.VideoCapture(video_path)
    
    lblVideo.place(x=25, y=0)
    if not cap.isOpened():
        print("Error al abrir el video")
    else:
        # Dimensiones deseadas para mostrar el video
        desired_width = 1298
        desired_height = 727

        canvas.config(width=desired_width, height=desired_height)
        # Crear el botón de cierre fuera del bucle
        btnCerrar = Button(root, text="STOP", command=cerrar_reproduccion, bg="red", fg="white", font=("Arial", 12))
        btnCerrar_window = canvas.create_window(150, 50, anchor=NW, window=btnCerrar)

        
        #Aqui almacenamos los caracteres de las placas
        Ctexto = ''

        # Establecemos la velocidad de reproducción deseada (por ejemplo, 30 fotogramas por segundo)
        # Comentar si no es necesario y controlar el ingreso de teclas
        #desired_fps = 30
        #cap.set(cv2.CAP_PROP_FPS, desired_fps)

        # Creamos una instancia de la clase LPR
        lpr = LPR()

        # Creamos nuestro while true
        while True:
            #btnPausar = Button(root, text="PAUSAR", command=pausar_reproduccion, bg="green", fg="white", font=("Arial", 12))
            #btnPausar_window = canvas.create_window(150, 100, anchor=NW, window=btnPausar)

            # Si estamos en estado de reproducción, leemos el siguiente fotograma
            
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
            #cv2.imshow("Video", frame)
            # Verificar si se debe seguir procesando y actualizando el label
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(PILImage.fromarray(img))

            lblVideo.configure(image=img)
            lblVideo.image = img
            
            root.update()

            # Para la reproduccion sin una velocidad de reproduccion establecida descomentar
            # Leemos una tecla
            #key = cv2.waitKey(1)

            # Para la reproduccion con una velocidad de reproduccion establecida descomentar
            # Leemos una tecla
            #key = cv2.waitKey(1000 // desired_fps)  # Espera según la velocidad de reproducción deseada

            # Manejo de eventos de teclado
            if salir_del_bucle:
                break
            

        cap.release()

def cerrar_aplicacion():
    root.quit()
    root.destroy() #Liberación de recursos y cierre adecuado

def seleccionar_video():
    
    video_path = filedialog.askopenfilename(filetypes=[
        ("all video format", ".mp4"),
        ("all video format", ".avi")
    ])
    
    if len(video_path) > 0:
        if(combo.get()=="Análisis de velocidad"):
            visualizarVelocidad(video_path)
        elif(combo.get()=="Análisis de patentes"):
            visualizarPatentes(video_path)
    else:
        lblInfoVideoPath.configure(text="Aún no ha seleccionado un video")

def on_combobox_select(event):
    # Habilitar el botón después de seleccionar una opción del ComboBox
    btnSelecionarVideo['state'] = 'normal'

root = Tk()
root.geometry("1405x810")
root.title("Reproductor de Video")

cap = None

# Crear un Canvas en lugar de Label para mostrar el video
canvas = Canvas(root)
canvas.grid(column=0, row=2, columnspan=2)

# Label del ComboBox
lblNewLabel = Label(root, text="Selecciona una operación a realizar:")
lblNewLabel.place(x=550, y=175)

# Crear el ComboBox
opciones = ["Análisis de velocidad", "Análisis de patentes"]  # Puedes personalizar las opciones
selected_option = StringVar()
combo = ttk.Combobox(root, textvariable=selected_option, values=opciones, width=45, height=2, state="readonly")
combo.set("Selecciona una opción")
combo.place(x=550, y=200)

# Vincular eventos
combo.bind("<<ComboboxSelected>>", on_combobox_select)

# Label del Botón video
lblNewLabel = Label(root, text="Debes seleccionar un video para el análisis:")
lblNewLabel.place(x=550, y=228)

# Botón selección video
btnSelecionarVideo = Button(root, bg="white", text='Seleccionar Video', command=lambda: seleccionar_video(), width=40, height=2, state='disabled')
btnSelecionarVideo.place(x=550, y=250)

lblInfoVideoPath = Label(root, text="Aún no ha seleccionado un video")
lblInfoVideoPath.place(x=550, y=300)

btnCerrar = Button(root, bg="white", text='Cerrar Programa', command=lambda: cerrar_aplicacion(), width=40, height=2)
btnCerrar.place(x=550, y=400)

phatVideo=Label(root)
phatVideo.place(x=25, y=0)
lblVideo = Label(root)
lblVideo.place(x=25, y=0)

root.mainloop()