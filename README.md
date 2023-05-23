# TSE_Proyecto_2

# Pasos para flashear la imagen a la tarjeta SD
1) Listar los discos para saber cual es la SD, esto con el comando:
      lsblk
      
2) Desmontar el disco con:
      sudo umount /dev/nombredelaSD* en este caso mmcblk0
      
3) Luego se corre: sudo dd if=direccion/de/la/imagen/creada of=/direccion/disco/a/flashear bs=4M

4) Despues se corre: sync

5) Luego: sudo umount /dev/nombredelaSD*


## Interfáz Gráfica de Usuario (GUI)
1) Esta interfáz se ubica en la carpeta GUI_proyecto2, el archivo llamado App_PC.py, este es un archivo que contiene código en Python, antes de ejecutar esta aplicación se debe contar con varias dependencias en la PC remota (Ordenador que controlará a la _Raspberry Pi_):
      -tkinter   
      -paramiko
      -stat
      -matplolib
      -collections
      -datetime
      -math
Si no se cuenta con alguna de ellas el programa no funcionará como debe.

2) Una vez que se cuente con todas las dependencias, ejecutar desde la terminal en Linux, utilizando VS Code o cualquier otra aplicación que pueda manejar programas de _Python_, esta aplicación fue probada ejecutando tanto desde VS Code como desde la terminal y ambas funcionaron correctamente.

3) Una vez ejecutada la aplicación se desplegará una ventana que preguntará por _hostname_(Dirección IP), _Username_(Nombre de usuario) y _Password_(Contraseña), una vez ingresados estos credenciales está el botón _Conectar_ para realizar la conexión SSH, si todos los datos son correctos se dedespleggará una nueva ventana.

      Nota: Debe conocer la IP, nombre de usuario y contraseña de su raspberry, además, tanto la PC como la _Raspberry_ tienen que estar conectada             a la misma red, o conectadas directamento por cable Ethernet desde la PC a la _Raspberry_.
      
4) La segunda ventana desplegada tiene más opciones y es la ventana que controla la aplicación:
      a) El botón _Ejecutar Aplicación_ corre el comando que lanza el detector de emociones.
      b) El botón _Finalizar Aplicación_ modifica un archivo de configuración que manda una señal para detener la ejecución del detector.
      c) El botón _Set Framerate_ modifica la configuración y establece un intervalo de toma de datos nuevo según lo que se ingrese en la casilla          a la par de dicho botón.
      d) El botón _Extraer Folder_ tomar la carpeta creada en la _Raspberry_, donde se almacenaron las fotos y un archivo de registros y las envía          a la PC que la controla.
      e) Finalmente, el botón _Graficar Datos_ toma los datos del archivo de registros extraído y realiza una gráfica de los mismos.
      
  



## Referencias
> https://github.com/atulapra/Emotion-detection


