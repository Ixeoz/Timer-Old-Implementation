# **La cantidad o conteo de procesos NO importa.**

La cantidad de procesos que vemos en el Task Manager / Administrador de tareas, realmente NO influye en el rendimiento dependiendo al conteo. Con esto quiero decir que hay cosas que influyen como: los **Cycles Delta** y los **Context Switch**.

[Generación de Procesos](https://github.com/Ixeoz/Timer-Old-Implementation/blob/main/Procesos/Generaci%C3%B3n/Generaci%C3%B3n%20procesos.py).

# **Prueba de rendimiento:**

![](https://i.imgur.com/NNUy9F2.png)

![](https://i.imgur.com/PyJIgRn.png)

## **Primero debemos tener conceptos fundamentales para comprender los Procesos.**

**¿Qué es un proceso?**

- Es un programa en ejecución.

**¿Cuál es la diferencia entre un programa y un proceso?**

- **Los programas son pasivos:** son archivos ejecutables que se almacenan en la memoria.

- **Los programas son activos:** los programas se convierten en procesos cuando el archivo ejecutable es cargado en memoria.

    Múltiples procesos pueden ejecutar diferentes instancias de un programa.

**¿Qué conforma un proceso?**

- **Sección de Texto:** es el código.

- **Contexto:** esto incluye el PC **(Program Counter)** y los registros del procesador.

- **Stack:** contiene parámetros de las funciones, las direcciones de retorno y variables locales.

- **Sección de datos:** contiene las variables globales.

- **Heap:** contiene la memoria dinámica que se asigna en tiempo de ejecución.

![](https://i.imgur.com/vsWlrc7.png)

- **Diseño de memoria en C:**

![](https://i.imgur.com/sDH9QOT.png)

**Estados de un Proceso.**

- **New:** se está creando el proceso.

- **Running:** la CPU está ejecutando las instrucciones de su programa.

- **Waiting:** el proceso está esperando a que ocurra algún evento.

- **Ready:** el proceso está esperando a que le asignen una CPU.

- **Terminated:** el proceso ha terminado su ejecución.

**Diagrama de los estados de un proceso:**

![](https://i.imgur.com/3HHAIJq.jpg)

**El Sistema Operativo cómo administra los procesos.**

- Esto lo hace por medio de una estructura de datos Process Control Block **(PCB)**.

![](https://i.imgur.com/S55jnf5.png)


El **Process Control Block (PCB)** es una estructura de datos del núcleo del sistema operativo que contiene la información necesaria para gestionar un proceso concreto. En resumen, el PCB sirve como repositorio de cualquier información que pueda variar de un proceso a otro.

**Ejemplo de información almacenada en el PCB.**

![](https://i.imgur.com/oBUUDRN.png)

**¿Cómo hacen los programas para poder comunicarse con el Sistema Operativo?**

- Hacen llamados al Sistema:

```cpp
(system calls: count = read(fd, buffer, nbytes)
```
![](https://i.imgur.com/NKIjl0V.png)

**Llamados al Sistema fork () y exec ().**

- **fork ():** se utiliza para crear un proceso separado y duplicado.

- **exec ():** permite ejecutar un proceso especifico (incluyendo todos sus hilos). Cuando se lanza después de fork() reemplaza el espacio de memoria con el nuevo proceso. 

**Comportamiento de fork () y exec ():**

![](https://i.imgur.com/8LX0Doj.png)

**Fork ():**

- Se crea un nuevo proceso que tiene una relación **padre-hijo** con el proceso principal. El proceso secundario creado por **fork()** copia completamente el proceso principal, por lo que se ejecuta exactamente igual que el proceso principal y se procesa en paralelo con el proceso principal para competir por los recursos de la CPU. La diferencia es que el valor de retorno de **fork()** en el proceso principal y secundario es diferente. En el proceso secundario, el valor de retorno de **fork()** es 0, mientras que en el proceso principal es la identificación del proceso secundario generado.

**Vista en memoria:**

![](https://i.imgur.com/gvJTaHQ.jpg)

```cpp
------------                     ------------            ------------
| pid = 7  |   llamado a fork    | pid = 7  |   forks    | pid = 22 |
| ppid = 4 | ------------------> | ppid = 4 | ---------> | ppid = 7 |
| bash     |                     | bash     |            | bash     |
------------                     ------------            ------------
                                      |                       |
                                      | Esperando por pid 22  |
                                      |                       | Llamado a exec para ejecutar ls
                                      |                       V
                                      |                  ------------
                                      |                  | pid = 22 | 
                                      |                  | ppid = 7 |
                                      V                  | ls       |
                                 ------------            ------------
                                 | pid = 7  |                 | Sale
                                 | ppid = 4 | <----------------
                                 | bash     | 
                                 ------------
                                      |
                                      | Continúa
                                      V
```
## **Ejemplo:**
```cpp
#include <stdlib.h>
#include <stdio.h>
#include <sys/wait.h>
#include <sys/types.h>

int main ()
{  
    int i;
    pid_t pid;

    pid = fork(); // Crear un nuevo proceso.

    if (pid < 0)
        printf("Fallo de Fork\n")

    else if (pid == 0)
    {   
        for (i = 0; i < 5; i++)
            printf("Hijo[1] --> pid = %d y PPID %d i= %d \n", getpid(), getppid(), i); // Imprimir el PID del proceso hijo, el PID del proceso padre y el contador del bucle.
    }
    else
    {
        wait(NULL); // Esperar a que el proceso hijo termine.
        for (i = 0; i < 5; i++)
            printf("Rutina Proceso Padre: %d \n\n", i); // Imprimir el contador del bucle.
    }   
}
```
# **Context Switch.**

- En informática, un **Context Switch** es el proceso de almacenar el estado de un proceso o de un hilo, para poder restaurarlo y reanudar la ejecución desde el mismo punto más adelante. Esto permite que varios procesos compartan una única **CPU**, y es una característica esencial de un sistema operativo multitarea. No basta con guardar y restaurar el contexto de la **CPU**. También hay que guardar y restaurar otra información, por ejemplo el estado del proceso. Cuando la **CPU** cambia a otro proceso, el sistema debe guardar el estado del proceso anterior y restaurar el estado para el nuevo proceso mediante un cambio de contexto. El contexto de un proceso se representa en el **PCB**. El tiempo de cambio de contexto es una sobrecarga; el sistema no realiza ningún trabajo útil durante el cambio. El tiempo de cambio de contexto depende del soporte de hardware.

![](https://i.imgur.com/lrx1J7U.png)

## **Colas de procesos.**

- Ya hemos visto dos ejemplos de colas de procesos: la cola de listos y la cola de **E/S.**

- **Ready Queue:** conjunto de todos los procesos que residen en la memoria principal, listos y esperando para ejecutarse.

- **Device Queue:** conjunto de procesos en espera de un dispositivo de **E/S.**

![](https://i.imgur.com/pV5bJBw.png)

# **CPU Scheduling.**

## **Multiprogramación:**

![](https://i.imgur.com/olNw8yC.png)

## **Multitarea:**

![](https://i.imgur.com/Htd09OD.png)

## **Creación de proceso:**

![](https://i.imgur.com/qzmgPDG.png)

## **Planificador a corto plazo:**

- El planificador a corto plazo (STS), planificador de la CPU, selecciona qué proceso de la cola de espera en memoria debe ejecutarse a continuación y asigna la CPU.

## **Envío del planificador:**

- El programador de la CPU selecciona un proceso de entre los procesos en memoria que están LISTOS para ejecutarse y le da al proceso seleccionado el control de la CPU. Esta acción se denomina despacho del planificador (SD).

## **Planificador a largo plazo:**

- El planificador a largo plazo decide si un nuevo proceso debe ponerse en la cola de procesos listos en memoria principal o retrasarse. Cuando un proceso está listo para ejecutarse, se añade a la reserva de trabajos (en disco). Cuando la memoria RAM está suficientemente libre, algunos procesos se llevan de la reserva de trabajos a la cola de listos (en RAM).

- En algunos sistemas, el planificador a largo plazo puede estar ausente o ser mínimo. Por ejemplo, los sistemas de tiempo compartido, como los sistemas UNIX y Microsoft Windows, a menudo no tienen planificador a largo plazo, sino que simplemente ponen cada nuevo proceso en memoria para el planificador a corto plazo.

## **Planificador a medio plazo:**

- El programador a medio plazo elimina temporalmente procesos de la memoria principal y los coloca en el almacenamiento secundario y viceversa, lo que se conoce comúnmente como "cambiar en" y "intercambio".

![](https://i.imgur.com/QwnqAwl.png)


# **Clasificación de Procesos.**

En general, los procesos se pueden clasificar por las siguientes características:

- Interactivos.

- Batch.

- Tiempo Real.

- Limitados por E/S.

- Limitados por la CPU.

## **Interactivos:**

Los procesos interactivos interactúan constantemente con sus usuarios.

- Pasan mucho tiempo esperando pulsaciones de teclas y operaciones del ratón.

- Cuando se recibe una entrada, el proceso debe despertarse rápidamente, o el usuario encontrará que el sistema no responde. Normalmente, el retardo medio debe situarse
entre 50 y 150 ms. La varianza de este retardo también debe ser limitada, o el usuario considerará que el sistema es erróneo o el sistema resultará errático.

- Ejemplos: intérpretes de comandos, editores de texto, aplicaciones gráficas y juegos.

## **Batch:**

Los procesos por Batch no interactúan con usuarios.

- No necesitan responder.

- A menudo se ejecutan en segundo plano.

- A menudo son penalizados por el planificador.

- Ejemplos: compiladores, motores de búsqueda de bases de datos y cálculos científicos.

## **Tiempo Real:**

Los procesos en tiempo real tienen requisitos de programación muy estrictos.

- Nunca deben ser bloqueados por procesos de menor prioridad.

- Deben tener un tiempo de respuesta corto.

- Y lo que es más importante, el tiempo de respuesta debe tener una variación mínima.

- Ejemplos típicos: aplicaciones de vídeo y sonido, controladores de robots y programas que recogen datos de sensores físicos.

## **Evaluación de programadores de CPU mediante simulación.**

- Para evaluar diferentes algoritmos de programación de CPU, los datos obtenidos de ejecutables instrumentados pueden utilizarse como entrada en simulaciones.

![](https://i.imgur.com/iW1Igw0.png)


# **Hilos.**

## **Procesos monohilo y multihilo:**

![](https://i.imgur.com/80tU6BR.png)


## **Paralelismo:**

- En los sistemas paralelos, dos tareas se ejecutan **simultáneamente**.  

- Se habla de paralelismo cuando las tareas **se ejecutan literalmente al mismo tiempo**, por ejemplo, en un procesador multinúcleo.

## **Concurrencia:**

- Dos tareas son concurrentes si el orden de ejecución de las dos tareas en el tiempo **no está predeterminado**.

- La **aparición** de varias tareas ejecutándose a la vez.

- En realidad, las tareas se dividen en trozos que comparten el procesador con trozos de otra tarea intercalando su ejecución en el tiempo.

- Las tareas pueden iniciarse, ejecutarse y completarse en **periodos de tiempo que se solapan**.    

Para mejorar la eficiencia, los procesadores suelen utilizar internamente pipelines. Esto permite procesar varias instrucciones a la vez. Las instrucciones se siguen consumiendo en el pipeline de una en una.

![](https://i.imgur.com/xuYtDr6.jpg)

# **CPU multinúcleo.**

- Un procesador multinúcleo está compuesto por dos o más núcleos independientes.

- Se puede describir como un circuito integrado que tiene dos o más procesadores individuales (llamados núcleos en este sentido).

- Para aprovechar al máximo los ordenadores multinúcleo, los programadores tendrán que aprender a utilizar la programación concurrente.

## **Ejecución simultánea de subprocesos:**

- Los hilos se ejecutan por turnos en el único núcleo de la CPU. Al cambiar de un hilo a otro con la suficiente rapidez, parece que se ejecutan "al mismo tiempo". Como máximo, dos subprocesos pueden ejecutarse en paralelo (realmente al mismo tiempo) en una CPU de doble núcleo. En cada núcleo, los subprocesos se ejecutan por turnos, igual que en una CPU mononúcleo.                                                    

**Los núcleos múltiples nos proporcionan más potencia de cálculo.**

**Desafíos:** 

- Dividir las actividades.

- Equilibrio.

- División de datos.

- Dependencia de datos.

- Pruebas y depuración.

## **División de actividades:**
- Encontrar áreas en una aplicación que puedan dividirse en tareas separadas y concurrentes y potencialmente ejecutarse en paralelo en núcleos individuales.

## **Equilibrio:** 
- Si se pueden encontrar tareas que se ejecuten de forma concurrente, los programadores también deben asegurarse de que realicen el mismo trabajo de igual valor. Utilizar un núcleo de ejecución separado para una tarea que no aporta mucho valor al proceso global puede no merecer la pena.

## **División de datos:**

- Al igual que las aplicaciones se dividen en tareas separadas, los datos a los que acceden y manipulan las tareas deben dividirse para ejecutarse en núcleos separados.

## **Dependencia de datos:**
- Los datos a los que acceden las tareas deben examinarse en busca de dependencias entre dos o más tareas. En los casos en que una tarea se sincroniza para acomodar la dependencia de datos.


## **Pruebas y depuración:**

- Cuando un programa se ejecuta simultáneamente en varios núcleos, existen muchas rutas de ejecución diferentes. Probar y depurar estos programas concurrentes es inherentemente más difícil que probar y depurar aplicaciones de un solo hilo.

# **Programación utilizando memoria compartida con hilos:**

## **Estado Compartido.**
```cpp
# define N 1000
int BALANCE 0;
```
## **Hilo A.**

```cpp
for (int i = 0; i < N; i++) {
    BALANCE++;
}
```
## **Hilo B.**
```cpp
for (int i = 0; i < N; i++) {
    BALANCE--;
}
```

# **Intercalación de hilos de ejecución:**

```cpp
---------------------------         ------------------------------
   Hilo A (incrementado)  |         |     Hilo B (disminución)   |
-----------------------------------------------------------|-----|     
OP   | Operando     | $t0 | BALANCE | OP   | Operando      | $t0 |
-----|--------------|-----|---------|------|---------------|-----|
lw   | $t0,         |  0  |    0    |      |               |     |
-----|--------------|-----|---------|------|---------------|-----|
addi | $t0, $t0, 1  |  1  |    0    |      |               |     |
-----|--------------|-----|---------|------|---------------|-----|
sw   | $t0, BALANCE |  1  |    0    |      |               |     |
-----|--------------|-----|---------|------|---------------|-----|
     |              |     |    1    |      |               |     |
-----|--------------|-----|---------|------|---------------|-----|
     |              |     |    1    | lw   | $t0, BALANCE  |  1  |
-----|--------------|-----|---------| -----|---------------|-----|
     |              |     |    1    | addi | $t0, $t0, -1  |  0  |
-----|--------------|-----|---------|------|---------------|-----|
     |              |     |    0    | sw   | $t0, BALANCE  |  0  |
------------------------------------------------------------------
```

- Si las instrucciones se ejecutan en este orden, el incremento y el decremento se anulan mutuamente, y el **BALANCE** resultante es **0**.

```cpp
---------------------------         ------------------------------
   Hilo A (incrementado)  |         |     Hilo B (disminución)   |
-----------------------------------------------------------|-----|     
OP   | Operando     | $t0 | BALANCE | OP   | Operando      | $t0 |
-----|--------------|-----|---------|------|---------------|-----|
     |              |     |    0    |      |               |     |
-----|--------------|-----|---------|------|---------------|-----|
lw   | $t0,         |  0  |    0    |      |               |     |
-----|--------------|-----|---------|------|---------------|-----|
     |              |     |    0    | lw   | $t0, BALANCE  |  0  |
-----|--------------|-----|---------|------|---------------|-----|
addi | $t0, $t0, 1  |  1  |    0    |      |               |     |
-----|--------------|-----|---------|------|---------------|-----|
sw   | $to, BALANCE |  1  |    1    |      |               |     |
-----|--------------|-----|---------|------|---------------|-----|
     |              |     |    1    | addi | $t0, $t0, -1  |  -1 |
-----|--------------|-----|---------|------|---------------|-----|
     |              |     |   -1    | sw   | $t0, BALANCE  |  -1 |
------------------------------------------------------------------
```

- Ambos hilos intentan acceder y actualizar la posición de memoria compartida **BALANCE** de forma concurrente. Las actualizaciones no son atómicas, y el resultado depende del orden particular en que se produzcan los accesos a los datos. En este ejemplo el **BALANCE** resultante es **-1**.

-  **Race Condition:** es el comportamiento de un sistema electrónico, de software o de otro tipo en el que la salida depende de la secuencia o el momento de otros eventos incontrolables. Se convierte en un error cuando los eventos no suceden en el orden previsto. El término tiene su origen en la idea de dos señales que compiten entre sí para influir primero en la salida.

- **Data Race:** dos hilos pueden leer y escribir la misma variable **BALANCE** sin sincronización.

## **Ejemplo:**

```cpp
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

#define THREAD_NUM 5 // Número de hilos a crear.

void *myfunc(void *args) // Función a ser ejecutada por cada hilo.
{
    char msg = *(int *)args; // Número de hilos del argumento.
    printf("Soy el Hilo %d\n", msg);
    for(int i = 0, i < 250; i++)
    {
        print("Thread [%d]: %d\n", msg, i); // Imprimir el número de hilos y el contador del bucle.
    }
}

int main()
{
    phtread_t thread[THREAD_NUM]; // Declarar un array de hilos.
    int i;

    for (i = 0; 1 < THREAD_NUM; i++)
        pthread_create(&thread[i], NULL, myfunc, &i);

    for (i = 0; i < THREAD_NUM; i++)
        pthread_join(thread[i], NULL);

    printf("Funcional de PID: %d\n", getpid());

    return 0;
}
```

# **Exclusión mutua:**

- El requisito de garantizar que no haya dos procesos o subprocesos concurrentes en su sección crítica al mismo tiempo. 

- Es un requisito básico del control de concurrencia para evitar condiciones de carrera.

- Identificado y resuelto por primera vez por **Edsger W. Dijkstra** en su artículo seminal de 1965 titulado [**Solución de un problema en un control de programación concurrente**](https://rust-class.org/static/classes/class19/dijkstra.pdf), se le atribuye el primer tema en el estudio de los algoritmos concurrentes.

![](https://i.imgur.com/6TOvxaU.png)

## **Bloqueo:**

- En computación concurrente, un punto muerto es un estado en el que cada miembro de un grupo está esperando a que algún otro miembro realice una acción, como enviar un mensaje o, más comúnmente, liberar un bloqueo.

![](https://i.imgur.com/fjJIftP.jpg)

![](https://i.imgur.com/E7dMHyw.png)

## **Ejemplo:**

```cpp
#include <semaphore.h>
#include <stdio.h>
#include <pthread.h>

#define THREAD_NUM 5

sem_t semaphore;

void *routine(void *args) // Función a ser ejecutada por cada hilo.
{
    sem_wait(&semaphore);
    sleep(5);
    char c = *(int *)args; // Obtener el número de hilos del argumento.
    printf("Hola desde el Hilo[%d]\n", c);
    sem_post(&semaphore);
}

int main(int argc, char *argv[])
{
    int i;
    phtread_t th[THREAD_NUM]; // Declarar un array de hilos.
    sem_init(&semaphore, 0, 5);

    for (i = 0; 1 < THREAD_NUM; i++)
        pthread_create(&th[i], NULL, &routine, &i); // Crear un nuevo hilo y pasar su índice como argumento.
    
    for (i = 0; i < THREAD_NUM; i++)
        pthread_join(th[i], NULL);

    sem_destroy(&semaphore);

    return 0;
}
```

- **Filósofos comensales:** es un problema de ejemplo utilizado a menudo en el diseño de algoritmos concurrentes para ilustrar los problemas de sincronización y las técnicas para resolverlos.

[**Explicación interesante sobre el algoritmo**](https://www.youtube.com/watch?v=70auqrv84y8).

 - [Solución a está problemática resuelta por mí](https://github.com/Ixeoz/Timer-Old-Implementation/blob/main/Procesos/Fil%C3%B3sofos%20comensales/filosofos.cpp).

# **Gestión de la memoria:** 

- El sistema operativo controla el hardware y coordina su uso entre los distintos programas de aplicación de los distintos usuarios. Un sistema operativo proporciona un entorno para la ejecución de programas.

![](https://i.imgur.com/jsXuw8G.png)

## **Espacio de memoria de proceso**

- Además de un **PCB**, el sistema operativo debe asignar un nuevo espacio de memoria para cada nuevo proceso. Este **espacio de memoria** suele denominarse imagen de memoria del proceso.

- **Asignación de memoria estática:** el sistema operativo debe asignar un blob de memoria para la nueva imagen de memoria del proceso.

- Un **programa** debe traerse (desde el disco) a la memoria y colocarse dentro de un proceso para que pueda ejecutarse.

- La **memoria principal** y **los registros** son el único almacenamiento al que la CPU puede acceder directamente.

- **El acceso a los registros** se realiza en un reloj de la CPU (o menos).

- **La memoria principal** puede tardar muchos ciclos.

- **La caché** se sitúa entre la memoria principal y los registros de la CPU.

- Debe reforzar la **protección de memoria** entre procesos.

# **Asignación contigua única:**

- La asignación única es la técnica de gestión de memoria más sencilla. Toda la memoria de la PC, normalmente con la excepción de una pequeña parte reservada para el sistema operativo, está disponible para una única aplicación.

- MS-DOS **(lanzado en 1981)** es un ejemplo de sistema que asigna memoria de esta forma.

- Un **sistema embebido** que ejecute una única aplicación también podría utilizar esta técnica.

- Un sistema que utilice la asignación contigua única puede seguir siendo multitarea intercambiando el contenido de la memoria para cambiar entre usuarios. A veces se utiliza el término monotarea en lugar de multitarea para este tipo de sistemas.

- MS-DOS es un sistema operativo monotarea. Tiene un intérprete de comandos que se invoca cuando se inicia el ordenador.

- MS-DOS simplemente carga un programa en memoria, escribiendo sobre la mayor parte del intérprete de comandos para dar al programa tanta memoria como sea posible.

- Cuando el programa termina, la pequeña parte del intérprete de comandos que no se sobrescribió reanuda la ejecución. Su primera tarea es recargar el resto del intérprete de comandos desde el disco.

![](https://i.imgur.com/TAS0LEF.jpg)

# **Intercambio:**

- Un proceso puede ser intercambiado temporalmente fuera de la memoria a un almacén de respaldo, y el traído de vuelta a la memoria para continuar la ejecución.

- **Backing Store**, disco rápido lo suficientemente grande como para alojar copias de todas las imágenes de memoria para todos los usuarios; debe proporcionar acceso directo a estas imágenes de memoria.

- **Roll out, Roll in**, variante de intercambio utilizada para algoritmos de programación basados en prioridades; el proceso de menor prioridad se intercambia para que el proceso de mayor prioridad pueda cargarse y ejecutarse.

- La mayor parte del tiempo de intercambio es **tiempo de transferencia**; el tiempo total de transferencia es directamente proporcional a la cantidad de memoria intercambiada.

- Existen versiones modificadas de swapping en muchos sistemas (por ejemplo, UNIX, Linux y Windows).

- El sistema mantiene una **cola de procesos** listos para ejecutarse que tienen imágenes de memoria en el disco.

![](https://i.imgur.com/t5u8gus.png)

# **Asignación particionada:** 

- La asignación particionada divide la memoria primaria en múltiples particiones de memoria, normalmente **áreas contiguas de memoria**.

- La asignación particionada divide la memoria primaria en múltiples particiones de memoria, normalmente áreas contiguas de memoria.

- Cada partición puede contener toda la información para un trabajo o tarea específica.

- La gestión de la memoria consiste en asignar una partición a un trabajo cuando se inicia y desasignarla cuando el trabajo finaliza. La memoria principal suele dividirse en dos particiones: una para el sistema operativo y otra para todos los procesos del sistema.

# **Espacio de direcciones lógicas:**

- Una dirección lógica es la dirección en la que una celda de memoria parece residir desde la perspectiva de un programa de aplicación en ejecución. 

- Un par de registros base y límite definen un espacio de direcciones lógicas de proceso.

![](https://i.imgur.com/Zkre9uO.png)

# **Unidad de gestión de memoria (MMU):**

- La **MMU** es una unidad de hardware del ordenador que hace pasar todas las referencias de memoria de direcciones lógicas de memoria a direcciones físicas.
Recolocación dinámica mediante un registro de recolocación.

- La **MMU** asigna direcciones lógicas a direcciones físicas.

- El valor de los registros de recolocación se añade a cada dirección generada por un proceso de usuario en el momento en que se envía a la memoria.
Los programas de usuario tratan con direcciones lógicas; nunca ven las direcciones físicas reales.

- Debe comprobar si la dirección está dentro de los límites de la imagen de memoria del proceso.

![](https://i.imgur.com/zAQpEAd.png)

# **Asignación continua:**

Memoria principal, normalmente dividida en dos particiones: 

- **Sistema operativo residente**, normalmente en memoria baja con vector de interrupción.

- **Los procesos de usuario** se alojan en la memoria alta.

  - Registros de reubicación y límite utilizados para proteger.
Los procesos de usuario entre sí.

  - El código y los datos del sistema operativo de los procesos de usuario.

  - El **registro de reubicación** contiene el valor de la dirección física más pequeña.

  - El **registro límite** contiene el rango de direcciones lógicas - cada dirección lógica debe ser menor que el registro límite.

  - La **MMU** asigna las direcciones lógicas dinámicamente.

# **Problema de asignación dinámica de almacenamiento:**

- **First-Fit:** Asignar el primer hueco suficientemente grande.

- **Best-Fit:** Asigna el hueco más pequeño que sea suficientemente grande; debe buscar en toda la lista, a menos que esté ordenada por tamaño.

  - Produce el agujero libre más pequeño.

Peor ajuste: Asigna el hueco más grande; también debe buscar en toda la lista.

  - Produce el agujero sobrante más grande.

          Las simulaciones demuestran que los resultados de first-fit y best-fit son mejores que los de worst-fit en términos de velocidad y utilización del almacenamiento.

# **Fragmentación:**

- Es un fenómeno en el que el espacio de almacenamiento se utiliza de forma ineficiente, reduciendo la capacidad y, a menudo, el rendimiento La fragmentación hace que se "desperdicie" espacio de almacenamiento, y el término también se refiere al propio espacio desperdiciado.

- **Fragmentación interna:** la memoria asignada puede ser ligeramente mayor que la memoria solicitada; esta diferencia de tamaño es memoria interna a una partición, pero que no se está utilizando.

- **Fragmentación externa:** existe espacio de memoria total para satisfacer una solicitud, pero no es contiguo.

# **Compactación:**

- Mover todos los procesos a un extremo del espacio de direcciones produciendo un gran agujero en el otro extremo del espacio de direcciones.

**¿Cuándo debe realizarse la compactación?**

- Este método puede ser caro (lleva mucho tiempo). La compactación hace que la imagen de memoria de un proceso se mueva en la memoria física durante el tiempo de ejecución.

# **Gestión de memoria paginada:** 

- La asignación por páginas divide la memoria primaria del ordenador en unidades de tamaño fijo denominadas marcos de páginas y el espacio de direcciones virtuales del programa en páginas del **mismo tamaño**.
La unidad hardware de gestión de memoria asigna las páginas a los marcos.

- La memoria física puede **asignarse de forma no contigua** por páginas, mientras que el espacio de direcciones lógicas aparece contiguo.

# **Direccionamiento de la memoria:** 

- La memoria física de tamaño $2^{(m)}$ bytes se divide en marcos de tamaño $2^{(n)}$ bytes cada uno.

- Numeramos las tramas 0, 1, ...

- **Tamaño de la memoria / Tamaño del marco**  = 2m / 2n = $2^{(m-n)}$


- Numeramos las tramas 0,1, ..., $[2^{(m-n)}]-1$

Elegir un marco (traducción de direcciones): 

- Cómo podemos asignar una dirección lógica vista por la CPU a una trama física en memoria.

- Dirección lógica de M bits vista por la CPU.

- Utilizar m-n bits de orden superior para elegir una trama.

**¿Qué significan los n bits menos significativos?**

- Los m-n bits de orden superior para elegir una trama.
Los n bits menos significativos denotan el desplazamiento de byte dentro de la trama.

**A = F (Número de trama) | D (Desplazamiento de trama)**

# **Páginas y marcos:**

Solución que permite la asignación no contigua de tramas físicas.

- Espacio de direcciones lógico dividido en páginas de tamaño fijo.

- Memoria física dividida en marcos del mismo tamaño fijo que las páginas.

**A = m - n (Número de páginas) | n (Desplazamiento de página)**

# **Gestión de la memoria paginada:**

- El espacio de direcciones lógicas de un proceso puede no ser contiguo; al proceso se le asigna memoria física siempre que ésta esté disponible.

- Dividir la memoria física en bloques del mismo tamaño llamados páginas.
Llevar un registro de todos los cuadros libres

   - Para ejecutar un programa de tamaño N páginas, es necesario encontrar N marcos libres y cargar el programa.

- Establecer una tabla de páginas para traducir las direcciones lógicas a físicas.

- Es posible la fragmentación interna.

- No hay fragmentación externa.

# **Esquema de traducción de direcciones:**

Las direcciones lógicas generadas por la CPU se dividen en:

- **Número de página (p):** se utiliza como índice en una tabla de páginas que contiene la dirección base de cada cuadro de la memoria física.

- **Desplazamiento de página (d):** se combina con la dirección base para definir la dirección de memoria física que se envía a la unidad de memoria.

- **32 bytes de memoria física y páginas de 4 bytes.**

$(32 \text{ bytes}) / [(4 \text{ bytes})/\text{frame}] = 8 \text{ frames}$

**¿Qué tamaño tiene la dirección física?**

- $2\log(32) = 2\log(2^5)= 5 \text{ bit dirección}$

**¿Cómo se divide la dirección física en número de trama y desplazamiento de trama?**

- $2\log(8) = 2\log(2^3) = 3 \text{ bits para el número de trama}$

- $2\log(4) = 2\log(2^2) = 2 \text{ bits para desplazamiento de trama}$

# **Protección de memoria:**

Protección de memoria entre procesos implementada asociando un bit válido a cada entrada de la tabla de páginas por proceso.

- **Válido:** indica que la página asociada está en el espacio de direcciones lógicas del proceso y, por tanto, es una página legal.

- **Inválido:** indica que la página no está en el espacio de direcciones lógicas del proceso.

# **Memoria intermedia de traducción:**

Es una memoria caché que se utiliza para reducir el tiempo de acceso a una posición de memoria de usuario. La TLB almacena las traducciones recientes de memoria virtual a memoria física.

## **Tiempo de acceso efectivo:**

Utiliza el ratio de aciertos y los tiempos de acceso relativos para medir el rendimiento:

- ∞ = ratio de aciertos = # TLB aciertos / # TLB aciertos + # TLB fallos.

- ∞ -> 1 cuando # TLB falla -> 0.

- ∞ -> 0 cuando # TLB aciertos << # TLB fallos.

## **Probabilidades de acceso:**

- P (acierto TLB) = α.

- P (fallo TLB) = (1- α).

Supongamos los siguientes tiempos de acceso a la memoria

- Búsqueda asociativa en la TLB = ∈.
- Tiempo de ciclo de memoria = 1 ms.

## **Hardware de paginación con TLB:**

- Un búfer de traducción (TLB) es una caché que el hardware de gestión de memoria utiliza para mejorar la velocidad de traducción de direcciones virtuales.

# **Referencias:**

- [Threads](https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/4_Threads.html).

- [Process Count Doesn’t Matter!](https://zusier.xyz/blog/posts/process-count-doesnt-matter/).

- [Operating Systems: Internals and Design Principles](https://engineering.futureuniversity.com/BOOKS%20FOR%20IT/William%20Stallings%20-%20Operating%20Systems%20(1).pdf).

- [Modern Operating Systems](https://csc-knu.github.io/sys-prog/books/Andrew%20S.%20Tanenbaum%20-%20Modern%20Operating%20Systems.pdf).

- [Operating System Concepts](https://os.ecci.ucr.ac.cr/slides/Abraham-Silberschatz-Operating-System-Concepts-10th-2018.pdf).
