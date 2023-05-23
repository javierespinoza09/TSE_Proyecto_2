import cv2
import numpy as np
import time
from tflite_runtime.interpreter import Interpreter
from datetime import datetime
import os
import paramiko
import getpass

# load the TFLite model
interpreter = Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# get the input and output index values
input_index = input_details[0]['index']
output_index = output_details[0]['index']



def adjust_brightness_contrast(image, brightness, contrast):
    # Ajustar el brillo y el contraste utilizando la transformación de píxeles
    adjusted_image = np.clip((image * contrast + brightness), 0, 255).astype(np.uint8)
    return adjusted_image


# dictionary which assigns each label an emotion (alphabetical order)
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}


# start the webcam feed
cap = cv2.VideoCapture(0)


# Variables de tiempo
tiempo_inicio = time.time()


while True:

    settings_path = "/usr/bin/settings.txt"##Verificar path de archivo settings final

    try:
        with open(settings_path, "r") as file:
            file_contents = file.readlines()

            if len(file_contents) >= 2:
                # Extract the "Off" string
                keyword_onoff = "On/Off: "

                #Extrae el framerate
                keyword_frame = "Framerate: "

                off_string = file_contents[1].strip().split(keyword_onoff)[1]
                framerate_int=int(file_contents[0].strip().split(keyword_frame)[1])
            else:
                print("Invalid file format: Insufficient lines in the file.")
    except FileNotFoundError:
        print("File not found.")
    
    #Condición para detener la ejecución del programa
    if off_string=="Off":
        break


    #Correrá hasta que la variable off_string cambie a off
    else:

        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()

        # Ajustar brillo y contraste
        adjusted_frame = adjust_brightness_contrast(frame, brightness=75, contrast=1.5)
        if not ret:
            break
        facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2GRAY)
        faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)


        # Comprobación del tiempo
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicio

        # Tomar foto cada 10 segundos
        if tiempo_transcurrido >= framerate_int:

            nombre_archivo = str(datetime.now())+".jpg"  #Pone a la imagen el nombre que es la hora y fecha en que fue tomada

            cv2.imwrite(nombre_archivo, adjusted_frame) #Guarda la imagen tomada

            tiempo_inicio = tiempo_actual # Actualiza el valor de tiempo

            ##Ejecuta el algoritmo de detección 
            for (x, y, w, h) in faces:
                cv2.rectangle(adjusted_frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
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
                cv2.putText(adjusted_frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            #cv2.imshow('Video', cv2.resize(frame,(1600,960),interpolation = cv2.INTER_CUBIC))
            
            # Comprueba si la carpeta ya existe para guardar las imágenes generadas y el archivo de texto
            imagenes = 'resultados'
            if not os.path.exists(imagenes):
            # Crea la carpeta
                os.mkdir(imagenes)
                
                print("Se ha creado la carpeta de imágenes.")
            else:
    
                print("La carpeta de imágenes ya existe.")
                ##Función para guardar un .txt con el tiempo y la emoción para esa foto
            image_path = os.path.join(imagenes, nombre_archivo)   
            cv2.imwrite(image_path, adjusted_frame)

            #Crea el registro de las emociones y el tiempo y lo guarda en la carpeta de las imagenes
            try:
                with open("tiempo.txt", "r") as f:
                    tiempo_anterior, expresion_anterior = f.read().strip().split(",")
            except FileNotFoundError:
                # Si el archivo no existe, el tiempo y fruta anteriores son cero y vacío, respectivamente
                tiempo_anterior = 0.0
                expresion_anterior = ""

            # Guardar el tiempo y la emoción en el archivo
            with open("resultados/registros.txt", "a") as f:
                f.write(f"{datetime.now()},{emotion_dict[maxindex]}\n")



cap.release()
cv2.destroyAllWindows()


