import random
from physics import Rocket
from utils import distance

class AIAgent:
    def __init__(self, dna_length=100):
        self.dna = [random.choice(['LEFT', 'RIGHT', 'UP']) for _ in range(dna_length)]
        self.current_step = 0
        self.fitness = 0
        self.tiebreaker = 0  # Para armazenar o valor de desempate
        self.success_count = 0  # Atributo para contar os pousos bem-sucedidos
        self.time_alive = 0  # Inicializa o contador de tempo de vida
        self.rocket = Rocket()
        self.finished = False
        self.screen_width = 800
        self.screen_height = 600

    def calculate_fitness(self, landing_pad):
        if self.rocket.check_collision(landing_pad):
            self.fitness = 10000 - abs(self.rocket.velocity_x) - abs(self.rocket.velocity_y)
        elif self.rocket.is_out_of_bounds(self.screen_width, self.screen_height):
            # Penalize mais fortemente se o foguete saiu do limite superior
            if self.rocket.y > self.screen_height - 10:
                self.fitness = -10000  # Penalização alta para sair por cima
            else:
                self.fitness = -5000  # Penalização padrão para outros limites
        distance_to_pad = distance(self.rocket.x, self.rocket.y, landing_pad.x + landing_pad.width // 2, landing_pad.y)
        self.fitness = max(0, 500 - distance_to_pad // 10)

        # Ajusta o tiebreaker
        self.tiebreaker = self.rocket.fuel
        self.fitness += self.time_alive

    def decide_action(self, rocket):
        """
        Decide a próxima ação com base no DNA.
        """
        if self.current_step < len(self.dna):
            action = self.dna[self.current_step]
            self.current_step += 1
            return action
        return 'NONE'


    def reset(self):
        """
        Reseta o agente para um novo início.
        """
        self.current_step = 0
        self.finished = False
        self.fitness = 0
        self.rocket = Rocket(x=700, y=300)

    def success(self):
        """
        Incrementa o contador de sucesso quando o agente pousa com sucesso.
        """
        self.success_count += 1
        self.finished = True  # Marca o agente como terminado

    def has_finished(self):
        """
        Retorna se o agente terminou de jogar.
        """
        return self.finished

    
    def reset_rocket(self, initial_x, initial_y):
        """
        Reinicia o foguete na posição inicial e reseta sua velocidade.
        """
        self.rocket.x = initial_x
        self.rocket.y = initial_y
        self.rocket.vx = 0
        self.rocket.vy = 0
