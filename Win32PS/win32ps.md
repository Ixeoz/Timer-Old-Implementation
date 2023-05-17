# Win32PrioritySeparation

Win32PrioritySeparation es una entrada en el registro de Windows que especifica la estrategia utilizada para optimizar el tiempo del procesador en el sistema. El valor de esta entrada determina, en parte, cuánto tiempo reciben los hilos de un proceso cada vez que se programan y cuánto puede variar el tiempo asignado. También afecta la prioridad relativa de los hilos de los procesos en primer y segundo plano.

Pero claro, esto tiene mucha más profundidad, entra el planificador de procesos que es un componente del Sistema Operativo para asignar los recursos del sistema. Entra el uso de uno de los algoritmos más usados como [Round Robin](https://es.wikipedia.org/wiki/Planificaci%C3%B3n_Round-robin), que esté asigna un tiempo de procesador fijo a cada proceso y subproceso antes de pasar a otro.

 la configuración de quantum modifica el valor del registro:
 ```
 Path: HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl

 DWORD: Win32PrioritySeparation
 ```

 Este valor del registro define si los hilos en el proceso de primer plano deben tener sus quantums aumentados y, si es así, la cantidad del aumento. Este valor consta de **6 bits** divididos en tres campos de **2 bits (AABBCC)**. Cada conjunto de dos bits determina una característica diferente de la estrategia de optimización.

- Los dos bits más altos **(AABBCC)** determinan si cada intervalo del procesador es relativamente largo o corto.

- Los dos bits del medio **(AABBCC)** determinan si la longitud del intervalo varía o es fija.

- Los dos bits más bajos **(AABBCC)** determinan si los hilos de los procesos en primer plano obtienen más tiempo del procesador que los hilos de los procesos en segundo plano cada vez que se ejecutan.

[Microsoft Documentation](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwj54Mu58vz-AhUqQzABHfowCmAQFnoECAoQAQ&url=https%3A%2F%2Fwww.techpowerup.com%2Fforums%2Fattachments%2Fwin32priorityseparation-_-microsoft-docs-pdf.163992%2F&usg=AOvVaw226tFMxny4dfXDvQ7tdOTi)

Solamente se leen **6 bits**, el valor máximo que se puede representar en hexadecimal sería ``0x3F``, que es igual a ``00111111`` en binario.

**Ejemplos:**

- Si el valor del registro es ``0x3F``, los **6 bits** menos significativos serían ``111111``. Si el valor del registro es ``0x2A``, los **6 bits** menos significativos serían ``101010``.

- Si el valor del registro es ``0xFFF3891``, que es igual a ``1111111111110011100010010001`` en binario, solo se leerían los **6 bits** menos significativos, que serían ``010001``. Esto se puede representar en hexadecimal como ``0x11``.

- Digamos que el valor actual del registro es ``0x2``, que es igual a ``000010`` en binario. Si el usuario quiere cambiar la configuración para que los hilos de los procesos en primer plano obtengan más tiempo del procesador que los hilos de los procesos en segundo plano cada vez que se ejecutan, puede cambiar el valor del registro a ``0x26``, que es igual a ``100110`` en binario. Al cambiar el valor del registro a ``0x26``, el usuario ha especificado intervalos de procesador cortos y variables en los que los procesos en primer plano obtienen tres veces más tiempo de procesador que los procesos en segundo plano.

Esto específica los **Quantums** y su longitud relativa de los hilos, entre **"shorts y longs"**. En este punto, define la(s) variable(s) de los **Quantums** y su separación de prioridad. Y va a determinar el **Quantum** que se utilizará cuando la variable está habilitada. Entonces, el propio planificado de Windows habitualmente apunta las prioridades de los hilos por una funcon de prioridad. Así que esto puede reducir las latencias, porque los hilos son más rápidos a los eventos que se quedan en **pausa / espera** y así hay más constancia. Pero, entonces, si depende de la velocidad del clock, también dependería del propio [HAL](https://en.wikipedia.org/wiki/Hardware_abstraction), ya que oculta las interruociones y los mecanismos de multiprocesador, porque esto ya dependería de la propia máquina, esto sería parte de los controladores que estén escritos por el propio usuario.

La prioridad de los hilos que no están en tiempo real. Pero en unos casos se deben eliminar el **PriorityBoost**, porque hay hilos de ajuste que pierden su **Boost** y da su prioridad a otro hilo que apenas está arrancando. Pero entonces el **seed** que se elige por el núcleo para **"cierto proceso"** es creado aleatoriamente por el algoritmo [Round Robin](https://es.wikipedia.org/wiki/Planificaci%C3%B3n_Round-robin) se asigna, si se aplica **LGAT** y se fuerza al **0** pero si hay **1**, siempre se va a elegir ese si es que existe.

## **Table Quantum Values**

|              | **Short Quantum Index** | **Long Quantum Index** |
|--------------|-------------------------|------------------------|
| **Variable** | 6  12 18                | 12 24 36               |
| **Fixed**    | 18 18 18                | 36 36 36               |

El **Quantum** es la cantidad del tiempo que se ejecuta el subproceso antes de que Windows verifique si hay otro subproceso con la misma prioridad en la cual se espera para ejecutarse. En caso tal de que, un subproceso complete su Quantum y no hay otros subprocesos de su prioridad, lo que hará el Windows es que permitirá que el subproceso se vaya a ejecutar en el próximo **Quantum**. Así que la duración del intervalo del reloj depende del Hardware y las frecuencias de las interrupciones dependen del [HAL](https://en.wikipedia.org/wiki/Hardware_abstraction), no del núcleo.

Entonces, para determinar los **Ciclos del Reloj por Quantum**, se debe saber cuál es el intervalo del temporizador que por defecto ***(normalmente)*** sería ``15.625000``

Para hacer esto se requiere: [WinDBG](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/debugger-download-tools), conjunto de [Windows SDK](https://go.microsoft.com/fwlink/p/?linkid=2196241).

- Se necesita entrar en modo debug:

```
bcdedit.exe /debug on
```
- Se debe conocer el valor almacenado del campo MHz.
```
ldk > !cpuinfo
```
- Básicamente, es el número de **ciclos de la CPU** que ocurre cada segundo *(cantidad que depende del Hardaware)*.

  - Por ejemplo: **4.250.000.000.**

```
lkd > dd nt!KiCyclesPerClockQuantum l1
```

- Todo resultado tendrá variación.
```
fffff803`144fb140  0151c278
```

Se toma la tercera opción ``0151c278``.

- Dividir el temporizador por **1000**, ya que equivale a un segundo. Entonces. se se activa **0,015625**.

```
15.625000 / 1000 = 0.015625
```
- Multiplicar el número de ciclos por el segundo en el que se activa.

```
4250 * 0.015625 = 66.406.625 
```

- Las unidades cuánticas son un tercio del intervalo del rejo, así que dividimo el ciclo entre tres.

```
66.406.625 / 3 = 22.135.416 -> Representado en Hexadecimal -> 0151c278 
```

- Estos valores cambian acorde al **Win32PrioritySeparation** asigando:

```
lkd > dd PsPrioritySeparation l1
```
```
lkd > dd PsForeGroundQuantum l1
```

## Algunos ejemplos:

- **Win32PrioritySeparation 26 Hexadecimal**.
```
lkd > dd PsPrioritySeparation l1
fffff803`144fc5c4  00000002
```
```
lkd > dd PsForeGroundQuantum l1
fffff803`1452e874  06 0c 12
```
- **Win32PrioritySeparation 28 Hexadecimal**.
```
lkd > dd PsPrioritySeparation l1
fffff803`144fc5c4  00000001
```
```
lkd > dd PsForeGroundQuantum l1
fffff803`1452e874  0c 18 24
```

# Referencias:

- [Processes, Threads, and Jobs in the Windows Operating System](https://www.microsoftpressstore.com/articles/article.aspx?p=2233328&seqNum=7).

- [The truth behind ambiguous values | AMIT](https://github.com/amitxv/PC-Tuning/blob/main/docs/research.md#win32priorityseparation).

- [If you modify Win32PrioritySeparation (process foreground and background quantum lengths) in the registry does it update in realtime or does it require a system restart? | Djdallmann](https://github.com/djdallmann/GamingPCSetup/blob/master/CONTENT/RESEARCH/WINKERNEL/README.md).
