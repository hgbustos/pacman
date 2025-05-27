import pygame

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
        self.color = (0, 255, 255)  # Cian

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