import pygame
from entity import Entity
from constants import *
from sprites import FruitSprites
"""
Representa una fruta en el juego, que otorga puntos al jugador al ser recogida.
Atributos:
    name (str): Nombre de la entidad (FRUIT).
    color (tuple): Color de la fruta (verde).
    lifespan (int): Tiempo de vida de la fruta en segundos.
    timer (float): Temporizador para controlar el tiempo de vida.
    destroy (bool): Indica si la fruta debe ser destruida.
    points (int): Puntos otorgados al recoger la fruta.
    sprites (FruitSprites): Sprites de animación de la fruta.
"""
class Fruit(Entity):
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

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True