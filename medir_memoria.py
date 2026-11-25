"""Item opcional (bônus): mede o pico de memória auxiliar das implementações em Python com tracemalloc,
sobre as entradas de pior caso, e compara com a complexidade de espaço teórica
(Busca Ingênua: O(1); KMP: Θ(m) por causa do vetor de prefixos/LPS).

Uso (a partir da raiz do repositório, depois de executar_experimentos.py ter gerado as entradas):
    python medir_memoria.py
"""

import csv
import os
import sys
import tracemalloc

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "python"))
from busca_padroes import busca_ingenua, busca_kmp  # noqa: E402

from executar_experimentos import TAMANHOS_N  # noqa: E402


def pico_memoria(funcao, texto, padrao):
    """Pico de memória (bytes) alocada durante a execução da função; texto e padrão já estão carregados."""
    tracemalloc.start()
    tracemalloc.reset_peak()
    funcao(texto, padrao)
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pico


def main():
    linhas = []
    for n in TAMANHOS_N:
        with open(f"entradas/T_pior_{n}.txt", encoding="utf-8") as f:
            texto = f.read().rstrip("\r\n")
        with open(f"entradas/P_pior_{n}.txt", encoding="utf-8") as f:
            padrao = f.read().rstrip("\r\n")
        m = len(padrao)

        pico_ingenua = pico_memoria(busca_ingenua, texto, padrao)
        pico_kmp = pico_memoria(busca_kmp, texto, padrao)
        linhas.append({
            "n": n,
            "m": m,
            "pico_ingenua_bytes": pico_ingenua,
            "pico_kmp_bytes": pico_kmp,
            "kmp_bytes_por_elemento": round(pico_kmp / m, 2),
        })
        print(f"n={n:6d} m={m:5d} | Ingênua: {pico_ingenua:7d} B | KMP: {pico_kmp:8d} B ({pico_kmp / m:.2f} B/elem)")

    os.makedirs("resultados", exist_ok=True)
    with open("resultados/memoria.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=linhas[0].keys())
        writer.writeheader()
        writer.writerows(linhas)
    print("Resultados salvos em resultados/memoria.csv.")


if __name__ == "__main__":
    main()
