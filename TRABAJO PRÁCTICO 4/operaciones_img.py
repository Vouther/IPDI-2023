import imageio as imageio
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image  # Importa el módulo Image de Pillow

# Normalizar los valores de RGB del pixel: dividir los valores 0 a 255 por 255
#para obtener valores en el rango de 0 a 1. (no se usa)
def normalize_rgb(img):
    return np.clip(img /255.,0.,1.)

#Convertir R’G’B’ a bytes y graficar el pixel
def RGB_to_bytes(img):
    image_rgb = (img*255).astype(int)
    return np.clip(image_rgb,0,255)

#Chequear que Y’ <= 1 (para que no se vaya de rango)
#Chequear -0.5957 < I’ < 0.5957 y -0.5226 < Q’ < 0.5226
def check_yiq(yiq):
    yiq[:, :, 0] = np.clip(yiq[:, :, 0], 0, 1)  # Asegura que Y' esté en [0, 1]
    yiq[:, :, 1] = np.clip(yiq[:, :, 1], -0.5957, 0.5957)# Asegura que I' esté en [-0.5957, 0.5957]
    yiq[:, :, 2] = np.clip(yiq[:, :, 2], -0.5226, 0.5226)# Asegura que Q' esté en [-0.5226, 0.5226]
    return yiq

def RGB_to_YIQ(rgb):
    yiq = np.zeros(rgb.shape)
    yiq[:, :, 0] = 0.229 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
    yiq[:, :, 1] = 0.595716 * rgb[:, :, 0] - 0.274453 * rgb[:, :, 1] - 0.321263 * rgb[:, :, 2]
    yiq[:, :, 2] = 0.211456 * rgb[:, :, 0] - 0.522591 * rgb[:, :, 1] + 0.311135 * rgb[:, :, 2]
    return yiq

def YIQ_to_RGB(yiq):
    rgb = np.zeros(yiq.shape)
    rgb[:, :, 0] = yiq[:, :, 0] + 0.9663 * yiq[:, :, 1] + 0.6210 * yiq[:, :, 2]
    rgb[:, :, 1] = yiq[:, :, 0] - 0.2721 * yiq[:, :, 1] - 0.6474 * yiq[:, :, 2]
    rgb[:, :, 2] = yiq[:, :, 0] - 1.1070 * yiq[:, :, 1] + 1.7046 * yiq[:, :, 2]
    return rgb

def igualar_dimensiones(image_1,image_2):
    # Obtenemos las dimensiones de ambas imágenes
    height1, width1, _ = image_1.shape
    height2, width2, _ = image_2.shape

    # Comparamos las dimensiones y redimensionamos si es necesario
    if height1 != height2 or width1 != width2:
        # Encontramos el tamaño máximo
        new_height = max(height1, height2)
        new_width = max(width1, width2)

        # Redimensionamos ambas imágenes al tamaño máximo con NumPy
        im1 = np.array(Image.fromarray(image_1).resize((new_width, new_height)))
        im2 = np.array(Image.fromarray(image_2).resize((new_width, new_height)))

    #print(im1.shape)
    #print(im2.shape)

    return im1,im2

#OPERACIONES EN EL ESPACIO RGB ************************************************

#SUMA CLAMPEADA EN EL ESPACIO RGB
def suma_clampeada_rgb(image_A,image_B):
    image_C = np.zeros(image_A.shape)
    image_C = image_A + image_B
    return image_C

#RESTA CLAMPEADA EN EL ESPACIO RGB
def resta_clampeada_rgb(image_A,image_B):
    image_C = np.zeros(image_A.shape)
    image_C = image_A - image_B
    return image_C

#SUMA PROMEDIADA EN EL ESPACIO RGB
def suma_promediada_rgb(image_A,image_B):
    image_C = np.zeros(image_A.shape)
    image_C = (image_A + image_B)/2
    return image_C

#RESTA CLAMPEADA EN EL ESPACIO RGB
def resta_promediada_rgb(image_A,image_B):
    image_C = np.zeros(image_A.shape)
    image_C = (image_A - image_B)/2
    return image_C

#OPERACIONES EN EL ESPACIO YIQ ***********************************************

# SUMA CLAMPEADA EN EL ESPACIO YIQ
# YC := YA + YB; If YC > 1 then YC:=1;
def suma_clampeada(A, B):
    s_clam = np.zeros(A[:, :, 0].shape)

    s_clam = A[:, :, 0] + B[:, :, 0]

    # If YC > 1 then YC:=1
    # print('Salida previa:',s_clam)
    s_clam[s_clam > 1] = 1
    # print('Salida modificada: ',s_clam)
    return s_clam


# RESTA CLAMPEADA EN EL ESPACIO YIQ
# YC := YA - YB; If YC < 0 then YC:=0;
def resta_clampeada(A, B):
    r_clam = np.zeros(A[:, :, 0].shape)

    r_clam = A[:, :, 0] - B[:, :, 0]

    # If YC < 0 then YC:=0
    # print('Luminansia previa:',r_clam)
    r_clam[r_clam < 0] = 0
    # print('Luminansia modificada: ',r_clam)
    return r_clam


# SUMA PROMEDIADA EN EL ESPACIO YIQ
# YC := (YA + YB) / 2;

def suma_promediada(A, B):
    s_prom = np.zeros(A[:, :, 0].shape)

    s_prom = (A[:, :, 0] + B[:, :, 0]) / 2

    return s_prom


# RESTA PROMEDIADA EN EL ESPACIO YIQ
# YC := (YA - YB) / 2;

def resta_promediada(A, B):
    r_prom = np.zeros(A[:, :, 0].shape)

    r_prom = (A[:, :, 0] - B[:, :, 0]) / 2

    return r_prom


def interpolacion(image_A, image_B):
    IC = np.zeros(image_A.shape)
    QC = np.zeros(image_A.shape)

    # IC := (YA * IA + YB * IB) / (YA + YB) ;
    IC = (image_A[:, :, 0] * image_A[:, :, 1] + image_B[:, :, 0] * image_B[:, :, 1]) / (
                image_A[:, :, 0] + image_B[:, :, 0])

    # QC := (YA * QA + YB * QB) / (YA + YB) ;
    QC = (image_A[:, :, 0] * image_A[:, :, 2] + image_B[:, :, 0] * image_B[:, :, 2]) / (
                image_A[:, :, 0] + image_B[:, :, 0])

    return IC, QC


# FUNCION IL_LIGTHER

# ifYA > YB then{YC := YA; IC := IA; QC := QA}
# else{YC := YB; IC := IB; QC := QB};

def if_lighter(image_A, image_B):
    # Extraer los componentes Y de las imágenes A y B
    YA = image_A[:, :, 0]
    IA = image_A[:, :, 1]
    QA = image_A[:, :, 2]

    YB = image_B[:, :, 0]
    IB = image_B[:, :, 1]
    QB = image_B[:, :, 2]

    # Inicializar las matrices de salida para Y, I y Q
    YC = np.zeros(YA.shape)
    IC = np.zeros(YA.shape)
    QC = np.zeros(YA.shape)
    image_C = np.zeros(image_A.shape)

    # Aplicar la operación if-lighter
    # ifYA > YB then{YC := YA; IC := IA; QC := QA}
    mask = YA > YB
    YC[mask] = YA[mask]
    IC[mask] = IA[mask]
    QC[mask] = QA[mask]

    mask = ~mask  # Negar la máscara para el caso opuesto
    # else{YC := YB; IC := IB; QC := QB};
    YC[mask] = YB[mask]
    IC[mask] = IB[mask]
    QC[mask] = QB[mask]

    # Combinar los componentes Y, I y Q en la imagen de salida
    # image_C = np.stack((YC, IC, QC), axis=-1)

    image_C[:, :, 0] = YC
    image_C[:, :, 1] = IC
    image_C[:, :, 2] = QC

    return image_C


# FUNCION IF_DARKER

def if_darker(image_A, image_B):
    # Extraer los componentes Y de las imágenes A y B
    YA = image_A[:, :, 0]
    IA = image_A[:, :, 1]
    QA = image_A[:, :, 2]

    YB = image_B[:, :, 0]
    IB = image_B[:, :, 1]
    QB = image_B[:, :, 2]

    # Inicializar las matrices de salida para Y, I y Q
    YC = np.zeros(YA.shape)
    IC = np.zeros(YA.shape)
    QC = np.zeros(YA.shape)

    # Aplicar la operación if-darker
    mask = YA < YB  # En lugar de YA > YB, ahora comparamos si YA es menor que YB
    YC[mask] = YA[mask]
    IC[mask] = IA[mask]
    QC[mask] = QA[mask]

    mask = ~mask  # Negar la máscara para el caso opuesto
    YC[mask] = YB[mask]
    IC[mask] = IB[mask]
    QC[mask] = QB[mask]

    # Combinar los componentes Y, I y Q en la imagen de salida
    image_C = np.stack((YC, IC, QC), axis=-1)

    return image_C

'''def mostrar_imagen(rgb, imagen):
    # Creamos una figura con dos subgráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))

    # Mostramos la imagen en el primer subgráfico
    ax1.imshow(imagen)
    ax1.set_title("Imágen Procesada")

    # Mostramos el histograma en el segundo subgráfico
    histogram, bins = np.histogram(rgb.flatten(), bins=10, range=(0, 1))
    ax2.bar(bins[:-1], histogram, width=0.1, align='center', alpha=0.7)
    ax2.set_title("Histograma")
    ax2.set_xlabel("Valor de píxel normalizado")
    ax2.set_ylabel("Frecuencia")
    ax2.set_xticks(bins[:-1])
    ax2.grid(True)

    # Ajustamos el espacio entre los subgráficos
    plt.tight_layout()

    # Mostramos la figura
    plt.show()'''

def mostrar_imagen(imagen):
    plt.imshow(imagen)
    plt.title("Imágen Procesada")
    plt.axis('off')
    plt.show()

def raiz_cuadrada(yiq):
    yiq[:, :, 0] = np.sqrt(yiq[:, :, 0])
    return yiq

def cuadratica(yiq):
    yiq[:, :, 0] = yiq[:, :, 0] * yiq[:, :, 0]
    return yiq

def lineal_a_tarzos(yiq,ymin,ymax):
    yiq[:, :, 0][yiq[:, :, 0] < ymin] = 0
    yiq[:, :, 0][yiq[:, :, 0] > ymax] = 1
    return yiq

#PROCESAMIENTO POR CONVOLUCION
def bartlett_kernel(size):
    if size % 2 == 0:
        raise ValueError("El tamaño del kernel debe ser impar.")

    kernel = np.zeros((size, size))
    mid = size // 2

    for x, y in np.ndindex((mid + 1, mid + 1)):
        kernel[x, y] = (y + 1) * (x + 1)

    kernel[:mid + 1, mid + 1:] = np.flip(kernel[:mid + 1, :mid], axis=1)
    kernel[mid + 1:, :] = np.flip(kernel[:mid, :], axis=0)

    return kernel
def gaussiano_kernel(dim):
    if dim <= 0:
        raise ValueError("La dimensión debe ser mayor que 0")

    ar = np.array([1])

    while len(ar) < dim:
        f = np.ones(len(ar) + 1)
        f[1:-1] = ar[:-1] + ar[1:]
        ar = f

    return ar.reshape(-1, 1) * ar

def laplaciano_kernel(v):
    kernel = None
    if v==4:
        kernel = np.zeros((3,3))
        kernel[1,:] = -1
        kernel[:,1] = -1
        kernel[1,1] = 4
    if v==8:
        kernel = np.ones((3,3))*(-1)
        kernel[1,1] = 8
    return kernel


def sobel_kernel(orientacion):
    f = np.array([1, 2, 1])
    kernel = np.zeros((3, 3))
    f_flat = f.flatten()  # Convertmos 'f' en un array unidimensional

    if orientacion == 'Oeste':
        kernel[:, 0] = f_flat * (-1)
        kernel[:, 2] = f_flat
    elif orientacion == 'Este':
        kernel[:, 0] = f_flat
        kernel[:, 2] = f_flat * (-1)
    elif orientacion == 'Norte':
        kernel[0, :] = f_flat * (-1)
        kernel[2, :] = f_flat
    else:
        kernel[0, :] = f_flat
        kernel[2, :] = f_flat * (-1)

    return kernel
