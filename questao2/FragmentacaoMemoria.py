"""
Simulador de fragmentacao interna com particoes fixas e First-Fit.

Regras do modelo:
    - A memoria possui 1000 unidades divididas em particoes fixas.
    - O algoritmo First-Fit usa a primeira particao livre que comporte o processo.
    - As particoes nao sao divididas nem unidas.
    - Fragmentacao interna = tamanho da particao - espaco usado pelo processo.
"""

# ---------------------------------------------------------------------------
# Configuracao
# ---------------------------------------------------------------------------

MEMORIA_TOTAL = 1000
TAMANHOS = [100, 150, 200, 250, 300]

# Estado da memoria: lista de dicionarios, na ordem em que o First-Fit procura.
particoes = []


# ---------------------------------------------------------------------------
# Inicializacao e calculos
# ---------------------------------------------------------------------------

def criar_memoria():
    """Inicializa a memoria na ordem em que o First-Fit procura."""
    if sum(TAMANHOS) != MEMORIA_TOTAL:
        raise ValueError("As particoes devem somar 1000 unidades.")

    particoes[:] = [
        {"id": i, "tamanho": tamanho, "processo": None, "usado": 0}
        for i, tamanho in enumerate(TAMANHOS, start=1)
    ]


def fragmentacao_interna_total():
    """Soma o desperdicio das particoes ocupadas (livres nao contam)."""
    return sum(
        p["tamanho"] - p["usado"]
        for p in particoes
        if p["processo"] is not None
    )


# ---------------------------------------------------------------------------
# Operacoes de memoria
# ---------------------------------------------------------------------------

def alocar_processo(nome, tamanho):
    """Aloca um processo com First-Fit.

    Retorna True se alocar; rejeicoes preservam o estado da memoria.
    """
    # Validacao da entrada.
    if not isinstance(nome, str) or not nome.strip():
        print("Erro: informe um nome valido.")
        return False
    nome = nome.strip()

    # bool e subtipo de int; nao deve ser aceito como tamanho.
    if isinstance(tamanho, bool) or not isinstance(tamanho, int) or tamanho <= 0:
        print("Erro: tamanho deve ser inteiro positivo.")
        return False

    if any(p["processo"] == nome for p in particoes):
        print(f"Erro: {nome} ja esta alocado.")
        return False

    # Para na PRIMEIRA particao livre suficiente, sem dividir a particao.
    for p in particoes:
        if p["processo"] is None and p["tamanho"] >= tamanho:
            p["processo"] = nome
            p["usado"] = tamanho
            print(f"{nome}: alocado na particao {p['id']} ({p['tamanho']}).")
            print(f"Fragmentacao interna da particao: {p['tamanho'] - tamanho}")
            print(f"Fragmentacao interna total: {fragmentacao_interna_total()}")
            return True

    # Nenhuma particao serviu: explica o motivo da falha.
    livre = sum(p["tamanho"] for p in particoes if p["processo"] is None)
    maior = max(p["tamanho"] for p in particoes)

    print(f"Falha ao alocar {nome} ({tamanho}): nenhuma particao livre comporta.")
    print(f"Memoria livre total: {livre}.")

    if tamanho > maior:
        print(f"O pedido supera a maior particao ({maior}); falharia mesmo vazia.")
    elif livre < tamanho:
        print("A memoria livre total e insuficiente.")
    else:
        print("Ha memoria livre suficiente, mas as particoes fixas nao sao unidas.")

    # Nao inferimos fragmentacao externa: particoes fixas adjacentes
    # continuam separadas por regra, mesmo sem processos entre elas.
    return False


def liberar_processo(nome):
    """Libera a particao inteira, eliminando sua fragmentacao interna."""
    if not isinstance(nome, str) or not nome.strip():
        print("Erro: informe um nome valido.")
        return False
    nome = nome.strip()

    for p in particoes:
        if p["processo"] == nome:
            p["processo"] = None
            p["usado"] = 0
            print(f"{nome}: liberado.")
            print(f"Fragmentacao interna total: {fragmentacao_interna_total()}")
            return True

    print(f"Erro: {nome} nao esta alocado.")
    return False


# ---------------------------------------------------------------------------
# Exibicao
# ---------------------------------------------------------------------------

def exibir_memoria():
    """Exibe as particoes e separa uso real, desperdicio e memoria livre."""
    print("\nID  Tamanho  Processo  Usado  Fragmentacao interna")

    for p in particoes:
        nome = p["processo"] if p["processo"] is not None else "Livre"
        frag = p["tamanho"] - p["usado"] if p["processo"] is not None else 0
        print(f"{p['id']:<3} {p['tamanho']:<8} {nome:<9} {p['usado']:<6} {frag}")

    usado = sum(p["usado"] for p in particoes)
    livre = sum(p["tamanho"] for p in particoes if p["processo"] is None)
    interna = fragmentacao_interna_total()

    print(f"Usado: {usado} | Fragmentacao interna: {interna} | Livre: {livre}")
    print(f"Conferencia: {usado} + {interna} + {livre} = {MEMORIA_TOTAL}\n")


# ---------------------------------------------------------------------------
# Cenario de teste
# ---------------------------------------------------------------------------

def executar_teste():
    """Executa a sequencia de alocacoes e liberacoes do teste."""
    criar_memoria()
    exibir_memoria()

    alocar_processo("P1", 90)
    alocar_processo("P2", 140)
    alocar_processo("P3", 180)
    liberar_processo("P2")
    alocar_processo("P4", 100)
    alocar_processo("P5", 350)

    exibir_memoria()
    print(f"Fragmentacao interna total final: {fragmentacao_interna_total()}")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

# Garante a memoria inicializada tambem quando o modulo e importado.
criar_memoria()

if __name__ == "__main__":
    executar_teste()