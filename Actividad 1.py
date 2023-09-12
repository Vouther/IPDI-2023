import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio

# Paso 2: Funcion que cambia de espacio de color de RGB a YIQ
def rgb_to_yiq(rgb):
    yiq = np.zeros(rgb.shape)
    yiq[:, :, 0] = 0.229 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
    yiq[:, :, 1] = 0.595716 * rgb[:, :, 0] - 0.274453 * rgb[:, :, 1] - 0.321263 * rgb[:, :, 2]
    yiq[:, :, 2] = 0.211456 * rgb[:, :, 0] - 0.522591 * rgb[:, :, 1] + 0.311135 * rgb[:, :, 2]
    return yiq

# Paso 7: Funcion que cambia de espacio de color Y'I'Q' a RGB
def yiq_to_rgb(yiq):
    rgb = np.zeros(yiq.shape)
    rgb[:, :, 0] = yiq[:, :, 0] + 0.9563 * yiq[:, :, 1] + 0.6210 * yiq[:, :, 2]
    rgb[:, :, 1] = yiq[:, :, 0] - 0.2721 * yiq[:, :, 1] - 0.6474 * yiq[:, :, 2]
    rgb[:, :, 2] = yiq[:, :, 0] - 1.1070 * yiq[:, :, 1] + 1.7046 * yiq[:, :, 2]
    return rgb

def manipulate_image():
    # Obtener los valores 'a' y 'b' de los Entry
    a = float(entry_a.get())  #Escalar la luminansia
    b = float(entry_b.get())  #Escalar la cromancia

    # Paso 1: Cargar la imagen y normalizar sus valores
    im = np.clip(imageio.imread('Charly.bmp') / 255.0, 0.0, 1.0)

    # Paso 2: Convertir RGB a YIQ
    yiq = rgb_to_yiq(im)

    # Paso 3: Escalar los valores de Y (Luminancia)
    yiq[:, :, 0] *= a

    # Paso 4: Escalar los valores de I y Q (Cromancia)
    yiq[:, :, 1] *= b
    yiq[:, :, 2] *= b

    # Paso 5: Chequear que Y' <= 1
    yiq[:, :, 0] = np.clip(yiq[:, :, 0], 0, 1)

    # Paso 6: Chequear los rangos de I' y Q'
    yiq[:, :, 1] = np.clip(yiq[:, :, 1], -0.5957, 0.5957)
    yiq[:, :, 2] = np.clip(yiq[:, :, 2], -0.5226, 0.5226)

    # Paso 7: Convertir YIQ a RGB'
    rgb_prime = yiq_to_rgb(yiq)

    # Paso 8: Convertir RGB' a bytes y mostrar la imagen
    plt.imshow(np.clip(rgb_prime, 0, 1))
    plt.axis('off')
    plt.show()

    '''# Convertir la imagen manipulada a formato Tkinter PhotoImage
    manipulated_image = Image.fromarray((rgb_prime * 255).astype(np.uint8))
    manipulated_image = ImageTk.PhotoImage(manipulated_image)

    # Mostrar la imagen en el Canvas
    canvas.image = manipulated_image
    # Mantener una referencia para evitar que sea eliminada por el recolector de basura
    canvas.create_image(0, 0, anchor=tk.NW, image=manipulated_image)'''


# Ventana principal
ventana = tk.Tk()
ventana.title("Manipulación de Imagen")

# Frame para organizar los widgets
frame = ttk.Frame(ventana, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Convertir la imagen original a formato Tkinter PhotoImage
imagen_pillow = Image.open('Charly.bmp')
imagen_tk = ImageTk.PhotoImage(imagen_pillow)

label_imagen = ttk.Label(frame)
label_imagen.grid(row=0, columnspan=2,padx=10, pady=10)
# Mostrar la imagen en el Frame
label_imagen.config(image=imagen_tk)
# Mantener una referencia para evitar que sea eliminada por el recolector de basura
label_imagen.image = imagen_tk

# Etiquetas y Entry para 'a' y 'b'
label_a = ttk.Label(frame, text="Valor de 'a' :", font=('Arial',10))
label_a.grid(row=1, column=0, padx=5, pady=5)
entry_a = ttk.Entry(frame)
entry_a.grid(row=1, column=1, padx=5, pady=5)
entry_a.insert(0, "1")

label_b = ttk.Label(frame, text="Valor de 'b' :", font=('Arial',10))
label_b.grid(row=2, column=0, padx=5, pady=5)
entry_b = ttk.Entry(frame)
entry_b.grid(row=2, column=1, padx=5, pady=5)
entry_b.insert(0, "1")

# Botón para aplicar la manipulación
button_manipulate = ttk.Button(frame, text="Aplicar Manipulación", command=manipulate_image)
button_manipulate.grid(row=3, columnspan=2, padx=5, pady=10)

#Texto derechos reservados
label_texto = ttk.Label(frame, text="@Copright 2023 - Derechos reservados Valeriano - Zerpa", font=('Arial',7))
label_texto.grid(row=5, columnspan=2, padx=5, pady=5)

'''# Crear un Canvas para mostrar la imagen
canvas = tk.Canvas(root, width=400, height=400)
canvas.grid(row=1, column=0)'''

# Iniciar la aplicación
ventana.mainloop()
