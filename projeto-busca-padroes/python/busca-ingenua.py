import time

def busca_ingenua(T: str, P: str) -> int:
    n = len(T)
    m = len(P)
    ocorrencias = 0

    for s in range(n - m + 1):
        j = 0
        while j < m and T[s + j] == P[j]:
            j += 1
        if j == m:
            ocorrencias += 1
    return ocorrencias

if __name__ == "__main__":
    n, m = 100_000, 1_000
    T = "A" * n
    P = "A" * (m - 1) + "B"

    t0 = time.perf_counter()
    res_ing = busca_ingenua(T, P)
    t_ing = time.perf_counter() - t0

    print(f"Busca Ingênua: {res_ing} ocorrências | Tempo: {t_ing:.6f} s")