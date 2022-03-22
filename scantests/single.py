import cv2
from pyzbar import pyzbar

im = cv2.imread("test2.jpg", cv2.IMREAD_GRAYSCALE)
ret, bw_im = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)

barcodes = pyzbar.decode(im)
#bw_im, symbols=[pyzbar.ZBarSymbol.CODE39]

for barcode in barcodes:
    print(barcode.type)
    print(barcode.data.decode("utf-8"))

cv2.imshow("img", bw_im)
cv2.waitKey(0)
cv2.destroyAllWindows()