import pygame
from constants import *
import numpy as np
from animation import Animator

BASETILEWIDTH = 16
BASETILEHEIGHT = 16
DEATH = 5
""" clase Spritesheet
    Representa una hoja de sprites que contiene imágenes para los personajes y objetos del juego.
    """
class Spritesheet(object):
    """ metodo constructor de la clase Spritesheet.
        Inicializa la hoja de sprites cargando la imagen y configurando el color de transparencia.
        Atributos:
            sheet (pygame.Surface): Superficie de la hoja de sprites.
            transcolor (tuple): Color de transparencia.
            width (int): Ancho de cada sprite en píxeles.
            height (int): Alto de cada sprite en píxeles.
            sheet (pygame.Surface): Superficie de la hoja de sprites escalada.
            """
    def __init__(self):
        self.sheet = pygame.image.load("spritesheet_mspacman.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))
    """ metodo getImage de la clase Spritesheet.
        Devuelve una subimagen de la hoja de sprites en función de las coordenadas y dimensiones especificadas.
        Args:
            x (int): Coordenada x de la subimagen.
            y (int): Coordenada y de la subimagen.
            width (int): Ancho de la subimagen.
            height (int): Alto de la subimagen."""
    def getImage(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

""" clase PacmanSprites
    Representa los sprites de Pacman en el juego."""
class PacmanSprites(Spritesheet):
    """ metodo constructor de la clase PacmanSprites.
        Inicializa los sprites de Pacman, definiendo las animaciones para cada dirección
        y el estado de muerte.
        Args: 
            entity (Entity): Entidad Pacman a la que se le asignan los sprites.
        Atributos:
            entity (Entity): Entidad Pacman a la que se le asignan los sprites. 
            animations (dict): Diccionario que contiene las animaciones para cada dirección.
            stopimage (tuple): Imagen de parada de Pacman.
            defineAnimations (dict): Método que define las animaciones para cada dirección.
            """
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()         
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (8, 0)
    """ metodo defineAnimations de la clase PacmanSprites.
        Define las animaciones para cada dirección (izquierda, derecha, arriba, abajo)
        y el estado de muerte.
        Atributos:
            LEFT (int): Dirección izquierda.
            RIGHT (int): Dirección derecha.
            UP (int): Dirección arriba.
            DOWN (int): Dirección abajo.
            DEATH (int): Estado de muerte.
            Animator (class): Clase que maneja la animación de los sprites."""
    def defineAnimations(self):
        self.animations[LEFT] = Animator(((8,0), (0, 0), (0, 2), (0, 0)))
        self.animations[RIGHT] = Animator(((10,0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Animator(((10,2), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Animator(((8,2), (4, 0), (4, 2), (4, 0)))
        self.animations[DEATH] = Animator(((0, 12), (2, 12), (4, 12), (6, 12), (8, 12), (10, 12), (12, 12), (14, 12), (16, 12), (18, 12), (20, 12)), speed=6, loop=False)
    """ metodo update de la clase PacmanSprites.
        Actualiza la imagen de Pacman en función de la dirección actual y el estado de vida.
        Si Pacman está vivo, cambia la imagen según la dirección.
        Si Pacman está muerto, muestra la animación de muerte.
        Args:
            dt (float): Delta time para la actualización de la animación."""
    def update(self, dt):
        if self.entity.alive == True:
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
                self.stopimage = (8, 0)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
                self.stopimage = (10, 0)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(*self.animations[DOWN].update(dt))
                self.stopimage = (8, 2)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(*self.animations[UP].update(dt))
                self.stopimage = (10, 2)
            elif self.entity.direction == STOP:
                self.entity.image = self.getImage(*self.stopimage)
        else:
            self.entity.image = self.getImage(*self.animations[DEATH].update(dt))
    """metodo reset de la clase PacmanSprites.
        Reinicia todas las animaciones de Pacman a su estado inicial.
        """
    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()
    """ metodo getStartImage de la clase PacmanSprites.
        Devuelve la imagen inicial de Pacman en función de su dirección."""
    def getStartImage(self):
        return self.getImage(8, 0)
    """ metodo getImage de la clase PacmanSprites.
        Devuelve una subimagen de la hoja de sprites en función de las coordenadas y dimensiones especificadas.
        Args:
            x (int): Coordenada x de la subimagen.
            y (int): Coordenada y de la subimagen."""
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

""" clase GhostSprites
    Representa los sprites de los fantasmas en el juego.
    """
class GhostSprites(Spritesheet):
    """ metodo constructor de la clase GhostSprites.
        Inicializa los sprites de los fantasmas, definiendo las posiciones iniciales
        y la imagen de inicio para cada fantasma.
        Args:
            entity (Entity): Entidad fantasma a la que se le asignan los sprites.
        Atributos:
            x (dict): Diccionario que almacena las posiciones iniciales de cada fantasma.
            entity (Entity): Entidad fantasma a la que se le asignan los sprites.
            """
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.x = {BLINKY:0, PINKY:2, INKY:4, CLYDE:6}
        self.entity = entity
        self.entity.image = self.getStartImage()

    """ metodo update de la clase GhostSprites.
        Actualiza la imagen del fantasma en función de su dirección y modo actual.
        Cambia la imagen según la dirección y el modo (dispersión, persecución, carga o aparición).
        Args:
            dt (float): Delta time para la actualización de la imagen.
        """
    def update(self, dt):
        x = self.x[self.entity.name]
        if self.entity.mode.current in [SCATTER, CHASE]:
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(x, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(x, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(x, 6)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(x, 4)
        elif self.entity.mode.current == FREIGHT:
            self.entity.image = self.getImage(10, 4)
        elif self.entity.mode.current == SPAWN:
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(8, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(8, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(8, 6)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(8, 4)
    """ metoddo getStartImage de la clase GhostSprites.
        Devuelve la imagen inicial del fantasma en función de su nombre."""    
    def getStartImage(self):
        return self.getImage(self.x[self.entity.name], 4)
    """ metodo getImage de la clase GhostSprites.
        Devuelve una subimagen de la hoja de sprites en función de las coordenadas y dimensiones especificadas.
        Args:
            x (int): Coordenada x de la subimagen.
            y (int): Coordenada y de la subimagen."""
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


""" clase fruitSprites
    Representa los sprites de las frutas en el juego."""
class FruitSprites(Spritesheet):
    """ metodo constructor de la clase FruitSprites.
        Inicializa los sprites de las frutas, definiendo las posiciones iniciales
        y la imagen de inicio para cada fruta.
        Args:
            entity (Entity): Entidad fruta a la que se le asignan los sprites.
            level (int): Nivel del juego para calcular la imagen inicial.
        Atributos:
            entity (Entity): Entidad fruta a la que se le asignan los sprites.
            fruits (dict): Diccionario que almacena las posiciones iniciales de cada fruta."""
    def __init__(self, entity, level):
        Spritesheet.__init__(self)
        self.entity = entity
        self.fruits = {0:(16,8), 1:(18,8), 2:(20,8), 3:(16,10), 4:(18,10), 5:(20,10)}
        self.entity.image = self.getStartImage(level % len(self.fruits))
    """ metodo getStartImage de la clase FruitSprites.
        Devuelve la imagen inicial de la fruta en función de su nombre.
        Args:
            key (int): Clave que representa la fruta en el diccionario.
        """
    def getStartImage(self, key):
        return self.getImage(*self.fruits[key])
    """ metodo getImage de la clase FruitSprites.
        Devuelve una subimagen de la hoja de sprites en función de las coordenadas y dimensiones especificadas.
        Args:
            x (int): Coordenada x de la subimagen.
            y (int): Coordenada y de la subimagen.
        returns:
            pygame.Surface: Subimagen de la hoja de sprites."""
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

""" clase LifeSprites
    Representa los sprites de las vidas en el juego."""
class LifeSprites(Spritesheet):
    """ metodo constructor de la clase LifeSprites.
        Inicializa los sprites de las vidas, definiendo la imagen inicial y el número de vidas.
        Args:
            numlives (int): Número de vidas iniciales.
        Atributos:
            images (list): Lista que almacena las imágenes de las vidas."""
    def __init__(self, numlives):
        Spritesheet.__init__(self)
        self.resetLives(numlives)
    """ metodo removeImage de la clase LifeSprites.
        Elimina la primera imagen de la lista de imágenes de vidas."""
    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)
    """metodo resetLives de la clase LifeSprites.
        Reinicia la lista de imágenes de vidas, creando nuevas imágenes en función del número de vidas.
        Args:
            numlives (int): Número de vidas iniciales.
        """
    def resetLives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.getImage(0,0))
    """ metodo getImage de la clase LifeSprites.
        Devuelve una subimagen de la hoja de sprites en función de las coordenadas y dimensiones especificadas.
        Args:
            x (int): Coordenada x de la subimagen.
            y (int): Coordenada y de la subimagen."""
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

""" clase MazeSprites
    Representa los sprites del laberinto en el juego."""
class MazeSprites(Spritesheet):
    """ metodo constructor de la clase MazeSprites.
        Inicializa los sprites del laberinto, cargando los datos del laberinto y la rotación de los sprites.
        Args:
            mazefile (str): Ruta al archivo que contiene la información del laberinto.
            rotfile (str): Ruta al archivo que contiene la información de rotación de los sprites."""
    def __init__(self, mazefile, rotfile):
        Spritesheet.__init__(self)
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)
    """ metodo getImage de la clase MazeSprites.
        Devuelve una subimagen de la hoja de sprites en función de las coordenadas y dimensiones especificadas.
        Args:
            x (int): Coordenada x de la subimagen.
            y (int): Coordenada y de la subimagen.
        """
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)
    """ metodo readMazeFile de la clase MazeSprites.
        Lee un archivo de texto que contiene la información del laberinto y lo convierte en un array de numpy.
        Args:
            mazefile (str): Ruta al archivo que contiene la información del laberinto.
        Returns:
            numpy.ndarray: Array que representa el laberinto."""
    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')
    """ metodo constructBackground de la clase MazeSprites.
        Construye el fondo del laberinto utilizando los datos del laberinto y la rotación de los sprites.
        Args:
            background (pygame.Surface): Superficie donde se dibuja el fondo del laberinto.
            y (int): Coordenada y de la subimagen.
        Returns:
            pygame.Surface: Superficie con el fondo del laberinto dibujado."""
    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.getImage(x, y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.getImage(10, 8)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))

        return background
    """ metodo rotate de la clase MazeSprites.
        Rota un sprite en función del valor especificado.
        Args:
            sprite (pygame.Surface): Superficie del sprite a rotar.
            value (int): Valor de rotación (0, 1, 2 o 3).
        Returns:
            pygame.Surface: Superficie del sprite rotado."""
    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value*90)
