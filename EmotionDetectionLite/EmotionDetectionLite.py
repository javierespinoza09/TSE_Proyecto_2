import cv2
import numpy as np
import time
from tflite_runtime.interpreter import Interpreter
from datetime import datetime
import paramiko
import getpass
import os

# load the TFLite model
interpreter = Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# get the input and output index values
input_index = input_details[0]['index']
output_index = output_details[0]['index']

# dictionary which assigns each label an emotion (alphabetical order)
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# start the webcam feed
cap = cv2.VideoCapture(0)

# Variables de tiempo
tiempo_inicio = time.time()
tiempo_inicio2=tiempo_inicio

while True:
    # Find haar cascade to draw bounding box around face
    ret, frame = cap.read()
    if not ret:
        break
    facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)

    # Comprobación del tiempo
    tiempo_actual = time.time()
    tiempo_transcurrido = tiempo_actual - tiempo_inicio
    tiempo_actualreal=tiempo_actual-tiempo_inicio2

    # Tomar foto cada 10 segundos
    if tiempo_transcurrido >= 10:
        nombre_archivo = f"{int(tiempo_actualreal)}.jpg"
        cv2.imwrite(nombre_archivo, frame)
        tiempo_inicio = tiempo_actual
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = cv2.resize(roi_gray, (48, 48)).astype('float32')
            cropped_img = cropped_img / 255.0
            cropped_img = np.expand_dims(np.expand_dims(cropped_img, -1), 0)
            interpreter.set_tensor(input_index, cropped_img)

            # run inference with TFLite interpreter
            interpreter.set_tensor(interpreter.get_input_details()[0]["index"], cropped_img)
            interpreter.invoke()
            output = interpreter.get_tensor(interpreter.get_output_details()[0]["index"])
            maxindex = int(np.argmax(output))
            cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('Video', cv2.resize(frame,(1600,960),interpolation = cv2.INTER_CUBIC))
        cv2.imwrite(nombre_archivo, frame)

        ##Función para guardar un .txt con el tiempo y la emoción para esa foto

        try:
            with open("tiempo.txt", "r") as f:
                tiempo_anterior, expresion_anterior = f.read().strip().split(",")
        except FileNotFoundError:
            # Si el archivo no existe, el tiempo y fruta anteriores son cero y vacío, respectivamente
            tiempo_anterior = 0.0
            expresion_anterior = ""

        print(datetime.now())
        # Guardar el tiempo y fruta en el archivo
        with open("registros.txt", "a") as f:
            f.write(f"{datetime.now()},   {emotion_dict[maxindex]}\n")
            

        #ssh = paramiko.SSHClient()
        #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect('20.14.138.43', username='lacordero', password="C*Mlu/001*Ant")
        #rutas=["registros.txt",f"{int(tiempo_actualreal)}.jpg"]
        #for ruta in rutas:
        #    path_local = os.path.basename(ruta)
        #    sftp = ssh.open_sftp()
        #    path_remoto = 'Desktop/'+ruta
        #    sftp.put(path_local, path_remoto)
        #sftp.close()
        #ssh.close()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


