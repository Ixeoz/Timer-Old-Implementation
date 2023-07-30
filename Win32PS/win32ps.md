# Win32PrioritySeparation

Win32PrioritySeparation es una entrada en el registro de Windows que especifica la estrategia utilizada para optimizar el tiempo del procesador en el sistema. El valor de esta entrada determina, en parte, cuánto tiempo reciben los hilos de un proceso cada vez que se programan y cuánto puede variar el tiempo asignado. También afecta la prioridad relativa de los hilos de los procesos en primer plano (o foreground, que es lo que estás haciendo en ese momento) y segundo plano (o background/CSRSS.exe, que es obligatoria para la entrada de dispositivos K&M).

Pero claro, esto tiene mucha más profundidad, entra el planificador de procesos que es un componente del Sistema Operativo para asignar los recursos del sistema. Entra el uso de uno de los algoritmos más usados como [Round Robin](https://es.wikipedia.org/wiki/Planificaci%C3%B3n_Round-robin), que esté asigna un tiempo de procesador fijo a cada proceso y subproceso antes de pasar a otro.

 **La configuración de quantum modifica el valor del registro:**
 ```
Path: HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl

DWORD: Win32PrioritySeparation
 ```

 Este valor del registro define si los hilos en el proceso de primer plano deben tener sus quantums aumentados y, si es así, la cantidad del aumento. Este valor consta de **6 bits** divididos en tres campos de **2 bits (AABBCC)**. Cada conjunto de dos bits determina una característica diferente de la estrategia de optimización.

- Los dos bits más altos (**AA**BBCC) determinan si cada intervalo del procesador es relativamente largo o corto.

- Los dos bits del medio (AA**BB**CC) determinan si la longitud del intervalo varía o es fija.

- Los dos bits más bajos (AABB**CC**) determinan si los hilos de los procesos en primer plano obtienen más tiempo del procesador que los hilos de los procesos en segundo plano cada vez que se ejecutan.

[Microsoft Documentation](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwj54Mu58vz-AhUqQzABHfowCmAQFnoECAoQAQ&url=https%3A%2F%2Fwww.techpowerup.com%2Fforums%2Fattachments%2Fwin32priorityseparation-_-microsoft-docs-pdf.163992%2F&usg=AOvVaw226tFMxny4dfXDvQ7tdOTi).

Solamente se leen **6 bits**, el valor máximo que se puede representar en hexadecimal sería ``0x3F``, que es igual a ``00111111`` en binario.

**Ejemplos:**

- Si el valor del registro es ``0x3F``, los **6 bits** menos significativos serían ``111111``. Si el valor del registro es ``0x2A``, los **6 bits** menos significativos serían ``101010``.

- Si el valor del registro es ``0xFFF3891``, que es igual a ``1111111111110011100010010001`` en binario, solo se leerían los **6 bits** menos significativos, que serían ``010001``. Esto se puede representar en hexadecimal como ``0x11``.

- Digamos que el valor actual del registro es ``0x2``, que es igual a ``000010`` en binario. Si el usuario quiere cambiar la configuración para que los hilos de los procesos en primer plano obtengan más tiempo del procesador que los hilos de los procesos en segundo plano cada vez que se ejecutan, puede cambiar el valor del registro a ``0x26``, que es igual a ``100110`` en binario. Al cambiar el valor del registro a ``0x26``, el usuario ha especificado intervalos de procesador cortos y variables en los que los procesos en primer plano obtienen tres veces más tiempo de procesador que los procesos en segundo plano.

Esto específica los **Quantums** y su longitud relativa de los hilos, entre **"shorts y longs"**. En este punto, define la(s) variable(s) de los **Quantums** y su separación de prioridad. Y va a determinar el **Quantum** que se utilizará cuando la variable está habilitada. Entonces, el propio planificado de Windows habitualmente apunta las prioridades de los hilos por una función de prioridad. Así que esto puede reducir las latencias, porque los hilos son más rápidos a los eventos que se quedan en **pausa / espera** y así hay más constancia. Pero, entonces, si depende de la velocidad del clock, también dependería del propio [HAL](https://en.wikipedia.org/wiki/Hardware_abstraction), ya que oculta las interrupciones y los mecanismos de multiprocesador, porque esto ya dependería de la propia máquina, esto sería parte de los controladores que estén escritos por el propio usuario.

La prioridad de los hilos que no están en tiempo real. Pero en unos casos se deben eliminar el **PriorityBoost**, porque hay hilos de ajuste que pierden su **Boost** y da su prioridad a otro hilo que apenas está arrancando. Pero entonces el **seed** que se elige por el núcleo para **"cierto proceso"** es creado aleatoriamente por el algoritmo [Round Robin](https://es.wikipedia.org/wiki/Planificaci%C3%B3n_Round-robin) se asigna, si se aplica y se fuerza al **0** pero si hay **1**, siempre se va a elegir ese si es que existe.

## **Table Quantum Values**

|              | **Short Quantum Index** | **Long Quantum Index** |
|--------------|-------------------------|------------------------|
| **Variable** | 6  12 18                | 12 24 36               |
| **Fixed**    | 18 18 18                | 36 36 36               |

- **Short** y **Long** se refieren a la duración relativa de cada intervalo del procesador. Los dos bits más altos del valor del registro determinan si cada intervalo del procesador es relativamente largo o corto.

- **Variable** y **Fixed** se refieren a si la duración del tiempo del procesador de los dos bits intermedios del valor del registro determina si la duración del intervalo varía o es fija. También determina si los hilos de los procesos en primer plano tienen intervalos de procesador más largos que los de los procesos en segundo plano. Si el intervalo del procesador es **Fixed**, ese intervalo se aplica por igual a los hilos de los procesos en primer y segundo plano. Si el intervalo del procesador es **Variable**, la duración del tiempo que cada hilo se ejecuta varía, pero la relación entre el tiempo del procesador de los hilos en primer plano y los hilos en segundo plano es fija.

**Ejemplos:**

- Imaginemos que tenemos dos procesos en ejecución en Windows: un proceso en primer plano (por ejemplo, una aplicación de edición de texto) y un proceso en segundo plano (por ejemplo, una descarga de archivo). El sistema operativo asigna tiempo del procesador a cada uno de estos procesos en intervalos.

- Si el valor está configurado para usar intervalos **Short**, cada proceso recibirá intervalos más cortos, pero más frecuentes de tiempo del procesador. Si está configurado para usar intervalos **Long**, cada proceso recibirá intervalos más largos, pero menos frecuentes de tiempo del procesador.

- Si el valor está configurado para usar intervalos **Variable**, la duración del tiempo del procesador asignado a cada proceso puede variar. Por ejemplo, el proceso en primer plano podría recibir más tiempo del procesador cuando el usuario está interactuando activamente con él y menos tiempo cuando está inactivo. Si está configurado para usar intervalos fijos **Fixed**, la duración del tiempo del procesador asignado a cada proceso será constante.

En [KernelOS](https://dsc.gg/kernelos) hay una carpeta en el PATH: 
```
C:\Windows\POST-INSTALL\Tweaking\Win32Priority
```
## **Tabla Win32PrioritySeparation que están en KernelOS.**

| Hexadecimal   | Interval | Length   | 
| --------------|----------|----------|
| 0x2           | Short    | Variable | 
| 0x1a          | Short    | Fixed    | 
| 0x2a          | Short    | Variable | 
| 0x10d         | Short    | Variable | 
| 0x14          | Long     | Variable | 
| 0x16          | Long     | Variable |
| 0x26          | Short    | Variable | 
| 0x28          | Short    | Fixed    | 
| 0x41ffaca5    | Long     | Variable | 
| 0x55fffff     | Short    | Variable | 
| 0x7777        | Short    | Variable |
| 0x666666      | Short    | Variable |
| 0xfff3891     | Long     | Variable |
| 0xfff9887     | Short    | Variable | 
| 0xfff55555    | Long     | Variable | 
| 0xffff3f91    | Long     | Variable |
| 0xffff9887    | Short    | Variable | 
| 0xfffff311    | Long     | Variable | 

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
- Básicamente, es el número de **ciclos de la CPU** que ocurre cada segundo *(cantidad que depende del Hardware)*.

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

- Las unidades cuánticas son un tercio del intervalo del rejo, así que dividimos el ciclo entre tres.

```
66.406.625 / 3 = 22.135.416 -> Representado en Hexadecimal -> 0151c278 
```

- Estos valores cambian acorde al **Win32PrioritySeparation** asignado:

```
lkd > dd PsPrioritySeparation l1
```
```
lkd > db PspForeGroundQuantum l3
```

## Algunos ejemplos:

- **Win32PrioritySeparation 26 Hexadecimal**.
```
lkd > dd PsPrioritySeparation l1
fffff803`144fc5c4  00000002
```
```
lkd > db PspForeGroundQuantum l3
fffff803`1452e874  06 0c 12
```
- **Win32PrioritySeparation 28 Hexadecimal**.
```
lkd > dd PsPrioritySeparation l1
fffff803`144fc5c4  00000001
```
```
lkd > db PspForeGroundQuantum l3
fffff803`1452e874  0c 18 24
```
- Por otro lado, para verificar el **BasePriority** y **QuantumReset**:

```
lkd > .process
Implicit process is now ffff8a0f`332ba180
```
- El valor **332ba180**, es el que se debe copiar.
```
lkd > dt _KPROCESS 332ba180
nt!_KPROCESS <información>
```

- En el momento que se ejecute, tendrán la información de **BasePriority** y **QuantumReset**.


# Referencias:

- [Processes, Threads, and Jobs in the Windows Operating System](https://www.microsoftpressstore.com/articles/article.aspx?p=2233328&seqNum=7).

- [The truth behind ambiguous values | AMIT](https://github.com/amitxv/PC-Tuning/blob/main/docs/research.md#win32priorityseparation).

- [If you modify Win32PrioritySeparation (process foreground and background quantum lengths) in the registry does it update in realtime or does it require a system restart? | Djdallmann](https://github.com/djdallmann/GamingPCSetup/blob/master/CONTENT/RESEARCH/WINKERNEL/README.md).

- [Windows System Internals 7e Part 1](https://empyreal96.github.io/nt-info-depot/Windows-Internals-PDFs/Windows%20System%20Internals%207e%20Part%201.pdf).
