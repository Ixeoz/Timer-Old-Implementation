import os
import time
import subprocess
import ctypes
import sys

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

os.system("mode con cols=110 lines=20")

print("***********************************************")
print("*                                             *")
print("*      Bienvenidos al configurador de Timer.  *")
print("*                                             *")
print("***********************************************")
print("\nEste programa permite configurar el Timer de Windows 11 y hacer varias muestras para comprobar si hay")
print("alguna variación en el temporizador. Por defecto, el Timer está configurado en 1.000ms, pero se puede")
print("forzar a 0.500ms si se requiere el viejo timer.")
print(f"{bcolors.OKGREEN}\nEste programa fue creado gracias a Schizobeyond y Amit, de los cuales usamos algunos recursos.{bcolors.ENDC}")

print(f"{bcolors.WARNING}\nEste programa se iniciará en unos segundos...{bcolors.ENDC}")
time.sleep(5)
print(f"{bcolors.OKGREEN}\n¡Comencemos!{bcolors.ENDC}")
os.system("cls")

result = subprocess.run('wmic computersystem get PCSystemType', capture_output=True, text=True)

if '2' in result.stdout:
    print(f"{bcolors.OKGREEN}Este programa no es compatible con Laptops o Notebooks, no es recomendable forzar el temporizador.{bcolors.ENDC}")
    print(f"{bcolors.WARNING}\nEl programa se cerrará.{bcolors.ENDC}")
    time.sleep(5)
    sys.exit()

result = subprocess.run('wmic os get Caption', capture_output=True, text=True)

if 'Windows 11' in result.stdout:
    print(f"{bcolors.OKGREEN}El sistema operativo es Windows 11.{bcolors.ENDC}")
    
    if 'GlobalTimerResolutionRequest' in subprocess.run('reg.exe query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\kernel"', capture_output=True, text=True).stdout:
        print(f"{bcolors.WARNING}\nADVERTENCIA: {bcolors.ENDC}")
        print (f"{bcolors.WARNING}\nSi elimina la clave GlobalTimerResolutionRequest, no podrás usar la implementación del viejo Temporizador.{bcolors.ENDC}")
        opcion_11 = input("\nDesea eliminar la clave GlobalTimerResolutionRequest? (Y/N): ")

        if opcion_11.upper() == "Y":
            subprocess.run('reg.exe delete "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "GlobalTimerResolutionRequest" /f', capture_output=True, text=True)
            print("Se ha eliminado la clave GlobalTimerResolutionRequest del registro.")
            time.sleep(5)
            os.system("cls")
            print(f"{bcolors.WARNING}\nSe requiere reiniciar la PC para que se apliquen los cambios.{bcolors.ENDC}")
            print("\nLa PC se reiniciará en 10 segundos...")
            time.sleep(10)
            os.system('shutdown /r /t 0')

        elif opcion_11.upper() == "N":
            print(f"{bcolors.OKGREEN}\nLa clave GlobalTimerResolutionRequest no será eliminada.{bcolors.ENDC}")
            time.sleep(5)

        else:
            print(f"{bcolors.OKGREEN}Opción no válida. Presione Enter para continuar...{bcolors.ENDC}")
    else:
        print(f"{bcolors.WARNING}\nSeleccione una opción: {bcolors.ENDC}")
        print("\n1. Agregar GlobalTimerResolutionRequest.")
        opcion_11 = input("\nIngrese una opción (1): ")

        if opcion_11 == "1":
            subprocess.run('reg.exe add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "GlobalTimerResolutionRequest" /t REG_DWORD /d "1" /f', capture_output=True, text=True)
            print(f"{bcolors.OKGREEN}\nSe ha agregado la clave GlobalTimerResolutionRequest al registro.{bcolors.ENDC}")
            time.sleep(5)
            os.system("cls")
            print(f"{bcolors.WARNING}\nSe requiere reiniciar la PC para que se apliquen los cambios.{bcolors.ENDC}")
            print(f"{bcolors.WARNING}\nVuelve a ejecutar Timer.exe una vez reiniciado.{bcolors.ENDC}")
            print("\nLa PC se reiniciará en 10 segundos...")
            time.sleep(10)
            os.system('shutdown /r /t 0')

        else:
            print(f"{bcolors.OKGREEN}Opción no válida. Presione Enter para continuar...{bcolors.ENDC}")
            time.sleep(5)
else:
    print("El sistema operativo no es Windows 11.")

# Definir la cadena de opciones
opciones = "\n1.  5000 (0.5000)\n2.  10000 (1.000)"
subprocess.Popen("start cmd /k Measure-Sleep.exe", shell=True)

# Solicitar al usuario la opción de resolución
while True:
    os.system('cls' if os.name == 'nt' else 'clear') # Borrar la pantalla
    print(f"{bcolors.WARNING}Seleccione una opción:\n{bcolors.ENDC}" + opciones)
    opcion = input(f"{bcolors.WARNING}\n> {bcolors.ENDC}")
    
    # Verificar la opción ingresada y ejecutar la acción correspondiente
    if opcion == "1":
        print(f"{bcolors.OKGREEN}La resolución se ha establecido en 5000 (0.500).{bcolors.ENDC}")
        print(f"{bcolors.WARNING}\nSe está ejecutando SetTimerResolution.exe, puedes detenerlo en el Administrador de Tareas.{bcolors.ENDC}")
        os.system("SetTimerResolution.exe --resolution 5000 --no-console")
        break
    
    elif opcion == "2":
        print(f"{bcolors.OKGREEN}La resolución se ha establecido en 10000 (1.000).{bcolors.ENDC}")
        print(f"{bcolors.WARNING}\nSe está ejecutando SetTimerResolution.exe, puedes detenerlo en el Administrador de Tareas.{bcolors.ENDC}")
        os.system("SetTimerResolution.exe --resolution 10000 --no-console")
        break
    
    else:
        print(f"{bcolors.OKGREEN}Opción no válida. Presione Enter para continuar...{bcolors.ENDC}")
        input()

## Créditos:

## MeasureSleep / SetTimerResolution.exe "Gracias a Amit".
## Clave del Registro "Gracias a SchizoBeyond".