import numpy as np
import cv2
import pytesseract
import skimage

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


class LPR:
    def __init__(self, min_w=60, max_w=140, min_h=20, max_h=60, ratio=3.07692307692):
        self.min_w = min_w
        self.max_w = max_w
        self.min_h = min_h
        self.max_h = max_h
        self.ratio = ratio

    '''
    los valores de min_w, max_w, min_h y max_h en la clase LPR deben interpretarse como distancias
    entre los puntos de los píxeles en la imagen. Estos valores determinan los límites permitidos
    para el ancho y el alto de los rectángulos de contorno que se están buscando en la detección de la patente.

    min_w y max_w: Representan el ancho mínimo y máximo permitido del rectángulo en píxeles.
    min_h y max_h: Representan la altura mínima y máxima permitida del rectángulo en píxeles.
    '''

    def grayscale(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def apply_threshold(self, img):
        return cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)[1]

    def apply_adaptive_threshold(self, img):
        return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 13)

    def find_contours(self, img):
        return cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

    def filter_candidates(self, contours):

        # Filtra contornos basados en área
        contours = [cnt for cnt in contours if 1000 < cv2.contourArea(cnt) < 5500]

        # Inicializa una lista para almacenar los contornos rectangulares aproximados
        rectangular_contours = []

        for cnt in contours:
            # Aproxima el contorno a un polígono
            epsilon = 0.03 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            x, y, w, h = cv2.boundingRect(cnt)

            # Verifica si el polígono tiene cuatro esquinas (es aproximadamente rectangular)
            # Tambien se verifica el ancho (with)
            if len(approx) == 4 and (69 <= w <= 130) and (16 <= h <= 50):
                # Si se corresponde a una patente nueva
                rectangular_contours.append(approx)
            elif len(approx) == 4 and (48 <= w <= 70) and (20 <= h <= 30):
                # Si se corresponde a una patente vieja
                rectangular_contours.append(approx)

        return rectangular_contours

    def get_lowest_candidate(self, candidates):
        ys = []
        for cnt in candidates:
            x, y, w, h = cv2.boundingRect(cnt)
            ys.append(y)
        return candidates[np.argmax(ys)]

    # AQUI COMENZAMOS A TRATAR LA ZONA DE LA PATEMTE
    def crop_license_plate(self, img, license):
        x, y, w, h = cv2.boundingRect(license)
        return img[y:y + h, x:x + w]

    def clear_border(self, img):
        return skimage.segmentation.clear_border(img)

    def invert_image(self, img):
        return cv2.bitwise_not(img)

    def view_result(self, img):
        cv2.imshow(f"Resultado", img)
        cv2.waitKey(0)  # Espera hasta que una tecla sea presionada
        cv2.destroyAllWindows()  # Cierra todas las ventanas abiertas

    def read_license(self, img, psm=7):
        # Suponemos que debe encontrar 7 caracteres
        alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        options = "-c tessedit_char_whitelist={}".format(alphanumeric)
        options += " --psm {}".format(psm)

        gray = self.grayscale(img)
        thresh = self.apply_threshold(gray)
        contours = self.find_contours(thresh)
        candidates = self.filter_candidates(contours)

        if candidates:
            license = candidates[0]

            if len(candidates) >= 1:
                # Si detecto los contornos con el umbral
                license = self.get_lowest_candidate(candidates)
            else:
                #Sino se aplica un umbral adaptativo
                thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 7)
                contours = self.find_contours(thresh)
                candidates = self.filter_candidates(contours)
                license = self.get_lowest_candidate(candidates)

            cropped = self.crop_license_plate(gray, license)
            thresh_cropped = self.apply_adaptive_threshold(cropped)
            clear_border = self.clear_border(thresh_cropped)
            final = self.invert_image(clear_border)
            txt = pytesseract.image_to_string(final, config=options)

            return txt
        else:
            return "NoReading"