import math
import random
from physics import Rocket

class LandingPad:
    def __init__(self, x, y, width=122, height=33):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

def distance(x1, y1, x2, y2):
    """
    Calcula a distância euclidiana entre dois pontos.
    """
    return (x2 - x1) ** 2 + (y2 - y1) ** 2