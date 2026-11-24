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

char *ler_arquivo(char *caminho) {
    FILE *arquivo = fopen(caminho, "rb");
    if (!arquivo) {
        fprintf(stderr, "Erro ao abrir arquivo: %s\n", caminho);
        exit(1);
    }

    fseek(arquivo, 0, SEEK_END);
    long tamanho = ftell(arquivo);
    fseek(arquivo, 0, SEEK_SET);

    char *conteudo = (char *)malloc((tamanho + 1) * sizeof(char));
    size_t lidos = fread(conteudo, 1, tamanho, arquivo);
    conteudo[lidos] = '\0';
    fclose(arquivo);

    while (lidos > 0 && (conteudo[lidos - 1] == '\n' || conteudo[lidos - 1] == '\r')) {
        conteudo[--lidos] = '\0';
    }

    return conteudo;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Uso: %s <ingenua|kmp> <arquivo_texto> <arquivo_padrao>\n", argv[0]);
        return 1;
    }

    char *algoritmo = argv[1];
    char *caminho_texto = argv[2];
    char *caminho_padrao = argv[3];

    char *texto = ler_arquivo(caminho_texto);
    char *padrao = ler_arquivo(caminho_padrao);

    int ocorrencias = 0;

    clock_t inicio = clock();
    if (strcmp(algoritmo, "ingenua") == 0) {
        ocorrencias = busca_ingenua(texto, padrao);
    } else if (strcmp(algoritmo, "kmp") == 0) {
        ocorrencias = busca_kmp(texto, padrao);
    } else {
        fprintf(stderr, "Algoritmo invalido. Use 'ingenua' ou 'kmp'.\n");
        free(texto);
        free(padrao);
        return 1;
    }
    double tempo = (double)(clock() - inicio) / CLOCKS_PER_SEC;

    printf("%d;%.6f\n", ocorrencias, tempo);

    free(texto);
    free(padrao);
    return 0;
}