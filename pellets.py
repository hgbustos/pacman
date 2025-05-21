import pygame
from vector import Vector2
from constants import *
import numpy as np
""" clase Pellet
    Representa un pellet en el juego Pacman."""
class Pellet(object):
    """ metodo constructor de la clase Pellet.
        Inicializa los atributos del pellet, incluyendo su posición, color,
        radio de colisión, puntos y visibilidad.
        Args: 
            row (int): Fila en la que se encuentra el pellet.
            column (int): Columna en la que se encuentra el pellet.
        atributos:
            name (str): Nombre de la entidad.
            position (Vector2): Posición del pellet en el laberinto.
            color (tuple): Color del pellet (blanco).
            radius (int): Radio del pellet.
            collideRadius (int): Radio de colisión del pellet.
            points (int): Puntos otorgados al recoger el pellet.
            visible (bool): Indica si el pellet es visible o no.
        """
    def __init__(self, row, column):
        self.name = PELLET
        self.position = Vector2(column*TILEWIDTH, row*TILEHEIGHT)
        self.color = WHITE
        self.radius = int(2 * TILEWIDTH / 16)
        self.collideRadius = 2 * TILEWIDTH / 16
        self.points = 10
        self.visible = True
    """ metodo render de la clase Pellet.
        Dibuja el pellet en la pantalla si es visible.
        Args:
            screen (pygame.Surface): Superficie de la pantalla donde se dibuja el pellet.
        """
    def render(self, screen):
        if self.visible:
            adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
            p = self.position + adjust
            pygame.draw.circle(screen, self.color, p.asInt(), self.radius)

""" clase PowerPellet
    Representa un pellet especial en el juego Pacman que otorga más puntos."""
class PowerPellet(Pellet):
    """ metodo constructor de la clase PowerPellet.
        Inicializa los atributos del power pellet, incluyendo su posición, color,
        radio de colisión, puntos, tiempo de parpadeo y temporizador.
        Args:
            row (int): Fila en la que se encuentra el power pellet.
            column (int): Columna en la que se encuentra el power pellet.
        atributos:
            name (str): Nombre de la entidad.
            position (Vector2): Posición del power pellet en el laberinto.
            color (tuple): Color del power pellet (blanco).
            radius (int): Radio del power pellet.
            collideRadius (int): Radio de colisión del power pellet.
            points (int): Puntos otorgados al recoger el power pellet.
            visible (bool): Indica si el power pellet es visible o no.
            flashTime (float): Tiempo de parpadeo del power pellet.
            timer (float): Temporizador para controlar el parpadeo.
            """
    def __init__(self, row, column):
        Pellet.__init__(self, row, column)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flashTime = 0.2
        self.timer= 0
    """ metodo update de la clase PowerPellet.
        Actualiza el temporizador del power pellet y verifica si ha alcanzado su tiempo de parpadeo.
        Si es así, cambia la visibilidad del power pellet.
        Args:
            dt (float): Delta time para el temporizador.
        """
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0

""" clase PelletGroup
    Representa un grupo de pellets en el juego Pacman."""
class PelletGroup(object):
    """ metodo constructor de la clase PelletGroup.
        Inicializa la lista de pellets y power pellets, y crea la lista de pellets a partir de un archivo.
        Args:
            pelletfile (str): Ruta al archivo que contiene la información de los pellets.
        atributos:
            pelletList (list): Lista de pellets en el grupo.
            powerpellets (list): Lista de power pellets en el grupo.
            numEaten (int): Número de pellets comidos."""
    def __init__(self, pelletfile):
        self.pelletList = []
        self.powerpellets = []
        self.createPelletList(pelletfile)
        self.numEaten = 0
    """ metodo update de la clase PelletGroup.
        Actualiza el estado de los power pellets en el grupo.
        Args:   
            dt (float): Delta time para el temporizador.
        """
    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)
    """ metodo createPelletList de la clase PelletGroup.
        Crea la lista de pellets a partir de un archivo de texto.
        Args:
            pelletfile (str): Ruta al archivo que contiene la información de los pellets.
        """     
    def createPelletList(self, pelletfile):
        data = self.readPelletfile(pelletfile)        
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.pelletList.append(Pellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    pp = PowerPellet(row, col)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)
    """ metodo readPelletfile de la clase PelletGroup. 
        Lee el archivo de texto que contiene la información de los pellets.
        Args:
            textfile (str): Ruta al archivo que contiene la información de los pellets.
        Returns:
            numpy.ndarray: Matriz con la información de los pellets.
        """           
    def readPelletfile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    """ metodo isEaten de la clase PelletGroup.
        Verifica si un pellet ha sido comido y lo elimina de la lista.
        Args:
            pellet (Pellet): Pellet a verificar.
        """
    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        return False
    """ metodo render de la clase PelletGroup.
        Dibuja todos los pellets en la pantalla.
        Args:
            screen (pygame.Surface): Superficie de la pantalla donde se dibujan los pellets.
        """
    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)