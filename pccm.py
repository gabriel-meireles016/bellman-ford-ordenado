import sys
from collections import defaultdict

def leitura_arquivo(arquivo):
    with open(arquivo, 'r') as arq:
        for linha in arq:
            linha = linha.strip()
            if (not linha) or (linha == 'T'):
                break
            
            partes = linha.split()
            tipo = partes[0]

            if tipo == 'I':
                grafo['num_vert'] = int(partes[1])
                grafo['num_arc'] = int(partes[2])
            elif tipo == 'N':
                id_v = int(partes[1])
                g_e = int(partes[2])
                g_s = int(partes[3])
                grafo['vertice'][id_v] = {
                    'grau_entrada': g_e,
                    'grau_saida': g_s
                }
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

def ordem_O(s, n):
    OI = list(range(n)) # Ordem Crescente
    OI.remove(s)
    OI.insert(0, s)

    OP = list(range(n))   # Ordem Decrescente
    OP.remove(s)
    OP = list(reversed(OP))
    OP.insert(0,s)

    return OI, OP

def ciclo_negativo(n, g, ant, dist):
    # Última rodada para ver se há ciclo negativo
    ciclo_neg = False
    for arco in g['arco']:
        u, v, custo = arco['origem'], arco['destino'], arco['custo']
        if dist[u] + custo < dist[v]:
            ciclo_neg = True
            print("CN")
            
            ciclo = []
            visitado = set()
            x = v

            for _ in range(n):
                x = ant[x]

            #ciclo_ini = x
            while x not in visitado:
                visitado.add(x)
                ciclo.append(x)
                x = ant[x]
            ciclo.append(x)
            ciclo.reverse()

            aux = ciclo[:-1]
            menor_id = aux.index(min(aux))
            ciclo_ordenado = aux[menor_id:] + aux[:menor_id]
            ciclo_ordenado.append(ciclo_ordenado[0])

            custo_ciclo = 0
            for i in range(len(ciclo_ordenado) - 1):
                u = ciclo_ordenado[i]
                v = ciclo_ordenado[i + 1]
                for arco in g['arco']:
                    if arco['origem'] == u and arco['destino'] == v:
                        custo_ciclo += arco['custo']
                        break
            
            #print("C", custo_ciclo, len(ciclo_ordenado) - 1, *ciclo_ordenado)
            print("C", len(ciclo_ordenado) - 1, custo_ciclo, *ciclo_ordenado)
            break
    
    return ciclo_neg

def imprimir_caminhos(n, dist, ant):
    for t in range(n):
        if dist[t] == float('inf'):
            print("U", t)
            continue
        
        caminho = []
        atual = t

        while atual is not None:
            caminho.append(atual)
            atual = ant[atual]

        print("P", t, dist[t], len(caminho), *reversed(caminho))
            
def pccm(g, s):
    # Inicializando os vetores Anterior e Distância
    n = g['num_vert']
    dist = [float('inf')] * n
    ant = [None] * n
    dist[s] = 0

    OI, OP = ordem_O(s, n)

    print("O I", *OI)
    print("O P", *OP)

    for rodada in range(1, n):
        atualizacao = False
        if rodada % 2 == 0:
            O = OP
        else:
            O = OI

        for u in O:
            if u in g['adj']:
                for v, custo in g['adj'][u]:
                    if dist[u] + custo < dist[v]:
                        dist[v] = dist[u] + custo
                        ant[v] = u
                        atualizacao = True
        
        if not atualizacao:
            break
    
    print("F", rodada) # última rodada completa
    print("D", *[v if v != float('inf') else "-" for v in dist])
    print("A", *[v if v is not None else "-" for v in ant])

    # Verificação de ciclo negativo
    ciclo_neg = ciclo_negativo(n, g, ant, dist)
    if not ciclo_neg:
        imprimir_caminhos(n, dist, ant)
        
grafo = {
    'num_vert': 0,
    'num_arc': 0,
    'vertice': {},
    'arco': [],
    'adj': defaultdict(list)
}

try:
    if len(sys.argv) < 2:
        print('E')
        sys.exit()

    arquivo = sys.argv[1]
    s = int(sys.argv[2])

    leitura_arquivo(arquivo)

    if s not in grafo['vertice'] or s < 0:
        print('E')
        sys.exit()

    pccm(grafo, s)
except Exception:
    print('E')
    sys.exit()