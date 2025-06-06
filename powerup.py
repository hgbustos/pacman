import pygame
from constants import *
#GABI
from entity import *

class PowerUp:
    def __init__(self, x, y, duration=5):
        self.x = x
        self.y = y
        self.duration = duration
        self.active = False
        self.radius = 10  # Radio para dibujar el power-up (puedes cambiarlo)
        self.color = YELLOW # Amarillo
        self.position = pygame.math.Vector2(x, y)
        self.collideRadius = self.radius
        self.name = DEFAULT
    
    #TODO un refactoring aca seguro
    def activate(self, pacman):
        self.active = True
        pacman.speed *= 3  # Duplica la velocidad de Pacman
    def deactivate(self, pacman):
        self.active = False
        pacman.speed /= 3  # Vuelve a la velocidad normal

    def update(self, pacman, dt):
        # Aquí puedes manejar el temporizador de duración si lo deseas
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
        self.name = LASER

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
        #GABI
        self.duration = 60
        self.name = GUN

    def activate(self, pacman):
        self.active = True

    def deactivate(self, pacman):
        self.active = False

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

class Bullet2(Entity):
    def __init__(self, pacman):
        Entity.__init__(self, pacman.node)
        self.direction = pacman.direction
        self.position = pacman.position
        self.target = pacman.target
        self.radius = 4
        self.color = PINK
        self.setSpeed(BULLET_SPEED)
        self.stuck = False
        self.name = BULLET
    
    def update(self, dt):
        #self.position += self.direction*self.speed*dt
        self.position += self.directions[self.direction]*self.speed*dt
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None: #balas siempre portal enabled
                self.node = self.node.neighbors[PORTAL]

            self.target = self.getNewTarget(self.direction)
            if self.target is not self.node:
                self.direction = self.direction
            else:
                self.visible = False
                #self.direction = self.getNewTarget(self.direction)
            self.setPosition()

    def getNewTarget(self, direction):
        if self.validDirection(self.direction):
            return self.node.neighbors[self.direction]
        else:
            return self.node

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)




