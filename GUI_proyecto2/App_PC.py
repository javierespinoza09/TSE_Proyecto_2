import tkinter as tk
from tkinter import messagebox
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
        
        # Connect and execute button
        tk.Button(root, text="Connect and Execute", command=self.connect_and_execute).grid(row=6, columnspan=2)
        
        # Extract folder button
        tk.Button(root, text="Extract Folder", command=self.extract_folder).grid(row=7, columnspan=2)
               
        # Botón para finalizar el programa
        tk.Button(root, text="Finalizar Programa", command=self.end_program).grid(row=8, columnspan=3)
        
    def connect_and_execute(self):
        # SSH connection details
        hostname = self.hostname.get()
        username = self.username.get()
        password = self.password.get()
        
        # Application command
        application_command = self.application_command.get()  # Modify this if the script name or path is different
        
        # SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            ssh_client.connect(hostname, username=username, password=password)
            # Execute the application command and get the output
            stdin, stdout, stderr = ssh_client.exec_command(application_command)
            output = stdout.read().decode().strip()
            
            # Display the output in a messagebox
            messagebox.showinfo("Output", output)
        
        except paramiko.AuthenticationException:
            messagebox.showerror("Error", "Authentication failed. Please check the credentials.")
        
        ssh_client.close()
    
    def end_program(self):
        # SSH connection details
        hostname = self.hostname.get()
        username = self.username.get()
        password = self.password.get()
        
        # Send the termination signal (SIGINT) to end the program
        command = "pkill -2 -f 'python your_script.py'"
        
        # SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            ssh_client.connect(hostname, username=username, password=password)
            # Send the termination signal command
            ssh_client.exec_command(command)
            messagebox.showinfo("Program Ended", "The program has been terminated.")
        
        except paramiko.AuthenticationException:
            messagebox.showerror("Error", "Authentication failed. Please check the credentials.")
        
        ssh_client.close()

    def extract_folder(self):
        # SSH connection details
        hostname = self.hostname.get()
        username = self.username.get()
        password = self.password.get()

        # Remote folder path
        remote_folder_path = self.remote_folder_path.get()

        # Local folder path
        local_folder_path = self.local_folder_path.get()

        # SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(hostname, username=username, password=password)
            sftp_client = ssh_client.open_sftp()

            # Ensure the local folder path exists
            if not os.path.exists(local_folder_path):
                os.makedirs(local_folder_path)

            # Recursively transfer files and folders
            self.transfer_folder(sftp_client, remote_folder_path, local_folder_path)

            sftp_client.close()
            ssh_client.close()

            messagebox.showinfo("Success", "Folder extracted successfully.")

        except paramiko.AuthenticationException:
            messagebox.showerror("Error", "Authentication failed. Please check the credentials.")

        except FileNotFoundError:
            messagebox.showerror("Error", "Local folder path is invalid.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def transfer_folder(self, sftp_client, remote_folder_path, local_folder_path):
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
                self.transfer_folder(sftp_client, remote_item_path, local_item_path)

root = tk.Tk()
app = SSHApplication(root)
root.mainloop()

