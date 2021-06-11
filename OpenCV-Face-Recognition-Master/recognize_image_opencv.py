import cv2
import os
import time
import sqlite3
import spreadsheet
import spreadsheet_lab

def recognize(subject):
    face_dict = {}
    end_time = time.time()+10
    cascade_path = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
    #faceCascade = cv2.CascadeClassifier(cascade_path)
    cap = cv2.VideoCapture(0)
    date = time.strftime("%d.%m.%Y")
    path = './pics_taken/' + date
    if not os.path.exists(path):
        os.makedirs(path)

    def getProfile(id):
        connect = sqlite3.connect("Face-DataBase")
        cmd = "SELECT * FROM Students WHERE ID=" + str(id)
        cursor = connect.execute(cmd)
        profile = None
        for row in cursor:
            profile = row
        connect.close()
        return profile

    rec = cv2.face.LBPHFaceRecognizer_create()                                           # Local Binary Patterns Histograms
    rec.read('./recognizer/trainingData.yml')                                       # loading the trained data
    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = 2
    fontColor = (0, 255, 0)         # the font of text on face recognition

    # make an array of all the students in the database initialied as zero
    picNum = 2

    while time.time()<end_time:
        #ret, img = cap.read()
        img = cv2.imread('TestCollage.PNG')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                # converting the camera input into GrayScale
        faces = cascade_path.detectMultiScale(
                                    gray,
                                    scaleFactor=1.1,
                                    minNeighbors=5,
                                    minSize=(20, 20)
                                    )
        totalConf = 0.0
        faceRec = 0
        for (x, y, w, h) in faces:
            id, conf = rec.predict(gray[y:y+h, x:x+w])
            if conf < 100:
                totalConf += conf
                faceRec += 1
                profile = getProfile(id)
                if profile is not None:
                    cv2.putText(img,
                                profile[1] + str("(%.2f)" % conf),
                                (x, y+h),
                                font, fontScale, fontColor,2)  # Writing the name of the face recognized
            else:
                cv2.putText(img,
                            "Unknown",
                            (x, y+h),
                            font, fontScale, fontColor,2)                                               # Writing the name of the face recognized

            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 1)
            cv2.imshow('frame', img)
            cv2.waitKey(3)      # Showing each frame on the window
            cv2.imwrite(path + '/pic' + str(picNum) + '.jpg', img)
            detectPrint = " %d face detected" % len(faces)
            if faceRec != 0:
                print(detectPrint + " and ", faceRec, " face recognized with confidence %.2f"%(totalConf / faceRec))
                face_dict[profile[1]] = 1
            else:
                print(detectPrint + " and 0 faces recognized")
    #cap.release()
    #print(face_dict)
    if subject[-2:] == "B1" or subject[-2:] == "B2" :
        spreadsheet_lab.create_excel(face_dict, subject)
    else:
        spreadsheet.create_excel(face_dict,subject)
    cv2.destroyAllWindows()                                                         # Closing all the opened windows
