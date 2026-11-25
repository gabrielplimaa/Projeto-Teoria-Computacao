# Busca de Padrões em Strings — Análise de Complexidade

Projeto desenvolvido para a disciplina de **Teoria da Computação**, com foco na implementação, análise assintótica e comparação empírica de algoritmos de busca exata de padrões em cadeias de caracteres (*strings*), utilizando **C** e **Python**, além da discussão sobre classes de complexidade ($\text{P}$, $\text{NP}$ e $\text{NP-difícil}$).

---

## 📋 Sobre o Problema

Dado um texto $T$ de comprimento $n$ e um padrão $P$ de comprimento $m$ ($m \le n$) sobre um alfabeto finito $\Sigma$, o objetivo é encontrar todos os deslocamentos válidos $s$ ($0 \le s \le n - m$) tais que $P[0 \dots m-1]$ ocorra como subcadeia contígua em $T[s \dots s+m-1]$.

### Algoritmos Implementados
1. **Algoritmo A — Busca Ingênua (Força Bruta):** Testa cada posição possível de alinhamento $s$ no texto $T$ e compara caractere por caractere com $P$, retrocedendo o ponteiro do texto a cada falha.
2. **Algoritmo B — Knuth-Morris-Pratt (KMP):** Pré-processa o padrão $P$ para construir a tabela **LPS** (*Longest Proper Prefix which is also Suffix*), evitando comparações redundantes e garantindo que o ponteiro do texto $T$ nunca retroceda.

---

## 📊 Resumo da Análise Assintótica

| Algoritmo | Melhor Caso | Caso Médio | Pior Caso | Espaço Auxiliar |
| :--- | :---: | :---: | :---: | :---: |
| **Busca Ingênua** | $\Omega(n)$ | $\Theta(n)$ | $O(n \cdot m)$ | $O(1)$ |
| **KMP** | $\Theta(n + m)$ | $\Theta(n + m)$ | $\Theta(n + m)$ | $\Theta(m)$ |

* **Entrada de Pior Caso (Busca Ingênua):** Textos com alta repetição de prefixos que falham apenas no último caractere do padrão, como $T = \text{"A"}^n$ e $P = \text{"A"}^{m-1}\text{"B"}$.
* **Entrada de Melhor Caso:** Quando o primeiro caractere $P[0]$ não ocorre em nenhuma posição do texto $T$.

---

## 🗂️ Estrutura do Repositório

```text
.
├── c/
│   └── busca_padroes.c          # Implementação em C (Busca Ingênua + KMP)
├── python/
│   └── busca_padroes.py         # Implementação em Python (Busca Ingênua + KMP)
├── entradas/                    # Textos (T_*) e padrões (P_*) gerados para cada cenário e tamanho
├── resultados/
│   ├── benchmark.csv            # Tempos médios e desvios-padrão de todas as execuções
│   ├── grafico_pior_caso_loglog.png
│   ├── grafico_cenarios_c.png
│   └── grafico_razao_teorico_medido.png
├── testes/
│   └── test_corretude.py        # Testes automatizados de corretude das 4 implementações
├── executar_experimentos.py     # Gera as entradas, roda os benchmarks, valida a corretude e plota os gráficos
└── README.md
```

---

## 🚀 Como Executar

### Pré-requisitos
* **C:** Compilador `gcc` (ou `clang`) instalado.
* **Python:** Python `3.10` ou superior, com `matplotlib` (`pip install matplotlib`) para os gráficos.

### 1. Compilando a versão em C
Compile o código com otimização (`-O2`), gerando o binário dentro da pasta `c/`:

```bash
gcc -O2 c/busca_padroes.c -o c/busca_padroes
```

*(No Windows, o binário gerado será `c/busca_padroes.exe`.)*

### 2. Executando um algoritmo individualmente
Ambas as implementações recebem o algoritmo (`ingenua` ou `kmp`), o arquivo do texto e o arquivo do padrão, e imprimem `ocorrencias;tempo_em_segundos`:

```bash
./c/busca_padroes kmp entradas/T_pior_8000.txt entradas/P_pior_8000.txt
python python/busca_padroes.py kmp entradas/T_pior_8000.txt entradas/P_pior_8000.txt
```

A leitura dos arquivos fica fora da medição de tempo; apenas a execução do algoritmo é cronometrada.

### 3. Rodando os testes de corretude
Com o binário em C compilado, rode a partir da raiz do repositório:

```bash
python -m unittest testes/test_corretude.py -v
```

Os testes executam as quatro implementações (C/Python × Ingênua/KMP) sobre as mesmas entradas e verificam que todas retornam o mesmo número de ocorrências, igual ao valor esperado. São cobertos casos com ocorrências sobrepostas, padrão no início e no fim do texto, padrão maior que o texto, padrão de um caractere, recuos da tabela LPS do KMP e 30 entradas aleatórias com semente fixa.

### 4. Executando todos os experimentos
Com o binário em C compilado, rode a partir da raiz do repositório:

```bash
python executar_experimentos.py
```

O script:
1. Gera as entradas em `entradas/` para os cenários de **melhor**, **médio** e **pior** caso, com $n \in \{1.000, 2.000, 4.000, 8.000, 16.000, 32.000\}$ (escala geométrica de razão 2) e $m = \max(10, n/5)$ (semente fixa `42`);
2. Executa cada combinação (C/Python × Ingênua/KMP) **15 vezes**, registrando média e desvio-padrão;
3. Verifica automaticamente que as quatro implementações retornam o mesmo número de ocorrências;
4. Salva os dados em `resultados/benchmark.csv` e gera os gráficos em `resultados/`.

---

## 📈 Resultados Experimentais

Tempos médios de 15 execuções no **pior caso** ($T = \text{"A"}^n$, $P = \text{"A"}^{m-1}\text{"B"}$, $m = n/5$):

| Tamanho ($n$) | Ingênua (C) [s] | KMP (C) [s] | Ingênua (Python) [s] | KMP (Python) [s] |
| :---: | :---: | :---: | :---: | :---: |
| $1.000$ | `0.000039` | `0.000002` | `0.003876` | `0.000114` |
| $2.000$ | `0.000151` | `0.000004` | `0.017490` | `0.000214` |
| $4.000$ | `0.000584` | `0.000007` | `0.074528` | `0.000411` |
| $8.000$ | `0.002248` | `0.000013` | `0.285808` | `0.000802` |
| $16.000$ | `0.008982` | `0.000026` | `1.130713` | `0.001589` |
| $32.000$ | `0.034851` | `0.000057` | `4.587982` | `0.003200` |

* Na Busca Ingênua, tanto em C quanto em Python, dobrar $n$ (e, consequentemente, $m$) multiplica o tempo por aproximadamente $4$, o comportamento quadrático esperado de $O(n \cdot m)$ com $m \propto n$.
* No KMP, dobrar $n$ multiplica o tempo por aproximadamente $2$, o crescimento linear esperado de $\Theta(n + m)$; em Python, a razão $T(n)/(n+m)$ se mantém aproximadamente constante (ver `grafico_razao_teorico_medido.png`).
* Nos cenários de melhor caso e caso médio, os dois algoritmos ficam na mesma ordem de grandeza, já que as falhas ocorrem logo nos primeiros caracteres.
* Os tempos em C são medidos com um relógio de alta precisão (`QueryPerformanceCounter` no Windows, `clock_gettime` no Linux/macOS).

Os dados completos (todos os cenários, com desvio-padrão) estão em `resultados/benchmark.csv`, e os gráficos em `resultados/`.

---

## 🧠 Reflexão sobre $\text{P}$, $\text{NP}$ e o Problema Vizinho

* **Pertinência à classe $\text{P}$:** A busca de padrões em strings pertence à classe **$\text{P}$**, pois ambos os algoritmos resolvem o problema em tempo polinomial determinístico ($O(n \cdot m)$ e $\Theta(n + m)$). Sua versão de decisão pertence a **$\text{NP}$** (já que $\text{P} \subseteq \text{NP}$), com certificado verificável em $O(m)$.
* **Problema Vizinho — Menor Superstring Comum ($\text{SCS}$):** Dado um conjunto de strings $S = \{s_1, s_2, \dots, s_k\}$, consiste em encontrar a menor string $W$ que contenha todas as $s_i$ como substrings.
  * **Por que se torna intratável ($\text{NP-difícil}$):** Enquanto na busca de padrões o texto $T$ é fixo, no problema da Menor Superstring Comum é necessário testar permutações das $k$ strings ($k!$ possibilidades) e decidir sobreposições ótimas entre prefixos e sufixos que afetam globalmente o restante da cadeia.
  * **Redução e Aproximação:** Redutível a partir do **Caminho Hamiltoniano** / **Caixeiro Viajante Assimétrico (ATSP)**. Na prática (como na montagem de genomas), utiliza-se o **Algoritmo Guloso**, que funde iterativamente os pares de maior sobreposição em tempo polinomial com fator de aproximação comprovado de $3.5$.

---

## 👥 Autores

* **Gabriel Pereira Lima**
* **Guilherme Tolentino Leitão de Melo**
* **João Eduardo Andrade de Azevedo** 