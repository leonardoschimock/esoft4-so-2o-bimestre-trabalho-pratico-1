import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Scanner;

/**
 * Questao Bonus - Simulador de substituicao de paginas.
 *
 * <p>Executa os algoritmos FIFO e LRU sobre a mesma sequencia de referencias
 * e compara a quantidade de faltas de pagina (page faults) de cada um.</p>
 */
public class QBonus {

    // ======================================================================
    // Estatisticas
    // ======================================================================

    /** Armazena as estatisticas de execucao de um algoritmo. */
    static class Resultado {
        int faltas;
        int totalReferencias;
        double taxa;

        Resultado(int faltas, int totalReferencias) {
            this.faltas = faltas;
            this.totalReferencias = totalReferencias;
            this.taxa = (double) faltas / totalReferencias * 100;
        }
    }

    // ======================================================================
    // Algoritmo FIFO - primeiro que entra, primeiro que sai
    // ======================================================================

    public static Resultado executarFIFO(int quantidadeFrames, int[] paginas) {
        Queue<Integer> frames = new LinkedList<>();
        int faltas = 0;

        System.out.println("\n========== ALGORITMO FIFO ==========");

        for (int pagina : paginas) {
            // Verifica se a pagina ja esta na memoria.
            if (frames.contains(pagina)) {
                System.out.println("Página: " + pagina
                        + " | Frames: " + frames
                        + " | PAGE HIT");
            } else {
                faltas++;
                String substituicao = "";

                // Se todos os frames estiverem ocupados,
                // remove a pagina que entrou primeiro.
                if (frames.size() == quantidadeFrames) {
                    int removida = frames.poll();
                    substituicao = " | Substituiu: " + removida;
                }

                // Adiciona a nova pagina.
                frames.add(pagina);

                System.out.println("Página: " + pagina
                        + " | Frames: " + frames
                        + " | PAGE FAULT" + substituicao);
            }
        }

        return new Resultado(faltas, paginas.length);
    }

    // ======================================================================
    // Algoritmo LRU - menos recentemente utilizada
    // ======================================================================

    public static Resultado executarLRU(int quantidadeFrames, int[] paginas) {
        // Paginas presentes na memoria.
        List<Integer> frames = new ArrayList<>();

        // Ultimo instante de uso de cada pagina.
        Map<Integer, Integer> ultimoUso = new HashMap<>();

        int faltas = 0;
        int tempo = 0;

        System.out.println("\n========== ALGORITMO LRU ==========");

        for (int pagina : paginas) {
            // Cada referencia recebe um novo instante.
            tempo++;

            // Verifica se a pagina ja esta carregada.
            if (frames.contains(pagina)) {
                // Atualiza o timestamp da pagina acessada.
                ultimoUso.put(pagina, tempo);

                System.out.println("Página: " + pagina
                        + " | Frames: " + frames
                        + " | PAGE HIT");
            } else {
                faltas++;
                String substituicao = "";

                // Verifica se a memoria esta cheia.
                if (frames.size() == quantidadeFrames) {
                    // Comeca considerando a primeira pagina.
                    int menosRecente = frames.get(0);

                    // Procura a pagina com o menor timestamp.
                    for (int p : frames) {
                        if (ultimoUso.get(p) < ultimoUso.get(menosRecente)) {
                            menosRecente = p;
                        }
                    }

                    // Remove a pagina menos recentemente utilizada.
                    frames.remove(Integer.valueOf(menosRecente));
                    ultimoUso.remove(menosRecente);

                    substituicao = " | Substituiu: " + menosRecente;
                }

                // Insere a nova pagina no frame disponivel.
                frames.add(pagina);

                // Registra o instante de entrada/ultimo uso.
                ultimoUso.put(pagina, tempo);

                System.out.println("Página: " + pagina
                        + " | Frames: " + frames
                        + " | PAGE FAULT" + substituicao);
            }
        }

        return new Resultado(faltas, paginas.length);
    }

    // ======================================================================
    // Programa principal
    // ======================================================================

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("======================================");
        System.out.println(" SIMULADOR DE SUBSTITUICAO DE PAGINAS");
        System.out.println("======================================");

        // ------------------------------------------------------------------
        // 1. Leitura da quantidade de frames
        // ------------------------------------------------------------------
        System.out.print("\nQuantidade de frames: ");

        int quantidadeFrames;

        try {
            quantidadeFrames = Integer.parseInt(scanner.nextLine().trim());

            if (quantidadeFrames <= 0) {
                System.out.println("Erro: a quantidade de frames deve ser positiva.");
                return;
            }
        } catch (NumberFormatException e) {
            System.out.println("Erro: informe uma quantidade válida de frames.");
            return;
        }

        // ------------------------------------------------------------------
        // 2. Leitura da sequencia de referencias
        // ------------------------------------------------------------------
        System.out.print("Sequência de páginas (separadas por vírgula): ");

        String entrada = scanner.nextLine().trim();

        try {
            if (entrada.isEmpty()) {
                throw new IllegalArgumentException();
            }

            String[] valores = entrada.split(",", -1);
            int[] paginas = new int[valores.length];

            // Converte cada referencia para inteiro.
            for (int i = 0; i < valores.length; i++) {
                if (valores[i].trim().isEmpty()) {
                    throw new IllegalArgumentException();
                }

                paginas[i] = Integer.parseInt(valores[i].trim());
            }

            // --------------------------------------------------------------
            // 3. Execucao de FIFO e LRU com os mesmos dados
            // --------------------------------------------------------------
            Resultado fifo = executarFIFO(quantidadeFrames, paginas);
            Resultado lru = executarLRU(quantidadeFrames, paginas);

            // --------------------------------------------------------------
            // 4. Comparacao final
            // --------------------------------------------------------------
            System.out.println("\n========== COMPARAÇÃO FINAL ==========");

            System.out.println("\nFIFO");
            System.out.println("Faltas de página: " + fifo.faltas);
            System.out.printf("Taxa de faltas: %.2f%%\n", fifo.taxa);

            System.out.println("\nLRU");
            System.out.println("Faltas de página: " + lru.faltas);
            System.out.printf("Taxa de faltas: %.2f%%\n", lru.taxa);

            // Analise automatica dos resultados.
            System.out.println("\n========== ANÁLISE COMPARATIVA ==========");

            if (lru.faltas < fifo.faltas) {
                System.out.println("O LRU apresentou menos faltas de página.");
                System.out.println("Diferença: "
                        + (fifo.faltas - lru.faltas) + " falta(s) a menos.");
            } else if (fifo.faltas < lru.faltas) {
                System.out.println("O FIFO apresentou menos faltas de página.");
                System.out.println("Diferença: "
                        + (lru.faltas - fifo.faltas) + " falta(s) a menos.");
            } else {
                System.out.println("Os dois algoritmos apresentaram a mesma quantidade de faltas.");
            }

            System.out.println("\nTotal de referências: " + paginas.length);

        } catch (IllegalArgumentException e) {
            System.out.println("Erro: informe somente números inteiros separados por vírgula.");
        } finally {
            scanner.close();
        }
    }
}