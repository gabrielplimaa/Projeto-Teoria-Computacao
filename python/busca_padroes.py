import time
import sys

def busca_ingenua(texto, padrao):
    tam_texto = len(texto)
    tam_padrao = len(padrao)
    ocorrencias = 0

    if tam_padrao == 0 or tam_texto < tam_padrao:
        return 0

    for pos_texto in range(tam_texto - tam_padrao + 1):
        achou = True
        for pos_padrao in range(tam_padrao):
            if texto[pos_texto + pos_padrao] != padrao[pos_padrao]:
                achou = False
                break
        if achou:
            ocorrencias += 1

    return ocorrencias

def busca_kmp(texto, padrao):
    tam_texto = len(texto)
    tam_padrao = len(padrao)
    if tam_padrao == 0 or tam_texto < tam_padrao:
        return 0

    prefixo = [0] * tam_padrao
    tam_borda = 0

    for i in range(1, tam_padrao):
        while tam_borda > 0 and padrao[tam_borda] != padrao[i]:
            tam_borda = prefixo[tam_borda - 1]
        if padrao[tam_borda] == padrao[i]:
            tam_borda += 1
        prefixo[i] = tam_borda

    ocorrencias = 0
    pos_padrao = 0

    for pos_texto in range(tam_texto):
        while pos_padrao > 0 and padrao[pos_padrao] != texto[pos_texto]:
            pos_padrao = prefixo[pos_padrao - 1]
        if padrao[pos_padrao] == texto[pos_texto]:
            pos_padrao += 1
        if pos_padrao == tam_padrao:
            ocorrencias += 1
            pos_padrao = prefixo[pos_padrao - 1]

    return ocorrencias

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python busca_padroes.py <ingenua|kmp> <arquivo_texto> <arquivo_padrao>", file=sys.stderr)
        sys.exit(1)

    algoritmo = sys.argv[1]
    caminho_texto = sys.argv[2]
    caminho_padrao = sys.argv[3]

    with open(caminho_texto, "r", encoding="utf-8") as f:
        texto = f.read().rstrip("\r\n")

    with open(caminho_padrao, "r", encoding="utf-8") as f:
        padrao = f.read().rstrip("\r\n")

    inicio = time.perf_counter()
    if algoritmo == "ingenua":
        ocorrencias = busca_ingenua(texto, padrao)
    elif algoritmo == "kmp":
        ocorrencias = busca_kmp(texto, padrao)
    else:
        print("Algoritmo inválido. Use 'ingenua' ou 'kmp'.", file=sys.stderr)
        sys.exit(1)
    tempo = time.perf_counter() - inicio

    print(f"{ocorrencias};{tempo:.6f}")