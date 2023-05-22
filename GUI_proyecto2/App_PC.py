import tkinter as tk
from tkinter import messagebox, filedialog
import paramiko
import os
import stat
from matplotlib import pyplot as plt
from collections import defaultdict

class SSHApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Conexión")
        
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
        tk.Button(root, text="Connect", command=self.connect_ssh).grid(row=6, columnspan=2)

        # Variable para comando de la aplicación
        self.application_command=tk.StringVar(value="python3 Desktop/stopwatch.py")
    
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
            messagebox.showinfo("Success", "SSH connection established.")
            self.ventana_app()
        except paramiko.AuthenticationException:
            messagebox.showerror("Error", "Authentication failed. Please check the credentials.")



        
        

    


    def transfer_folder(self, remote_folder_path, local_folder_path):
        sftp_client = self.ssh_client.open_sftp()

        # Iterate over the files and subdirectories in the remote folder
        for item in sftp_client.listdir(remote_folder_path):
            remote_item_path = os.path.join(remote_folder_path, item)
            local_item_path = os.path.join(local_folder_path, item)

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



    def enviar_settings(self, local_file_path, remote_file_path, ssh_client):
        sftp_client = ssh_client.open_sftp()
        sftp_client.put(local_file_path, remote_file_path)
        sftp_client.close()

    def call_plot(self):
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
                self.plot_emotions(nombre_archivo)

            # Crear botones para cada archivo
            for archivo in archivos_txt:
                boton = tk.Button(ventana_seleccion, text=archivo, command=lambda archivo=archivo: imprimir_archivo_seleccionado(archivo))
                boton.pack()

        else:
            print("No se encontraron archivos TXT en la carpeta 'peliculas'")

    def plot_emotions(self,filename):
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

        

###############################################################
# VENTANA DE APLICACION
###############################################################

    def ventana_app(self):
        nueva_ventana=tk.Toplevel(self.root)
        nueva_ventana.title("Aplicación para detector de emociones")

        # Ruta del folder remoto
        remote_folder_path_g = tk.StringVar(value="Desktop/Folderprueba")
        
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


        def execute():
 
            # Set the on/off variable to True
            on_off_var.set(True)
            
            # Application command
            application_command = self.application_command.get()  # Modify this if the script name or path is different
            print(application_command)
            # Check if the application command is not blank
            if not application_command.strip():
                messagebox.showerror("Error", "Application command is blank.")
                return
            # Execute the command
            stdin, stdout, stderr = self.ssh_client.exec_command(application_command)

            # Update the file
            update_file()
            
            # Transfer the file to the remote server
            remote_path = f"Desktop/{os.path.basename(self.file_path)}"  # Update the remote directory path
            self.enviar_settings(self.file_path, remote_path, self.ssh_client)
            # Display the output in a messagebox
            messagebox.showinfo("Application excecuted","Aplicación ejecutada con éxito")

        
        def end_program():
            

            # Set the on/off variable to False
            on_off_var.set(False)

            # Update the file
            update_file()
            
            # Transfer the file to the remote server
            remote_path = f"Desktop/{os.path.basename(self.file_path)}"  # Update the remote directory path
            self.enviar_settings(self.file_path, remote_path, self.ssh_client)

            messagebox.showinfo("Program Terminated", "The remote program has been terminated.")
            
        

        def extract_folder():

            # Remote folder path
            remote_folder_path = remote_folder_path_g.get()

            # Local folder path
            local_folder_path = local_folder_path_g.get()

            # Ensure the local folder path exists
            if not os.path.exists(local_folder_path):
                os.makedirs(local_folder_path)

            # Recursively transfer files and folders
            self.transfer_folder(remote_folder_path, local_folder_path)

            messagebox.showinfo("Success", "Folder extracted successfully.")
        
        
        
        def set_framerate():
            # Get the new framerate value
            new_framerate = framerate.get()
            
            # Update the file
            update_file()
            
            # Transfer the file to the remote server
            remote_path = f"Desktop/{os.path.basename(self.file_path)}"  # Update the remote directory path
            print("Archivo a enviar: ",self.file_path,"\n")
            print("Dirección a almacenar",remote_path,"\n")
            print("Objeto a enviar: ",self.ssh_client,"\n")
            self.enviar_settings(self.file_path, remote_path, self.ssh_client)

            # Display a message
            messagebox.showinfo("Framerate Set", f"The framerate has been set to {new_framerate}.")


        def create_file():
            # File creation variables
            frame = framerate.get()
            on_off = on_off_var.get()
            
            # Create the file with the given variables
            file_content = f"Framerate: {frame}\nOn/Off: {'On' if on_off else 'Off'}"
            
            # Open a file dialog to select the file location
            file_path = "settings.txt"
            
            if file_path:
                # Save the file with the provided file path
                with open(file_path, "w") as file:
                    file.write(file_content)
                    
                messagebox.showinfo("Success", "File created successfully.")
            else:
                messagebox.showwarning("Warning", "File creation cancelled.")

            return file_path
        
        def update_file():
            # File update variables
            frame = framerate.get()
            on_off = on_off_var.get()
            
            # Update the file content
            file_content = f"Framerate: {frame}\nOn/Off: {'On' if on_off else 'Off'}"
            
            # Get the file path from the previous creation or selection
            file_path = self.file_path
            
            if file_path:
                # Update the file with the modified content
                with open(file_path, "w") as file:
                    file.write(file_content)

        # Create the file
        self.file_path = create_file()

        
        # Local folder path input#### Quitar...  Debe ser fijo
        locallabel=tk.Label(nueva_ventana, text="Local Folder Path:").grid(row=1, column=0, sticky="e")
        localfolder=tk.Entry(nueva_ventana, textvariable=local_folder_path_g).grid(row=5, column=1)

        # Execute button
        ejecutar=tk.Button(nueva_ventana, text="Execute Command", command=execute).grid(row=2, columnspan=2)
        
        # Extract folder button
        extraer=tk.Button(nueva_ventana, text="Extract Folder", command=extract_folder).grid(row=3, columnspan=2)
               
        # Botón para finalizar el programa
        fin=tk.Button(nueva_ventana, text="Finalizar Programa", command=end_program).grid(row=4, columnspan=2)
    
        

        graph = tk.Button(nueva_ventana, text="Graficar datos", command=self.call_plot).grid(row=2, column=2, padx=5)
        # Set Framerate button
        setframe=tk.Button(nueva_ventana, text="Set Framerate", command=set_framerate).grid(row=0, column=4, padx=5)
       
       




        # Start the main event loop
        nueva_ventana.mainloop()

    

root = tk.Tk()
app = SSHApplication(root)
root.mainloop()

