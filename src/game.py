import os
import pygame
from ai_agent import AIAgent
from genetic_algorithm import select_best_agent, create_variations
from utils import LandingPad

def initialize_screen():
    """Inicializa a tela do jogo e retorna os objetos principais."""
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Rocket Landing Game - Múltiplos Agentes")
    clock = pygame.time.Clock()
    return screen, clock, screen_width, screen_height

def load_assets(screen_width, screen_height):
    """Carrega e redimensiona os recursos gráficos."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")

    # Carregando imagens
    background = pygame.image.load(os.path.join(ASSETS_DIR, "background.png"))
    rocket = pygame.image.load(os.path.join(ASSETS_DIR, "rocket.png"))
    landing_pad = pygame.image.load(os.path.join(ASSETS_DIR, "landing_pad.png"))
    explosion = pygame.image.load(os.path.join(ASSETS_DIR, "explosion.png"))

    # Redimensiona imagens
    background = pygame.transform.scale(background, (screen_width, screen_height))
    return background, rocket, landing_pad, explosion

def reset_agents(agents):
    """Reinicia os foguetes dos agentes no topo da tela."""
    for agent in agents:
        agent.reset_rocket(700, 300)


def update_agents(agents, screen, rocket_img, explosion_img, landing_pad, screen_width, screen_height):
    active_agents = 0

    for agent in agents:
        if not agent.has_finished():

            agent.time_alive += 1  # Incrementa o tempo de vida do agente
            # Ação do agente
            action = agent.decide_action(agent.rocket)
            apply_action(agent, action)

            # Atualizar física e posição
            agent.rocket.apply_gravity()
            agent.rocket.update_position()

            # Verificar condições de finalização
            if check_conditions(agent, landing_pad, screen_width, screen_height, explosion_img, screen):
                continue

            active_agents += 1
            render_agent(agent, screen, rocket_img, explosion_img, screen_height)

    return active_agents

def apply_action(agent, action):
    """Aplica a ação ao foguete do agente."""
    thrust_mapping = {
        "LEFT": (-0.6, 0),
        "RIGHT": (0.6, 0),
        "UP": (0, 0.4),     
    }
    if action in thrust_mapping:
        thrust_x, thrust_y = thrust_mapping[action]
        agent.rocket.apply_thrust(thrust_x, thrust_y)

def check_conditions(agent, landing_pad, screen_width, screen_height, explosion_img, screen):
    rocket = agent.rocket

    if rocket.x < 0 or rocket.x > screen_width or rocket.y < 0 or rocket.y > screen_height:
        agent.finished = True
        agent.calculate_fitness(landing_pad)
        print(f"Agente {agent} finalizado: Saiu dos limites. Fitness: {agent.fitness}")
        screen.blit(explosion_img, (agent.rocket.x, agent.rocket.y))
        return True

    if rocket.check_collision(landing_pad):
        agent.success()
        agent.calculate_fitness(landing_pad)
        print(f"Agente {agent} pousou com sucesso. Fitness: {agent.fitness}")
        return True

    if rocket.fuel <= 0:
        agent.finished = True
        agent.calculate_fitness(landing_pad)
        print(f"Agente {agent} finalizado: Sem combustível. Fitness: {agent.fitness}")
        return True
    return False

def render_agent(agent, screen, rocket_img, explosion_img, screen_height):
    """Renderiza o agente na tela."""
    if agent.has_finished():
        if agent.rocket.y >= screen_height or agent.rocket.y < 0:
            screen.blit(explosion_img, (agent.rocket.x, agent.rocket.y))
        else:
            screen.blit(rocket_img, (agent.rocket.x, agent.rocket.y))
    else:
        screen.blit(rocket_img, (agent.rocket.x, agent.rocket.y))

def main(number_of_agents=30, generations=100):
    """Função principal do jogo."""
    pygame.init()

    # Inicializações
    screen, clock, screen_width, screen_height = initialize_screen()
    background, rocket_img, landing_pad_img, explosion_img = load_assets(screen_width, screen_height)
    rocket_width, rocket_height = rocket_img.get_width(), rocket_img.get_height()
    landing_pad_width, landing_pad_height = landing_pad_img.get_width(), landing_pad_img.get_height()

    landing_pad = LandingPad(
        x=100,
        y=300,
        width=landing_pad_width,
        height=landing_pad_height,
    )

    # Inicializa a população
    agents = [AIAgent() for _ in range(number_of_agents)]

    for generation in range(generations):
        print(f"--- Geração {generation + 1} ---")

        # Reseta os foguetes para o início
        reset_agents(agents)

        # Executa a simulação para todos os agentes
        active_agents = number_of_agents
        while active_agents > 0:
            screen.blit(background, (0, 0))
            screen.blit(landing_pad_img, (landing_pad.x, landing_pad.y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            active_agents = update_agents(
                agents, screen, rocket_img, explosion_img, landing_pad, screen_width, screen_height
            )

            pygame.display.flip()
            clock.tick(60)

        # Calcula o fitness de cada agente
        for agent in agents:
            agent.calculate_fitness(landing_pad)

        # Seleciona o melhor agente
        best_agent = select_best_agent(agents)
        print(f"Melhor agente:{agent} da geração {generation + 1}: Fitness {best_agent.fitness:.4f}")
        print("Melhor agente encontrado:")
        print(f"Fitness: {best_agent.fitness}")
        print(f"Combustível restante: {best_agent.rocket.fuel}")
        print(f"Tempo vivo: {best_agent.time_alive}")

        # Gera a próxima geração de agentes
        agents = create_variations(best_agent, number_of_agents)

        pygame.display.flip()
        clock.tick(60)



    pygame.quit()

if __name__ == "__main__":
    main()
