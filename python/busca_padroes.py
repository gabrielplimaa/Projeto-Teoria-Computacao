import time

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
    tam_texto, tam_padrao = 100_000, 1_000
    texto = "A" * tam_texto
    padrao = "A" * (tam_padrao - 1) + "B"

    t1 = time.perf_counter()
    achados_ing = busca_ingenua(texto, padrao)
    tempo_ing = time.perf_counter() - t1

    t2 = time.perf_counter()
    achados_kmp = busca_kmp(texto, padrao)
    tempo_kmp = time.perf_counter() - t2

    print(f"ingenua: {achados_ing} ocorrencias ({tempo_ing:.6f} s)")
    print(f"kmp: {achados_kmp} ocorrencias ({tempo_kmp:.6f} s)")