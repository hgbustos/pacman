import pygame
from entity import Entity
from constants import *
from sprites import FruitSprites

""" Clase que representa una fruta en el juego Pacman.
    Atributos:
        name (str): Nombre de la entidad.
        color (tuple): Color de la fruta (verde).
        lifespan (int): Tiempo de vida de la fruta en segundos.
        timer (float): Temporizador para controlar el tiempo de vida.
        destroy (bool): Indica si la fruta debe ser destruida.
        points (int): Puntos otorgados al recoger la fruta.
        sprites (FruitSprites): Sprites de animación de la fruta.
    """
class Fruit(Entity):
    """ metodo constructor de la clase Fruit.
        Inicializa los atributos de la fruta, incluyendo el nombre, color, tiempo de vida,
        temporizador, puntos y sprites de animación.
        
        Args:
            node (Node): Nodo en el que se encuentra la fruta.
            level (int): Nivel del juego para calcular los puntos.
    """
    def __init__(self, node, level=0):
        Entity.__init__(self, node)
        self.name = FRUIT
        self.color = GREEN
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.points = 100 + level*20
        self.setBetweenNodes(RIGHT)
        self.sprites = FruitSprites(self, level)
    """ metodo update de la clase Fruit.
        Actualiza el temporizador de la fruta y verifica si ha alcanzado su tiempo de vida.
        Si es así, marca la fruta para ser destruida.
        
        Args:
            dt (float): Delta time para el temporizador.
    """
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True