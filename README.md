# Timer-Old-Implementation

Cabe destacar, que a partir de Windows 11, si un proceso de propiedad de una ventana se vuelve completamente ocluido/minimizado/invisible para el usuario final, Windows no garantizará una resolución más alta que la resolución predeterminada del sistema: 64 Hz / 15.625 ms. Windows 11 solo garantiza un temporizador de alta resolución para las aplicaciones si tiene prioridad en primer plano o se está utilizando activamente.

Windows cambió esto para permitir que los temporizadores se resuelvan en incrementos de tiempo de solo 100 microsegundos (µs), lo que permite una resolución de temporizador más precisa. Esto significa que cualquier temporizador que se establezca para menos de 1 ms ahora se resolverá a una resolución de 100 µs en lugar de redondearse automáticamente a 1 ms. En general, este cambio en la resolución del temporizador de Windows es una buena noticia para los desarrolladores que necesitan temporizadores precisos y confiables en sus programas. Pero, también significa que los desarrolladores deben tener en cuenta este cambio al diseñar sus programas para asegurarse de que funcionen correctamente en la nueva resolución de temporizador.

- La mayoría de los Hardware modernos estarían usando [TSC](https://www.oreilly.com/library/view/mastering-linux-kernel/9781785883057/20712c1b-f659-40da-a09d-55efc93b0597.xhtml), la gran parte de sus beneficios es que tienen una menor cantidad de latencia para tomar y/o obtener los datos del reloj. 

- Uno de sus problemas es que puede reducir o aumentar según cierta carga implementada, esto podría ser contraproducente, ya que podría ofrecernos mediciones inexactas. 

"Windows uses timers for many things, such as synchronization or ensuring linearity, and there are sets of software relating to monitoring and overclocking that require the timer with the most granularity - specifically they often require the [High Precision Event Timer (HPET)](https://en.wikipedia.org/wiki/High_Precision_Event_Timer)."

- [A Timely Discovery: Examining Our AMD 2nd Gen Ryzen Results](https://www.anandtech.com/show/12678/a-timely-discovery-examining-amd-2nd-gen-ryzen-results)

El uso de temporizadores es una forma común de medir el tiempo en un juego, ya sea para actualizar la física, la IA o la animación. Sin embargo, los temporizadores no son una herramienta precisa para medir el tiempo, ya que están sujetos a la latencia del sistema operativo y otros factores externos. Además, en sistemas multinúcleo, los temporizadores pueden ser menos precisos debido a que la ejecución de diferentes núcleos puede desincronizarse. El uso de [time stamps](https://en.wikipedia.org/wiki/Timestamp) basados en procesador como una alternativa más precisa para medir el tiempo en sistemas multicore. En lugar de usar temporizadores, los time stamps registran el tiempo en que ocurrió un evento en el procesador, lo que permite una mayor precisión en la sincronización de los procesos.

Desde la introducción del conjunto de [instrucciones x86](https://es.wikipedia.org/wiki/Anexo:Instrucciones_x86) P5, muchos desarrolladores de juegos han utilizado la instrucción [RDTSC](https://www.felixcloutier.com/x86/rdtsc). para realizar tiempos de alta resolución. Sin embargo, este uso de RDTSC para la temporización adolece de problemas fundamentales como valores discontinuos, disponibilidad de hardware dedicado y variabilidad de la frecuencia de la CPU. Por lo tanto, se recomienda utilizar [QueryPerformanceCounter](https://faculty.etsu.edu/tarnoff/labs4717/performance/hpc.htm) y [QueryPerformanceFrequency](https://help.intervalzero.com/product_help/RTX/Content/PROJECTS/SDK%20Reference/Win32Ref/QueryPerformanceFrequency.htm) en lugar de RDTSC y seguir ciertos pasos para implementar el tiempo de alta resolución.

Se introdujo un cambio en la forma en que el sistema operativo maneja el temporizador del sistema. A partir de la versión 1809, el temporizador se cambió a una frecuencia de 10 milisegundos (10 MHz).

La razón detrás de este cambio es que el nuevo temporizador de 10 MHz permite una mayor precisión en la medición del tiempo. Con el temporizador anterior, las mediciones de tiempo podían tener un error máximo de aproximadamente 15,6 milisegundos debido a la imprecisión del temporizador. Con el nuevo temporizador de 10 MHz, este error máximo se reduce a aproximadamente 1 milisegundo, lo que permite una mayor precisión en aplicaciones que dependen de mediciones de tiempo precisas, como la medición del rendimiento de la CPU o la sincronización de dispositivos.

Uno de los problemas que se ha informado es que, en algunas configuraciones de hardware, el temporizador de 10 MHz puede generar latencia adicional y empeorar el rendimiento en ciertas aplicaciones. Esto puede ocurrir en sistemas antiguos o con hardware específico que no es compatible con el nuevo temporizador de 10 MHz.

# Referencias:

- [amitxv/PC-Tuning](https://github.com/amitxv/PC-Tuning/blob/main/docs/research.md#fixing-timing-precision-in-windows-after-the-great-rule-change).

- [Windows Timer Resolution: The Great Rule Change](https://randomascii.wordpress.com/2020/10/04/windows-timer-resolution-the-great-rule-change/).

- [Game Timing and Multicore Processors](https://github.com/MicrosoftDocs/win32/blob/docs/desktop-src/DxTechArts/game-timing-and-multicore-processors.md).

- [Optimising your time](https://computinglife.wordpress.com/2020/06/06/optimising-your-time/).

- [Time Stamp Counter](https://en.wikipedia.org/wiki/Time_Stamp_Counter).

- [Pitfalls of TSC usage](http://oliveryang.net/2015/09/pitfalls-of-TSC-usage/).
