import os
import shutil
import urllib.request
import platform
import time
import subprocess
import ctypes

# Obtener el identificador de la ventana actual
hwnd = ctypes.windll.kernel32.GetConsoleWindow()

# Definir la posición de la ventana
left = 0
top = 10

# Cambiar la posición de la ventana
ctypes.windll.user32.SetWindowPos(hwnd, None, left, top, 0, 10, 0x0001)

# Colores para la interfaz
class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

# Tamaño de la ventana
os.system("mode con cols=110 lines=20")

# Interfaz de bienvenida
print("***********************************************")
print("*                                             *")
print("*      Bienvenidos al configurador de Timer.  *")
print("*                                             *")
print("***********************************************")
print("\nEste programa permite configurar el Timer de Windows 11 y hacer varias muestras para comprobar si hay")
print("alguna variación en el temporizador. Por defecto, el Timer está configurado en 1.000ms, pero se puede")
print("forzar a 0.500ms si se requiere el viejo timer.")
print(f"{bcolors.OKGREEN}\nEste programa fue creado gracias a Schizobeyond y Amit, de los cuales usamos algunos recursos.{bcolors.ENDC}")

# Tiempo de espera de 5 segundos
print(f"{bcolors.WARNING}\nEste programa se iniciará en unos segundos...{bcolors.ENDC}")
time.sleep(5)

print(f"{bcolors.OKGREEN}\n¡Comencemos!{bcolors.ENDC}")

# Obtener información del sistema operativo
system_info = platform.platform()

# Verificar si el sistema operativo es Windows 10 o 11
if "Windows-10" in system_info:
    print("El sistema operativo es Windows 10.")
    time.sleep(5)
elif "Windows-11" in system_info:
    print("El sistema operativo es Windows 11.")
    time.sleep(5)
    # Opciones adicionales para Windows 11
    print(f"{bcolors.WARNING}Seleccione una opción:\n{bcolors.ENDC}")
    print("1. Agregar GlobalTimerResolutionRequests.")
    print("2. Eliminar GlobalTimerResolutionRequests.")
    opcion_11 = input("Ingrese una opción (1 o 2): ")
    if opcion_11 == "1":
        os.system('reg.exe add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Kernel" /v "GlobalTimerResolutionRequests" /t REG_DWORD /d "1" /f')
        print("Se ha agregado la clave GlobalTimerResolutionRequests al registro.")
    elif opcion_11 == "2":
        os.system('reg.exe delete "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Kernel" /v "GlobalTimerResolutionRequests" /f')
        print("Se ha eliminado la clave GlobalTimerResolutionRequests del registro.")
    else:
        print("Opción no válida.")

# Definir la cadena de opciones
opciones = "\n1.  5000 (0.5000)\n2.  10000 (1.000)"
subprocess.Popen("start cmd /k Measure-Sleep.exe", shell=True)

# Solicitar al usuario la opción de resolución
while True:
    os.system('cls' if os.name == 'nt' else 'clear') # Borrar la pantalla
    print(f"{bcolors.WARNING}Seleccione una opción:\n{bcolors.ENDC}" + opciones)
    opcion = input("\n> ")
    
    # Verificar la opción ingresada y ejecutar la acción correspondiente
    if opcion == "1":
        os.system("cd C:\\ && SetTimerResolution.exe --resolution 5000")
        print("La resolución se ha establecido en 5000 (0.500).")
        break # Salir del bucle
    
    elif opcion == "2":
        os.system("cd C:\\ && SetTimerResolution.exe --resolution 10000")
        print("La resolución se ha establecido en 10000 (1.000).")
        break # Salir del bucle
    
    else:
        # Opción no válida
        print("Opción no válida. Presione Enter para continuar...")
        input()