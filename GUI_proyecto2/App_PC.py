import tkinter as tk
from tkinter import messagebox, filedialog
import paramiko
import os
import stat

class SSHApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación para detector de emociones")
        
        # Variables para la conexión SSH
        self.hostname = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        # Framerate variable
        self.framerate = tk.StringVar(value="30")
        
        # On/Off variable
        self.on_off = tk.BooleanVar(value=False)
        
        # Framerate entry
        tk.Label(root, text="Framerate:").grid(row=0, column=2, sticky="e")
        self.framerate_entry = tk.Entry(root, textvariable=self.framerate)
        self.framerate_entry.grid(row=0, column=3)
        
        # Set Framerate button
        tk.Button(root, text="Set Framerate", command=self.set_framerate).grid(row=0, column=4, padx=5)

        # Variable para comando de la aplicación
        self.application_command = tk.StringVar()
        
        # Ruta del folder remoto
        self.remote_folder_path = tk.StringVar()
        
        # Ruta del folder local
        self.local_folder_path = tk.StringVar()
        
        # Entradas de conexión para SSH
        tk.Label(root, text="Hostname(Dirección IP):").grid(row=0, column=0, sticky="e")
        tk.Entry(root, textvariable=self.hostname).grid(row=0, column=1)
        
        tk.Label(root, text="Username:").grid(row=1, column=0, sticky="e")
        tk.Entry(root, textvariable=self.username).grid(row=1, column=1)
        
        tk.Label(root, text="Password:").grid(row=2, column=0, sticky="e")
        tk.Entry(root, textvariable=self.password, show="*").grid(row=2, column=1)
        
        # Application command input### Quitar...  Debe ser fijo
        tk.Label(root, text="Comando a ejecutar:").grid(row=3, column=0, sticky="e")
        tk.Entry(root, textvariable=self.application_command).grid(row=3, column=1)
        
        # Remote folder path input#### Quitar...  Debe ser fijo
        tk.Label(root, text="Remote Folder Path:").grid(row=4, column=0, sticky="e")
        tk.Entry(root, textvariable=self.remote_folder_path).grid(row=4, column=1)
        
        # Local folder path input#### Quitar...  Debe ser fijo
        tk.Label(root, text="Local Folder Path:").grid(row=5, column=0, sticky="e")
        tk.Entry(root, textvariable=self.local_folder_path).grid(row=5, column=1)
        
       # Connect button
        tk.Button(root, text="Connect", command=self.connect_ssh).grid(row=6, columnspan=2)

        # Execute button
        tk.Button(root, text="Execute Command", command=self.execute).grid(row=7, columnspan=2)
        
        # Extract folder button
        tk.Button(root, text="Extract Folder", command=self.extract_folder).grid(row=8, columnspan=2)
               
        # Botón para finalizar el programa
        tk.Button(root, text="Finalizar Programa", command=self.end_program).grid(row=9, columnspan=2)

       # Create the file
        self.file_path = self.create_file()

    
    def set_framerate(self):
        # Check if SSH connection is established
        if not hasattr(self, 'ssh_client'):
            messagebox.showerror("Error", "SSH connection is not established.")
            return
        
        # Get the new framerate value
        new_framerate = self.framerate.get()
        
        # Update the file
        self.update_file()
        
        # Transfer the file to the remote server
        remote_path = f"Desktop/{os.path.basename(self.file_path)}"  # Update the remote directory path
        print("Archivo a enviar: ",self.file_path,"\n")
        print("Dirección a almacenar",remote_path,"\n")
        print("Objeto a enviar: ",self.ssh_client,"\n")
        self.enviar_settings(self.file_path, remote_path, self.ssh_client)

        # Display a message
        messagebox.showinfo("Framerate Set", f"The framerate has been set to {new_framerate}.")
        
    
    
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
        except paramiko.AuthenticationException:
            messagebox.showerror("Error", "Authentication failed. Please check the credentials.")


    def execute(self):
       # Check if SSH connection is established
        if not hasattr(self, 'ssh_client'):
            messagebox.showerror("Error", "SSH connection is not established.")
            return
        
        # Set the on/off variable to True
        self.on_off.set(True)

        # Application command
        application_command = self.application_command.get()  # Modify this if the script name or path is different

        # Check if the application command is not blank
        if not application_command.strip():
            messagebox.showerror("Error", "Application command is blank.")
            return
        # Execute the command
        stdin, stdout, stderr = self.ssh_client.exec_command(application_command)

        # Update the file
        self.update_file()
        
        # Transfer the file to the remote server
        remote_path = f"Desktop/{os.path.basename(self.file_path)}"  # Update the remote directory path
        self.enviar_settings(self.file_path, remote_path, self.ssh_client)
        # Display the output in a messagebox
        messagebox.showinfo("Application excecuted","Aplicación ejecutada con éxito")
        
        

    
    def end_program(self):
        

        # Set the on/off variable to False
        self.on_off.set(False)

        # Update the file
        self.update_file()
        
        # Transfer the file to the remote server
        remote_path = f"Desktop/{os.path.basename(self.file_path)}"  # Update the remote directory path
        self.enviar_settings(self.file_path, remote_path, self.ssh_client)

        messagebox.showinfo("Program Terminated", "The remote program has been terminated.")
        
    

    def extract_folder(self):
        # SSH connection
        if not hasattr(self, "ssh_client"):
            messagebox.showerror("Error", "SSH connection not established.")
            return

        # Remote folder path
        remote_folder_path = self.remote_folder_path.get()

        # Local folder path
        local_folder_path = self.local_folder_path.get()

        # Ensure the local folder path exists
        if not os.path.exists(local_folder_path):
            os.makedirs(local_folder_path)

        # Recursively transfer files and folders
        self.transfer_folder(remote_folder_path, local_folder_path)

        messagebox.showinfo("Success", "Folder extracted successfully.")

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

    def create_file(self):
        # File creation variables
        framerate = self.framerate.get()
        on_off = self.on_off.get()
        
        # Create the file with the given variables
        file_content = f"Framerate: {framerate}\nOn/Off: {'On' if on_off else 'Off'}"
        
        # Open a file dialog to select the file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            # Save the file with the provided file path
            with open(file_path, "w") as file:
                file.write(file_content)
                
            messagebox.showinfo("Success", "File created successfully.")
        else:
            messagebox.showwarning("Warning", "File creation cancelled.")

        return file_path


    def update_file(self):
        # File update variables
        framerate = self.framerate.get()
        on_off = self.on_off.get()
        
        # Update the file content
        file_content = f"Framerate: {framerate}\nOn/Off: {'On' if on_off else 'Off'}"
        
        # Get the file path from the previous creation or selection
        file_path = self.file_path
        
        if file_path:
            # Update the file with the modified content
            with open(file_path, "w") as file:
                file.write(file_content)

    def enviar_settings(self, local_file_path, remote_file_path, ssh_client):
        sftp_client = ssh_client.open_sftp()
        sftp_client.put(local_file_path, remote_file_path)
        sftp_client.close()


root = tk.Tk()
app = SSHApplication(root)
root.mainloop()

