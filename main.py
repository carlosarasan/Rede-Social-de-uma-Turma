import networkx as nx
import matplotlib.pyplot as plt


# 1. MODELAGEM DO GRAFO (Dicionário de Adjacência)

# Vértices: 12 Alunos
# Arestas: Afinidade por áreas de estudo (Ex: Web, Redes, Dados)
# Grafo não direcionado (se A está ligado a B, B está ligado a A).


grafo_turma = {
    "Carlos": ["Ana", "Pedro", "Bia", "Joao"], # Carlos conecta Web e Redes
    "Ana": ["Carlos", "Pedro", "Bia"],
    "Pedro": ["Carlos", "Ana", "Bia"],
    "Bia": ["Carlos", "Ana", "Pedro"],
    "Joao": ["Carlos", "Lucas", "Marcos", "Maria"], # Joao conecta Redes com Web e Dados
    "Lucas": ["Joao", "Marcos"],
    "Marcos": ["Joao", "Lucas"],
    "Maria": ["Joao", "Julia", "Sofia"], # Maria conecta Dados com Redes
    "Julia": ["Maria", "Sofia", "Tiago", "Vitor"],
    "Sofia": ["Maria", "Julia", "Tiago", "Vitor"],
    "Tiago": ["Julia", "Sofia", "Vitor"],
    "Vitor": ["Julia", "Sofia", "Tiago"]
}


# 2. FUNÇÕES DE CÁLCULO E ANÁLISE 

def exibir_dados_grafo(grafo):
    print("\n--- DADOS DA REDE SOCIAL DA TURMA ---")
    for aluno, conexoes in grafo.items():
        print(f"Aluno: {aluno} | Conectado a: {', '.join(conexoes)}")

def analisar_graus(grafo):
    graus = {}
    total_arestas_duplas = 0
    
    for aluno, conexoes in grafo.items():
        grau = len(conexoes)
        graus[aluno] = grau
        total_arestas_duplas += grau
        
    num_vertices = len(grafo)
    total_arestas = total_arestas_duplas // 2 # Divide por 2 porque é não direcionado
    grau_medio = total_arestas_duplas / num_vertices
    
    aluno_maior_grau = max(graus, key=graus.get)
    aluno_menor_grau = min(graus, key=graus.get)
    
    print("\n--- ANÁLISE DE GRAUS ---")
    print(f"Total de Vértices (Alunos): {num_vertices}")
    print(f"Total de Arestas (Relações): {total_arestas}")
    for aluno, grau in graus.items():
        print(f"O grau de {aluno} é {grau}.")
    print(f"\nGrau Médio da Rede: {grau_medio:.2f}")
    print(f"Pessoa com MAIOR número de conexões: {aluno_maior_grau} (Grau {graus[aluno_maior_grau]})")
    print(f"Pessoa com MENOR número de conexões: {aluno_menor_grau} (Grau {graus[aluno_menor_grau]})")
    
    return num_vertices, total_arestas

def calcular_densidade(num_vertices, total_arestas):
    # Fórmula da densidade para grafos não direcionados: 2E / (V * (V - 1))
    densidade = (2 * total_arestas) / (num_vertices * (num_vertices - 1))
    print("\n--- DENSIDADE DA REDE ---")
    print(f"A densidade da rede é: {densidade:.2f} (ou {densidade * 100:.1f}%)")

def busca_em_profundidade(grafo, inicio, visitados):
    # Algoritmo DFS simples para visitar os vizinhos
    visitados.add(inicio)
    for vizinho in grafo[inicio]:
        if vizinho not in visitados:
            busca_em_profundidade(grafo, vizinho, visitados)

def contar_componentes(grafo):
    visitados = set()
    componentes = 0
    for aluno in grafo:
        if aluno not in visitados:
            busca_em_profundidade(grafo, aluno, visitados)
            componentes += 1
    return componentes

def analisar_conexidade(grafo):
    qtd_componentes = contar_componentes(grafo)
    print("\n--- CONEXIDADE ---")
    if qtd_componentes == 1:
        print("O grafo é CONEXO (Todos os alunos estão interligados de alguma forma).")
    else:
        print("O grafo é DESCONEXO.")
    print(f"Quantidade de Componentes Conexos: {qtd_componentes}")
    return qtd_componentes

def encontrar_vertices_de_corte(grafo, componentes_originais):
    vertices_corte = []
    for aluno in grafo:
        # Cria um grafo temporário sem o aluno
        grafo_temp = {k: v[:] for k, v in grafo.items() if k != aluno}
        for k in grafo_temp:
            if aluno in grafo_temp[k]:
                grafo_temp[k].remove(aluno)
                
        # Conta componentes novamente
        if contar_componentes(grafo_temp) > componentes_originais:
            vertices_corte.append(aluno)
            
    print("\n--- VÉRTICES DE CORTE ---")
    if vertices_corte:
        print(f"Pessoas que, se removidas, desconectam a rede: {', '.join(vertices_corte)}")
        print("-> Estes são os pontos vitais de conexão entre os grupos de estudo!")
    else:
        print("Não existem vértices de corte nesta rede.")

def encontrar_arestas_de_corte(grafo, componentes_originais):
    arestas_corte = []
    arestas_verificadas = set()
    
    for aluno, vizinhos in grafo.items():
        for vizinho in vizinhos:
            aresta = frozenset([aluno, vizinho])
            if aresta not in arestas_verificadas:
                arestas_verificadas.add(aresta)
                
                # Remove a aresta temporariamente
                grafo_temp = {k: v[:] for k, v in grafo.items()}
                grafo_temp[aluno].remove(vizinho)
                grafo_temp[vizinho].remove(aluno)
                
                # Verifica se quebrou a rede
                if contar_componentes(grafo_temp) > componentes_originais:
                    arestas_corte.append(f"{aluno} <-> {vizinho}")
                    
    print("\n--- ARESTAS DE CORTE ---")
    if arestas_corte:
        print("Relações que, se desfeitas, desconectam a rede:")
        for a in arestas_corte:
            print(f" - {a}")
    else:
        print("Não existem arestas de corte nesta rede.")

def encontrar_caminho(grafo, origem, destino, caminho_atual=None):
    if caminho_atual is None:
        caminho_atual = []
        
    caminho_atual = caminho_atual + [origem]
    
    if origem == destino:
        return [caminho_atual]
        
    if origem not in grafo:
        return []
        
    caminhos = []
    for vizinho in grafo[origem]:
        if vizinho not in caminho_atual: # Evita ciclos
            novos_caminhos = encontrar_caminho(grafo, vizinho, destino, caminho_atual)
            for novo in novos_caminhos:
                caminhos.append(novo)
    return caminhos


# 3. INTERAÇÃO E VISUALIZAÇÃO


def gerar_visualizacao(grafo):
    print("\n[!] Gerando visualização gráfica do grafo...")
    G = nx.Graph(grafo)
    
    plt.figure(figsize=(10, 7))
    plt.title("Rede Social da Turma - Afinidade por Áreas de Estudo")
    
    # Layout que espalha bem os nós
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=2500, font_size=10, font_weight='bold', 
            edge_color='gray', width=2)
            
    plt.show()

def executar_programa():
    # 1. Apresentar dados
    exibir_dados_grafo(grafo_turma)
    
    # 2. Cálculos obrigatórios
    v, e = analisar_graus(grafo_turma)
    calcular_densidade(v, e)
    
    comp_originais = analisar_conexidade(grafo_turma)
    encontrar_vertices_de_corte(grafo_turma, comp_originais)
    encontrar_arestas_de_corte(grafo_turma, comp_originais)
    
    # 3. Interação com o Usuário
    print("\n--- CONSULTA DE CAMINHOS ---")
    print("Digite o nome de dois alunos para ver como eles estão conectados.")
    print("Opções:", ", ".join(grafo_turma.keys()))
    
    origem = input("Digite o nome do Aluno Origem: ").strip()
    destino = input("Digite o nome do Aluno Destino: ").strip()
    
    if origem in grafo_turma and destino in grafo_turma:
        caminhos = encontrar_caminho(grafo_turma, origem, destino)
        if caminhos:
            print(f"\nForam encontrados {len(caminhos)} caminho(s) entre {origem} e {destino}.")
            print("Caminho mais curto:", caminhos[0])
        else:
            print(f"\nNão há caminho possível entre {origem} e {destino}.")
    else:
        print("\nNome(s) inválido(s). Verifique a ortografia.")
        
    # 4. Gerar Gráfico
    gerar_visualizacao(grafo_turma)

# Inicia a execução do programa
if __name__ == "__main__":
    executar_programa()