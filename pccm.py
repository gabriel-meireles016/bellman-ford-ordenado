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


grafo = {
    'num_vert': 0,
    'num_arc': 0,
    'vertice': {},
    'arco': []
}

if len(sys.argv) < 2:
    print('Argumentos insuficientes')
    sys.exit()

arquivo = sys.argv[1]
s = sys.argv[2]

leitura_arquivo(arquivo)


'''print("Número de vértices:", grafo['num_vert'])
print("Número de arcos:", grafo['num_arc'])
print("Vértices:", grafo['vertice'])
print("Arcos:", grafo['arco'])'''