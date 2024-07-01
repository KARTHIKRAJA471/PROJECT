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

# Global threading events
video_control_event = threading.Event()
stop_flag = threading.Event()

def play_audio():    
    try:
        # Initialize pygame mixer
        pygame.mixer.init()

        # Load the audio file
        pygame.mixer.music.load('audio.mp3')

        # Play the audio file
        pygame.mixer.music.play()

        # Wait for audio playback to finish or for stop event
        while pygame.mixer.music.get_busy() and not stop_flag.is_set():
            pass

        # Stop the audio playback if the stop event is set
        pygame.mixer.music.stop()
    except Exception as e:
        print("Error:", e)

def play_video(video_control_event):
    # Open the video file
    cap = cv2.VideoCapture('video.mp4')

    # Check if the video file opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get the total number of frames and FPS of the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Create a window
    cv2.namedWindow('Video Player')

    # Loop to play the video
    while cap.isOpened():
        # Read a frame from the video
        ret, frame = cap.read()

        if ret:
            # Resize the frame
            frame = cv2.resize(frame, (1900, 900))

            # Display the frame
            cv2.imshow('Video Player', frame)

            # Get the current frame number
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

            key = cv2.waitKey(30)

            # Calculate the current time in seconds
            #current_time = current_frame / fps

            # Display current frame number and time
            #print(f"Frame: {current_frame}/{total_frames}, Time: {current_time:.2f}seconds", end='\r')

            # Check for key events
            if key & 0xFF == ord('p'):  # Pause or resume playback
                video_control_event.set()  # Set the event to pause the video
                cv2.waitKey(-1)
                video_control_event.clear()  # Clear the event after resuming

            elif key & 0xFF == ord('q'):  # Quit
                break

            # Check if stop event is set
            if stop_flag.is_set():
                break

        else:
            # End of video
           break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

def combined():
    thread1 = threading.Thread(target=play_audio)
    thread2 = threading.Thread(target=play_video, args=(video_control_event,))
    thread1.start()
    thread2.start()

def video():
    model  = load_model("model.h5")
    label = np.load("labels.npy")

    holistic = mp.solutions.holistic
    holis = holistic.Holistic()

    cap = cv2.VideoCapture(0)

    count = 0
    s = 0
    run = 0
    while True:
        lst = []
        ret, frm = cap.read()
        if ret:
            run = run+1
            if(run>10):
                stop_flag.set()
                break
            
                    
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
                run = 0

            if pred == "not focus":
                count = count+1
                if(count>10):
                    engine = pyttsx3.init()    
                    engine.say("you not focus on screen")
                    engine.runAndWait()
                    count = 0
                    s = s+1
                    
                if(s>3):
                    engine = pyttsx3.init()    
                    engine.say("you not properly attend class so today class over")
                    engine.runAndWait()   
                    stop_flag.set()  # Set the stop flag to stop audio and video
                    #mail() 
                    break
                    
            
            cv2.putText(frm, pred, (50,50),cv2.FONT_ITALIC, 1, (255,0,0),2)
        
        # Resize the frame to desired dimensions
        resized_frm = cv2.resize(frm, (200, 200))  # Change dimensions as needed
        cv2.imshow("window", resized_frm)

        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            cap.release()
            break

def combined_function():
    thread1 = threading.Thread(target=combined)
    thread2 = threading.Thread(target=video)
    thread1.start()
    thread2.start()
