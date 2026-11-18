"""
Questão 4 - Garbage Collection em Python

Demonstra, em cinco cenários, como o Python gerencia a memória:
    1. Contagem de referências;
    2. Referência circular entre dois objetos;
    3. Objeto que referencia a si mesmo;
    4. Gerações do coletor de lixo;
    5. Contagem de referências x coleta geracional.
"""

import gc   # coletor de lixo (garbage collector)
import sys  # acesso a sys.getrefcount() e à versão do Python


# ---------------------------------------------------------------------------
# Classe auxiliar
# ---------------------------------------------------------------------------

class Objeto:
    """Objeto que ocupa memória e avisa quando é criado e destruído."""

    def __init__(self, nome):
        """Executa assim que o objeto é criado."""
        self.nome = nome

        # Lista com 100 mil zeros, apenas para ocupar memória.
        self.dados = [0] * 100000

        # Usado nos cenários de referência circular.
        self.referencia = None

        print(f"--- [CRIADO] {self.nome} ---")

    def __del__(self):
        """Executa quando o objeto é destruído."""
        print(f"--- [DESTRUÍDO] {self.nome} ---")


# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------

def titulo(texto):
    """Imprime um cabeçalho para separar os cenários."""
    print("\n" + "=" * 60)
    print(texto)
    print("=" * 60)


# ---------------------------------------------------------------------------
# Cenário 1: contagem de referências
# ---------------------------------------------------------------------------

def cenario_1_contagem_referencias():
    """
    Mostra como funciona a contagem de referências. Cada vez que um objeto
    é referenciado de uma nova forma, o contador dele aumenta.
    """
    titulo("CENÁRIO 1 - Contagem de referências")

    a = Objeto("A")

    # sys.getrefcount(a) conta quantas referências existem para o objeto.
    # O valor mostrado é sempre 1 a mais, pois a própria chamada da função
    # cria uma referência temporária.
    print(f"  Variável 'a': {sys.getrefcount(a)}")

    b = a  # b aponta para o mesmo objeto (+1 referência)
    print(f"  b = a: {sys.getrefcount(a)}")

    lista = [a, a]  # cada elemento conta como uma referência (+2)
    print(f"  lista = [a, a]: {sys.getrefcount(a)}")

    del lista
    print(f"  Lista deletada: {sys.getrefcount(a)}")

    del b
    print(f"  'b' deletado: {sys.getrefcount(a)}")

    del a  # o contador chega a 0 e o objeto é destruído na hora


# ---------------------------------------------------------------------------
# Cenário 2: referência circular sem coletor (vazamento)
# ---------------------------------------------------------------------------

def cenario_2_referencia_circular():
    """
    Mostra o efeito da referência circular: dois objetos que se referenciam
    formam um ciclo. Mesmo após o del das variáveis, os contadores não
    chegam a zero e os objetos continuam ocupando memória.

    Observação: o número retornado por gc.collect() não é só a quantidade de
    objetos Objeto. Ele também inclui as estruturas internas que o coletor
    rastreia, como a lista 'dados' de cada objeto.
    """
    titulo("CENÁRIO 2 - Referência circular (coletor desligado)")

    gc.collect()  # limpa objetos pendentes antes do teste

    # Desligamos o coletor para que os objetos não sejam removidos sozinhos.
    gc.disable()

    # Criação de dois objetos.
    x = Objeto("X")
    y = Objeto("Y")

    # Referência circular.
    x.referencia = y  # X aponta para Y
    y.referencia = x  # Y aponta para X (ciclo)

    print(f"Referências de X: {sys.getrefcount(x)}")
    print(f"Referências de Y: {sys.getrefcount(y)}")

    print("Removendo as variáveis x e y...")
    del x
    del y

    # Nada foi destruído: cada objeto ainda é referenciado pelo outro,
    # então os contadores não chegam a zero.
    print("Sem mensagem de delete. Os objetos continuam na memória")

    # Chamada manual do coletor: ele identifica os objetos presos no ciclo.
    inalcancaveis = gc.collect()

    print(f"gc.collect() encontrou {inalcancaveis} objetos inalcançáveis "
        "(os objetos X e Y e as listas 'dados' de cada um)")

    gc.enable()  # religa o coletor automático


# ---------------------------------------------------------------------------
# Cenário 3: objeto que referencia a si mesmo
# ---------------------------------------------------------------------------

def cenario_3_autorreferencia():
    """
    Funciona de forma parecida com o cenário 2, mas o ciclo é formado por um
    único objeto que aponta para si mesmo.
    """
    titulo("CENÁRIO 3 - Objeto que referencia a si mesmo")

    gc.collect()
    gc.disable()

    z = Objeto("Z")
    z.referencia = z  # o objeto guarda uma referência para ele mesmo

    # Total: variável z + autorreferência + referência temporária da chamada.
    print(f"Referências de Z: {sys.getrefcount(z)}")

    del z
    print(" Depois de del z, o objeto ainda existe (nenhuma mensagem).")

    gc.collect()
    gc.enable()


# ---------------------------------------------------------------------------
# Cenário 4: gerações do coletor
# ---------------------------------------------------------------------------

def cenario_4_geracoes():
    """
    O coletor divide os objetos em 3 gerações:
        - geração 0: objetos novos;
        - geração 1: objetos que sobreviveram a uma coleta da geração 0;
        - geração 2: objetos antigos.
    """
    titulo("CENÁRIO 4 - Gerações do coletor de lixo")

    # Limites: quantas alocações (geração 0) ou coletas (gerações 1 e 2)
    # são necessárias para disparar a coleta daquela geração.
    print(f"Limites (threshold): {gc.get_threshold()}")

    gc.collect()  # começa com os contadores zerados
    print(f"  Contadores logo após gc.collect(): {gc.get_count()}")

    # Cria vários objetos pequenos que ficam vivos em uma lista
    # (assim o contador da geração 0 sobe).
    lista = [[] for _ in range(500)]
    print(f"  Contadores após criar 500 listas:  {gc.get_count()}")

    # Objetos que sobrevivem a uma coleta são promovidos para a geração
    # seguinte (0 -> 1 -> 2), pois provavelmente viverão mais tempo.
    gc.collect(0)
    print(f"  Contadores após coletar a geração 0: {gc.get_count()}")

    gc.collect(1)
    print(f"  Contadores após coletar a geração 1: {gc.get_count()}")

    del lista


# ---------------------------------------------------------------------------
# Cenário 5: contagem de referências x coleta geracional
# ---------------------------------------------------------------------------

def cenario_5_comparacao():
    """Compara objetos sem ciclo (contagem de referências) e com ciclo (coletor)."""
    titulo("CENÁRIO 5 - Contagem de referências x coleta geracional")

    gc.collect()
    gc.disable()

    # Parte 1: objetos SEM ciclo (a contagem de referências resolve sozinha).
    print("  Parte 1 - 3 objetos sem ciclo:")
    for i in range(3):
        Objeto(f"Simples{i}")  # sem variável, é destruído na hora

    print(f"  gc.collect() liberou: {gc.collect()} objeto(s) (nada sobrou,")
    print("  a contagem de referências já tinha feito tudo)")

    # Parte 2: objetos COM ciclo (só o coletor geracional resolve).
    print("\n  Parte 2 - 3 pares de objetos com ciclo:")
    for i in range(3):
        p = Objeto(f"Par{i}-a")
        q = Objeto(f"Par{i}-b")
        p.referencia = q
        q.referencia = p
        del p, q  # os contadores continuam > 0 por causa do ciclo

    print("  Nenhum objeto foi destruído ainda. Chamando gc.collect()...")

    liberados = gc.collect()
    print(f"  gc.collect() encontrou {liberados} objeto(s) inalcançável(is).")
    print("  Obs.: são os 6 objetos criados mais as estruturas internas de cada")
    print("  um (como a lista 'dados'), por isso o número é maior que 6.")

    gc.enable()


# ---------------------------------------------------------------------------
# Estatísticas do coletor
# ---------------------------------------------------------------------------

def exibir_estatisticas():
    """Exibe, por geração, as estatísticas acumuladas do coletor."""
    titulo("ESTATÍSTICAS DO COLETOR - gc.get_stats()")

    # gc.get_stats() retorna uma lista com um dicionário por geração.
    for numero, estatistica in enumerate(gc.get_stats()):
        print(f"  Geração {numero}:")
        print(f"    coletas realizadas:      {estatistica['collections']}")
        print(f"    objetos coletados:       {estatistica['collected']}")
        print(f"    objetos não coletáveis:  {estatistica['uncollectable']}")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main():
    print("DEMONSTRAÇÃO DO GARBAGE COLLECTOR DO PYTHON")
    print(f"Versão do Python: {sys.version.split()[0]}")

    try:
        cenario_1_contagem_referencias()
        cenario_2_referencia_circular()
        cenario_3_autorreferencia()
        cenario_4_geracoes()
        cenario_5_comparacao()
        exibir_estatisticas()
    except Exception as erro:
        # Garante que o coletor volte ao normal mesmo se algo der errado.
        gc.enable()
        print(f"Erro durante a execução: {erro}")
        raise


if __name__ == "__main__":
    main()