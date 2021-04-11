############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import serial
import playsound
from PIL import ImageFont
from PIL import ImageDraw
import codecs
from sendmysql import insertmysql

ser = serial.Serial('com3',baudrate = 115200, timeout=1)
############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

##################################################################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

###################################################################################

def contact():
    mess._show(title='ติดต่อ', message="หากมีปัญหา ติดต่อที่เบอร์ 01-23456789 ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='หาไฟล์เปรียบเทียบใบหน้าไม่เจอ', message='กรุณาติดต่อที่เบอร์ 01-23456789')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('ไม่พบรหัสผ่านเก่า', 'โปรดป้อนรหัสผ่านใหม่ด้านล่าง', show='*')
        if new_pas == None:
            mess._show(title='ไม่ได้ใส่รหัสผ่าน', message='ยังไม่ได้กำหนดรหัสผ่าน!! กรุณาใส่ใหม่')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='รหัสผ่านลงทะเบียน', message='ลงทะเบียนรหัสผ่านใหม่เรียบร้อยแล้ว !!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='ผิดพลาด', message='ยืนยันรหัสผ่านใหม่อีกครั้ง !!!')
            return
    else:
        mess._show(title='รหัสผ่านผิด', message='กรุณากรอกรหัสผ่านเดิมให้ถูกต้อง')
        return
    mess._show(title='เปลี่ยนรหัสผ่านแล้ว', message='เปลี่ยนรหัสผ่านเรียบร้อย !!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("เปลี่ยนรหัสผ่าน")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    ใส่รหัสเก่า',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   ใส่รหัสผ่านใหม่', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='ใส่รหัสผ่านใหม่', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="ยกเลิก", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="บันทึก", command=save_pass, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('ไม่พบรหัสผ่านเก่า', 'โปรดป้อนรหัสผ่านใหม่ด้านล่าง', show='*')
        if new_pas == None:
            mess._show(title='ไม่ได้ใส่รหัสผ่าน', message='ไม่ได้ตั้งรหัสผ่าน !! กรุณาลองอีกครั้ง')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='ลงทะเบียนรหัสผ่าน', message='ลงทะเบียนรหัสผ่านใหม่เรียบร้อยแล้ว !!')
            return
    password = tsd.askstring('รหัสผ่าน', 'ใส่รหัสผ่าน', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='รหัสผ่านผิด', message='คุณป้อนรหัสผ่านผิด')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)ถ่ายรูป  >>>  2)บันทึกข้อมูล"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)ถ่ายรูป  >>>  2)บันทึกข้อมูล"
    message1.configure(text=res)

#######################################################################################

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    
    exists = os.path.isfile("StudentDetails\StudentDetails.csv", )
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r', encoding = "cp874") as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+', encoding = "cp874") as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())   
    if ((Id.isalnum()) or (' ' in Id)):
        cam = cv2.VideoCapture(0)
       
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()            
            start_time = time.time()        

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.05, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                # display the frame
                fpsInfo = "FPS: " + str(1.0 / (time.time() - start_time)) 
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(img, fpsInfo, (10, 20), font, 0.4, (255, 255, 255), 1)
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()


        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+', encoding = "cp874") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "ใส่ชื่อ"
            print("ใส่ชื่อ")
            message.configure(text=res)

########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='ไม่มีการลงทะเบียน', message='กรุณาลงทะเบียนก่อน !!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "บันทึกสำเร็จแล้ว"
    message1.configure(text=res)
    message.configure(text='การลงทะเบียนทั้งหมดจนถึงขณะนี้  : ' + str(ID[0]))

############################################################################################3

def getImagesAndLabels(path):    
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

def TrackImages():
  
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    #startTime = 0
    waiting2s  = False
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='ไม่มีข้อมูล', message='กรุณาคลิกที่บันทึกข้อมูลเพื่อเพิ่มข้อมูล!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time', '', 'temp']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv") 
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv", encoding = "cp874") #, encoding = "ISO-8859-1", engine='python')
    else:
        mess._show(title='ไม่มีรายละเอียด', message='ไม่มีรายละเอียดข้อมูลโปรดตรวจสอบ!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        None
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)            
        csvFile1.close()
    
    while True:

        #timenow = time.time()
        if(waiting2s == True):
            time.sleep(2)
            waiting2s = False
        #ลูปการทำงานกล้อง
        ret, im = cam.read()

        start_time = time.time()
        #if (nowTime - startTime) > 0.01:
        
          
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.05, 5,minSize=(20, 20))
        for (x, y, w, h) in faces: 
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
               
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    
            if (conf < 50):     
                print(conf)  
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                
                arduinoData = ser.read(ser.in_waiting).decode('ascii')  
                print(arduinoData)  
                if (arduinoData == '5'):                                  
                    TEMP = getValuestemp()
                    font1 = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(im,TEMP,(x, y-10), font1, 1, (255, 255, 255), 3) 
                    waiting2s = True
                    time2s = time.time()
                    attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp), '', str(TEMP)]
                    sendexcal(attendance) 
                    insertmysql(id_human=str(ID), name=bb, date=str(date), time=str(timeStamp), temp=str(TEMP))
                    try:
                        TEMP1 = float(TEMP)
                    except:
                        playsound.playsound('noscan.mp3', True)
                    else:                        
                        sound(TEMP1)                                                     
                                         
            else:
                print(conf)
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timeStamp1 = datetime.datetime.fromtimestamp(ts).strftime('%H-%M-%S')
                ID = '000000'
                ID = ID[1:-1]  
                bb = 'ไม่รู้จัก'  
                                                                
                arduinoData = ser.read(ser.in_waiting).decode('ascii')    
                if (arduinoData == '5'): 
                    waiting2s = True
                    time2s = time.time() 
                    TEMP = getValuestemp()
                    font1 = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(im,TEMP,(x, y-10), font1, 1, (255, 255, 255), 3) 
                    cv2.imwrite("unknown\ " + str(date) + "." + str(timeStamp1) + "." + TEMP + ".jpg", gray[y:y + h, x:x + w])
                                                                                    
                    attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp),'', str(TEMP)]
                    sendexcal(attendance)
                    try:
                        TEMP1 = float(TEMP)
                    except:
                        playsound.playsound('noscan.mp3', True)
                    else:                        
                        sound(TEMP1)   
                                          
            #font1 = cv2.FONT_HERSHEY_SIMPLEX
            #cv2.putText(im,"36.8",(x, y-10), font1, 1, (255, 255, 255), 3)            
            print(bb)
            fontpath = "./angsau_0.ttf" 
            font = ImageFont.truetype(fontpath, 32)
            img_pil = Image.fromarray(im)
            draw = ImageDraw.Draw(img_pil)
            draw.text((x, y + h), bb, font = font, fill = (255, 255, 255))
            im = np.array(img_pil)
            
        fpsInfo = "FPS: " + str(1.0 / (time.time() - start_time)) 
        font = cv2.FONT_HERSHEY_DUPLEX
                   
      
 
        cv2.putText(im, fpsInfo, (10, 20), font, 0.4, (255, 255, 255), 1)
        startTime = time.time()   
       
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break 
        #จบลุปการทำงานของกล้อง
    
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '                                
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6]), str(lines[8])))                         
    csvFile1.close()
    
    cam.release()
    cv2.destroyAllWindows()   
    
   
#######################################sound####################################################
def sound(TEMP1):
    if (TEMP1 < 37.5):        
        playsound.playsound('yes.mp3' , True)
    else:               
        playsound.playsound('no.mp3', True)
    return

########################################serial.Serial############################################
def getValuestemp():
    ser.write(b'g')
    arduinoDataTemp = ser.readline().decode('ascii')
    return arduinoDataTemp

######################################## SEND EXCAL #############################################
def sendexcal(attendance):
    print(attendance)
    #col_names = ['Id', '', 'Name', '', 'Date', '', 'Time', '', 'temp']
    #i = 0
    #j = 0
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    """
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '                                
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6]), str(lines[8])))                         
    csvFile1.close()
    """
    return
######################################## USED STUFFS ############################################

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'มกราคม',
      '02':'กุมภาพันธ์',
      '03':'มีนาคม',
      '04':'เมษายน',
      '05':'พฤษภาคม',
      '06':'มิถุนายน',
      '07':'กรกฎาคม',
      '08':'สิงหาคม',
      '09':'กันยายน',
      '10':'ตุลาคม',
      '11':'พฤศจิกายน',
      '12':'ธันวาคม'
      }

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("โปรแกรมเช็คชื่อ ด้วยใบหน้า")
window.configure(background='#262523')

frame1 = tk.Frame(window, bg="#708090")
frame1.place(relx=0.30, rely=0.17, relwidth=0.39, relheight=0.80)

#frame2 = tk.Frame(window, bg="#00aeff")
#frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="โปรแกรมเช็คชื่อ ด้วยใบหน้า" ,fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text = " "+day+" "+mont[month]+" "+year+"  |  ", fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 20, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
clock.pack(fill='both',expand=1)
tick()

#head2 = tk.Label(frame2, text="                        ลงทะเบียนใบหน้า                             ", fg="black",bg="#3ece48" ,font=('times', 17, ' bold ') )
#head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                              แสดงรายการ                               ", fg="black",bg="#00FF00" ,font=('times', 17, ' bold ') )
head1.place(x=0,y=0)

#lbl = tk.Label(frame2, text="รหัส",width=20  ,height=1  ,fg="black"  ,bg="#00aeff" ,font=('times', 17, ' bold ') )
#lbl.place(x=80, y=55)

#txt = tk.Entry(frame2,width=32 ,fg="black",font=('./angsau_0', 15, ' bold '))
#txt.place(x=30, y=88)

#lbl2 = tk.Label(frame2, text="ชื่อ นามสกุล",width=20  ,fg="black"  ,bg="#00aeff" ,font=('times', 17, ' bold '))
#lbl2.place(x=80, y=140)

#txt2 = tk.Entry(frame2, width=32 ,fg="black",font=('Courier', 15, ' bold ')  )
#txt2.place(x=30, y=173)

#message1 = tk.Label(frame2, text="1)ถ่ายรูป  >>>  2)บันทึกข้อมูล" ,bg="#00aeff" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
#message1.place(x=7, y=230)

#message = tk.Label(frame2, text="" ,bg="#00aeff" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
#message.place(x=7, y=450)

#lbl3 = tk.Label(frame1, text="ข้อมูล",width=20  ,fg="black"  ,bg="#00aeff"  ,height=1 ,font=('times', 17, ' bold '))
#lbl3.place(x=100, y=115)



res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2)
    csvFile1.close()
else:
    res = 0
#message.configure(text='จำนวนข้อมูลที่บันทึก  : '+str(res))

##################### MENUBAR #################################

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='เปลี่ยนรหัส', command = change_pass)
filemenu.add_command(label='ติดต่อ', command = contact)
filemenu.add_command(label='ออก',command = window.destroy)
menubar.add_cascade(label='ตั้งค่า',font=('times', 29, ' bold '),menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time','temp'))
tv.column('#0',width=75)
tv.column('name',width=110)
tv.column('date',width=110)
tv.column('time',width=110)
tv.column('temp',width=71)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='รหัส')
tv.heading('name',text ='ชื่อ')
tv.heading('date',text ='วันที่')
tv.heading('time',text ='เวลา')
tv.heading('temp',text ='อุณหภูมิ')


###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

#clearButton = tk.Button(frame2, text="ลบ", command=clear  ,fg="black"  ,bg="#ea2a2a"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
#clearButton.place(x=335, y=86)
#clearButton2 = tk.Button(frame2, text="ลบ", command=clear2  ,fg="black"  ,bg="#ea2a2a"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
#clearButton2.place(x=335, y=172)    
#takeImg = tk.Button(frame2, text="ถ่ายรูป", command=TakeImages  ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
#takeImg.place(x=30, y=300)
#trainImg = tk.Button(frame2, text="บันทึกข้อมูล", command=psw ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
#trainImg.place(x=30, y=380)
trackImg = tk.Button(frame1, text="เปิดกล้อง", command=TrackImages  ,fg="black"  ,bg="#FFFF00"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=30,y=50)
quitWindow = tk.Button(frame1, text="ออกจากโปรแกรม", command=window.destroy  ,fg="black"  ,bg="red"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=30, y=450)

##################### END ######################################

window.configure(menu=menubar)
window.mainloop()

####################################################################################################
