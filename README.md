# Gerenciamento de Memória em Sistemas Operacionais

Trabalho prático da disciplina de **Sistemas Operacionais** — Engenharia de Software, **Universidade Cesumar (UniCesumar)**, Curitiba, 2026.

O projeto reúne cinco simulações e uma questão bônus sobre gerenciamento de memória: alocação estática e dinâmica, fragmentação, substituição de páginas (FIFO e LRU), coleta de lixo em Python e desempenho de pilha (*stack*) versus *heap*. O relatório completo, com fundamentação teórica, resultados e análises, está em `docs/`.

## Índice
- [Integrantes](#integrantes)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Resumo das Questões](#resumo-das-questões)
- [Pré Requisitos](#pré-requisitos)
- [Como Executar](#como-executar)
- [Questão 01](#questão-1--alocação-estática-vs-dinâmica)
- [Questão 02](#questão-2--fragmentação-de-memória)
- [Questão 03](#questão-3--fifo)
- [Questão 04](#questão-4--garbage-collection-em-python)
- [Questão 05](#questão-5--pilha-vs-heap)
- [Bonus](#bônus--fifo-vs-lru)
- [Compilação Rápida e Otimizada](#compilação-rápida-e-otimizada)
- [Referências](#referências-principais)


## Integrantes

| Nome | RA |
| --- | --- |
| Arthur de Andrade Malvaso | 25212854-2 |
| Alex Rafael Ferreira | 25169060-2 |
| Carlos Eduardo da Silva | 25034198-2 |
| Isadora Tereza Taques Fernandes | 25216341-2 |
| Jean Carlos dos Santos | 25357718-2 |
| Leonardo Schimock Silveira | 25363487-2 |
| Maria Clara Vichinheski da Silva | 26004659-2 |

## Estrutura do repositório

```
trabalho-pratico-sistemas-operacionais/
├── questao1/   AlocacaoEstaticaDinamica.c
├── questao2/   FragmentacaoMemoria.py
├── questao3/   FIFO.java
├── questao4/   GarbageCollection.py
├── questao5/   ComparacaoDesempenhoAlocacao.c
├── bonus/      QBonus.java
├── docs/       trabalho-sistemas-operacionais.pdf
└── README.md
```

## Resumo das questões

| # | Tema | Linguagem | Arquivo |
| --- | --- | --- | --- |
| 1 | Alocação estática vs. dinâmica | C | `questao1/AlocacaoEstaticaDinamica.c` |
| 2 | Simulação de fragmentação de memória (First-Fit, partições fixas) | Python | `questao2/FragmentacaoMemoria.py` |
| 3 | Algoritmo de substituição de páginas FIFO | Java | `questao3/FIFO.java` |
| 4 | Garbage collection em Python | Python | `questao4/GarbageCollection.py` |
| 5 | Comparação de desempenho: pilha vs. heap | C | `questao5/ComparacaoDesempenhoAlocacao.c` |
| Bônus | Algoritmo LRU comparado ao FIFO | Java | `bonus/QBonus.java` |

## Pré-requisitos

| Ferramenta | Usada em | Observação |
| --- | --- | --- |
| GCC (com suporte a C11) | Questões 1 e 5 | No Windows, MinGW ou Dev-C++ |
| Python 3 | Questões 2 e 4 | Apenas biblioteca padrão (`gc`, `sys`) |
| JDK (Java Development Kit) | Questão 3 e Bônus | `javac` e `java` no PATH |

Nenhuma biblioteca externa precisa ser instalada.

## Como executar

Abra o terminal na pasta de cada questão antes de rodar os comandos.

### Questão 1 — Alocação estática vs. dinâmica

```bash
cd questao1
gcc -Wall -Wextra -std=c11 AlocacaoEstaticaDinamica.c -o AlocacaoEstaticaDinamica
./AlocacaoEstaticaDinamica          # Windows: .\AlocacaoEstaticaDinamica.exe
```

Declara um vetor local de 5 inteiros e outro de 10 inteiros alocado com `malloc`, imprime valores e endereços, calcula a distância entre os endereços base e libera o bloco com `free`. Os endereços variam a cada execução.

### Questão 2 — Fragmentação de memória

```bash
cd questao2
python FragmentacaoMemoria.py       # em alguns sistemas: python3
```

Memória de 1.000 unidades dividida em partições fixas de 100, 150, 200, 250 e 300, com alocação First-Fit. A sequência de teste executa automaticamente:

| Operação | Resultado | Fragmentação interna total |
| --- | --- | --- |
| P1 — 90 | Partição 1 (100) | 10 |
| P2 — 140 | Partição 2 (150) | 20 |
| P3 — 180 | Partição 3 (200) | 40 |
| Liberar P2 | Partição 2 livre | 30 |
| P4 — 100 | Partição 2 (150) | 80 |
| P5 — 350 | Falha (maior partição: 300) | 80 |

### Questão 3 — FIFO

```bash
cd questao3
javac FIFO.java
java FIFO
```

Entrada de teste: **3** frames e a sequência `7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2` (aceita vírgulas ou espaços).
Resultado esperado: **10 page faults, 3 page hits, taxa de faltas de 76,92%**.

### Questão 4 — Garbage collection em Python

```bash
cd questao4
python GarbageCollection.py         # em alguns sistemas: python3
```

Cinco cenários: contagem de referências, referência circular, autorreferência, gerações do coletor e comparação entre os dois mecanismos, seguidos das estatísticas de `gc.get_stats()`. Os valores de `gc.get_threshold()`, `gc.get_count()` e `gc.get_stats()` dependem da versão do Python e do estado do coletor.

### Questão 5 — Pilha vs. heap

```bash
cd questao5
gcc -Wall -Wextra -std=c11 ComparacaoDesempenhoAlocacao.c -o ComparacaoDesempenhoAlocacao
./ComparacaoDesempenhoAlocacao      # Windows: .\ComparacaoDesempenhoAlocacao.exe
```

Também é possível abrir o arquivo no Dev-C++ e usar **Executar > Compilar e Executar (F11)**.

São 1.000.000 de operações por teste, repetidas 5 vezes, na pilha (variável local de 32 bytes) e no heap (pares `malloc()`/`free()` do mesmo tamanho). Nas medições do relatório o heap foi, em média, cerca de 11,8 vezes mais lento. Como `clock()` tem resolução de 1 ms, esse valor deve ser lido como ordem de grandeza.

### Bônus — FIFO vs. LRU

```bash
cd bonus
javac QBonus.java
java QBonus
```

Entrada de teste: **3** frames e a sequência `7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2`. Nesta versão os números devem ser separados por **vírgula**.

| Indicador | FIFO | LRU |
| --- | --- | --- |
| Page faults | 10 | 9 |
| Page hits | 3 | 4 |
| Taxa de faltas | 76,92% | 69,23% |

Nesta sequência o LRU teve uma falta a menos, mas um único teste curto não permite concluir que ele é sempre superior; a análise completa está no relatório.

## Compilação Rápida e Otimizada
[Códigos Java - FIFO e LRU](https://onlinegdb.com/PNa4kTfy1a)<br>
[Garbage Collection](https://onlinegdb.com/y83lxOuYU)<br>
[Fragmentação de Memória](https://onlinegdb.com/lSzf_fNvw)<br>
[Alocação Dinâmica e Estática](https://onlinegdb.com/MyFS6ISA4O)<br>
[Pilha x Heap](https://onlinegdb.com/bR0QkMYYkO)<br>

## Referências principais

- ARPACI-DUSSEAU, Remzi H.; ARPACI-DUSSEAU, Andrea C. *Operating Systems: Three Easy Pieces*. Arpaci-Dusseau Books, 2018.
- SILBERSCHATZ, Abraham; GALVIN, Peter B.; GAGNE, Greg. *Operating System Concepts*. 10. ed. Wiley, 2018.
- KERNIGHAN, Brian W.; RITCHIE, Dennis M. *The C Programming Language*. 2. ed. Prentice Hall, 1988.
- Documentação do Python: módulos [`gc`](https://docs.python.org/3/library/gc.html) e `sys`.

A lista completa está na seção *Referências* do relatório em `docs/`.
