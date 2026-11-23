#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int busca_ingenua(char *texto, char *padrao){
    int tam_texto = strlen(texto);
    int tam_padrao = strlen(padrao);
    int ocorrencias = 0;

    for(int pos_texto=0; pos_texto<=tam_texto-tam_padrao; pos_texto++){
        int pos_padrao;
        for(pos_padrao=0; pos_padrao<tam_padrao; pos_padrao++){
            if(texto[pos_texto + pos_padrao] != padrao[pos_padrao]){
                break;
            }
        }
        if(pos_padrao == tam_padrao){
            ocorrencias++;
        }
    }
    return ocorrencias;
}

int busca_kmp(char *texto, char *padrao){
    int tam_texto = strlen(texto);
    int tam_padrao = strlen(padrao);
    if (tam_padrao == 0 || tam_texto < tam_padrao){
        return 0;
    }

    int *prefixo = malloc(tam_padrao*sizeof(int));
    prefixo[0] = 0;
    int tam_borda = 0;

    for(int i=1; i<tam_padrao; i++){
        while(tam_borda > 0 && padrao[tam_borda] != padrao[i]){
            tam_borda = prefixo[tam_borda - 1];
        }
        if(padrao[tam_borda] == padrao[i]){
            tam_borda++;
        }
        prefixo[i] = tam_borda;
    }

    int ocorrencias = 0;
    int pos_padrao = 0;

    for(int pos_texto = 0; pos_texto < tam_texto; pos_texto++){
        while(pos_padrao>0 && padrao[pos_padrao] != texto[pos_texto]){
            pos_padrao = prefixo[pos_padrao - 1];
        }
        if(padrao[pos_padrao] == texto[pos_texto]){
            pos_padrao++;
        }
        if(pos_padrao == tam_padrao){
            ocorrencias++;
            pos_padrao = prefixo[pos_padrao - 1];
        }
    }

    free(prefixo);
    return ocorrencias;
}

int main() {
    int tam_texto = 100000;
    int tam_padrao = 1000;

    char *texto = malloc((tam_texto + 1) * sizeof(char));
    char *padrao = malloc((tam_padrao + 1) * sizeof(char));

    for (int i = 0; i < tam_texto; i++) {
        texto[i] = 'A';
    }
    texto[tam_texto] = '\0';

    for (int i = 0; i < tam_padrao - 1; i++) {
        padrao[i] = 'A';
    }
    padrao[tam_padrao - 1] = 'B';
    padrao[tam_padrao] = '\0';

    clock_t t1 = clock();
    int achados_ing = busca_ingenua(texto, padrao);
    double tempo_ing = (double)(clock() - t1) / CLOCKS_PER_SEC;

    clock_t t2 = clock();
    int achados_kmp = busca_kmp(texto, padrao);
    double tempo_kmp = (double)(clock() - t2) / CLOCKS_PER_SEC;

    printf("ingenua: %d ocorrencias (%.6f s)\n", achados_ing, tempo_ing);
    printf("kmp: %d ocorrencias (%.6f s)\n", achados_kmp, tempo_kmp);

    free(texto);
    free(padrao);
    return 0;
}