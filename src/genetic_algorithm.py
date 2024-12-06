import random
from ai_agent import AIAgent

def mutate(dna, mutation_rate, diversity_rate=0.1):
    new_dna = []
    for gene in dna:
        if random.random() < mutation_rate:
            # Pequena mutação (muda ligeiramente o gene atual)
            new_dna.append(random.choice(['LEFT', 'RIGHT', 'UP']))
        elif random.random() < diversity_rate:
            # Grande mutação (gera um gene totalmente aleatório)
            new_dna.append(random.choice(['LEFT', 'RIGHT', 'UP']))
        else:
            # Mantém o gene original
            new_dna.append(gene)
    return new_dna



def create_next_generation(agents, population_size):
    agents.sort(key=lambda agent: agent.fitness, reverse=True)
    survivors = agents[:population_size // 2]

    next_generation = [agents[0]]  # Elitismo
    while len(next_generation) < population_size:
        parent = random.choice(survivors)
        child = AIAgent()
        child.dna = mutate(parent.dna)
        next_generation.append(child)

    return next_generation

def select_best_agent(agents):
    # Ordena agentes apenas pelo fitness em ordem decrescente
    agents_sorted = sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    
    # Verifica se o primeiro e o segundo lugar estão empatados no fitness
    if len(agents_sorted) > 1 and agents_sorted[0].fitness == agents_sorted[1].fitness:
        # Desempata apenas entre o primeiro e o segundo lugar usando tiebreaker
        if (agents_sorted[0].tiebreaker, agents_sorted[0].time_alive) < (agents_sorted[1].tiebreaker, agents_sorted[1].time_alive):
            agents_sorted[0], agents_sorted[1] = agents_sorted[1], agents_sorted[0]
    
    best_agent = agents_sorted[0]
    print(f"Melhor agente selecionado: Fitness={best_agent.fitness:.4f}, Combustível={best_agent.tiebreaker}, Tempo vivo={best_agent.time_alive}")
    return best_agent



def create_variations(best_agent, population_size, mutation_rate=0.35):
    """
    Gera uma nova geração de agentes com base no melhor agente.
    """
    next_generation = []
    for _ in range(population_size):
        new_agent = AIAgent()
        new_agent.dna = mutate(best_agent.dna, mutation_rate)
        next_generation.append(new_agent)
    return next_generation