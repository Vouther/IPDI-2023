import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import imageio.v2 as imageio
import matplotlib.pyplot as plt
import operaciones_img as ope

def manipulate_image():
    seleccion = combobox.get()
    '''if seleccion:
        mensaje = f"Seleccionaste la operacion {seleccion}"
        messagebox.showinfo("Identificación", mensaje)'''
    im1 = imageio.imread('bosque.bmp')
    im2 = imageio.imread('fuente.bmp')
    im1,im2 = ope.igualar_dimensiones(im1,im2)
    im1 = ope.normalize_rgb(im1)
    im2 = ope.normalize_rgb(im2)

    if seleccion == "Suma Clampeada RGB":
        ope.mostrar_imagen(ope.RGB_to_bytes(ope.suma_clampeada_rgb(im1,im2)))
    elif seleccion == "Resta Clampeada RGB":
        ope.mostrar_imagen(ope.RGB_to_bytes(ope.resta_clampeada_rgb(im1,im2)))
    elif seleccion == "Suma Promediada RGB":
        ope.mostrar_imagen(ope.RGB_to_bytes(ope.suma_promediada_rgb(im1,im2)))
    elif seleccion == "Resta Promediada RGB":
        ope.mostrar_imagen(ope.RGB_to_bytes(ope.resta_promediada_rgb(im1,im2)))
    else:
        mensaje = f"Debes selecionar una de las opciones"
        messagebox.showinfo("Identificación", mensaje)

def cerrar_aplicacion():
    ventana.quit()

# Ventana principal
ventana = tk.Tk()
ventana.title("Aritmetica de pixeles")

# Frame para organizar los widgets
frame = ttk.Frame(ventana, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

#IMAGEN 1
# Convertir la imagen original a formato Tkinter PhotoImage
imagen_pillow1 = Image.open('bosque.bmp')
imagen_tk1 = ImageTk.PhotoImage(imagen_pillow1)

label_imagen1 = ttk.Label(frame)
label_imagen1.grid(row=0, column=0,padx=10, pady=10)
# Mostrar la imagen en el Frame
label_imagen1.config(image=imagen_tk1)
# Mantener una referencia para evitar que sea eliminada por el recolector de basura
label_imagen1.image = imagen_tk1

#IMAGEN 2
# Convertir la imagen original a formato Tkinter PhotoImage
imagen_pillow2 = Image.open('fuente.bmp')
imagen_tk2 = ImageTk.PhotoImage(imagen_pillow2)

label_imagen2 = ttk.Label(frame)
label_imagen2.grid(row=0, column=1,padx=10, pady=10)
# Mostrar la imagen en el Frame
label_imagen2.config(image=imagen_tk2)
# Mantener una referencia para evitar que sea eliminada por el recolector de basura
label_imagen2.image = imagen_tk2

# Etiquetas
label_a = ttk.Label(frame, text="Operacion a realizar :", font=('Arial',10))
label_a.grid(row=1, column=0, padx=5, pady=5)

# Crear el Combobox con las opciones
opciones = ["Suma Clampeada RGB",
            "Resta Clampeada RGB",
            "Suma Promediada RGB",
            "Resta Promediada RGB",
            "If Ligther","If Darker"]
combobox = ttk.Combobox(frame, values=opciones, state="readonly")
combobox.set("Seleccione una opción")  # Texto predeterminado en el Combobox
combobox.grid(row=1, column=1, padx=5, pady=5)

# Botón para aplicar la manipulación
button_manipulate = ttk.Button(frame, text="Mostrar imagen", command=manipulate_image)
button_manipulate.grid(row=3, column=0, padx=5, pady=5)

# Botón para cerrar la aplicacion
button_manipulate = ttk.Button(frame, text="Salir", command=cerrar_aplicacion)
button_manipulate.grid(row=3, column=1, padx=5, pady=10)

#Texto derechos reservados
label_texto = ttk.Label(frame, text="@Copright 2023 - Derechos reservados Valeriano - Zerpa", font=('Arial',7))
label_texto.grid(row=5, columnspan=2, padx=5, pady=5)


# Iniciar la aplicación
ventana.mainloop()
