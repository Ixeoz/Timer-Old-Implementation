# Timer-Old-Implementation

# Información

[Temporizador](https://github.com/amitxv/PC-Tuning/blob/main/docs/research.md#fixing-timing-precision-in-windows-after-the-great-rule-change).

[Explicación de Cambios](https://randomascii.wordpress.com/2020/10/04/windows-timer-resolution-the-great-rule-change/).

Cabe destacar, que a partir de Windows 11, si un proceso de propiedad de una ventana se vuelve completamente ocluido/minimizado/invisible para el usuario final, Windows no garantizará una resolución más alta que la resolución predeterminada del sistema: 64 Hz / 15.625 ms. Windows 11 solo garantiza un temporizador de alta resolución para las aplicaciones si tiene prioridad en primer plano o se está utilizando activamente. Windows cambió esto para permitir que los temporizadores se resuelvan en incrementos de tiempo de solo 100 microsegundos (µs), lo que permite una resolución de temporizador más precisa. Esto significa que cualquier temporizador que se establezca para menos de 1 ms ahora se resolverá a una resolución de 100 µs en lugar de redondearse automáticamente a 1 ms. En general, este cambio en la resolución del temporizador de Windows es una buena noticia para los desarrolladores que necesitan temporizadores precisos y confiables en sus programas. Pero, también significa que los desarrolladores deben tener en cuenta este cambio al diseñar sus programas para asegurarse de que funcionen correctamente en la nueva resolución de temporizador.
