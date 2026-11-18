import java.util.ArrayDeque;
import java.util.Queue;
import java.util.Scanner;

/**
 * Simulador do algoritmo de substituicao de paginas FIFO
 * (First-In, First-Out).
 *
 *  A pagina que esta ha mais tempo na memoria e a primeira a ser removida
 * quando todos os frames estao ocupados.
 */
public class FIFO {

    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);

        System.out.println("=== SIMULADOR FIFO ===");

        // ------------------------------------------------------------------
        // 1. Leitura da quantidade de frames
        // ------------------------------------------------------------------
        System.out.print("Quantidade de frames: ");
        int quantidadeFrames;

        try {
            quantidadeFrames = Integer.parseInt(entrada.nextLine().trim());
        } catch (NumberFormatException e) {
            System.out.println("Erro: informe um numero inteiro.");
            entrada.close();
            return;
        }

        if (quantidadeFrames <= 0) {
            System.out.println("Erro: a quantidade de frames deve ser maior que zero.");
            entrada.close();
            return;
        }

        // ------------------------------------------------------------------
        // 2. Leitura da sequencia de paginas (separadas por virgula ou espaco)
        // ------------------------------------------------------------------
        System.out.print("Sequencia de paginas (ex.: 7, 0, 1, 2): ");
        String texto = entrada.nextLine().trim();

        if (texto.isEmpty()) {
            System.out.println("Erro: a sequencia nao pode estar vazia.");
            entrada.close();
            return;
        }

        String[] partes = texto.split("[,\\s]+");
        int[] paginas = new int[partes.length];

        try {
            for (int i = 0; i < partes.length; i++) {
                paginas[i] = Integer.parseInt(partes[i]);

                if (paginas[i] < 0) {
                    System.out.println("Erro: as paginas devem ser numeros nao negativos.");
                    entrada.close();
                    return;
                }
            }
        } catch (NumberFormatException e) {
            System.out.println("Erro: a sequencia possui um valor invalido.");
            entrada.close();
            return;
        }

        // ------------------------------------------------------------------
        // 3. Simulacao
        // ------------------------------------------------------------------
        // A fila mantem as paginas na ordem em que chegaram.
        Queue<Integer> frames = new ArrayDeque<>();
        int faltas = 0;
        int acertos = 0;

        System.out.println("\n--- SIMULACAO ---");

        for (int pagina : paginas) {
            if (frames.contains(pagina)) {
                // A pagina ja esta na memoria: Page Hit.
                acertos++;

                System.out.println("Referencia: " + pagina
                        + " | Frames: " + frames
                        + " | Page Hit"
                        + " | Total Faults: " + faltas);
            } else {
                // A pagina nao esta na memoria: Page Fault.
                faltas++;
                Integer removida = null;

                // Se a fila estiver cheia, remove a pagina mais antiga.
                if (frames.size() == quantidadeFrames) {
                    removida = frames.poll();
                }

                // A nova pagina entra no final da fila.
                frames.offer(pagina);

                System.out.print("Referencia: " + pagina
                        + " | Frames: " + frames
                        + " | Page Fault");

                if (removida != null) {
                    System.out.print(" (substituiu " + removida + ")");
                }

                System.out.println(" | Total Faults: " + faltas);
            }
        }

        // ------------------------------------------------------------------
        // 4. Resultado final
        // ------------------------------------------------------------------
        // Porcentagem de faltas em relacao ao total de referencias.
        double taxaFaltas = (double) faltas / paginas.length * 100.0;

        System.out.println("\n--- RESULTADO FINAL ---");
        System.out.println("Total de referencias: " + paginas.length);
        System.out.println("Total de page faults: " + faltas);
        System.out.println("Total de page hits: " + acertos);
        System.out.printf("Taxa de faltas de pagina: %.2f%%%n", taxaFaltas);

        entrada.close();
    }
}