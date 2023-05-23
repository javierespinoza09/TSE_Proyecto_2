import tkinter as tk
from tkinter import messagebox, filedialog
import paramiko
import os
import stat
from matplotlib import pyplot as plt
from collections import defaultdict
from datetime import datetime
import math


class SSHApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Conexión SSH")
        
        # Variables para la conexión SSH
        self.hostname = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
  
        # Entradas de conexión para SSH
        tk.Label(root, text="Hostname(Dirección IP):").grid(row=0, column=0, sticky="e")
        tk.Entry(root, textvariable=self.hostname).grid(row=0, column=1)
        
        tk.Label(root, text="Username:").grid(row=1, column=0, sticky="e")
        tk.Entry(root, textvariable=self.username).grid(row=1, column=1)
        
        tk.Label(root, text="Password:").grid(row=2, column=0, sticky="e")
        tk.Entry(root, textvariable=self.password, show="*").grid(row=2, column=1)
        
        # Connect button
        tk.Button(root, text="Conectar", command=self.connect_ssh).grid(row=6, columnspan=2)

        # Variable para comando de la aplicación
        self.date1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.application_command=tk.StringVar(value="cd /usr/bin && python3 EmotionDetectionLite.py")
        # Ruta del folder remoto
        self.remote_folder_path = tk.StringVar()
        
        # Ruta del folder local
        self.local_folder_path = tk.StringVar()


    
    def connect_ssh(self):
        # SSH connection details
        hostname = self.hostname.get()
        username = self.username.get()
        password = self.password.get()

        # SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(hostname, username=username, password=password)
            self.ssh_client = ssh_client
            messagebox.showinfo("Conexión exitosa", "Conexión SSH establecida.")
            self.ventana_app()
        except paramiko.AuthenticationException:
            messagebox.showerror("Error", "Fallo de autenticación. Revise sus credenciales.")


    def transfer_folder(self, remote_folder_path, local_folder_path):
        sftp_client = self.ssh_client.open_sftp()

        # Iterate over the files and subdirectories in the remote folder
        for item in sftp_client.listdir(remote_folder_path):
            remote_item_path = os.path.join(remote_folder_path, item)
            local_item_path = os.path.join(self.local_folder_path, item)

            # Get the attributes of the item
            item_attributes = sftp_client.stat(remote_item_path)

            # If it's a file, transfer it
            if stat.S_ISREG(item_attributes.st_mode):
                sftp_client.get(remote_item_path, local_item_path)

            # If it's a directory, create a corresponding local directory and recursively transfer its contents
            elif stat.S_ISDIR(item_attributes.st_mode):
                os.makedirs(local_item_path, exist_ok=True)
                self.transfer_folder(remote_item_path, local_item_path)

        sftp_client.close()


    ##Función para eviar el archivo de configuración PC -> Raspberry
    def enviar_settings(self, local_file_path, remote_file_path, ssh_client):
        sftp_client = ssh_client.open_sftp()
        sftp_client.put(local_file_path, remote_file_path)
        sftp_client.close()


    ##Función para llamar a la graficadora
    def call_plot(self):
        ruta_peliculas = self.local_folder_path
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
                self.plot_emotions(nombre_archivo)

            # Crear botones para cada archivo
            for archivo in archivos_txt:
                boton = tk.Button(ventana_seleccion, text=archivo, command=lambda archivo=archivo: imprimir_archivo_seleccionado(archivo))
                boton.pack()

        else:
            print("No se encontraron archivos TXT en la carpeta 'peliculas'")

    #Función para graficar
    def plot_emotions(self,filename):


        # Crea un diccionario para almacenar los datos de las emociones
        emotions = defaultdict(list)

        # Lee el archivo de texto
        with open(self.local_folder_path+"/registros.txt", "r") as file:
            for line in file:
                line = line.strip()  # Elimina los espacios en blanco al inicio y al final
                if line:
                    timestamp, emotion = line.split(",")  # Separa el timestamp y la emoción
                    _, minutes, seconds_milliseconds = timestamp.split(" ")[1].split(":")
                    seconds = seconds_milliseconds.split(".")[0]
                    milliseconds = seconds_milliseconds.split(".")[1][:2]
                    emotions[emotion].append((int(minutes), float(f"{seconds}.{milliseconds}"), timestamp))

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

        # Obtén todos los timestamps de la lista de emociones
        timestamps = []
        for data in emotions.values():
            timestamps.extend(data)

        # Ordena los valores del eje y (segundos y milisegundos)
        timestamps.sort(key=lambda x: x[1])

        # Grafica los datos de las emociones
        scatter_points = []
        for emotion, data in emotions.items():
            minutes, seconds_milliseconds, _ = zip(*data)
            scatter = plt.scatter(minutes, seconds_milliseconds, color=emotion_colors[emotion], label=emotion)
            scatter_points.append(scatter)

        # Configura el marcado del eje y
        max_milliseconds = math.ceil(max(seconds_milliseconds))
        plt.yticks(range(0, max_milliseconds + 1, 10))

        plt.xlabel("Minutos")
        plt.ylabel("Segundos.Milisegundos")
        plt.title("Emociones en función del tiempo")
        legend = plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        legend.set_title("Emociones", prop={"size": 10})  # Ajusta el tamaño de la leyenda

        annotations = []


        def on_click(event):
            if event.button == 1:  # Solo se activa para clics izquierdos
                if event.inaxes:  # Verifica si el clic está dentro de la gráfica
                    x, y = event.xdata, event.ydata
                    min_dist = float('inf')
                    closest_timestamp = None

                    for timestamp in timestamps:
                        min_val, sec_val, _ = timestamp
                        dist = math.sqrt((min_val - x) ** 2 + (sec_val - y) ** 2)
                        if dist < min_dist:
                            min_dist = dist
                            closest_timestamp = timestamp

                    min_value, sec_value, timestamp_str = closest_timestamp
                    text = f"{min_value}:{sec_value:.2f} ({timestamp_str})"
                    annotation = plt.annotate(text, (x, y), xytext=(5, 5), textcoords="offset points", fontsize=8, color="black",
                                            ha='left', va='bottom')
                    annotations.append(annotation)
                    plt.gcf().canvas.draw()
            elif event.button == 3:  # Se activa para clics derechos
                for annotation in annotations:
                    annotation.remove()
                annotations.clear()
                plt.gcf().canvas.draw()


        plt.gcf().canvas.mpl_connect('button_press_event', on_click)
        plt.tight_layout()  # Ajustar márgenes y espacios
        plt.show()

        

###############################################################
# VENTANA DE APLICACION
###############################################################

    def ventana_app(self):
        nueva_ventana=tk.Toplevel(self.root)
        nueva_ventana.title("Aplicación para detector de emociones")

        # Ruta del folder remoto
        remote_folder_path_g = tk.StringVar(value="/usr/bin/resultados")
        
        # Ruta del folder local
        local_folder_path_g = tk.StringVar()

        # Framerate variable
        framerate = tk.StringVar(value="30")

        # On/Off variable
        on_off_var = tk.BooleanVar(value=False)

        # Framerate entry
        framelabel=tk.Label(nueva_ventana, text="Framerate:").grid(row=0, column=2, sticky="e")
        framerate_entry = tk.Entry(nueva_ventana, textvariable=framerate)
        framerate_entry.grid(row=0, column=3)

        ##Función para la ejecución del programa detector de emociones
        def execute():
 
            # Cambiar el valor de la variable on/off a True
            on_off_var.set(True)
            
            # Comando para la aplicación
            application_command = self.application_command.get()  
        
            print(application_command)

            # Verificación de que haya un comando para ejecutar
            if not application_command.strip():
                messagebox.showerror("Error", "Comando para aplicación está en blanco.")
                return
            
            #Ejecutar el comando via SSH
            self.ssh_client.exec_command(f'date -s "{self.date1}"')  #  Primero se establece la fecha correcta
            stdin, stdout, stderr = self.ssh_client.exec_command(application_command) #Luego se ejecuta la aplicación
            
            # Actualizar el archivo de configuraciones
            update_file()
            
            # Enviar el archivo de configuración actualizado a la Raspberry
            remote_path = f"/usr/bin/{os.path.basename(self.file_path)}"  # Dirección de almacenamiento en la Raspberry
            self.enviar_settings(self.file_path, remote_path, self.ssh_client)

            # Mostrar un messagebox de ejecución exitosa
            messagebox.showinfo("Aplicación ejecutada","La aplicación ha sido ejecutada con éxito")

        
        #Función para terminar el programa
        def end_program():
            

            # Cambiar el valor de la variable on/off a False
            on_off_var.set(False)

            # Actualizar el archivo de configuraciones
            update_file()
            
            # Enviar el archivo de configuración actualizado a la Raspberry
            remote_path = f"/usr/bin/{os.path.basename(self.file_path)}" 
            self.enviar_settings(self.file_path, remote_path, self.ssh_client)

            messagebox.showinfo("Program Terminated", "The remote program has been terminated.")
            
        
        ##Función para extraer el folder con las fotos tomadas y con el archivo de los registros de las emociones
        def extract_folder():

            # Dirección en la Raspberry
            remote_folder_path = remote_folder_path_g.get()

            # Nombre de la dirección donde se desea guardar
            self.local_folder_path = local_folder_path_g.get()

            # Asegura de que el folder local exista
            if not os.path.exists(self.local_folder_path):
                os.makedirs(self.local_folder_path)

            # Transfiere los archivos
            self.transfer_folder(remote_folder_path, self.local_folder_path)

            messagebox.showinfo("Extracción exitosa", "El folder ha sido extraído exitosamente")
        
        
        ##Función para cambiar el intervalo de captura de datos
        def set_framerate():
            # Obtener nuevo valor de framerate
            new_framerate = framerate.get()
            
            # Actualizar archivo de configuraciones
            update_file()
            
            # Enviar configuraciones
            remote_path = f"/usr/bin/{os.path.basename(self.file_path)}"  # Update the remote directory path
            print("Archivo a enviar: ",self.file_path,"\n")
            print("Dirección a almacenar",remote_path,"\n")
            print("Objeto a enviar: ",self.ssh_client,"\n")
            self.enviar_settings(self.file_path, remote_path, self.ssh_client)

            # Display a message
            messagebox.showinfo("Framerate Set", f"El framerate ha sido modificado a {new_framerate}.")


        ##Función para crear el archivo de configuraciones
        def create_file():
            # Variables a incluir en le archivo
            frame = framerate.get()
            on_off = on_off_var.get()
            
            # Crea el archivo con las variables dadas
            file_content = f"Framerate: {frame}\nOn/Off: {'On' if on_off else 'Off'}"
            

            file_path = "settings.txt"
            
            if file_path:
                # Guarda las configuraciones en la dirección dada
                with open(file_path, "w") as file:
                    file.write(file_content)
            else:
                messagebox.showwarning("Advertencia", "Se ha cancelado la creación del archivo.")

            return file_path
        

        ##Función para actualizar las configuraciones
        def update_file():
            # Variables a actualizar
            frame = framerate.get()
            on_off = on_off_var.get()
            
            # Actualización de archivo
            file_content = f"Framerate: {frame}\nOn/Off: {'On' if on_off else 'Off'}"
            
            # Obtener dirección del lugar donde se creó originalmente el archivo
            file_path = self.file_path
            
            if file_path:
                # Actualizar los contenidos de las configuraciones
                with open(file_path, "w") as file:
                    file.write(file_content)

        # Crea el archivo de configuraciones una vez que la segunda ventana es abierta
        self.file_path = create_file()

        
        # Entrada para dirección del folder local donde se guardarán los datos recolectados#### 
        locallabel=tk.Label(nueva_ventana, text="Ruta local del folder:").grid(row=1, column=2, sticky="e")
        localfolder=tk.Entry(nueva_ventana, textvariable=local_folder_path_g).grid(row=1, column=3)

        # Botón para ejecutar la aplicación
        ejecutar=tk.Button(nueva_ventana, text="Ejecutar Aplicación", command=execute).grid(row=0, columnspan=2)
        
        # Botón para extracción de folder
        extraer=tk.Button(nueva_ventana, text="Extraer Folder", command=extract_folder).grid(row=1, column=4, padx=5)
               
        # Botón para finalizar el programa
        fin=tk.Button(nueva_ventana, text="Finalizar Aplicación", command=end_program).grid(row=1,columnspan=2)
    
        
        #Botón para graficar los datos
        graph = tk.Button(nueva_ventana, text="Graficar Datos", command=self.call_plot).grid(row=4, column=0, padx=5)
        # Botón para cambiar framerate
        setframe=tk.Button(nueva_ventana, text="Cambiar Framerate", command=set_framerate).grid(row=0, column=4, padx=5)
       
       




        # Inicia el loop de la segunda ventana
        nueva_ventana.mainloop()

    

root = tk.Tk()
app = SSHApplication(root)
root.mainloop()

