import threading
import tkinter as tk
from tkinter import ttk
import cv2 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model 
import pyttsx3
import pygame
from mail import *
def video():
    model  = load_model("model.h5")
    label = np.load("labels.npy")

    holistic = mp.solutions.holistic
    holis = holistic.Holistic()

    cap = cv2.VideoCapture(0)

    a = 0
    s = 0
    z = 0
    while True:
        # Check if the VideoCapture object is still open
        #if not cap.isOpened():
            #print("Error: VideoCapture object is not open.")
            #break
        
        lst = []
        ret, frm = cap.read()
        if ret:
            z = z+1
            if(z>10):
                break
        #if not ret:
        #print("Error: Unable to read frame from VideoCapture.")
            #break
        print(z)    
        frm = cv2.flip(frm, 1)
        res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))    
        if res.face_landmarks:
            for i in res.face_landmarks.landmark:
                lst.append(i.x - res.face_landmarks.landmark[1].x)
                lst.append(i.y - res.face_landmarks.landmark[1].y)
            if res.left_hand_landmarks:
                for i in res.left_hand_landmarks.landmark:
                    lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
                    lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
            else:
                for i in range(42):
                    lst.append(0.0)

            if res.right_hand_landmarks:
                for i in res.right_hand_landmarks.landmark:
                    lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
                    lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
            else:
                for i in range(42):
                    lst.append(0.0)

            lst = np.array(lst).reshape(1,-1)
            pred = label[np.argmax(model.predict(lst))]
            
            if pred:
                z = 0

            if pred == "you not focus":
                a=a+1
                if(a>10):
                    engine = pyttsx3.init()    
                    engine.say("santhosh you not focus on screen")
                    engine.runAndWait()
                    print(a)
                    a = 0
                    s = s+1
                    
                if(s>3):
                    engine = pyttsx3.init()    
                    engine.say("you not properly attend class so today class over")
                    engine.runAndWait() 
                    #mail()   
                    stop_flag.set()  # Set the stop flag to stop audio and video
                    break
                    
            
            cv2.putText(frm, pred, (50,50),cv2.FONT_ITALIC, 1, (255,0,0),2)
        
        # Resize the frame to desired dimensions
        resized_frm = cv2.resize(frm, (200, 200))  # Change dimensions as needed
        cv2.imshow("window", resized_frm)

        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            cap.release()
            break


video()