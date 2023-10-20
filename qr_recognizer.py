#!/usr/bin/python3
import cv2
import numpy as np
import os
import motorcortex
import time

qrCodeDetector = cv2.QRCodeDetector()

class QrRecognizer(object):
    def __init__(self):
        self.decoded_text = ""
        self.ip = "192.168.42.1"
        self.frame = "tracking_cam3"
        parameter_tree = motorcortex.ParameterTree()
        motorcortex_types = motorcortex.MessageTypes()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.req, self.sub = motorcortex.connect("ws://"+self.ip+":5558:5557", motorcortex_types, parameter_tree,
                                    certificate=dir_path+"/motorcortex.crt", timeout_ms=1000,
                                    login="root", password="12345")

        self.image_sub = self.sub.subscribe(["root/Comm_task/utilization_max","root/Processing/image"], "camera", 1)
        self.image_sub.get()
        self.image_sub.notify(self.onImage)

    
    def onImage(self, val):
        try:
            image = cv2.imdecode(np.frombuffer(val[1].value, np.uint8), cv2.COLOR_BGR2GRAY)
            self.decoded_text, points, _ = qrCodeDetector.detectAndDecode(image)
        except Exception as e:
            print(e)
        
        if points is not None:
            print(self.decoded_text)    
        else:
            print("QR not detected")


if __name__ == "__main__":
    qr_recognizer = QrRecognizer()
    while True:
        try:
            time.sleep(0)
        except KeyboardInterrupt as e:
            qr_recognizer.req.close()
            qr_recognizer.sub.close()
