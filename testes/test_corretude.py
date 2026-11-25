"""Testes de corretude: verifica que as quatro implementações (Ingênua e KMP, em C e em Python)
retornam o mesmo número de ocorrências para as mesmas entradas, e que esse número está correto.

Uso (a partir da raiz do repositório, com o binário em C já compilado):
    python -m unittest testes/test_corretude.py -v
"""

import os
import random
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE_C = os.path.join(RAIZ, "c", "busca_padroes.exe" if os.name == "nt" else "busca_padroes")
SCRIPT_PY = os.path.join(RAIZ, "python", "busca_padroes.py")

IMPLEMENTACOES = [
    ("C", "ingenua", [EXE_C, "ingenua"]),
    ("C", "kmp", [EXE_C, "kmp"]),
    ("Python", "ingenua", [sys.executable, SCRIPT_PY, "ingenua"]),
    ("Python", "kmp", [sys.executable, SCRIPT_PY, "kmp"]),
]


def contar_referencia(texto, padrao):
    """Contagem de referência (com sobreposição), independente das implementações testadas."""
    if not padrao:
        return 0
    return sum(1 for i in range(len(texto) - len(padrao) + 1) if texto[i:i + len(padrao)] == padrao)


def rodar_implementacoes(texto, padrao):
    """Executa as quatro implementações sobre os mesmos arquivos e devolve {nome: ocorrências}."""
    with tempfile.TemporaryDirectory() as pasta:
        arq_t = os.path.join(pasta, "texto.txt")
        arq_p = os.path.join(pasta, "padrao.txt")
        with open(arq_t, "w", encoding="utf-8", newline="") as f:
            f.write(texto)
        with open(arq_p, "w", encoding="utf-8", newline="") as f:
            f.write(padrao)

        respostas = {}
        for lang, alg, base_cmd in IMPLEMENTACOES:
            res = subprocess.run(base_cmd + [arq_t, arq_p], capture_output=True, text=True, check=True)
            respostas[f"{alg} ({lang})"] = int(res.stdout.strip().split(";")[0])
        return respostas


class TestCorretude(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(EXE_C):
            raise unittest.SkipTest(f"Binário em C não encontrado em {EXE_C}. Compile antes de rodar os testes.")

    def verificar(self, texto, padrao, esperado=None):
        if esperado is None:
            esperado = contar_referencia(texto, padrao)
        respostas = rodar_implementacoes(texto, padrao)
        for nome, ocorrencias in respostas.items():
            self.assertEqual(
                ocorrencias, esperado,
                f"{nome} retornou {ocorrencias}, esperado {esperado} (texto={texto[:40]!r}, padrao={padrao[:40]!r})",
            )

    # Casos escritos à mão, com a resposta esperada conhecida
    def test_ocorrencia_unica(self):
        self.verificar("ABCDEF", "CD", 1)

    def test_ocorrencias_sobrepostas(self):
        self.verificar("AAAA", "AA", 3)
        self.verificar("ABABABA", "ABA", 3)

    def test_padrao_no_inicio_e_no_fim(self):
        self.verificar("ABCXXXABC", "ABC", 2)

    def test_padrao_igual_ao_texto(self):
        self.verificar("ABCD", "ABCD", 1)

    def test_nenhuma_ocorrencia(self):
        self.verificar("AAAAAAAA", "AAB", 0)

    def test_padrao_maior_que_texto(self):
        self.verificar("ABC", "ABCD", 0)

    def test_padrao_vazio(self):
        # Convenção adotada nas 4 implementações: padrão vazio não tem ocorrências
        self.verificar("ABC", "", 0)

    def test_padrao_de_um_caractere(self):
        self.verificar("BANANA", "A", 3)

    def test_tabela_lps_com_recuo(self):
        # Exercita os recuos do KMP (falhas no meio de uma borda parcial)
        self.verificar("AABAACAADAABAABA", "AABA", 3)
        self.verificar("ABABDABACDABABCABAB", "ABABCABAB", 1)

    def test_texto_repetitivo_grande(self):
        self.verificar("A" * 1000, "A" * 10, 991)

    # Casos aleatórios com semente fixa (alfabeto pequeno para gerar muitas ocorrências)
    def test_aleatorios(self):
        rng = random.Random(42)
        for _ in range(30):
            n = rng.randint(1, 300)
            m = rng.randint(1, 6)
            texto = "".join(rng.choices("AB", k=n))
            padrao = "".join(rng.choices("AB", k=m))
            with self.subTest(n=n, m=m):
                self.verificar(texto, padrao)


if __name__ == "__main__":
    unittest.main(verbosity=2)
