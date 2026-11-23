import csv
import os
import random
import statistics
import subprocess
import matplotlib.pyplot as plt

# 6 tamanhos em escala geométrica (exigência do edital)
TAMANHOS_N = [1_000, 2_000, 5_000, 10_000, 20_000, 30_000]
REPETICOES = 15
SEED = 42

EXE_C = os.path.join("c", "busca_padroes.exe" if os.name == "nt" else "busca_padroes")
SCRIPT_PY = os.path.join("python", "busca_padroes.py")


def gerar_entradas():
    os.makedirs("entradas", exist_ok=True)
    rng = random.Random(SEED)
    alfabeto = ["A", "B", "C", "D"]

    for n in TAMANHOS_N:
        m = max(10, n // 5)

        # 1. Melhor caso (Ingênua falha no 1º caractere em todas as posições)
        t_melhor = "B" * n
        p_melhor = "A" * m

        # 2. Caso médio (texto e padrão aleatórios com semente fixa)
        t_medio = "".join(rng.choices(alfabeto, k=n))
        p_medio = "".join(rng.choices(alfabeto, k=m))

        # 3. Pior caso (prefixos repetidos falhando apenas no último caractere)
        t_pior = "A" * n
        p_pior = "A" * (m - 1) + "B"

        cenarios = {
            "melhor": (t_melhor, p_melhor),
            "medio": (t_medio, p_medio),
            "pior": (t_pior, p_pior),
        }

        for nome, (texto, padrao) in cenarios.items():
            with open(f"entradas/T_{nome}_{n}.txt", "w", encoding="utf-8") as ft:
                ft.write(texto)
            with open(f"entradas/P_{nome}_{n}.txt", "w", encoding="utf-8") as fp:
                fp.write(padrao)


def executar_comando(cmd: list[str]) -> tuple[int, float]:
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    ocorr_str, tempo_str = res.stdout.strip().split(";")
    return int(ocorr_str), float(tempo_str)


def rodar_testes_e_benchmark():
    os.makedirs("resultados", exist_ok=True)
    resultados = []

    implementacoes = [
        ("C", "ingenua", [EXE_C, "ingenua"]),
        ("C", "kmp", [EXE_C, "kmp"]),
        ("Python", "ingenua", ["python", SCRIPT_PY, "ingenua"]),
        ("Python", "kmp", ["python", SCRIPT_PY, "kmp"]),
    ]

    for cenario in ["melhor", "medio", "pior"]:
        for n in TAMANHOS_N:
            m = max(10, n // 5)
            arq_t = f"entradas/T_{cenario}_{n}.txt"
            arq_p = f"entradas/P_{cenario}_{n}.txt"

            respostas_corretude = set()

            for lang, alg, base_cmd in implementacoes:
                cmd = base_cmd + [arq_t, arq_p]
                tempos = []

                for _ in range(REPETICOES):
                    ocorr, tempo = executar_comando(cmd)
                    respostas_corretude.add(ocorr)
                    tempos.append(tempo)

                # Teste automatizado de corretude entre as 4 implementações
                assert len(respostas_corretude) == 1, (
                    f"Erro de corretude em {cenario}, n={n}: {respostas_corretude}"
                )

                media = statistics.mean(tempos)
                desvio = statistics.stdev(tempos)
                resultados.append(
                    {
                        "cenario": cenario,
                        "n": n,
                        "m": m,
                        "linguagem": lang,
                        "algoritmo": alg,
                        "media_s": media,
                        "desvio_s": desvio,
                        "ocorrencias": list(respostas_corretude)[0],
                    }
                )
                print(
                    f"[{cenario.upper():6s}] n={n:7d} | {lang:6s} | {alg:7s} -> "
                    f"{media:.6f}s (±{desvio:.6f}s)"
                )

    csv_path = "resultados/benchmark.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)

    print(f"\nCorretude 100% validada! Resultados salvos em {csv_path}.")
    return resultados


def gerar_graficos(resultados):
    # Gráfico 1: Pior Caso (Ingênua vs KMP em C e Python) - Escala Log-Log
    plt.figure(figsize=(9, 5))
    for lang in ["C", "Python"]:
        for alg in ["ingenua", "kmp"]:
            dados = [
                r for r in resultados
                if r["cenario"] == "pior" and r["linguagem"] == lang and r["algoritmo"] == alg
            ]
            ns = [d["n"] for d in dados]
            medias = [max(d["media_s"], 1e-7) for d in dados]
            plt.loglog(ns, medias, marker="o", label=f"{alg.upper()} ({lang})")

    plt.title("Pior Caso: Busca Ingênua vs KMP (C e Python) — Escala Log-Log")
    plt.xlabel("Tamanho do Texto n (log)")
    plt.ylabel("Tempo Médio [s] (log)")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("resultados/grafico_pior_caso_loglog.png", dpi=200)
    plt.close()

    # Gráfico 2: Comparação de Cenários em C (Melhor, Médio e Pior Caso)
    plt.figure(figsize=(9, 5))
    for cenario in ["melhor", "medio", "pior"]:
        for alg in ["ingenua", "kmp"]:
            dados = [
                r for r in resultados
                if r["cenario"] == cenario and r["linguagem"] == "C" and r["algoritmo"] == alg
            ]
            ns = [d["n"] for d in dados]
            medias = [d["media_s"] for d in dados]
            estilo = "--" if alg == "ingenua" else "-"
            plt.plot(ns, medias, linestyle=estilo, marker="o", label=f"{alg.upper()} - {cenario}")

    plt.title("Comparação de Cenários em C (Melhor, Médio e Pior Caso)")
    plt.xlabel("Tamanho do Texto (n)")
    plt.ylabel("Tempo Médio [s]")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("resultados/grafico_cenarios_c.png", dpi=200)
    plt.close()

    # Gráfico 3: Teórico x Medido (Razão T(n) / (n + m) para KMP em Python no Pior Caso)
    dados_kmp_py = [
        r for r in resultados
        if r["cenario"] == "pior" and r["linguagem"] == "Python" and r["algoritmo"] == "kmp"
    ]
    ns = [d["n"] for d in dados_kmp_py]
    razoes = [d["media_s"] / (d["n"] + d["m"]) * 1e6 for d in dados_kmp_py]  # microssegundos/op

    plt.figure(figsize=(9, 5))
    plt.plot(ns, razoes, marker="s", color="darkgreen", label="T(n) / (n + m) [µs/op]")
    plt.title("Validação Assintótica KMP (Python): Razão T(n) / (n + m) tende a constante")
    plt.xlabel("Tamanho do Texto (n)")
    plt.ylabel("Tempo por unidade (n + m) [microssegundos]")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("resultados/grafico_razao_teorico_medido.png", dpi=200)
    plt.close()
    print("Gráficos salvos em resultados/.")


if __name__ == "__main__":
    gerar_entradas()
    dados = rodar_testes_e_benchmark()
    gerar_graficos(dados)