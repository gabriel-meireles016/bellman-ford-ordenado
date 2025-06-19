import sys
from collections import defaultdict

# estrutura de dados usada para armazenar o grafo
grafo = {
    'num_vert': 0,
    'num_arc': 0,
    'vertice': {},
    'arco': [],
    'adj': defaultdict(list)
}

# função para leitura dos arquivos de entrada
def leitura_arquivo(arquivo):
    with open(arquivo, 'r') as arq:
        for linha in arq:
            linha = linha.strip()
            if (not linha) or (linha == 'T'):
                break
            
            partes = linha.split()
            tipo = partes[0]

            # leitura dos números de vértices e arestas
            if tipo == 'I':
                grafo['num_vert'] = int(partes[1])
                grafo['num_arc'] = int(partes[2])
            # leitura dos vértices e seus atributos
            elif tipo == 'N':
                id_v = int(partes[1])
                g_e = int(partes[2])
                g_s = int(partes[3])
                grafo['vertice'][id_v] = {
                    'grau_entrada': g_e,    # graus de entrada e saída não são utilizados no algoritmo, podem ser substituidos apenas por True
                    'grau_saida': g_s       # foram mantidos para algoritmos futuros, caso sejam solicitados
                }
            # leitura das arestas e seus atributos
            elif tipo == 'E':
                origem = int(partes[1])
                destino = int(partes[2])
                custo = int(partes[3])
                grafo['arco'].append({
                    'origem': origem,
                    'destino': destino,
                    'custo': custo
                })
                grafo['adj'][origem].append((destino, custo))

# função para criar as listas de ordem par e ímpar (OP e OI)
def ordem_O(s, n):
    OI = list(range(n)) # ordem crescente
    OI.remove(s)        # remove o vértice s do vetor
    OI.insert(0, s)     # coloca o vértice s na primeira posição

    OP = list(range(n))     # ordem decrescente
    OP.remove(s)            # remove o vértice s do vetor
    OP = list(reversed(OP)) # inverte para a ordem decrescente
    OP.insert(0,s)          # coloca o vértice s na primeira posição

    return OI, OP

# função que identifica se existe ciclo negativo e, caso exista, o imprime
def ciclo_negativo(n, g, ant, dist):
    # última rodada para ver se há ciclo negativo
    ciclo_neg = False
    
    # itera mais uma vez sobre todas as arestas do grafo
    for arco in g['arco']:
        u, v, custo = arco['origem'], arco['destino'], arco['custo']
        # se for possível relaxar uma aresta, significa que existe um ciclo negativo
        if dist[u] + custo < dist[v]:
            ciclo_neg = True    # ciclo encontrado
            print("CN")
            
            ciclo = []          # lista para vértices do ciclo
            visitado = set()    # conjunto que vai detectar repetição de vértices do ciclo
            x = v               # começa do destino da aresta que foi relaxada

            # retrocede n passos para garantir que está no ciclo
            for _ in range(n):
                x = ant[x]

            # reconstrói o ciclo percorrendo predecessores até fechar o ciclo
            while x not in visitado:
                visitado.add(x)
                ciclo.append(x)
                x = ant[x]
            ciclo.append(x) # adiciona o vértice que fecha o ciclo
            ciclo.reverse() # inverte o ciclo para que fique na ordem certa

            # remove o último vértice que é o mesmo do primeiro para organização
            aux = ciclo[:-1]

            # encontra o vértice de menor ID
            menor_id = aux.index(min(aux))

            # reorganiza o ciclo para começar do menor vértice encontrado na linha anterior
            ciclo_ordenado = aux[menor_id:] + aux[:menor_id]
            ciclo_ordenado.append(ciclo_ordenado[0])

            # calcula o custo do ciclo
            custo_ciclo = 0
            for i in range(len(ciclo_ordenado) - 1):
                u = ciclo_ordenado[i]
                v = ciclo_ordenado[i + 1]
                for arco in g['arco']:
                    if arco['origem'] == u and arco['destino'] == v:
                        custo_ciclo += arco['custo']
                        break
            
            # impressão do ciclo
            print("C", custo_ciclo, len(ciclo_ordenado) - 1, *ciclo_ordenado)
            break
    
    return ciclo_neg

# função para imprimir os caminhos mínimos a partir de s
def imprimir_caminhos(n, dist, ant):
    for t in range(n):
        # verifica se existe algum vértice inalcançável
        if dist[t] == float('inf'):
            print("U", t)
            continue
        
        caminho = []
        atual = t

        # reconstrói o caminho de t até s utilizando os predecessores
        while atual is not None:
            caminho.append(atual)
            atual = ant[atual]

        # impressão dos caminhos
        print("P", t, dist[t], len(caminho), *reversed(caminho))
            
def pccm(g, s):
    # inicializando os vetores Distância e Anterior
    n = g['num_vert']
    dist = [float('inf')] * n   # Distância[]
    ant = [None] * n            # Anterior[]
    dist[s] = 0

    # chamando a função para criar OI e OP
    OI, OP = ordem_O(s, n)

    # impressão de OI/OP
    print("O I", *OI)
    print("O P", *OP)

    # laço principal do código que executa n-1 vezes
    for rodada in range(1, n):
        atualizacao = False     # inicializando variável que vai verificar se houve atualização
        
        # alterna entre as ordens OI e OP com base na rodada atual
        if rodada % 2 == 0:
            O = OP
        else:
            O = OI

        # para cada vértice de origem u na ordem O
        for u in O:
            # se u tem vizinhos, ou seja, se u está em g['adj']
            if u in g['adj']:
                # para cada vizinho v de u com custo da aresta
                for v, custo in g['adj'][u]:
                    # se puder relaxar a aresta, realiza a troca dos valores e assume que houve atualização
                    if dist[u] + custo < dist[v]:
                        dist[v] = dist[u] + custo
                        ant[v] = u
                        atualizacao = True
        # se não houver atualização, o laço principal para
        if not atualizacao:
            break
    
    # impressão da rodada, distâncias e anteriores
    print("F", rodada) # última rodada completa
    print("D", *[v if v != float('inf') else "-" for v in dist])
    print("A", *[v if v is not None else "-" for v in ant])

    # verificação de ciclo negativo
    ciclo_neg = ciclo_negativo(n, g, ant, dist)
    # se não houver ciclo negativo, imprime os caminhos mínimos
    if not ciclo_neg:
        imprimir_caminhos(n, dist, ant)

# execução principal
try:
    # erro de argumentos
    if len(sys.argv) < 2:
        print('E')
        sys.exit()

    arquivo = sys.argv[1]
    s = int(sys.argv[2])    # vértice de origem s

    # armazena o grafo
    leitura_arquivo(arquivo)

    # erro de vértice s inválido
    if s not in grafo['vertice'] or s < 0:
        print('E')
        sys.exit()

    # execução do algoritmo
    pccm(grafo, s)
except Exception:
    print('E')
    sys.exit()