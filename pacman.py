
import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites

class Pacman(Entity):
    """
    Representa al personaje Pac-Man en el juego.

    Atributos:
        name (str): Nombre de la entidad.
        color (tuple): Color del personaje (amarillo).
        direction (int): Dirección inicial del movimiento.
        alive (bool): Estado de vida del personaje.
        sprites (PacmanSprites): Sprites de animación de Pac-Man.
    """

    def __init__(self, node):
        Entity.__init__(self, node )
        self.name = PACMAN    
        self.color = YELLOW #
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)
        
        #27/05
        self.has_gun = False
        #mod Joa 
        self.has_laser = False
        self.has_front_beam = False
        #self.bullets = []
    
    """ Inicializa la posición y el radio de colisión del personaje. 
    al igual que la dirección inicial y el estado de vida.
    Args:
        node (Node): Nodo en el que se encuentra el personaje.
    """
    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()


    """ Establece la posición del personaje en el nodo actual. 
        Se asegura de que la posición esté dentro de los límites del nodo.
        
        Args:
            node (Node): Nodo en el que se encuentra el personaje.
        """ 
    def die(self):
        self.alive = False
        self.direction = STOP

    
    """ metodo para actualizar la posición del personaje en función de la dirección y la velocidad.
        Se mueve en la dirección actual y verifica si ha alcanzado el nodo objetivo.
        Si es así, cambia la dirección y establece un nuevo nodo objetivo.
        
        Args:
            dt (float): Delta time para el movimiento.
        """
    def update(self, dt):	
        self.sprites.update(dt)
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()


    """ Cambia la dirección del personaje en función de la tecla presionada.
        Args:
            direction (int): Nueva dirección del movimiento.
        
        Returns:
            int: Nueva dirección del movimiento.
        """
    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP  


    """ metodo para verificar si el personaje ha alcanzado el nodo objetivo.
        Se utiliza para determinar si el personaje ha llegado a su destino.
        
        Returns:
            bool: True si ha alcanzado el nodo objetivo, False en caso contrario.
        """
    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None    
    

    
    """ metodo colision para verificar si el personaje ha colisionado con un fantasma.
        Se utiliza para determinar si el personaje ha chocado con un fantasma.
        
        Args:
            ghost (Ghost): Fantasma con el que se verifica la colisión.
        
        Returns:
            bool: True si ha colisionado, False en caso contrario.
        """
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)


    """ metodo colision para verificar si el personaje ha colisionado con un pellet.
        Se utiliza para determinar si el personaje ha chocado con un pellet.
        
        Args:
            pellet (Pellet): Pellet con el que se verifica la colisión.
        
        Returns:
            bool: True si ha colisionado, False en caso contrario.
        """
    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False
    
    #27/5 dario
    def draw(self, screen):
        # Dibuja el sprite normal
        screen.blit(self.image, (self.position.x - self.image.get_width() // 2, self.position.y - self.image.get_height() // 2))
        # Si tiene arma, dibuja el arma
        if self.has_gun:
            pygame.draw.rect(screen, (150, 150, 150), (self.position.x - 5, self.position.y - 20, 10, 15))
        # Dibuja las balas si existen
        for bullet in self.bullets:
            bullet.draw(screen)
    def render(self, screen):
        # Dibuja el sprite normal (ajusta según tu código)
        screen.blit(self.image, (self.position.x - self.image.get_width() // 2, self.position.y - self.image.get_height() // 2))
        # Dibuja el arma si la tiene
        if self.has_gun:
            pygame.draw.rect(screen, (150, 150, 150), (self.position.x-5, self.position.y-20, 10, 15))
        # Dibuja el laser
        if self.has_laser:
            laserVertical = pygame.Rect(int(self.position.x - LASERWIDTH//2), 0, LASERWIDTH, SCREENHEIGHT)
            pygame.draw.rect(screen, (0, 255, 0), laserVertical)