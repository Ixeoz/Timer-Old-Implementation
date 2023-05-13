import os
import time
import subprocess
import ctypes

# Obtener el identificador de la ventana actual
hwnd = ctypes.windll.kernel32.GetConsoleWindow()

# Definir la posición de la ventana
left = 0
top = 355

# Cambiar la posición de la ventana
ctypes.windll.user32.SetWindowPos(hwnd, None, left, top, 0, 355, 0x0001)

# Colores para la interfaz
class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

os.system("mode con cols=110 lines=20")

print("***********************************************")
print("*                                             *")
print("*      Bienvenidos al MeasureSleep.           *")
print("*                                             *")
print("***********************************************")
print("\nEste programa permite ver el MeasureSleep y ver la variabilidad del temporizador en los juegos,")
print("o en el programa que quieras verificar para ver si hay una fluctuación en el temporizador al forzarlo.")
print("forzar a 0.500ms si se requiere el viejo Timer.")
print(f"{bcolors.WARNING}\nTe recomendamos hacer entre 50 a 100 samples para tener mayor visibilidad de resultados.{bcolors.ENDC}")
print(f"{bcolors.OKGREEN}\nEste programa fue basado en Amit, de los cuales usamos algunos recursos.{bcolors.ENDC}")


print(f"{bcolors.WARNING}\nEste programa se iniciará en unos segundos...{bcolors.ENDC}")
time.sleep(10)
os.system("cls")

def ejecutar_measure_sleep(samples):
    # Ejecutar el archivo MeasureSleep con los argumentos deseados
    subprocess.run(["MeasureSleep", "--samples", samples])
    
    # Pausa para dar tiempo al usuario a revisar los resultados
    input(f"{bcolors.OKGREEN}\nPresiona Enter para continuar...{bcolors.ENDC}")
    
while True:
    # Limpiar la terminal antes de mostrar el mensaje
    os.system("cls")
    
    # Pedir al usuario que ingrese el número de samples
    while True:
        samples = input(f"{bcolors.WARNING}Ingresa el valor para --samples (debe ser un número entero): {bcolors.ENDC}")
        if samples.isdigit():
            break
        else:
            print("Error: debes ingresar un número entero.")
    
    # Ejecutar el programa MeasureSleep
    ejecutar_measure_sleep(samples)
    
    # Preguntar si el usuario desea realizar otra prueba
    while True:
        respuesta = input(f"{bcolors.WARNING}\n¿Deseas realizar otra prueba? (Y/N): {bcolors.ENDC}")
        if respuesta.upper() == "Y":
            break
        elif respuesta.upper() == "N":
            print("¡Gracias por usarlo!")
            exit()
        else:
            print("Respuesta inválida. Por favor, ingresa 'Y' para sí o 'N' para no.")
