import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk, ImageFilter
import imageio.v2 as imageio
import operaciones_img as ope

'''MAT_YIQ = np.array([0.299, 0.595716, 0.211456],
                   [0.587, -0.274453, -0.522591],
                   [0.114, -0.321263, 0.311135])

def rgbtoyiq(_im):
    return (_im.reshape((-1,1))@MAT_YIQ).reshape(_im.shape)'''

def get_ymin_ymax(yiq):
    ventana2 = tk.Tk()
    ventana2.title("Valores ymin y ymax")
    ventana2.geometry("200x100")  # Cambia el tamaño de la ventana

    ymin_label = tk.Label(ventana2, text="ymin:")
    ymin_label.grid(row=0, column=0, padx=10, pady=5)  # Ajuste del espaciado
    ymin_entry = tk.Entry(ventana2)
    ymin_entry.grid(row=0, column=1, padx=10, pady=5)  # Ajuste del espaciado

    ymax_label = tk.Label(ventana2, text="ymax:")
    ymax_label.grid(row=1, column=0, padx=10, pady=5)  # Ajuste del espaciado
    ymax_entry = tk.Entry(ventana2)
    ymax_entry.grid(row=1, column=1, padx=10, pady=5)  # Ajuste del espaciado

    def submit_values():
        ymin = float(ymin_entry.get())
        ymax = float(ymax_entry.get())
        ventana2.destroy()  # Cierra la ventana después de recopilar los valores
        if not (ymin < ymax):
            messagebox.showerror("Error", "ymin debe ser menor que ymax")
        else:
            perform_operation_with_ymin_ymax(yiq,ymin, ymax)

    submit_button = tk.Button(ventana2, text="Aceptar", command=submit_values)
    submit_button.grid(row=2, columnspan=2, pady=10)  # Ajuste del espaciado

    ventana2.mainloop()


def perform_operation_with_ymin_ymax(yiq,ymin, ymax):
    # Realizamos la operación con los valores ymin y ymax
    rgb_result = ope.YIQ_to_RGB(ope.check_yiq(ope.lineal_a_tarzos(yiq,ymin,ymax)))
    ope.mostrar_imagen(rgb_result,ope.RGB_to_bytes(rgb_result))

def manipulate_image():
    seleccion = combobox.get()

    if image_path != "":
        img = imageio.imread(image_path)
        img = ope.normalize_rgb(img)
        yiq = ope.RGB_to_YIQ(img)

        if seleccion == "Raiz":
            rgb_result = ope.YIQ_to_RGB(ope.check_yiq(ope.raiz_cuadrada(yiq)))
            ope.mostrar_imagen(rgb_result, ope.RGB_to_bytes(rgb_result))
        elif seleccion == "Cuadrado":
            rgb_result = ope.YIQ_to_RGB(ope.check_yiq(ope.cuadratica(yiq)))
            ope.mostrar_imagen(rgb_result,ope.RGB_to_bytes(rgb_result))
        elif seleccion == "Trazos":
            get_ymin_ymax(yiq)  # Esta función abre una ventana personalizada
        else:
            mensaje = f"Debes selecionar una de las opciones"
            messagebox.showinfo("Identificación", mensaje)
    else:
        mensaje = "Debes abrir una imagen para manipular."
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
        image = image.resize((350, 350))
        photo = ImageTk.PhotoImage(image)
        label_imagen.config(image=photo)
        label_imagen.image = photo  # Evita que la imagen sea eliminada por el recolector de basura


# Inicializar la ventana
ventana = tk.Tk()
ventana.title("Operaciones de Luminansia")

#Dimension de la ventana pixeles x pixeles
ventana.geometry('400x600')

# Frame para organizar los widgets
frame = ttk.Frame(ventana, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Inicializar la variable para guardar la ruta de la imagen
image_path = ""

# Etiquetas de Titulo
label_a = ttk.Label(frame, text="Operaciones de Luminansia",
                    font=('Arial', 18, 'bold'),
                    foreground='white',
                    background='blue', borderwidth=2, relief='solid')
label_a.grid(row=0, columnspan=2, padx=5, pady=5)

#IMAGEN SUBIR
# Convertir la imagen original a formato Tkinter PhotoImage
imagen_pillow = Image.open('abrir_carpeta.png')
# Redimensionar la imagen al tamaño deseado (350x350)
imagen_pillow = imagen_pillow.resize((350, 350))
imagen_tk = ImageTk.PhotoImage(imagen_pillow)

label_imagen = ttk.Label(frame)
label_imagen.grid(row=1, columnspan=2,padx=10, pady=10)
# Mostrar la imagen en el Frame
label_imagen.config(image=imagen_tk)
# Mantener una referencia para evitar que sea eliminada por el recolector de basura
label_imagen.image = imagen_tk

'''
# Crear una etiqueta para mostrar la imagen
label = tk.Label(root)
label.pack()

# Después de cerrar la ventana, puedes acceder a la ruta de la imagen en la variable 'image_path'
print("Ruta de la imagen seleccionada:", image_path)'''

# Botón para abrir la imagen
button_open = ttk.Button(frame, text="Abrir imagen", command=open_image)
button_open.grid(row=2, column=1, padx=5, pady=5)

# Etiquetas de seleccion
label_a = ttk.Label(frame, text="Operacion a realizar :", font=('Arial',10))
label_a.grid(row=3, column=0, padx=5, pady=5)

# Crear el Combobox con las opciones
opciones = ["Raiz",
            "Cuadrado",
            "Trazos"]
combobox = ttk.Combobox(frame, values=opciones, state="readonly")
combobox.set("Seleccion")  # Texto predeterminado en el Combobox
combobox.grid(row=3, column=1, padx=5, pady=5)

# Botón para aplicar la manipulación
button_manipulate = ttk.Button(frame, text="Mostrar imagen", command=manipulate_image)
button_manipulate.grid(row=4, column=0, padx=5, pady=5)

# Botón para cerrar la aplicacion
button_manipulate = ttk.Button(frame, text="Salir", command=cerrar_aplicacion)
button_manipulate.grid(row=4, column=1, padx=5, pady=10)

#Texto derechos reservados
label_texto = ttk.Label(frame, text="@Copright 2023 - Derechos reservados Valeriano - Zerpa", font=('Arial',7))
label_texto.grid(row=7, columnspan=2, padx=5, pady=10)

# Iniciar la aplicación
ventana.mainloop()

