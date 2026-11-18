/*
 * ============================================================================
 *  ALOCACAO ESTATICA x ALOCACAO DINAMICA
 * ============================================================================
 *  Disciplina : Sistemas Operacionais
 *  Objetivo   : Comparar um vetor de duracao estatica com um vetor alocado
 *               dinamicamente (heap), exibindo valores, enderecos e tamanhos.
 * ============================================================================
 */

#if defined(__MINGW32__)
#define __USE_MINGW_ANSI_STDIO 1
#endif

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>

/* ------------------------------------------------------------------------- */
/*  Constantes                                                               */
/* ------------------------------------------------------------------------- */

#define TAM_ESTATICO  5
#define TAM_DINAMICO  10

/* ------------------------------------------------------------------------- */
/*  Programa principal                                                       */
/* ------------------------------------------------------------------------- */

int main(void)
{
    /* 1. Declaracao e alocacao ------------------------------------------- */

    /* "static" garante duracao estatica: este vetor nao fica na pilha. */
    static int array_estatico[TAM_ESTATICO];

    /* Bloco alocado no heap; precisa ser liberado com free(). */
    int *array_dinamico = malloc(TAM_DINAMICO * sizeof *array_dinamico);

    /* Verifica a alocacao antes de acessar o bloco. */
    if (array_dinamico == NULL) {
        fprintf(stderr, "Erro: nao foi possivel alocar memoria.\n");
        return EXIT_FAILURE;
    }

    /* 2. Preenchimento dos vetores --------------------------------------- */

    for (int i = 0; i < TAM_ESTATICO; i++) {
        array_estatico[i] = i + 1;
    }

    for (int i = 0; i < TAM_DINAMICO; i++) {
        array_dinamico[i] = i + 10;
    }

    /* 3. Exibicao de valores e enderecos --------------------------------- */

    printf("Array estatico - base: %p\n", (void *)array_estatico);
    for (int i = 0; i < TAM_ESTATICO; i++) {
        printf("[%d] valor = %d | endereco = %p\n",
               i, array_estatico[i], (void *)&array_estatico[i]);
    }

    printf("\nArray dinamico - base: %p\n", (void *)array_dinamico);
    for (int i = 0; i < TAM_DINAMICO; i++) {
        printf("[%d] valor = %d | endereco = %p\n",
               i, array_dinamico[i], (void *)&array_dinamico[i]);
    }

    /* 4. Distancia entre os enderecos ------------------------------------ */

    /*
     * Nao subtrair ponteiros de objetos distintos diretamente.
     * uintptr_t permite comparar suas representacoes numericas neste
     * ambiente. A interpretacao como distancia em bytes depende da
     * representacao de enderecos da plataforma e nao e garantia geral de C.
     * Os valores observados sao enderecos virtuais, nao memoria fisica.
     */
    uintptr_t a = (uintptr_t)array_estatico;
    uintptr_t b = (uintptr_t)array_dinamico;
    uintptr_t diferenca = (a >= b) ? a - b : b - a;

    printf("\nDiferenca absoluta entre enderecos: %" PRIuPTR "\n", diferenca);
    printf("Em plataformas de enderecamento linear, esse valor esta em bytes.\n");

    /* 5. Tamanhos -------------------------------------------------------- */

    printf("sizeof(int): %zu bytes\n", sizeof(int));
    printf("Tamanho estatico: %zu bytes\n", sizeof array_estatico);
    printf("Tamanho dinamico: %zu bytes\n", TAM_DINAMICO * sizeof *array_dinamico);

    /* A distancia pode variar; ela, isoladamente, nao identifica regioes. */

    /* 6. Liberacao da memoria dinamica ----------------------------------- */

    free(array_dinamico);
    array_dinamico = NULL;
    printf("Memoria dinamica liberada.\n");

    return EXIT_SUCCESS;
}