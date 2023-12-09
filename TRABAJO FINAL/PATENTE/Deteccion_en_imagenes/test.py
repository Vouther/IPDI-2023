import cv2
import LPR
import matplotlib.pyplot as plt

lpr = LPR.LPR()
plates = ["AA757PV", "AD030NV", "AE056RO", "AB712KE", "AA659IL",
          "AD719OA", "AC369ED", "AA275KH", "AG291XM", "AE114MX",
          "AE956VK", "AA462ZV", "AA022HK", "AD426NC"]

for i in range(14):
    img = cv2.imread(f"./imgs/{i:03}.png")
    cv2.imshow(f"Image {i}", img)
    cv2.waitKey(0)  # Espera hasta que una tecla sea presionada
    cv2.destroyAllWindows()  # Cierra todas las ventanas abiertas

    txt = lpr.read_license(img)
    if txt[:-1] == plates[i]:
        print(f"{i:03} OK")
    else:
        print(f"{i:03} ERROR | Original: {plates[i]}",
              f"Recognized: {txt}")

