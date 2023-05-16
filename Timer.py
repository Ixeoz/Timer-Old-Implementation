import os
import time
import subprocess
import ctypes
import winreg
import requests
import shutil

# Obtener el identificador de la ventana actual.
hwnd = ctypes.windll.kernel32.GetConsoleWindow()

# Definir la posición de la ventana.
left = 0
top = 10

# Cambiar la posición de la ventana.
ctypes.windll.user32.SetWindowPos(hwnd, None, left, top, 0, 10, 0x0001)

# Colores para la interfaz.
class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

os.system("mode con cols=110 lines=20")

print("***********************************************")
print("*                                             *")
print("*    Bienvenidos al configurador de Timer.    *")
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

result = subprocess.run('wmic os get Caption', capture_output=True, text=True)
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
    version_string = winreg.QueryValueEx(key, "DisplayVersion")[0]

output = subprocess.check_output("wmic os get Caption,Version /value", shell=True).decode()
for line in output.splitlines():
    if "Version=" in line:
        version_wmic = line.split("=")[1]
        break
else:
    print("No se pudo encontrar la información de la versión.")
    exit()
    
if 'Windows 11' in result.stdout:
    print(f"{bcolors.OKGREEN}El sistema operativo es Windows 11 {version_string} ({version_wmic}). {bcolors.ENDC}")
    time.sleep(5)
    os.system("cls")

    if 'GlobalTimerResolutionRequest' in subprocess.run('reg.exe query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\kernel"', capture_output=True, text=True).stdout:
        print(f"{bcolors.WARNING}ADVERTENCIA: {bcolors.ENDC}")
        print (f"{bcolors.WARNING}\nSi elimina la clave GlobalTimerResolutionRequest, no podrás usar la implementación del viejo Temporizador.{bcolors.ENDC}")
        opcion_11 = input("\nDesea eliminar la clave GlobalTimerResolutionRequest? (Y/N): ")

        if opcion_11.upper() == "Y":
            subprocess.run('reg.exe delete "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "GlobalTimerResolutionRequest" /f', capture_output=True, text=True)
            os.system("cls")
            print(f"{bcolors.OKGREEN}Se ha eliminado la clave GlobalTimerResolutionRequest del registro.{bcolors.ENDC}")
            time.sleep(5)
            os.system("cls")
            print(f"{bcolors.WARNING}Se requiere reiniciar la PC para que se apliquen los cambios.{bcolors.ENDC}")
            print("\nLa PC se reiniciará en 10 segundos...")
            time.sleep(10)
            os.system('shutdown /r /t 0')

        elif opcion_11.upper() == "N":
            os.system("cls")
            print(f"{bcolors.OKGREEN}La clave GlobalTimerResolutionRequest no será eliminada.{bcolors.ENDC}")
            time.sleep(5)

        else:
            print(f"{bcolors.OKGREEN}Opción no válida. Presione Enter para continuar...{bcolors.ENDC}")
    else:
        print(f"{bcolors.WARNING}Seleccione una opción: {bcolors.ENDC}")
        print("\n1. Agregar GlobalTimerResolutionRequest.")
        opcion_11 = input(f"{bcolors.WARNING}\nIngrese una opción: {bcolors.ENDC}")

        if opcion_11 == "1":
            subprocess.run('reg.exe add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "GlobalTimerResolutionRequest" /t REG_DWORD /d "1" /f', capture_output=True, text=True)
            os.system("cls")
            print(f"{bcolors.OKGREEN}Se ha agregado la clave GlobalTimerResolutionRequest al registro.{bcolors.ENDC}")
            time.sleep(5)
            os.system("cls")
            print(f"{bcolors.WARNING}Se requiere reiniciar la PC para que se apliquen los cambios.{bcolors.ENDC}")
            print(f"{bcolors.WARNING}\nVuelve a ejecutar Timer.exe una vez reiniciado.{bcolors.ENDC}")
            print("\nLa PC se reiniciará en 10 segundos...")
            time.sleep(10)
            os.system('shutdown /r /t 0')

        else:
            print(f"{bcolors.OKGREEN}Opción no válida. Presione Enter para continuar...{bcolors.ENDC}")
            time.sleep(5)

elif 'Windows 10' in result.stdout:
    os.system('cls')
    print(f"{bcolors.OKGREEN}El sistema operativo es Windows 10 {version_string} ({version_wmic}). {bcolors.ENDC}")
    time.sleep(5)

else:
    print("El sistema operativo no es Windows 11.")

# Definir la cadena de opciones.
opciones = "\n1.  5000 (0.5000)\n2.  10000 (1.000) / Valor Default"
subprocess.Popen("start cmd /k Measure-Sleep.exe", shell=True)

# Solicitar al usuario la opción de resolución.
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{bcolors.WARNING}Seleccione una opción:\n{bcolors.ENDC}" + opciones)
    opcion = input(f"{bcolors.WARNING}\n> {bcolors.ENDC}")

    if opcion == "1":
        os.system('cls')
        pregunta = input(f"{bcolors.WARNING}¿Quieres que se ejecute el ajustador de temporizador cuando enciendas la PC? (S/N) {bcolors.ENDC}")
        if pregunta.lower() == "s":
            # Descargar el archivo
            url = "https://cdn.discordapp.com/attachments/1020161708477661184/1108097896571736198/StartTimer.bat"
            filename = "StartTimer.bat"
            r = requests.get(url)
            with open(filename, 'wb') as f:
                f.write(r.content)
            # Mover el archivo a shell:startup
            startup_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
            shutil.move(filename, startup_path)
            os.system('cls')
            print(f"{bcolors.WARNING}Se ha descargado y movido el archivo StartTimer.bat.{bcolors.ENDC}")
            time.sleep(5)
        elif pregunta.lower() == "n":
            os.system('cls')
            print(f"{bcolors.WARNING}No se ejecutará el ajustador de temporizador al iniciar la PC.{bcolors.ENDC}")
            time.sleep(5)

        else:
            os.system('cls')
            print(f"{bcolors.OKGREEN}Opción no válida. Presione Enter para continuar...{bcolors.ENDC}")
            input()

        os.system('cls')
        print(f"{bcolors.OKGREEN}La resolución se ha establecido en 5000 (0.500).{bcolors.ENDC}")
        print(f"{bcolors.WARNING}\nSe está ejecutando SetTimerResolution.exe, puedes detenerlo en el Administrador de Tareas.{bcolors.ENDC}")
        print(f"{bcolors.OKGREEN}\nPuedes cerrar está ventana.{bcolors.ENDC}")
        os.system("SetTimerResolution.exe --resolution 5000 --no-console")
        break

    elif opcion == "2":
        os.system('cls')
        print(f"{bcolors.OKGREEN}La resolución se ha establecido en 10000 (1.000) / Valor Default.{bcolors.ENDC}")
        print(f"{bcolors.WARNING}\nSe está ejecutando SetTimerResolution.exe, puedes detenerlo en el Administrador de Tareas.{bcolors.ENDC}")
        print(f"{bcolors.OKGREEN}\nPuedes cerrar está ventana.{bcolors.ENDC}")
        os.system("SetTimerResolution.exe --resolution 10000 --no-console")
        break
    
    else:
        os.system('cls')
        print(f"{bcolors.OKGREEN}Opción no válida. Presione Enter para continuar...{bcolors.ENDC}")
        input()

## Créditos:

## MeasureSleep.exe / SetTimerResolution.exe "Gracias a Amit".
## Clave del Registro "Gracias a SchizoBeyond".