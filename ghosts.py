import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController
from sprites import GhostSprites

#from nodes import * #GABI TODO

""" Clase que representa a los fantasmas en el juego
    Atributos:  
        name (str): Nombre del fantasma.
        points (int): Puntos que otorga al ser comido.      
        goal (Vector2): Objetivo al que se dirige el fantasma.
        directionMethod (function): Método para determinar la dirección del movimiento.
        pacman (Pacman): Referencia al objeto Pacman.
        blinky (Blinky): Referencia al objeto Blinky.
        spawnNode (Node): Nodo de aparición del fantasma.
        mode (ModeController): Controlador de modos del fantasma.
        homeNode (Node): Nodo de inicio del fantasma.
        spawnNode (Node): Nodo de aparición del fantasma.
        color (tuple): Color del fantasma.
        sprites (GhostSprites): Sprites de animación del fantasma.
        visible (bool): Indica si el fantasma es visible o no.
        speed (int): Velocidad de movimiento del fantasma.
        direction (int): Dirección actual del fantasma.
        position (Vector2): Posición actual del fantasma.
        betweenNodes (bool): Indica si el fantasma está entre nodos o no.
        image (Surface): Imagen del fantasma.
        rect (Rect): Rectángulo de colisión del fantasma.
        """
class Observer():
    def notify():
        pass

class Ghost(Entity, Observer):

    """ metodo constructor de la clase Ghost
        Args:
            node (Node): Nodo en el que se encuentra el fantasma.
            pacman (Pacman): Referencia al objeto Pacman.
            blinky (Blinky): Referencia al objeto Blinky.
        """
    #TODO GABI
    def __init__(self, node, pacman=None, ghost_subject=None, blinky=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node
        #TODO
        self.gabimode = SCATTER
        self.ghost_subject = ghost_subject #TODO GABI
        #modiificaion 27 / 5 para armas
        self.position = pygame.math.Vector2(node.position.x, node.position.y)  

    """metodo para inicializar la posición y el radio de colisión del fantasma
        Args:
            node (Node): Nodo en el que se encuentra el fantasma.
        """
    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

    """ meodo para establecer la posición del fantasma en el nodo actual
        Args:
            node (Node): Nodo en el que se encuentra el fantasma.
        """
    def update(self, dt):
        self.sprites.update(dt)
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def update2(self, dt):
        self.sprites.update(dt)
        #self.mode.update(dt)
        #
        if self.gabimode is SCATTER:
            self.scatter()
        elif self.gabimode is CHASE:
            self.chase()
        elif self.gabimode is SPAWN:
            if self.node == self.spawnNode:
                self.normalMode()
                self.gabimode = SCATTER #GABI TODO aca deberia usar el estado actual
        Entity.update(self, dt)

    """ metodo para establecer la velocidad del fantasma
        Args:
            speed (int): Velocidad del fantasma.
        """
    def scatter(self):
        self.goal = Vector2()

    """ metodo chase para establecer la dirección del fantasma
        Args:
            direction (int): Dirección del fantasma.
        """
    def chase(self):
        self.goal = self.pacman.position

    """ metodo spawn para establecer la posición de aparición del fantasma
        Args:   
            node (Node): Nodo de aparición del fantasma.
        """
    def spawn(self):
        self.goal = self.spawnNode.position

    """ metodo setSpawnNode para establecer el nodo de aparición del fantasma
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def setSpawnNode(self, node):
        self.spawnNode = node

    """ metodo startSpawn funciona para iniciar el modo de aparición del fantasma
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()

    """ metodo startFreight funciona para iniciar el modo de carga del fantasma
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def startFreight(self):
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection         
    #TODO GABI
    def startFreight2(self):
        if self.gabimode is not SPAWN:
            self.gabimode = FREIGHT
            self.setSpeed(50)
            self.directionMethod = self.randomDirection         

    def startSpawn2(self):
        if self.gabimode is FREIGHT:
            self.gabimode = SPAWN
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()

    def observe(self):
        if self.ghost_subject.state is FREIGHT:
            self.startFreight2()
            return
        if self.ghost_subject.state not in [FREIGHT, SPAWN]:
            self.normalMode()
            self.gabimode = self.ghost_subject.state
            return
        if self.ghost_subject.state is SPAWN: #Sin uso, ergo el mal orden TODO
            self.startSpawn2()

    def subscribe(self):
        self.ghost_subject.attach(self)



    ##
    """ metodo normalMode funciona para iniciar el modo normal del fantasma
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def normalMode(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection
        self.homeNode.denyAccess(DOWN, self)



""" clase que representa a Blinky, un fantasma específico
    Atributos:
        name (str): Nombre del fantasma.
        color (tuple): Color del fantasma.
        sprites (GhostSprites): Sprites de animación del fantasma.
        """
class Blinky(Ghost):

    """ metodo constructor de la clase Blinky
        Args:
            node (Node): Nodo en el que se encuentra el fantasma.
            pacman (Pacman): Referencia al objeto Pacman.
            blinky (Blinky): Referencia al objeto Blinky.
        """
    def __init__(self, node, pacman=None, ghost_subject=None, blinky=None):
    #def __init__(self, node, pacman=None, blinky=None): TODO GABI
        Ghost.__init__(self, node, pacman, ghost_subject, blinky)
        self.name = BLINKY
        self.color = RED
        self.sprites = GhostSprites(self)

""" clase para Pinky, un fantasma específico
    Atributos:
        name (str): Nombre del fantasma.
        color (tuple): Color del fantasma.
        sprites (GhostSprites): Sprites de animación del fantasma."""
class Pinky(Ghost):
    """ metodo constructor de la clase Pinky
        Args:
            node (Node): Nodo en el que se encuentra el fantasma.
            pacman (Pacman): Referencia al objeto Pacman.
            blinky (Blinky): Referencia al objeto Blinky.
        """
    def __init__(self, node, pacman=None, ghost_subject=None, blinky=None):
        Ghost.__init__(self, node, pacman, ghost_subject, blinky)
        self.name = PINKY
        self.color = PINK
        self.sprites = GhostSprites(self)

    """ metodo scatter para establecer la dirección del fantasma
        Args:
            direction (int): Dirección del fantasma.
        """
    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, 0)

    """ metodo chase para establecer la dirección del fantasma
        Args:
            direction (int): Dirección del fantasma.
        """
    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

""" clase para Inky, un fantasma específico
    Atributos:
        name (str): Nombre del fantasma.
        color (tuple): Color del fantasma.
        sprites (GhostSprites): Sprites de animación del fantasma."""
class Inky(Ghost):
    """ metodo constructor de la clase Inky
        Args:
            node (Node): Nodo en el que se encuentra el fantasma.
            pacman (Pacman): Referencia al objeto Pacman.
            blinky (Blinky): Referencia al objeto Blinky.
        """
    def __init__(self, node, pacman=None, ghost_subject=None, blinky=None):
        Ghost.__init__(self, node, pacman, ghost_subject, blinky)
        self.name = INKY
        self.color = TEAL
        self.sprites = GhostSprites(self)

    """ metodo scatter para establecer la dirección del fantasma
        Args:
            direction (int): Dirección del fantasma.
        """
    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)

    """ metodo chease para establecer la dirección del fantasma
        Args:
            direction (int): Dirección del fantasma.
        """
    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2

""" clase para Clyde, un fantasma específico
    Atributos:
        name (str): Nombre del fantasma.
        color (tuple): Color del fantasma.
        sprites (GhostSprites): Sprites de animación del fantasma."""
class Clyde(Ghost):
    """ metodo constructor de la clase Clyde
        Args:
            node (Node): Nodo en el que se encuentra el fantasma.
            pacman (Pacman): Referencia al objeto Pacman.
            blinky (Blinky): Referencia al objeto Blinky.
        """
    def __init__(self, node, pacman=None, ghost_subject=None, blinky=None):
        Ghost.__init__(self, node, pacman, ghost_subject, blinky)
        self.name = CLYDE
        self.color = ORANGE
        self.sprites = GhostSprites(self)


    """ metodo scatter para establecer la dirección del fantasma
        Args:
            direction (int): Dirección del fantasma.
        """
    def scatter(self):
        self.goal = Vector2(0, TILEHEIGHT*NROWS)

    """ metodo chase para establecer la dirección del fantasma
        Args:
            direction (int): Dirección del fantasma.
        """
    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

""" clase que representa a un grupo de fantasmas en el juego
    Atributos:
        blinky (Blinky): Referencia al objeto Blinky.
        pinky (Pinky): Referencia al objeto Pinky.
        inky (Inky): Referencia al objeto Inky.	
        clyde (Clyde): Referencia al objeto Clyde.
        ghosts (list): Lista de fantasmas."""
class GhostGroup(object):
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    """ metodo para obtener el fantasma por su nombre
        Args:
            name (str): Nombre del fantasma.
        """
    def __iter__(self):
        return iter(self.ghosts)
    """ meoto update para actualizar la posición de los fantasmas
        Args:
            dt (float): Delta time para el movimiento.
        """
    def update(self, dt):
        for ghost in self:
            ghost.update(dt)
    """ metodo startSpawn para iniciar el modo de aparición del fantasma 
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def startFreight(self):
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()
    """ metodo setSpawnNode para establecer el nodo de aparición del fantasma
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)
    """ metodo updatePoints para actualizar los puntos de los fantasmas
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2
    """ metodo resetPoints para restablecer los puntos de los fantasmas
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def resetPoints(self):
        for ghost in self:
            ghost.points = 200
    """ metodo hide para ocultar los fantasmas
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def hide(self):
        for ghost in self:
            ghost.visible = False
    """ metodo show para mostrar los fantasmas
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def show(self):
        for ghost in self:
            ghost.visible = True
    """ metodo reset para restablecer los fantasmas
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def reset(self):
        for ghost in self:
            ghost.reset()
    """ metodo render para renderizar los fantasmas
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def render(self, screen):
        
        for ghost in self:
            ghost.render(screen)


class GhostGroup2(object):

    def __init__(self):
        self.timer = 0
        self.timelimit = SCATTER_TIMELIMIT
        self.ghosts = []
        self.state = SCATTER
        #Inicia fantasmas
        #self.blinky = Blinky(node, pacman)
        #self.pinky = Blinky(node, pacman)
        #self.inky = Blinky(node, pacman)#, self.blinky)
        #self.clyde = Blinky(node, pacman)
        #self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]


    def notify(self):
        for ghost in self.ghosts:
            ghost.observe()

    def notifyUpdate(self, dt):
        if self.timer == 0 and self.state == FREIGHT:
            self.notify()
        self.timer += dt
        if self.timer >= self.timelimit:#Mejor forma seguro hay
            self.timer = 0
            if self.state is SCATTER:
                self.state = CHASE
                self.timelimit = CHASE_TIMELIMIT
                self.notify() #No es estrictamente desacoplado
                #print("switched to chase") #TODO sacar estos prints
            elif self.state is CHASE or FREIGHT:
                self.state = SCATTER
                self.timelimit = SCATTER_TIMELIMIT
                self.notify()
                #print("switched to scatter")

    def setBlue(self):
        self.timer = 0
        self.time = FREIGHT_TIMELIMIT

    def attach(self, ghost):
        self.ghosts.append(ghost)

    def deattach(self, ghost):
        self.ghosts.remove(ghost)

    def notifyChase(self, dt):
        for ghost in self.ghosts:
                ghost.notify()
                #ghost.gabimode = CHASE
                #ghost.chase()
                #ghost.update(dt)

    def notifyScatter(self, dt):
        pass
        #for ghost in self.ghosts:
            #if ghost.gabimode is not SPAWN or FREIGHT:
            #    ghost.normalMode() 
            #    ghost.gabimode = SCATTER
            #    #ghost.scatter()
            #    #ghost.update(dt)

    def update(self, dt):
        for ghost in self.ghosts:
            ghost.update2(dt)

    #copypaste GABI
    def __iter__(self):
        return iter(self.ghosts)

    def startFreight(self):
        for ghost in self.ghosts:
            ghost.startFreight2()
        self.resetPoints()

    def setSpawnNode(self, node):
        for ghost in self.ghosts:
            ghost.setSpawnNode(node)
    """ metodo updatePoints para actualizar los puntos de los fantasmas
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def updatePoints(self):
        for ghost in self.ghosts:
            ghost.points *= 2
    """ metodo resetPoints para restablecer los puntos de los fantasmas
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def resetPoints(self):
        for ghost in self.ghosts:
            ghost.points = 200
    """ metodo hide para ocultar los fantasmas
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def hide(self):
        for ghost in self.ghosts:
            ghost.visible = False
    """ metodo show para mostrar los fantasmas
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def show(self):
        for ghost in self.ghosts:
            ghost.visible = True
    """ metodo reset para restablecer los fantasmas
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def reset(self):
        for ghost in self.ghosts:
            ghost.reset()
    """ metodo render para renderizar los fantasmas
        Args:
            node (Node): Nodo de aparición del fantasma.
        """
    def render(self, screen):
        for ghost in self.ghosts:
            ghost.render(screen)
