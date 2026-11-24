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
│   └── busca_padroes.c       # Implementação em C (Busca Ingênua + KMP + Benchmark)
├── python/
│   └── busca_padroes.py      # Implementação em Python (Busca Ingênua + KMP + Benchmark)
├── relatorio/
│   └── relatorio.pdf         # Relatório completo com gráficos e tabelas experimentais
└── README.md                 # Documentação do projeto
```

---

## 🚀 Como Executar

### Pré-requisitos
* **C:** Compilador `gcc` (ou `clang`) instalado.
* **Python:** Python `3.10` ou superior.

### 1. Executando a versão em C
Compile o código com otimização (`-O2`) e execute o binário gerado:

```bash
gcc -O2 c/busca_padroes.c -o busca_padroes
./busca_padroes
```

*(No Windows, execute `busca_padroes.exe` no terminal.)*

### 2. Executando a versão em Python
Execute diretamente via interpretador Python:

```bash
python python/busca_padroes.py
```

---

## 📈 Resultados Experimentais

| Tamanho ($n$) | Cenário | Ingênua (C) [s] | KMP (C) [s] | Ingênua (Python) [s] | KMP (Python) [s] |
| :---: | :--- | :---: | :---: | :---: | :---: |
| $10.000$ | Pior Caso | `-` | `-` | `-` | `-` |
| $100.000$ | Pior Caso | `-` | `-` | `-` | `-` |
| $500.000$ | Pior Caso | `-` | `-` | `-` | `-` |
| $100.000$ | Caso Médio | `-` | `-` | `-` | `-` |
| $500.000$ | Caso Médio | `-` | `-` | `-` | `-` |

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