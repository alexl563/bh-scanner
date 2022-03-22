from base64 import decode
import cv2
from pyzbar import pyzbar

#turn on the camera
cap = cv2.VideoCapture(0)
cap.set(3, 640) #width
cap.set(4, 480) #height

camera = True

#initializing some lists for students
#id_numbers = []
#students_status = dict.fromkeys(id_numbers, 0)

barcodes_scanned = []

while camera == True:
	success, frame = cap.read()

	#data preprocessing
	new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret, bw_frame = cv2.threshold(new_frame, 127, 255, cv2.THRESH_BINARY)
	decoded_frame = pyzbar.decode(frame)
	#bw_frame, symbols=[pyzbar.ZBarSymbol.CODE39]

	for code in decoded_frame:
		data_decoded = code.data.decode("utf-8")

		if data_decoded in barcodes_scanned:
			print("barcode already scanned")
		
		else:
			print(code.type)
			print(data_decoded)
			barcodes_scanned.append(data_decoded)


		(x, y, w, h) = code.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
	
	cv2.imshow("image", bw_frame)
	cv2.waitKey(1)
	cv2.destroyAllWindows()





""" 
image_path = "IMG_2593.JPG"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# preprocessing using opencv
im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
blur = cv2.GaussianBlur(im, (5, 5), 0)
ret, bw_im = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# zbar

detectedBarcodes = pyzbar.decode(bw_im, symbols=[pyzbar.ZBarSymbol.QRCODE])

 """

