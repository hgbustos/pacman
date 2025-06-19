import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint

class Entity(object):
    """
    Representa una entidad en el juego, como un fantasma o un objeto.
    Atributos:
        name (str): Nombre de la entidad.
        directions (dict): Diccionario que mapea direcciones a vectores.
        direction (int): Dirección actual de la entidad.
        speed (float): Velocidad de movimiento de la entidad.
        radius (int): Radio de colisión de la entidad.
        collideRadius (int): Radio de colisión efectivo.
        color (tuple): Color de la entidad.
        visible (bool): Indica si la entidad es visible o no.
        disablePortal (bool): Indica si el portal está deshabilitado.
        goal (Vector2): Objetivo al que se dirige la entidad.
        directionMethod (function): Método para determinar la dirección a seguir.
        node (Node): Nodo actual en el que se encuentra la entidad.
        startNode (Node): Nodo inicial de la entidad.
        target (Node): Nodo objetivo al que se dirige la entidad.
        image (Surface): Imagen de la entidad.
    """
    def __init__(self, node):
        self.name = None
        self.directions = {UP:Vector2(0, -1),DOWN:Vector2(0, 1), 
                          LEFT:Vector2(-1, 0), RIGHT:Vector2(1, 0), STOP:Vector2()}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartNode(node)
        self.image = None
        

        
    """    Establece la posición de la entidad en el nodo actual.
        La posición se establece como una copia de la posición del nodo."""
    def setPosition(self):
        self.position = self.node.position.copy()
        
    """    Actualiza la posición de la entidad en función de su dirección y velocidad.
        Si la entidad ha superado su objetivo, se actualiza el nodo actual y se determina"""
    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt
         
        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()
          
    """    Establece la dirección de la entidad en función de la tecla presionada.
        Si la tecla presionada corresponde a una dirección válida, se actualiza la dirección."""
    def validDirection(self, direction):
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    """    Devuelve la dirección válida presionada por el usuario.
        Si la tecla presionada corresponde a una dirección válida, se devuelve esa dirección."""
    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    """    Comprueba si la entidad ha superado su objetivo.
        Compara la distancia entre la posición de la entidad y el nodo objetivo.
        Si la distancia es mayor o igual a la distancia entre el nodo actual y el objetivo, se considera que ha superado el objetivo.
        Devuelve True si ha superado el objetivo, False en caso contrario."""
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False
    
    """    Devuelve la dirección opuesta a la dirección actual de la entidad.
        Si la dirección es diferente de STOP, se devuelve la dirección opuesta."""
    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp
        
    """    Comprueba si la dirección es opuesta a la dirección actual de la entidad.
        Si la dirección es diferente de STOP y es igual a la dirección opuesta, devuelve True."""
    def oppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    """    Devuelve la dirección válida más cercana al objetivo.
        Calcula la distancia entre la posición de la entidad y el objetivo para cada dirección válida."""
    def validDirections(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    """    Devuelve una dirección aleatoria de las direcciones válidas.
        Selecciona una dirección aleatoria de la lista de direcciones válidas."""
    def randomDirection(self, directions):
        return directions[randint(0, len(directions)-1)]

   
    """    Devuelve la dirección más cercana al objetivo.
        Calcula la distancia entre la posición de la entidad y el objetivo para cada dirección válida."""
    def goalDirection(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position  + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]


    """    Establece el nodo inicial de la entidad.
        Se establece el nodo actual y el nodo objetivo como el nodo inicial.
        También se establece la posición de la entidad en el nodo inicial."""
    def setStartNode(self, node):
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()

    """    Establece la velocidad de la entidad.
        La velocidad se multiplica por el ancho de la entidad dividido por 16."""
    def setBetweenNodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    """    Comprueba si la entidad es visible.
        Si la entidad es visible, se establece su imagen como la imagen de inicio.
        Si no es visible, se establece la imagen como None.
        También se establece la dirección y la velocidad de la entidad."""
    def reset(self):
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True

    """    Establece la velocidad de la entidad.
        La velocidad se multiplica por el ancho de la entidad dividido por 16."""
    def setSpeed(self, speed):
        self.speed = speed * TILEWIDTH / 16

    """    Establece la imagen de la entidad.
        Si la imagen es None, se establece el color de la entidad.
        Si la imagen no es None, se establece la imagen de la entidad.
        También se establece la posición de la entidad."""
    def render(self, screen):
        if self.visible:
            if self.image is not None:
                adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
                p = self.position - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)
