import pygame
from constants import *

class PowerUp:
    def __init__(self, x, y, duration=5):
        self.x = x
        self.y = y
        self.duration = duration
        self.active = False
        self.radius = 10
        self.color = YELLOW
        self.position = pygame.math.Vector2(x, y)
        self.collideRadius = self.radius
        self._effect_active = False
        self._original_speed = None  # Guarda la velocidad original

    def activate(self, pacman):
        self.active = True
        if not self._effect_active:
            self._original_speed = pacman.speed
            pacman.speed = self._original_speed * 3
            self._effect_active = True
        self.duration = 5  # Reinicia la duración

    def deactivate(self, pacman):
        self.active = False
        if self._effect_active and self._original_speed is not None:
            pacman.speed = self._original_speed
            self._effect_active = False
            self._original_speed = None

    def update(self, pacman, dt):
        if self.active:
            self.duration -= dt
            if self.duration <= 0:
                self.deactivate(pacman)

    #TODO Hacen lo mismo estos
    def draw(self, screen):
        # Dibuja el power-up solo si no está activo (es decir, aún no lo ha recogido Pacman)
        if not self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    def render(self, screen):
         if not self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class LaserPowerUp(PowerUp):
    def __init__(self, x, y, duration=5):
        super().__init__(x, y, duration)
        self.color = CYAN  # Cian

    def activate(self, pacman):
        self.active = True
        # Efecto especial aquí

    def deactivate(self, pacman):
        self.active = False
        # Quitar efecto aquí

    def update(self, pacman, dt):
        # Igual que PowerUp, o tu lógica especial
        if self.active:
            self.duration -= dt
            if self.duration <= 0:
                self.deactivate(pacman)

#arma
class GunPowerUp(PowerUp):
    def __init__(self, x, y, duration=5):
        super().__init__(x, y, duration)
        self.color = RED  # Rojo para distinguirlo

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
        self.color = WHITE

    def update(self, dt):
        self.position += self.direction * self.speed * dt

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)



