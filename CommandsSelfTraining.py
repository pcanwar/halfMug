#!/usr/bin/python
'''
@author: anwar
'''
from __future__ import print_function
from FaceAuthentication import FaceAuthentication
from imutils import encodings
import numpy as np
import random
import glob
import re
import subprocess
import cv2
import imutils

class Commands(object):
    def __init__(self):#, userName):
        #self.userName = userName
        self.commandersSwitch = {"quit": None, "help": self.printHelp, "adduser": self.addUser, "clear":self.clearing, "save":self.saveUser}

    def processes(self, command):
        '''Process each command line from user input
        '''
        command = command.strip()
        arr = re.split('\s+', command, 1)
        commandName = arr[0]
        if not commandName in self.commandersSwitch.keys():
            print ("{0} is not a valid command, please try again.".format(commandName))
            return True
        if (commandName == "quit"):
            return False
        else:
            self.doWork(commandName, arr[1:])
            return True

    def doWork(self, commandName, arguments):
        '''Do real work, i.e. add, save, delete, ..
        '''
        f = self.commandersSwitch[commandName]
        if not commandName in ['help', 'clear', 'save'] and len(arguments) == 0:
            print ("{0} must have one argument.".format(commandName))
            return
        f(arguments)

    def addUser(self, arguments):
        self.fileName = ''.join(arguments)
        faceDetecting = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        captureMode = False
        color = (200, 0, 0)
        camera = cv2.VideoCapture(0)
        f = open("authrizedUser/usersFaces/" + self.fileName + '.txt', 'a')
        total = 0

        while True:
            (cap, frame) = camera.read()
            if not cap:
                break

            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faceDetection = faceDetecting.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=8,
                                                           minSize=(100, 100))  # , flags=cv2.CASCADE_SCALE_IMAGE)
            # if detecting one face
            # print (len(faceDetection))
            # if len(faceDetection) < 1:
            #   print "It is only detect one face, try again with clear backgrond"
            # elif len(faceDetection) == 1:
            if len(faceDetection) > 0:
                (x, y, w, h) = max(faceDetection, key=lambda v: (v[2] * v[3]))
                if captureMode:
                    face = gray[y:y + h, x:x + w].copy(order="C")
                    f.write("{}\n".format(encodings.base64_encode_image(face)))
                    total += 1
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

                # show the frame and record if the user presses a key
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF

                # press w to capture mode
                if key == ord("w"):
                    # if we are not already in capture mode, drop into capture mode
                    if not captureMode:
                        captureMode = True
                        color = (0, 150, 100)

                    # otherwise, back out of capture mode
                    else:
                        captureMode = False
                        color = (150, 0, 150)
                elif key == ord("q"):
                    break

        # close the output file, clean up the camera, and close any open windows
        print("There are {} frames in your file".format(total))
        f.close()
        camera.release()
        cv2.destroyAllWindows()

    def clearing(self,arguments):
        subprocess.call("clear")


    def printHelp(self, arguments):
        print ("""
    help - Print this help information
    quit - Quit this system
    clear - Clear the terminal screen
    adduser username - Add a user to your system
    save - to save any change of users on your system

    """)

    def saveUser(self, arguments ):
        beginRecognizing = FaceAuthentication(cv2.createLBPHFaceRecognizer(radius=1, neighbors=8, grid_x=8, grid_y=8))
        userName = []
        print('Completed training for users:')
        for faceDBfile, path in enumerate(glob.glob("authrizedUser/usersFaces/" + "/*.txt")):
            names = path[path.rfind("/") + 1:].replace(".txt", "")
            print("{0} account".format(names))
            userAccount = open(path).read().strip().split("\n")
            userAccount = random.sample(userAccount, min(len(userAccount), 100))
            faces = []
            for face in userAccount:
                faces.append(encodings.base64_decode_image(face))
            beginRecognizing.newOrUpdateTrain(faces, np.array([faceDBfile] * len(faces)))
            userName.append(names)
        beginRecognizing.defindNames(userName)
        beginRecognizing.saveInfo("authrizedUser/hushFaces/")
