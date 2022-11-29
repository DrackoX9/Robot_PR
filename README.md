# Robot_PR - Proyecto de Robótica

## Para crear un entorno virtual en Python
 ```sh
py -m venv env 
```

## Para activar el entorno virtual 
1. Otorgar permisos de ejecucion de script
```sh
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
2. Ingresar a la carpeta scripts y ejecutar ./activate/

## Para cambiar el Path y poder instalar paquetes con pip
1.  Ir a las variables de entorno y agregar el Path del env EJM: C:\Users\SnakeHacKx\developer\Robot_PR\env
2.  Agregar el Path de los Scripts: C:\Users\SnakeHacKx\developer\Robot_PR\env\Scripts\
3.  Reinstalar pip: ```python -m pip install --upgrade --force-reinstall pip```

## Para instalar los paquetes utilizados con requeriments.txt
1.   Cambiar el path al env creado
2.   ```pip install -r requeriments.txt```

## Para instalar un paquete en una carpeta especifica
```sh
pip install imutils --target=ruta
```
