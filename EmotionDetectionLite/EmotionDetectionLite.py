import cv2
import numpy as np
import time
import tensorflow as tf
from datetime import datetime
import os
# load the TFLite model
interpreter = tf.lite.Interpreter(model_path="model.tflite")
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
tiempo_inicio2=tiempo_inicio

while True:
    try:
        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()
        # Ajustar brillo y contraste
        adjusted_frame = adjust_brightness_contrast(frame, brightness=75, contrast=4)
        if not ret:
            break
        facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2GRAY)
        faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)

        # Comprobación del tiempo
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicio
        tiempo_actualreal=tiempo_actual-tiempo_inicio2

        # Tomar foto cada 10 segundos
        if tiempo_transcurrido >= 10:
            nombre_archivo = f"{int(tiempo_actualreal)}.jpg"
            cv2.imwrite(nombre_archivo, adjusted_frame)
            tiempo_inicio = tiempo_actual
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
            
            # Comprueba si la carpeta ya existe
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



            try:
                with open("tiempo.txt", "r") as f:
                    tiempo_anterior, expresion_anterior = f.read().strip().split(",")
            except FileNotFoundError:
                # Si el archivo no existe, el tiempo y fruta anteriores son cero y vacío, respectivamente
                tiempo_anterior = 0.0
                expresion_anterior = ""

            print(datetime.now())
            # Guardar el tiempo y fruta en el archivo
            with open("resultados/registros.txt", "a") as f:
                f.write(f"{datetime.now()} {emotion_dict[maxindex]}\n")

    except KeyboardInterrupt:
        break


cap.release()
cv2.destroyAllWindows()


