import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import imageio.v2 as imageio
import operaciones_img as ope
import re
import numpy as np
import datetime  # Importa el módulo datetime

nombre_archivo = ""

def generar_imagen(imagen):

    # Convertir la imagen al rango [0, 255] y cambiar el tipo de datos a uint8
    imagen_convertida = (imagen * 255).astype(np.uint8)

    # Generarmos un nombre de archivo único basado en la fecha y hora actual

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    global nombre_archivo
    nombre_archivo = f"imagen_filtrada_{timestamp}.png"

    # Guardarmos la imagen filtrada en formato PNG con el nombre único
    imageio.imwrite(nombre_archivo, imagen_convertida)

    # Cargar la imagen convertida en formato PIL
    imagen_pil = Image.open(nombre_archivo)

    # Redimensionar la imagen a 300x300
    imagen_pil = imagen_pil.resize((300, 300))

    # Convertir la imagen a formato PhotoImage
    imagen_tk = ImageTk.PhotoImage(imagen_pil)

    # Cargar la imagen convertida en PhotoImage y mostrarla en el Label
    label_imagen2.config(image=imagen_tk)
    label_imagen2.image = imagen_tk

def manipulate_image():
    seleccion = combobox.get()
    primera_palabra = seleccion.split()[0]

    if image_path != "":
        img = imageio.imread(image_path)
        img = ope.normalize_rgb(img)

        print('Tamaño: ',img.shape)

        if primera_palabra == "Erosion":
            imagen_filtrada = ope.im_erode(img, np.ones((3,3),bool))
            '''plt.imshow(imagen_filtrada, 'gray')
            plt.show()'''
            generar_imagen(imagen_filtrada)

        elif primera_palabra == "Dilatacion":
            imagen_filtrada = ope.im_dilate(img, np.ones((3,3),bool))
            '''plt.imshow(imagen_filtrada, 'gray')
            plt.show()'''
            generar_imagen(imagen_filtrada)

        elif primera_palabra == "Apertura":
            imagen_filtrada = ope.im_open(img, np.ones((3,3),bool))
            '''plt.imshow(imagen_filtrada, 'gray')
            plt.show()'''
            generar_imagen(imagen_filtrada)

        elif primera_palabra == "Cierre":
            imagen_filtrada = ope.im_close(img,np.ones((3,3),bool))
            '''plt.imshow(imagen_filtrada, 'gray')
            plt.show()'''
            generar_imagen(imagen_filtrada)

        elif primera_palabra == "Mediana":
            imagen_filtrada = ope.im_mediana(img, np.ones((3, 3), bool))
            '''plt.imshow(imagen_filtrada, 'gray')
            plt.show()'''
            generar_imagen(imagen_filtrada)
        else:
            mensaje = f"Debes selecionar una de las opciones"
            messagebox.showinfo("Identificación", mensaje)
    else:
        mensaje = "Debes abrir una imagen para aplicar un filtro."
        messagebox.showinfo("Identificación", mensaje)

def cerrar_aplicacion():
    ventana.quit()
    ventana.destroy() #Liberación de recursos y cierre adecuado

def copiar_imagen():
    global image_path

    if nombre_archivo == "":
        mensaje = "Debes aplicar un filtro para poder copiar."
        messagebox.showinfo("Identificación", mensaje)
    else:
        # Cargar la imagen convertida en formato PIL
        imagen_cop = Image.open(nombre_archivo)

        # Redimensionar la imagen a 300x300
        imagen_cop = imagen_cop.resize((300, 300))

        # Cargamos la imagen filtrada en PhotoImage y mostramos en el Label
        imagen_tk = ImageTk.PhotoImage(imagen_cop)
        label_imagen.config(image=imagen_tk)
        label_imagen.image = imagen_tk

        #Actualizamos la tura de la imagen a procesar
        image_path = nombre_archivo

    # Actualizamos el fondo de la imagen filtrada
    imagen_tk = ImageTk.PhotoImage(imagen_pillow)
    # Mostrar la imagen en el Frame
    label_imagen2.config(image=imagen_tk)
    # Mantener una referencia para evitar que sea eliminada por el recolector de basura
    label_imagen2.image = imagen_tk
def open_image():
    global image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.bmp *.tif")])

    if file_path:
        image_path = file_path
        image = Image.open(file_path)
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)
        label_imagen.config(image=photo)
        label_imagen.image = photo  # Evita que la imagen sea eliminada por el recolector de basura

    # Actualizamos el fondo de la imagen filtrada
    imagen_tk = ImageTk.PhotoImage(imagen_pillow)
    # Mostrar la imagen en el Frame
    label_imagen2.config(image=imagen_tk)
    # Mantener una referencia para evitar que sea eliminada por el recolector de basura
    label_imagen2.image = imagen_tk


# Inicializar la ventana
ventana = tk.Tk()
ventana.title("Procesamiento morfológico binario")

# Dimension de la ventana pixeles x pixeles
ventana.geometry('770x600')

# Configurar la ventana principal para expandirse en ambas direcciones
ventana.rowconfigure(0, weight=1)
ventana.columnconfigure(0, weight=1)

# Creamos un estilo personalizado para el botón
style = ttk.Style()
style.configure("RoundedButton.TButton", borderwidth=5, relief="ridge",
                bordercolor="gray", padding=2, foreground="black", background="lightgray",
                font=("Helvetica", 10))
style.map("RoundedButton.TButton",
    foreground=[("active", "green"), ("disabled", "grey")],
    background=[("active", "green")]
)

# Frame para organizar los widgets ------------------------- FRAME1
frame = ttk.Frame(ventana, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Inicializamos la variable para guardar la ruta de la imagen
image_path = ""

# Etiquetas de Titulo
label_a = ttk.Label(frame, text="Procesamiento morfológico",
                    font=('Arial', 18, 'bold'),
                    foreground='green',padding=5,
                    background='lightgray', borderwidth=2, relief='solid')
label_a.grid(row=0, columnspan=3, padx=5, pady=5)

# IMAGEN SUBIR
# Convertir la imagen original a formato Tkinter PhotoImage
imagen_pillow = Image.open('abrir_carpeta.png')
# Redimensionar la imagen al tamaño deseado (350x350)
imagen_pillow = imagen_pillow.resize((300, 300))
imagen_tk = ImageTk.PhotoImage(imagen_pillow)

# IMAGEN ORIGINAL
label_imagen = ttk.Label(frame, text="Imagen Original",
                        font=('Arial', 12, 'bold'),
                        borderwidth=2, relief='solid')
label_imagen.grid(row=1, column=0,padx=10, pady=10)
# Mostrar la imagen en el Frame
label_imagen.config(image=imagen_tk)
# Mantener una referencia para evitar que sea eliminada por el recolector de basura
label_imagen.image = imagen_tk

# Botón para cambiar de imagen
button_copiar = ttk.Button(frame, text="<- Copiar", style="RoundedButton.TButton", command=copiar_imagen)
button_copiar.grid(row=1, column=1, padx=5, pady=5)

# IMAGEN FILTRADA
label_imagen2 = ttk.Label(frame, text="Imagen Filtrada",
                        font=('Arial', 12, 'bold'),
                        borderwidth=2, relief='solid')
label_imagen2.grid(row=1, column=2,padx=10, pady=10)
# Mostrar la imagen en el Frame
label_imagen2.config(image=imagen_tk)
# Mantener una referencia para evitar que sea eliminada por el recolector de basura
label_imagen2.image = imagen_tk

# Frame para organizar los widgets ------------------------- FRAME2
frame2 = ttk.Frame(ventana, padding=10)
frame2.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame2.grid_rowconfigure(0, weight=1)
frame2.grid_columnconfigure(0, weight=1)

# Etiquetas imagen original
label_original = ttk.Label(frame2, text="Imagen Original", font=('Arial',12,'bold'))
label_original.grid(row=0, column=0, padx=5, pady=5)

# Botón para abrir la imagen
button_abrir = ttk.Button(frame2, text="Abrir imagen", style="RoundedButton.TButton", command=open_image)
button_abrir.grid(row=1, column=0, padx=5, pady=5)

# Etiquetas de seleccion
label_a = ttk.Label(frame2, text="Filtro a aplicar: ", font=('Arial',10))
label_a.grid(row=0, column=1, padx=5, pady=5)

# Crear el Combobox con las opciones
opciones = ["Erosion",
            "Dilatacion",
            "Apertura",
            "Cierre",
            "Mediana"]
combobox = ttk.Combobox(frame2, values=opciones, state="readonly")
combobox.set("Seleccion")  # Texto predeterminado en el Combobox
combobox.grid(row=1, column=1, padx=5, pady=5)

# Etiquetas de imagen filtrada
label_filtro = ttk.Label(frame2, text="Imagen Filtrada", font=('Arial',12,'bold'))
label_filtro.grid(row=0, column=2, padx=5, pady=5)

# Botón para aplicar la manipulación
button_aplicar = ttk.Button(frame2, text="Aplicar", style="RoundedButton.TButton", command=manipulate_image)
button_aplicar.grid(row=1, column=2, padx=5, pady=5)

# Botón para cerrar la aplicacion
button_salir = ttk.Button(frame2, text="Salir", style="RoundedButton.TButton", command=cerrar_aplicacion)
button_salir.grid(row=2, column=2, padx=5, pady=5)

# Texto derechos reservados
label_texto = ttk.Label(frame2, text="@Copright 2023 - Derechos reservados Valeriano - Zerpa", font=('Arial',7))
label_texto.grid(row=3, columnspan=3, padx=5, pady=20)

# Iniciar la aplicación
ventana.mainloop()