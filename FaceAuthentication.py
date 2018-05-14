#!/usr/bin/python
"""
@author: anwar
"""

from collections import namedtuple
import cv2
import os
import cPickle
import time

UserName = namedtuple("UserName", ["trains", "names"])


class FaceAuthentication:
    def __init__(self, recognition, trains=False, names=None):
        self.recognition = recognition
        self.names = names
        self.trains = trains

    def defindStart(self, defindStart):
        self.recognition.setDouble("threshold", defindStart)

    def newOrUpdateTrain(self, info, names):
        if not self.trains:
            self.recognition.train(info, names)
            self.trains = True
            return
        self.recognition.update(info, names)

    def defindNames(self, names):
        self.names = names

    def tellNames(self, face):
        tell, confirm = self.recognition.predict(face)
        # tell < confirm,
        # tell how many person recognize then count but it is -1 if there is unknown person
        # disabled how many person when they are recognized because my goal is for detect only
        # the unknown person.

        if tell == -1 :
            #if confirm < 25:
            return ("Unauthorized", 0)

        return (self.names[tell], confirm)

    def saveInfo(self, db):
        addUser = UserName(trains=self.trains, names=self.names)
        if not os.path.exists(db + "/rating.facesDB"):
            f = open(db + "/rating.facesDB", "w")
            f.close()
        self.recognition.save(db + "/rating.facesDB")
        f = open(db + "/file.cppDump", "w")
        f.write(cPickle.dumps(addUser))
        f.close()

    @staticmethod
    def load(db):
        addUser = cPickle.loads(open(db + "/file.cppDump").read())
        recognition = cv2.createLBPHFaceRecognizer()
        recognition.load(db + "/rating.facesDB")
        return FaceAuthentication(recognition, trains=addUser.trains, names=addUser.names)
