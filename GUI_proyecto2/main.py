import os
import tkinter as tk
from matplotlib import pyplot as plt
from collections import defaultdict

def verificar_datos():
    # Obtiene los valores ingresados por el usuario
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    ip_direction = entry_ip.get()

    # Verifica los datos ingresados
    if usuario == "user" and contrasena == "1234" and ip_direction == "123456":
        # Limpia la ventana actual
        ventana_principal.destroy()

        # Crea una nueva ventana
        menu_window = tk.Tk()
        menu_window.title("Ventana de verificación exitosa")
        menu_window.geometry("800x600")

        # Etiqueta en la nueva ventana
        etiqueta = tk.Label(menu_window, text="¡Verificación exitosa!")
        etiqueta.pack()

        # Espacio de texto para ingresar frames
        entry_frames = tk.Entry(menu_window)
        entry_frames.pack(side=tk.LEFT)

        def almacenar_frames():
            frames = entry_frames.get()
            if frames.isdigit():
                ejecutar_comando_2(frames)
            else:
                print("Ingresa un número entero para los frames")

        # Botón para confirmar los frames ingresados
        boton_confirmar = tk.Button(menu_window, text="Confirmar", command=almacenar_frames)
        boton_confirmar.pack(side=tk.LEFT)

        def ejecutar_comando_1():
            print("Hola")

        def ejecutar_comando_2(frames):
            print("Frames ingresados:", frames)

        def ejecutar_comando_3():
            print("Comando 3")

        def ejecutar_comando_4():
            print("12345678")

        def ejecutar_comando_5():
            ruta_peliculas = "peliculas/"
            archivos_txt = [archivo for archivo in os.listdir(ruta_peliculas) if archivo.endswith(".txt")]

            if archivos_txt:
                print("Archivos disponibles:")
                for i, archivo in enumerate(archivos_txt):
                    print(f"{i + 1}. {archivo}")

                # Crear una nueva ventana para mostrar los botones
                ventana_seleccion = tk.Toplevel()
                ventana_seleccion.title("Seleccionar archivo")

                def imprimir_archivo_seleccionado(nombre_archivo):
                    print("Archivo seleccionado:", nombre_archivo)
                    plot_emotions(nombre_archivo)

                # Crear botones para cada archivo
                for archivo in archivos_txt:
                    boton = tk.Button(ventana_seleccion, text=archivo, command=lambda archivo=archivo: imprimir_archivo_seleccionado(archivo))
                    boton.pack()

            else:
                print("No se encontraron archivos TXT en la carpeta 'peliculas'")


        # Botones de comando
        comando_1 = tk.Button(menu_window, text="Comando 1", command=ejecutar_comando_1)
        comando_1.pack()

        comando_2 = tk.Button(menu_window, text="Comando 2", command=ejecutar_comando_2)
        comando_2.pack()

        comando_3 = tk.Button(menu_window, text="Comando 3", command=ejecutar_comando_3)
        comando_3.pack()

        comando_4 = tk.Button(menu_window, text="Comando 4", command=ejecutar_comando_4)
        comando_4.pack()

        comando_5 = tk.Button(menu_window, text="Comando 5", command=ejecutar_comando_5)
        comando_5.pack()

        # Bucle principal de la ventana del menú
        menu_window.mainloop()
    else:
        # Limpia los campos de texto
        entry_usuario.delete(0, tk.END)
        entry_contrasena.delete(0, tk.END)
        entry_ip.delete(0, tk.END)

def plot_emotions(filename):
    # Crea un diccionario para almacenar los datos de las emociones
    emotions = defaultdict(list)

    # Lee el archivo de texto
    with open("peliculas/"+filename, "r") as file:
        for line in file:
            line = line.strip()  # Elimina los espacios en blanco al inicio y al final
            if line:
                timestamp, emotion = line.split(",")  # Separa el timestamp y la emoción
                _, minutes, seconds_milliseconds = timestamp.split(" ")[1].split(":")
                seconds = seconds_milliseconds.split(".")[0]
                milliseconds = seconds_milliseconds.split(".")[1][:2]
                emotions[emotion].append((minutes, f"{seconds}.{milliseconds}"))

    # Configura los colores para cada emoción
    emotion_colors = {
        "Angry": "red",
        "Disgusted": "blue",
        "Fearful": "orange",
        "Happy": "green",
        "Neutral": "yellow",
        "Sad": "purple",
        "Surprised": "pink"
    }

    # Ordena los valores del eje y (segundos y milisegundos)
    for emotion, data in emotions.items():
        minutes, seconds_milliseconds = zip(*data)
        seconds_milliseconds = [float(sm) for sm in seconds_milliseconds]
        sorted_indices = sorted(range(len(seconds_milliseconds)), key=lambda k: seconds_milliseconds[k])
        minutes = [minutes[i] for i in sorted_indices]
        seconds_milliseconds = [seconds_milliseconds[i] for i in sorted_indices]

        # Grafica los datos de las emociones
        plt.scatter(minutes, seconds_milliseconds, color=emotion_colors[emotion], label=emotion)

    # Configura el marcado del eje y
    plt.yticks(range(0, int(max(seconds_milliseconds))+1, 10))

    plt.xlabel("Minutos")
    plt.ylabel("Segundos.Milisegundos")
    plt.title("Emociones en función del tiempo")
    plt.legend()
    plt.show()




# Crea la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Verificación de datos")
ventana_principal.geometry("800x600")

# Etiquetas de texto
label_usuario = tk.Label(ventana_principal, text="Usuario:")
label_usuario.pack()

# Campo de texto para el usuario
entry_usuario = tk.Entry(ventana_principal)
entry_usuario.pack()

label_contrasena = tk.Label(ventana_principal, text="Contraseña:")
label_contrasena.pack()

# Campo de texto para la contraseña
entry_contrasena = tk.Entry(ventana_principal, show="*")
entry_contrasena.pack()

label_ip = tk.Label(ventana_principal, text="Dirección IP:")
label_ip.pack()

# Campo de texto para la dirección IP
entry_ip = tk.Entry(ventana_principal)
entry_ip.pack()

# Botón de verificación
boton_verificar = tk.Button(ventana_principal, text="Connect", command=verificar_datos)
boton_verificar.pack()

# Ejecuta el bucle principal de la ventana
ventana_principal.mainloop()



