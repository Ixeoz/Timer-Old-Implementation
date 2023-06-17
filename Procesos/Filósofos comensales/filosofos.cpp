#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>


#define NUM_FILOSOFOS 5
#define IZQUIERDA (i + NUM_FILOSOFOS - 1) % NUM_FILOSOFOS
#define DERECHA (i + 1) % NUM_FILOSOFOS

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond_filosofos[NUM_FILOSOFOS];

enum { PENSANDO, HAMBRIENTO, COMIENDO } estado[NUM_FILOSOFOS];
int tenedores[NUM_FILOSOFOS];

void pensar(int i) {
    printf("Filosofo %d esta pensando...\n", i);
    sleep(rand() % 5 + 1);
}

void comer(int i) {
    printf("Filosofo %d esta comiendo...\n", i);
    sleep(rand() % 5 + 1);
}

void tomar_tenedor(int i) {
    pthread_mutex_lock(&mutex);
    estado[i] = HAMBRIENTO;
    printf("Filosofo %d esta hambriento y quiere comer...\n", i);
    while (tenedores[IZQUIERDA] || tenedores[DERECHA]) {
        pthread_cond_wait(&cond_filosofos[i], &mutex);
    }
    tenedores[IZQUIERDA] = tenedores[DERECHA] = 1;
    estado[i] = COMIENDO;
    printf("Filosofo %d tomo los tenedores %d y %d y esta comiendo...\n", i, IZQUIERDA, i);
    pthread_mutex_unlock(&mutex);
}

void liberar_tenedor(int i) {
    pthread_mutex_lock(&mutex);
    tenedores[IZQUIERDA] = tenedores[DERECHA] = 0;
    estado[i] = PENSANDO;
    printf("Filosofo %d liberó los tenedores %d y %d y está pensando...\n", i, IZQUIERDA, i);
    pthread_cond_signal(&cond_filosofos[IZQUIERDA]);
    pthread_cond_signal(&cond_filosofos[DERECHA]);
    pthread_mutex_unlock(&mutex);
}

void *filosofo(void *arg) {
    int i = *(int *)arg;
    while (1) {
        pensar(i);
        tomar_tenedor(i);
        comer(i);
        liberar_tenedor(i);
    }
}

int main() {
    pthread_t hilos[NUM_FILOSOFOS];
    int id[NUM_FILOSOFOS];

    for (int i = 0; i < NUM_FILOSOFOS; i++) {
        pthread_cond_init(&cond_filosofos[i], NULL);
        tenedores[i] = 0;
        estado[i] = PENSANDO;
        id[i] = i;
        pthread_create(&hilos[i], NULL, filosofo, &id[i]);
    }

    for (int i = 0; i < NUM_FILOSOFOS; i++) {
        pthread_join(hilos[i], NULL);
    }

    return 0;
}
