/*
 * ============================================================================
 *  ATIVIDADE 05 - COMPARACAO DE DESEMPENHO DE ALOCACAO
 * ============================================================================
 *  Disciplina : Sistemas Operacionais
 *  Aluno      : Alex Rafael Ferreira
 *  Curso      : Engenharia de Software
 *
 *  Objetivo   : Comparar o tempo de alocacao na PILHA (stack) e no MONTE (heap).
 *
 *  Metodologia:
 *    - 1.000.000 de operacoes na stack por teste;
 *    - 1.000.000 de operacoes no heap por teste;
 *    - cada teste e repetido 5 vezes e e calculada a media dos tempos.
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/* ------------------------------------------------------------------------- */
/*  Constantes                                                               */
/* ------------------------------------------------------------------------- */

#define NUM_OPERACOES 1000000   /* operacoes por teste   */
#define NUM_EXECUCOES 5         /* repeticoes de teste   */

/* ------------------------------------------------------------------------- */
/*  Tipos                                                                    */
/* ------------------------------------------------------------------------- */

/* Estrutura utilizada nos dois testes. */
typedef struct {
    int    id;
    double valor;
    char   nome[16];
} Objeto;

/* ------------------------------------------------------------------------- */
/*  Teste 1 - Alocacao na pilha (stack)                                      */
/* ------------------------------------------------------------------------- */

/*
 * Cria uma variavel local, armazenada na stack. Quando a funcao termina,
 * a memoria utilizada pela variavel e liberada automaticamente.
 */
static long usar_variavel_local(int i)
{
    volatile Objeto obj;

    obj.id = i;
    obj.valor = i * 1.5;
    obj.nome[0] = 'A';

    /* Retorna dados para garantir o uso da variavel. */
    return obj.id + obj.nome[0];
}

/*
 * Executa NUM_OPERACOES chamadas da funcao acima e mede o tempo total
 * com clock(). Retorna o tempo em segundos.
 */
static double testar_pilha(double *soma)
{
    clock_t inicio, fim;
    int i;

    inicio = clock();

    for (i = 0; i < NUM_OPERACOES; i++) {
        *soma += usar_variavel_local(i);
    }

    fim = clock();

    return (double)(fim - inicio) / CLOCKS_PER_SEC;
}

/* ------------------------------------------------------------------------- */
/*  Teste 2 - Alocacao no heap (monte)                                       */
/* ------------------------------------------------------------------------- */

/*
 * Utiliza malloc() para reservar memoria dinamicamente e free() para
 * libera-la apos o uso. Retorna o tempo total em segundos.
 */
static double testar_heap(double *soma)
{
    clock_t inicio, fim;
    int i;
    volatile Objeto *obj;

    inicio = clock();

    for (i = 0; i < NUM_OPERACOES; i++) {
        /* Reserva memoria no heap. */
        obj = (volatile Objeto *)malloc(sizeof(Objeto));

        /* Verifica se a alocacao funcionou. */
        if (obj == NULL) {
            printf("Erro ao alocar memoria!\n");
            exit(1);
        }

        /* Preenche os dados do objeto. */
        obj->id = i;
        obj->valor = i * 1.5;
        obj->nome[0] = 'A';

        /* Utiliza os dados do objeto. */
        *soma += obj->id + obj->nome[0];

        /* Libera a memoria utilizada. */
        free((void *)obj);
    }

    fim = clock();

    return (double)(fim - inicio) / CLOCKS_PER_SEC;
}

/* ------------------------------------------------------------------------- */
/*  Funcao principal                                                         */
/* ------------------------------------------------------------------------- */

int main(void)
{
    int i;

    double tempo_pilha;
    double tempo_heap;

    double total_pilha = 0.0;
    double total_heap = 0.0;

    double media_pilha;
    double media_heap;
    double diferenca;

    /* Acumula os resultados para impedir que o compilador elimine os testes. */
    double soma = 0.0;

    /* Cabecalho --------------------------------------------------------- */

    printf("============================================\n");
    printf(" COMPARACAO DE DESEMPENHO DE ALOCACAO\n");
    printf("============================================\n");
    printf("Operacoes por teste: %d\n", NUM_OPERACOES);
    printf("Quantidade de testes: %d\n\n", NUM_EXECUCOES);
    printf("INICIANDO OS TESTES...\n\n");

    /* Execucao dos testes (repetidos para calcular a media) -------------- */

    for (i = 0; i < NUM_EXECUCOES; i++) {
        tempo_pilha = testar_pilha(&soma);
        tempo_heap = testar_heap(&soma);

        total_pilha += tempo_pilha;
        total_heap += tempo_heap;

        printf("Teste %d:\n", i + 1);
        printf("Tempo na Stack: %.6f segundos\n", tempo_pilha);
        printf("Tempo no Heap: %.6f segundos\n\n", tempo_heap);
    }

    /* Calculo das medias ------------------------------------------------- */

    media_pilha = total_pilha / NUM_EXECUCOES;
    media_heap = total_heap / NUM_EXECUCOES;

    /* Resultados finais -------------------------------------------------- */

    printf("============================================\n");
    printf(" RESULTADO FINAL\n");
    printf("============================================\n");
    printf("Media da Stack: %.6f segundos\n", media_pilha);
    printf("Media do Heap: %.6f segundos\n", media_heap);

    /* Diferenca percentual do heap em relacao a stack. */
    if (media_pilha > 0.0) {
        diferenca = ((media_heap - media_pilha) / media_pilha) * 100.0;

        printf("\nDiferenca percentual: %.2f%%\n", diferenca);

        if (media_heap > media_pilha) {
            printf("\nA Stack foi mais rapida neste teste.\n");
        } else if (media_heap < media_pilha) {
            printf("\nO Heap foi mais rapido neste teste.\n");
        } else {
            printf("\nOs dois testes apresentaram tempos iguais.\n");
        }
    } else {
        printf("\nNao foi possivel calcular a diferenca percentual.\n");
    }

    printf("\nValor de verificacao: %.2f\n", soma);

    printf("\n============================================\n");
    printf(" FIM DOS TESTES\n");
    printf("============================================\n");

    return 0;
}