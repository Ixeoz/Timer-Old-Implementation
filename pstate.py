import pynvml
import time

pynvml.nvmlInit()

handle = pynvml.nvmlDeviceGetHandleByIndex(0)

def show_pstate():
    try:
        pstate = pynvml.nvmlDeviceGetPerformanceState(handle)
        print(f'PState: P{pstate}')
    except pynvml.NVMLError as error:
        print(f'Error al obtener el estado PState: {error}')

try:
    while True:
        show_pstate()
        time.sleep(0.5)
finally:
    pynvml.nvmlShutdown()