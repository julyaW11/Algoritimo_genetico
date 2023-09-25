import random

class Individuo:
    def __init__(self, genes):
        self.genes = genes # armazena os genes
        self.fitness = None #Inicializa a aptidão (fitness) do indivíduo como None
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=- 
#Cria a ppopulação inicial. 
def inicializar_populacao(tamanho_populacao, gene_length):
    return [Individuo([random.choice('01') for _ in range(gene_length)]) for _ in range(tamanho_populacao)]
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=- 
def binario_para_decimal(genes):
    gene_str = ''.join(genes)
    max_valor = int('1' * len(genes), 2)
    return -10.0 + (20.0 * int(gene_str, 2) / max_valor)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=- 
def funcao_objetivo(x):
    return x**2 - 3*x + 4
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=- 
#converte a representação binária  indivíduo para um valor decimal para
#calcular a aptidão com base na função objetivo fornecida
def calcular_aptidao(individuo):
    x = binario_para_decimal(individuo.genes)
    individuo.fitness = 1.0 / (1.0 + funcao_objetivo(x))

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=- 
def torneio(populacao, num_participantes=4):
    participantes = random.sample(populacao, num_participantes)
    participantes.sort(key=lambda x: x.fitness if x.fitness is not None else 0, reverse=True)
    return participantes[0]

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--
def crossover(pai, mae, taxa_crossover=0.6):
    if random.random() > taxa_crossover:
        return pai, mae

    ponto_corte = random.randint(0, len(pai.genes) - 1)
    filho1 = Individuo(pai.genes[:ponto_corte] + mae.genes[ponto_corte:])
    filho2 = Individuo(mae.genes[:ponto_corte] + pai.genes[ponto_corte:])
    return filho1, filho2
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--
def mutacao(individuo, taxa_mutacao=0.01):
    genes_mutados = []
    for gene in individuo.genes:
        if random.random() < taxa_mutacao:
            genes_mutados.append('0' if gene == '1' else '1')
        else:
            genes_mutados.append(gene)
    return Individuo(genes_mutados)

def algoritmo_genetico(tamanho_populacao, gene_length, num_geracoes, taxa_crossover, taxa_mutacao):
    populacao = inicializar_populacao(tamanho_populacao, gene_length)

    for geracao in range(num_geracoes):
        for individuo in populacao:
            if individuo.fitness is None:
                calcular_aptidao(individuo)

        melhor_individuo = max(populacao, key=lambda x: x.fitness if x.fitness is not None else 0, default=None)
        if melhor_individuo is not None:
            x_melhor_individuo = binario_para_decimal(melhor_individuo.genes)
            genes_melhor_individuo = ''.join(melhor_individuo.genes) 
            print(f"Geração {geracao + 1}, Melhor Aptidão: {melhor_individuo.fitness}, Valor dos Genes: {genes_melhor_individuo}, Valor de x correspondente: {x_melhor_individuo}")

        nova_geracao = []
        for _ in range(tamanho_populacao // 2):
            pai = torneio(populacao)
            mae = torneio(populacao)
            filho1, filho2 = crossover(pai, mae, taxa_crossover)
            filho1_mutado = mutacao(filho1, taxa_mutacao)
            filho2_mutado = mutacao(filho2, taxa_mutacao)
            nova_geracao.append(filho1_mutado)
            nova_geracao.append(filho2_mutado)

        populacao = nova_geracao

# Parâmetros
tamanho_populacao = 4
gene_length = 10  
num_geracoes = 5
taxa_crossover = 0.6
taxa_mutacao = 0.01

# Executar algoritmo genético
algoritmo_genetico(tamanho_populacao, gene_length, num_geracoes, taxa_crossover, taxa_mutacao)
