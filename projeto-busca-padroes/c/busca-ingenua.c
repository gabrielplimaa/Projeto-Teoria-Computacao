#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int busca_ingenua(const char *T, const char *P) {
    int n = strlen(T);
    int m = strlen(P);
    int ocorrencias = 0;

    for (int s = 0; s <= n - m; s++) {
        int j = 0;
        while (j < m && T[s + j] == P[j]) {
            j++;
        }
        if (j == m) {
            ocorrencias++;
        }
    }
    return ocorrencias;
}

int main() {
    // Exemplo sintético de pior caso para Busca Ingênua
    int n = 100000;
    int m = 1000;
    char *T = (char *)malloc((n + 1) * sizeof(char));
    char *P = (char *)malloc((m + 1) * sizeof(char));

    memset(T, 'A', n);
    T[n] = '\0';
    memset(P, 'A', m - 1);
    P[m - 1] = 'B';
    P[m] = '\0';

    clock_t inicio = clock();
    int res_ing = busca_ingenua(T, P);
    double tempo_ing = (double)(clock() - inicio) / CLOCKS_PER_SEC;

    printf("Busca Ingenua: %d ocorrencias | Tempo: %f s\n", res_ing, tempo_ing);

    free(T);
    free(P);
    return 0;
}