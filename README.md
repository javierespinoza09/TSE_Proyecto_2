# TSE_Proyecto_2

#Pasos para flashear la imagen a la tarjeta SD
1) Listar los discos para saber cual es la SD, esto con el comando:
      lsblk
      
2) Desmontar el disco con:
      sudo umount /dev/nombredelaSD* en este caso mmcblk0
      
3) Luego se corre: sudo dd if=direccion/de/la/imagen/creada of=/direccion/disco/a/flashear bs=4M

4) Despues se corre: sync

5) Luego: sudo umount /dev/nombredelaSD*




## Referencias
> https://github.com/atulapra/Emotion-detection
