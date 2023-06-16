# import library yang digunakan
import cv2
import serial
import time
from datetime import datetime
import mysql.connector

# deklarasi komunikasi serial di COM dan baudrate
konter = 0
serialcomm = serial.Serial('/dev/ttyACM0', 9600)
serialcomm.timeout = 1

# klasifikasi wajah dan mulut dengan metode haarcascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
cap = cv2.VideoCapture(0)

# mengkoneksikan python ke mysql
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dbmasker",
    # auth_plugin="mysql_native_password"
)
# kursor untuk akses di database mysql
mycursor = mydb.cursor()
# format menambahkan data ke database mysql
sqlstuff = "INSERT INTO data_masker (No, Tanggal, Jam, Suhu, Ket_Masker) VALUES (%s, %s, %s, %s, %s)"
white_color = (255, 0, 0)
red_color = (0, 0, 255)
while True:
    # membaca dari serial arduino yang diterima
    serialread = serialcomm.readline().decode('ascii')

    _, img = cap.read()
    # konversi gambar ke gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # variabel untuk klasifikasi yang digunakan
    faces = face_cascade.detectMultiScale(gray, 1.2, 6)
    mouth = mouth_cascade.detectMultiScale(gray, 1.5, 9)
    # jika terdeteksi maka menampilkan persegi pada wajah / mulut
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    for (x, y, w, h) in mouth:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    # jika terdapat / tidak wajah dan mulut serta keterangannya, mengirim data ke serial
    if (len(faces) == 1 and len(mouth) == 0):
        cv2.putText(img, 'Wajah', (50, 50), font, 1, (0, 255, 0), 2, cv2.LINE_4)
        cv2.putText(img, "Menggunakan Masker (ya)", (50, 80), font, 1, (0, 255, 0), 2, cv2.LINE_4)
        if(float(serialread)  <=26):
            cv2.putText(img, "suhu normal "+serialread+" (ya)", (50, 120), font, 1, (0, 255, 0), 2, cv2.LINE_4)
            cv2.putText(img, "pintu terbuka  (ya)", (50, 160), font, 1, (0, 255, 0), 2, cv2.LINE_4)
            serialcomm.write("on".encode())
            ketmask = "yes"
        else:
            cv2.putText(img, "suhu Tinggi " + serialread + "C (ya)", (50, 120), font, 1, (0, 0, 255), 2, cv2.LINE_4)
            cv2.putText(img, "pintu tidak terbuka (ya)", (50, 160), font, 1, (0, 0, 255), 2, cv2.LINE_4)
            serialcomm.write("off".encode())
    elif (len(faces) == 1 and len(mouth) == 1):
        cv2.putText(img, 'tidak ada masker', (50, 80), font, 1, red_color, 2, cv2.LINE_4)
        serialcomm.write("off".encode())
        ketmask = "no mask"
    elif (len(faces) == 1 and len(mouth) == 2):
        cv2.putText(img, 'tidak ada masker', (50, 80), font, 1, red_color, 2, cv2.LINE_4)
        serialcomm.write("off".encode())
        ketmask = "no mask"
    elif (len(faces) == 0):
        cv2.putText(img, 'tidak ada wajah', (50, 80), font, 1, (0, 0, 0), 2, cv2.LINE_4)
        serialcomm.write("off".encode())
        ketmask = "nothing"

    konter = konter + 1
    # jam dan tanggal
    now = datetime.now()
    dt_string1 = now.strftime("%d/%m/%Y")
    dt_string2 = now.strftime("%H:%M:%S")

    # mengirim data no, jam, tanggal, suhu, keterangan masker ke database mysql
    record1 = (konter, dt_string1, dt_string2, serialread, ketmask)
    mycursor.execute(sqlstuff, record1)
    mydb.commit()

    cv2.imshow('Detected Face', img)
    # keyboard esc untuk keluar dari loop
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    time.sleep(0.5)

cap.release()
serialcomm.close()

# menampilkan semua data di database mysql
print("(No, Tanggal, Jam, Suhu, Ket_Masker)")
query = "SELECT * FROM data_masker"
mycursor.execute(query)
records = mycursor.fetchall()
for x in records:
    print(x)
