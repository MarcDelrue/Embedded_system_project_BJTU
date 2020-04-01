# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import cv2

def search_qr_code():
	vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)
	found = False
	while found == False:
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
		barcodes = pyzbar.decode(frame)
		for barcode in barcodes:
			found = True
			barcodeData = barcode.data.decode("utf-8")
			vs.stop()
			return (barcodeData)
	vs.stop()