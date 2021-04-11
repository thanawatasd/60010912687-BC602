
import cv2,os
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time 
process_this_frame = True



recognizer = cv2.face.LBPHFaceRecognizer_create()  
os.path.isfile("TrainingImageLabel\Trainner.yml")
recognizer.read("TrainingImageLabel\Trainner.yml")
harcascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(harcascadePath);

cam = cv2.VideoCapture(0) 
#waitframe = 10
#cam.set(cv2.CAP_PROP_FPS, 10)
prev_frame_time = 0
new_frame_time = 0
fps1 = 0
fpsLimit = 1 # throttle limit
startTime = time.time()
cv = cv2.VideoCapture(0)
col_names = ['Id', '', 'Name', '', 'Date', '', 'Time', '', 'temp']
exists1 = os.path.isfile("StudentDetails\StudentDetails.csv") 
if exists1:
    df = pd.read_csv("StudentDetails\StudentDetails.csv")
while True:
    
    ret, im = cam.read()
    font = cv2.FONT_HERSHEY_SIMPLEX   
    """
    new_frame_time = time.time()
    fps = 0.6/(new_frame_time-prev_frame_time)         
    prev_frame_time = new_frame_time 
    #fps1 = fps
         
    fps = int(fps)        
    fps = str(fps)
    print(fps) 
    """
    nowTime = time.time()
    if (nowTime - startTime) > 0.06:
      

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
        font = cv2.FONT_HERSHEY_SIMPLEX 
    

        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
    
            
        for (x, y, w, h) in faces: 
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
        
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):   
                #print(conf)    
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values    
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]         
            else:
                #print(conf) 
                Id = 'Unknown'
                #bb = str(Id)   
            startTime = time.time()          
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
            #cv2.putText(gray, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 
            
        cv2.imshow('Program', im)
        if (cv2.waitKey(1) == ord('q')):
            break
        
