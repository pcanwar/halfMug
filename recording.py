#!/usr/bin/python
'''
@author: anwar
'''
from __future__ import print_function
import FaceAuthentication
import cv2
import numpy as np
import imutils
import time
import datetime
import smtplib
import time
import sendMessage 

class Record(object):
    def recordingCam(self):
        c1 =0
#from messages.sendMessage import SendMessage
        frontFaceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faceRegnitionInfo= FaceAuthentication.FaceAuthentication.load("authrizedUser/hushFaces")
        faceRegnitionInfo.defindStart(100)

        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise IOError("cannot open the camear")
        color = (0, 100, 200)
        lastSent = None
        faceNono = None
        while True:
            cap, frame = camera.read()
            if not cap:
                break
            intruder = False
            frame = imutils.resize(frame, width=500)
            #flipFace = cv2.flip(frame, 1, 0)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            overFaces = frontFaceCascade.detectMultiScale(gray,
                    scaleFactor=1.2, # when faces are closer to the camera, they appears bigger than those faces in the back.
                    minNeighbors=5,   # minNeighbors defines how many objects are detected near the current
                    minSize=(100, 100),  # one before it declares the face found.
                    # minSize, meanwhile, gives the size of each window.
                    )

            #timestamp = datetime.datetime.now()
            #ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            #cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                      #  0.35, (0, 0, 255), 1)

            for (faceFile,(fx,fy,fw,fh)) in enumerate(overFaces):

                displayFace = gray[fy:fy +fh, fx:fx+fw]
                tell, confirm = faceRegnitionInfo.tellNames(displayFace)
                if faceNono is None:
                    faceNono = [tell, 1]
                    color = (0, 0, 0)

                elif tell == faceNono[0]:
                    faceNono[1] += 1
                if faceNono[0] == "Unauthorized"  and faceNono[1] >= 30:
                    #sImage= np.vectorize(saveImageName)
                    #cv2.imread(sImage, frame)
                    color = (100, 90, 0)
                    intruder = True
                    #frameFace = frame.copy()

                tell=  "{}: {:.2f}".format(tell, confirm)
                cv2.putText(frame, tell, (fx,fy -20), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                cv2.rectangle(frame, (fx, fy), (fx+fw, fy+fh), color, 2)
                if intruder : #or (timestamp - lastSent).seconds >= 2:
                    saveImageName = time.strftime("%c") + '.jpg'
                    #cv2.imwrite(saveImageName, frame)

                    sendMessage.sendMessages(frame)

            cv2.imshow("Recording", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        camera.release()
        cv2.destroyAllWindows()



run1 =Record()
run1.recordingCam()
