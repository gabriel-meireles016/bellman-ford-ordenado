# python .\pccm.py .\grafo.txt s

import sys

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

def pccm(g, s):
    # Inicializando os vetores Anterior e Distância
    n = grafo['num_vert']
    dist = [float('inf')] * n
    ant = [None] * n
    dist[s] = 0

    OI = list(range(n)) # Ordem Crescente
    OP = reversed(OI)   # Ordem Decrescente
    OP_2 = list(reversed(OI))

    print("O I", OI)
    print("O P", OP_2)

    for rodada in range(1, n - 1):
        atualizacao = False
        if rodada % 2 == 0:
            O = OP
        else:
            O = OI

        #print('R',rodada)
        for u in O:
            for arco in grafo['arco']:
                if arco['origem'] == u:
                    v = arco['destino']
                    custo = arco['custo']
                    if dist[u] + custo < dist[v]:
                        #print(u, v)
                        dist[v] = dist[u] + custo
                        ant[v] = u
                        atualizacao = True
        if atualizacao == False:
            break
        #print()
    
    print("F", rodada) # última rodada completa
    print("D", *dist)
    print("D", *ant)

    # Verificação de ciclo negativo
    ciclo_neg = False
    # Última rodada para ver se há ciclo negativo
    for arco in grafo['arco']:
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
                for arco in grafo['arco']:
                    if arco['origem'] == u and arco['destino'] == v:
                        custo_ciclo += arco['custo']
                        break
            
            print("C", custo_ciclo, len(ciclo_ordenado) - 1, *ciclo_ordenado)
            break
    
    if not ciclo_neg:
        for t in range(n):
            if dist[t] != float('inf'):
                caminho = []
                atual = t

                while atual is not None:
                    caminho.append(atual)
                    atual = ant[atual]
                caminho.reverse()

                custo = dist[t]
                comprimento = len(caminho) - 1
                print("P", t, custo, comprimento, *caminho)
            else:
                print("U", t)

grafo = {
    'num_vert': 0,
    'num_arc': 0,
    'vertice': {},
    'arco': []
}

try:
    if len(sys.argv) < 2:
        print('E')
        sys.exit()

    arquivo = sys.argv[1]
    s = int(sys.argv[2])

    leitura_arquivo(arquivo)

    if s not in grafo['vertice'] or s < 0: # or s >= grafo['num_vert']:
        print('E')
        sys.exit()

    pccm(grafo, s)
except Exception:
    print('E')
    sys.exit()