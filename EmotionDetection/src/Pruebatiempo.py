import cv2
import time

# Configuración de la cámara
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Variables de tiempo
tiempo_inicio = time.time()
tiempo_inicio2=tiempo_inicio
# Bucle principal
while True:
    # Captura de fotograma
    ret, frame = cam.read()

    # Comprobación de la captura
    if not ret:
        print("No se pudo capturar el fotograma")
        break

    # Comprobación del tiempo
    tiempo_actual = time.time()
    tiempo_transcurrido = tiempo_actual - tiempo_inicio
    tiempo_actualreal=tiempo_actual-tiempo_inicio2

    # Tomar foto cada 10 segundos
    if tiempo_transcurrido >= 10:
        nombre_archivo = f"{int(tiempo_actualreal)}.jpg"
        cv2.imwrite(nombre_archivo, frame)
        tiempo_inicio = tiempo_actual

        # Mostrar la última imagen tomada en la ventana
        cv2.imshow("Imagen", frame)
        cv2.waitKey(1)

    # Salida del bucle si se pulsa la tecla 'q'
    if cv2.waitKey(1) == ord("q"):
        break

# Liberar recursos y cerrar ventanas
cam.release()
cv2.destroyAllWindows()


