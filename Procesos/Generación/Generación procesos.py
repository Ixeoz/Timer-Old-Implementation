import multiprocessing
import tkinter as tk

def create_window():
    window = tk.Tk()
    label = tk.Label(window, text="Procesos Creados.")
    label.pack()
    window.mainloop()

if __name__ == '__main__':
    processes = []
    for _ in range(50): # Cantidad de procesos creados.
        p = multiprocessing.Process(target=create_window)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
