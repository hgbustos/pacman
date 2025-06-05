import pygame
from ghosts import GhostGroup 
from ghosts import Ghost
from constants import *

class PowerUp:
    def __init__(self, x, y, duration=5):
        self.x = x
        self.y = y
        self.duration = duration
        self.active = False
        self.radius = 10  # Radio para dibujar el power-up (puedes cambiarlo)
        self.color = (255, 255, 0)  # Amarillo
        self.position = pygame.math.Vector2(x, y)
        self.collideRadius = self.radius
    
    def activate(self, pacman):
        pass # Método a ser implementado en las subclases
    
    def deactivate(self, pacman):
        pass # Método a ser implementado en las subclases

    def update(self, pacman, dt):
        # Temporizador para el power-up
        if self.active:
            self.duration -= dt
            if self.duration <= 0:
                self.deactivate(pacman)

    def is_active(self):
        return self.active

    def render(self, screen):
        # Dibuja el power-up solo si no está activo (es decir, aún no lo ha recogido Pacman)
        if not self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)



class SpeedBoostPowerUp(PowerUp):
    def __init__(self, x, y, duration=5):
        super().__init__(x, y, duration)
        self.color = (255, 0, 255)  # Magenta para distinguirlo

    def activate(self, pacman):
        self.active = True
        pacman.speed *= 2  # Duplica la velocidad de Pacman

    def deactivate(self, pacman):
        self.active = False
        pacman.speed /= 2  # Vuelve a la velocidad normal

    # update no es necesario hacer override porque no tiene lógica especial



""" PowerUp que otorga a Pacman la capacidad de disparar un láser """
class LaserPowerUp(PowerUp):
    def __init__(self, x, y, duration=5):
        super().__init__(x, y, duration)
        self.color = CYAN  # Cian

    def activate(self, pacman):
        self.active = True
        pacman.has_laser = True

    def deactivate(self, pacman):
        self.active = False
        pacman.has_laser = False

    def update(self, pacman, dt):
        if self.active:
            self.duration -= dt
            if self.duration <= 0:
                self.deactivate(pacman)
  
# update() no es necesario hacer override porque no tiene lógica especial 

    def render(self, screen):
        super().render(screen)
        # dibujo del láser solo si está activo:
        """if self.active: 
            laserVertical = pygame.Rect(int(self.x - LASERWIDTH//2), 0, LASERWIDTH, SCREENHEIGHT)
            pygame.draw.rect(screen, self.color, laserVertical)"""

"""class FrontBeamPowerUp(PowerUp):
    def __init__(self, x, y, duration=5):
        super().__init__(x, y, duration)
        self.color = (0, 0, 255)  # Azul para distinguirlo

    def activate(self, pacman):
        self.active = True
        pacman.has_front_beam = True

    def deactivate(self, pacman):
        self.active = False
        pacman.has_front_beam = False

    # update no es necesario hacer override porque no tiene lógica especial"""
#arma
class GunPowerUp(PowerUp):
    def __init__(self, x, y, duration=5):
        super().__init__(x, y, duration)
        self.color = (255, 0, 0)  # Rojo para distinguirlo

    def activate(self, pacman):
        self.active = True
        pacman.has_gun = True
        pacman.bullets = []  # Lista para almacenar balas

    def deactivate(self, pacman):
        self.active = False
        pacman.has_gun = False
        pacman.bullets = []

    def update(self, pacman, dt):
        if self.active:
            self.duration -= dt
            if self.duration <= 0:
                self.deactivate(pacman)
#balas
class Bullet:
    def __init__(self, x, y, direction, speed=400):
        self.position = pygame.math.Vector2(x, y)
        self.direction = pygame.math.Vector2(direction).normalize()
        self.speed = speed
        self.radius = 4
        self.color = (255, 255, 255)

    def update(self, dt):
        self.position += self.direction * self.speed * dt

    def render(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)



