import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import imageio.v2 as imageio
import operaciones_img as ope
import re
import numpy as np
import datetime  # Importa el módulo datetime


'''MAT_YIQ = np.array([0.299, 0.595716, 0.211456],
                   [0.587, -0.274453, -0.522591],
                   [0.114, -0.321263, 0.311135])

def rgbtoyiq(_im):
    return (_im.reshape((-1,1))@MAT_YIQ).reshape(_im.shape)'''

def generar_imagen(imagen):
    # Generarmos un nombre de archivo único basado en la fecha y hora actual
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo = f"imagen_filtrada_{timestamp}.ppm"

    # Guardarmos la imagen filtrada en formato PPM con el nombre único
    imageio.imwrite(nombre_archivo, imagen)

    # Cargamos la imagen filtrada en PhotoImage y mostramos en el Label
    imagen_tk = ImageTk.PhotoImage(file=nombre_archivo)
    label_imagen2.config(image=imagen_tk)
    label_imagen2.image = imagen_tk
def obtener_numero(cadena):
    # Utilizarmos una expresión regular para buscar el último número en la cadena
    numero = re.search(r'\d+$', cadena)
    if numero:
        return int(numero.group())  # Convertirmos el número encontrado a entero
    else:
        return None  # Devolvermos None si no se encontró ningún número
def manipulate_image():
    seleccion = combobox.get()
    primera_palabra = seleccion.split()[0]

    if image_path != "":
        img = imageio.imread(image_path)
        img = ope.normalize_rgb(img)
        #yiq = ope.RGB_to_YIQ(img)
        numero = obtener_numero(seleccion)

        if primera_palabra == "Bartlett":
            bartlett = ope.bartlett_kernel(numero)
            #ope.mostrar_imagen(ope.aplicar_filtro(img,bartlett))

            imagen_filtrada = ope.aplicar_filtro(img,bartlett).astype(np.uint8)  # Combinamos canales y convertimos a uint8
            generar_imagen(imagen_filtrada)

        elif primera_palabra == "Gaussiano":
            gausiano = ope.gaussiano_kernel(numero)
            #ope.mostrar_imagen(ope.aplicar_filtro(img,gausiano))

            imagen_filtrada = ope.aplicar_filtro(img,gausiano).astype(np.uint8)  # Combinamos canales y convertimos a uint8
            generar_imagen(imagen_filtrada)

        elif primera_palabra == "Laplaciano":
            laplaciano = ope.laplaciano_kernel(numero)
            #ope.mostrar_imagen(ope.aplicar_filtro(img,laplaciano))

            imagen_filtrada = ope.aplicar_filtro(img,laplaciano).astype(np.uint8)  # Combinamos canales y convertimos a uint8
            generar_imagen(imagen_filtrada)

        elif primera_palabra == "Sobel":
            ultima_palabra = seleccion.split()[-1]
            sobel = ope.sobel_kernel(ultima_palabra)
            #ope.mostrar_imagen(ope.aplicar_filtro(img,sobel))

            imagen_filtrada = ope.aplicar_filtro(img,sobel).astype(np.uint8)  # Combinamos canales y convertimos a uint8
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


# Inicializar la ventana
ventana = tk.Tk()
ventana.title("Filtrado por Convolucion")

#Dimension de la ventana pixeles x pixeles
ventana.geometry('680x550')

# Configurar la ventana principal para expandirse en ambas direcciones
ventana.rowconfigure(0, weight=1)
ventana.columnconfigure(0, weight=1)

# Frame para organizar los widgets ------------------------- FRAME1
frame = ttk.Frame(ventana, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Inicializamos la variable para guardar la ruta de la imagen
image_path = ""

# Etiquetas de Titulo
label_a = ttk.Label(frame, text="Imagen Original",
                    font=('Arial', 18, 'bold'),
                    foreground='green',padding=5,
                    background='lightgray', borderwidth=2, relief='solid')
label_a.grid(row=0, column=0, padx=5, pady=5)

# Botón para abrir la imagen
button_abrir = ttk.Button(frame, text="Abrir imagen", command=open_image)
button_abrir.grid(row=0, column=1, padx=5, pady=5)

#IMAGEN SUBIR
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

#IMAGEN FILTRADA
label_imagen2 = ttk.Label(frame, text="Imagen Filtrada",
                        font=('Arial', 12, 'bold'),
                        borderwidth=2, relief='solid')
label_imagen2.grid(row=1, column=1,padx=10, pady=10)
# Mostrar la imagen en el Frame
label_imagen2.config(image=imagen_tk)
# Mantener una referencia para evitar que sea eliminada por el recolector de basura
label_imagen2.image = imagen_tk

'''
# Crear una etiqueta para mostrar la imagen
label = tk.Label(root)
label.pack()

# Después de cerrar la ventana, puedes acceder a la ruta de la imagen en la variable 'image_path'
print("Ruta de la imagen seleccionada:", image_path)'''

# Creamos un estilo personalizado para el botón
style = ttk.Style()
style.configure("RoundedButton.TButton", borderwidth=5, relief="ridge",
                bordercolor="gray", padding=2, foreground="black", background="lightgray",
                font=("Helvetica", 10))
style.map("RoundedButton.TButton",
    foreground=[("active", "green"), ("disabled", "grey")],
    background=[("active", "green")]
)

# Frame para organizar los widgets ------------------------- FRAME2
frame2 = ttk.Frame(ventana, padding=10)
frame2.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame2.grid_rowconfigure(0, weight=1)
frame2.grid_columnconfigure(0, weight=1)

# Etiquetas de seleccion
label_a = ttk.Label(frame2, text="Filtro a aplicar: ", font=('Arial',10))
label_a.grid(row=0, column=0, padx=5, pady=5)

# Crear el Combobox con las opciones
opciones = [
            "Bartlett 3x3",
            "Bartlett 5x5",
            "Bartlett 7x7",
            "Gaussiano 5x5",
            "Gaussiano 7x7",
            "Laplaciano v4",
            "Laplaciano v8",
            "Sobel 3x3 Oeste",
            "Sobel 3x3 Este",
            "Sobel 3x3 Norte",
            "Sobel 3x3 Sur"]
combobox = ttk.Combobox(frame2, values=opciones, state="readonly")
combobox.set("Seleccion")  # Texto predeterminado en el Combobox
combobox.grid(row=0, column=1, padx=5, pady=5)

# Botón para aplicar la manipulación
button_aplicar = ttk.Button(frame2, text="Aplicar", style="RoundedButton.TButton", command=manipulate_image)
button_aplicar.grid(row=0, column=2, padx=5, pady=5)

# Botón para guardar la imagen
button_guardar = ttk.Button(frame2, text="Guardar", style="RoundedButton.TButton", command=cerrar_aplicacion)
button_guardar.grid(row=1, column=2, padx=5, pady=5)

# Botón para cerrar la aplicacion
button_salir = ttk.Button(frame2, text="Salir", style="RoundedButton.TButton", command=cerrar_aplicacion)
button_salir.grid(row=1, column=1, padx=5, pady=5)

#Texto derechos reservados
label_texto = ttk.Label(frame2, text="@Copright 2023 - Derechos reservados Valeriano - Zerpa", font=('Arial',7))
label_texto.grid(row=2, columnspan=3, padx=5, pady=20)

# Iniciar la aplicación
ventana.mainloop()