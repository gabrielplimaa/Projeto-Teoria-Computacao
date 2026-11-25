import csv
import os
import random
import statistics
import subprocess
import sys
import matplotlib.pyplot as plt

# 6 tamanhos em escala geométrica de razão 2 (exigência do edital)
TAMANHOS_N = [1_000, 2_000, 4_000, 8_000, 16_000, 32_000]
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


def carregar_resultados_csv(caminho="resultados/benchmark.csv"):
    """Lê um benchmark já salvo, para regenerar os gráficos sem rodar as medições de novo."""
    with open(caminho, encoding="utf-8") as f:
        return [
            {
                **r,
                "n": int(r["n"]),
                "m": int(r["m"]),
                "media_s": float(r["media_s"]),
                "desvio_s": float(r["desvio_s"]),
                "ocorrencias": int(r["ocorrencias"]),
            }
            for r in csv.DictReader(f)
        ]


def filtrar(resultados, cenario, lang, alg):
    dados = [
        r for r in resultados
        if r["cenario"] == cenario and r["linguagem"] == lang and r["algoritmo"] == alg
    ]
    return sorted(dados, key=lambda r: r["n"])


# Função de custo teórica f(n, m) de cada algoritmo no pior caso
CUSTO_TEORICO = {
    "ingenua": ("(n - m + 1) · m", lambda n, m: (n - m + 1) * m),
    "kmp": ("n + m", lambda n, m: n + m),
}


def gerar_graficos(resultados):
    # Gráfico 1: Pior Caso (Ingênua vs KMP em C e Python) - Escala Log-Log, com desvio-padrão
    plt.figure(figsize=(9, 5))
    for lang in ["C", "Python"]:
        for alg in ["ingenua", "kmp"]:
            dados = filtrar(resultados, "pior", lang, alg)
            ns = [d["n"] for d in dados]
            medias = [d["media_s"] for d in dados]
            desvios = [d["desvio_s"] for d in dados]
            plt.errorbar(ns, medias, yerr=desvios, marker="o", capsize=3, label=f"{alg.upper()} ({lang})")

    plt.xscale("log")
    plt.yscale("log")
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
            dados = filtrar(resultados, cenario, "C", alg)
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

    # Gráfico 3: Teórico x Medido no Pior Caso — razão T(n) / f(n, m) para os 2 algoritmos nas 2 linguagens.
    # Se f é a complexidade correta, a razão tende a uma constante (curva horizontal).
    fig, eixos = plt.subplots(2, 2, figsize=(11, 7))
    for i, alg in enumerate(["ingenua", "kmp"]):
        nome_f, f = CUSTO_TEORICO[alg]
        for j, lang in enumerate(["C", "Python"]):
            dados = filtrar(resultados, "pior", lang, alg)
            ns = [d["n"] for d in dados]
            razoes = [d["media_s"] / f(d["n"], d["m"]) * 1e9 for d in dados]  # nanossegundos por operação
            ax = eixos[i][j]
            ax.plot(ns, razoes, marker="s", color="darkgreen" if alg == "kmp" else "darkred")
            ax.set_xscale("log")
            ax.set_ylim(0, max(razoes) * 1.3)
            ax.set_title(f"{alg.upper()} ({lang}): T(n) / [{nome_f}]")
            ax.set_xlabel("Tamanho do Texto n (log)")
            ax.set_ylabel("ns por operação")
            ax.grid(True, linestyle="--", alpha=0.5)
    fig.suptitle("Teórico x Medido (Pior Caso): a razão T(n) / f(n) tende a uma constante")
    fig.tight_layout()
    fig.savefig("resultados/grafico_razao_teorico_medido.png", dpi=200)
    plt.close(fig)

    # Gráfico 4: Linguagem x Linguagem — quantas vezes Python é mais lento que C, por algoritmo e cenário
    plt.figure(figsize=(11, 5))
    for cenario in ["melhor", "medio", "pior"]:
        for alg in ["ingenua", "kmp"]:
            dados_c = filtrar(resultados, cenario, "C", alg)
            dados_py = filtrar(resultados, cenario, "Python", alg)
            ns = [d["n"] for d in dados_c]
            fatores = [py["media_s"] / c["media_s"] for c, py in zip(dados_c, dados_py)]
            estilo = "--" if alg == "ingenua" else "-"
            plt.plot(ns, fatores, linestyle=estilo, marker="o", label=f"{alg.upper()} - {cenario}")

    plt.xscale("log")
    plt.yscale("log")
    plt.title("Python x C: razão entre os tempos (T_Python / T_C)")
    plt.xlabel("Tamanho do Texto n (log)")
    plt.ylabel("Vezes que Python é mais lento (log)")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend(loc="center left", bbox_to_anchor=(1.01, 0.5))
    plt.tight_layout()
    plt.savefig("resultados/grafico_python_vs_c.png", dpi=200)
    plt.close()
    print("Gráficos salvos em resultados/.")


if __name__ == "__main__":
    # "python executar_experimentos.py --graficos" regenera só os gráficos a partir do benchmark.csv
    if "--graficos" in sys.argv:
        gerar_graficos(carregar_resultados_csv())
    else:
        gerar_entradas()
        dados = rodar_testes_e_benchmark()
        gerar_graficos(dados)
