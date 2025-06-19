import pygame
from vector import Vector2
from constants import *
import numpy as np
""" Clase que representa un nodo en el juego Pacman."""
class Node(object):
    """ metodo constructor de la clase Node.
        Inicializa la posición del nodo, los vecinos y el acceso a los nodos.
        Atributos:
            position (Vector2): Posición del nodo en el laberinto.
            neighbors (dict): Diccionario que almacena los nodos vecinos en diferentes direcciones.
            access (dict): Diccionario que almacena las entidades que pueden acceder a cada dirección
            """
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL:None}
        self.access = {UP:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT, BULLET], 
                       DOWN:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT, BULLET], 
                       LEFT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT, BULLET], 
                       RIGHT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT, BULLET]}
    """metodo denyAccess de la clase Node.
        Deniega el acceso a una entidad en una dirección específica.
        Args:
            direction (int): Dirección en la que se deniega el acceso.
            entity (Entity): Entidad a la que se le deniega el acceso.
        """
    def denyAccess(self, direction, entity):
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)
    """ metodo allowAccess de la clase Node.
        Permite el acceso a una entidad en una dirección específica.
        Args:
            direction (int): Dirección en la que se permite el acceso.
            entity (Entity): Entidad a la que se le permite el acceso."""
    def allowAccess(self, direction, entity):
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)
    """ metodo render de la clase Node.
        Dibuja el nodo y sus conexiones en la pantalla.
        Args:
            screen (pygame.Surface): Superficie de la pantalla donde se dibujan los nodos.
        """
    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)

""" clase NodeGroup
    Representa un grupo de nodos en el juego Pacman."""
class NodeGroup(object):
    """ metodo constructor de la clase NodeGroup.
        Inicializa el nivel del laberinto y crea la tabla de nodos.
        Atributos:
            level (int): Nivel del laberinto.
            nodesLUT (dict): Diccionario que almacena los nodos del laberinto.
            nodeSymbols (list): Lista de símbolos que representan nodos.
            pathSymbols (list): Lista de símbolos que representan caminos.
            homekey (tuple): Coordenadas del nodo de inicio de Pacman."""
    def __init__(self, level):
        self.level = level
        self.nodesLUT = {}
        self.nodeSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)
        self.homekey = None
    """ metodo readMazeFile de la clase NodeGroup.
        Lee el archivo de texto del laberinto y lo convierte en una matriz de caracteres.
        Args:
            textfile (str): Ruta del archivo de texto que representa el laberinto."""
    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    """ metodo createNodeTable de la clase NodeGroup.
        Crea una tabla de nodos a partir de los datos del laberinto.
        Args:
            data (numpy.ndarray): Matriz de caracteres que representa el laberinto.
            xoffset (int): Desplazamiento en la dirección x.
            yoffset (int): Desplazamiento en la dirección y.
        """
    def createNodeTable(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)
    """ metodo constructKey de la clase NodeGroup.
        Crea una clave para acceder a los nodos en el diccionario.
        Args:
            x (int): Coordenada x del nodo.
            y (int): Coordenada y del nodo.
        Returns:
            tuple: Tupla que representa la clave del nodo en el diccionario."""
    def constructKey(self, x, y):
        return x * TILEWIDTH, y * TILEHEIGHT

    """ metodo connectHorizontally de la clase NodeGroup.
        Conecta los nodos horizontalmente en el laberinto.
        Args:
            data (numpy.ndarray): Matriz de caracteres que representa el laberinto.
            xoffset (int): Desplazamiento en la dirección x.
            yoffset (int): Desplazamiento en la dirección y.
        """
    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[LEFT] = self.nodesLUT[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None
    """ metodo connectVertically de la clase NodeGroup.
        Conecta los nodos verticalmente en el laberinto.
        Args:
            data (numpy.ndarray): Matriz de caracteres que representa el laberinto.
            xoffset (int): Desplazamiento en la dirección x.
            yoffset (int): Desplazamiento en la dirección y.
        """
    def connectVertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[UP] = self.nodesLUT[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    """ metodo getStartTempNode de la clase NodeGroup.
        Devuelve el primer nodo temporal del laberinto.
        Returns:
            Node: Primer nodo temporal del laberinto."""
    def getStartTempNode(self):
        nodes = list(self.nodesLUT.values())
        return nodes[0]
    """ metodo setPortalPair de la clase NodeGroup.
        Establece un par de portales en el laberinto.
        Args:
            pair1 (tuple): Primer par de coordenadas del portal.
            pair2 (tuple): Segundo par de coordenadas del portal.
        """
    def setPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

    """ metodo createHomeNodes de la clase NodeGroup.
        Crea los nodos de inicio de Pacman en el laberinto.
        Args:
            xoffset (int): Desplazamiento en la dirección x.
            yoffset (int): Desplazamiento en la dirección y.
            Returns:
                tuple: Tupla que representa la clave del nodo de inicio de Pacman en el diccionario."""
    def createHomeNodes(self, xoffset, yoffset):
        homedata = np.array([['X','X','+','X','X'],
                             ['X','X','.','X','X'],
                             ['+','X','.','X','+'],
                             ['+','.','+','.','+'],
                             ['+','X','X','X','+']])

        self.createNodeTable(homedata, xoffset, yoffset)
        self.connectHorizontally(homedata, xoffset, yoffset)
        self.connectVertically(homedata, xoffset, yoffset)
        self.homekey = self.constructKey(xoffset+2, yoffset)
        return self.homekey
    """ metodo conectHomeNodes de la clase NodeGroup.
        Conecta los nodos de inicio de Pacman con otros nodos en el laberinto.
        Args:
            homekey (tuple): Coordenadas del nodo de inicio de Pacman.
            otherkey (tuple): Coordenadas del otro nodo a conectar.
            direction (int): Dirección en la que se conecta el nodo."""
    def connectHomeNodes(self, homekey, otherkey, direction):     
        key = self.constructKey(*otherkey)
        self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key]
        self.nodesLUT[key].neighbors[direction*-1] = self.nodesLUT[homekey]
    """ metodo getNodeFromPixels de la clase NodeGroup.
        Devuelve el nodo correspondiente a las coordenadas de píxeles.
        Args:
            xpixel (int): Coordenada x en píxeles.
            ypixel (int): Coordenada y en píxeles.
        Returns:
            Node: Nodo correspondiente a las coordenadas de píxeles."""
    def getNodeFromPixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None
    """ metodo getNodeFromTiles de la clase NodeGroup.
        Devuelve el nodo correspondiente a las coordenadas de la cuadrícula.
        Args:
            col (int): Columna de la cuadrícula.
            row (int): Fila de la cuadrícula.
        Returns:
            Node: Nodo correspondiente a las coordenadas de la cuadrícula."""   
    def getNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None
    """ metodo denyAccess de la clase NodeGroup.
        Deniega el acceso a una entidad en una dirección específica en un nodo.
        Args:
            col (int): Columna del nodo.
            row (int): Fila del nodo.
            direction (int): Dirección en la que se deniega el acceso.
            entity (Entity): Entidad a la que se le deniega el acceso.
        """
    def denyAccess(self, col, row, direction, entity):
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.denyAccess(direction, entity)
    """ metodo allowAccess de la clase NodeGroup.
        Permite el acceso a una entidad en una dirección específica en un nodo.
        Args:
            col (int): Columna del nodo.
            row (int): Fila del nodo.
            direction (int): Dirección en la que se permite el acceso.
            entity (Entity): Entidad a la que se le permite el acceso.
        """
    def allowAccess(self, col, row, direction, entity):
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.allowAccess(direction, entity)

    """ metodo denyAccessList de la clase NodeGroup.
        Deniega el acceso a una lista de entidades en una dirección específica en un nodo.
        Args:
            col (int): Columna del nodo.
            row (int): Fila del nodo.
            direction (int): Dirección en la que se deniega el acceso.
            entities (list): Lista de entidades a las que se les deniega el acceso.
        """
    def denyAccessList(self, col, row, direction, entities):
        for entity in entities:
            self.denyAccess(col, row, direction, entity)
    """ metodo allowAccessList de la clase NodeGroup.
        Permite el acceso a una lista de entidades en una dirección específica en un nodo.
        Args:
            col (int): Columna del nodo.
            row (int): Fila del nodo.
            direction (int): Dirección en la que se permite el acceso.
            entities (list): Lista de entidades a las que se les permite el acceso.
        """
    def allowAccessList(self, col, row, direction, entities):
        for entity in entities:
            self.allowAccess(col, row, direction, entity)
    """ metodo denyHomeAccess de la clase NodeGroup.
        Deniega el acceso a una entidad en la casa de Pacman.
        Args:
            entity (Entity): Entidad a la que se le deniega el acceso.
        """
    def denyHomeAccess(self, entity):
        self.nodesLUT[self.homekey].denyAccess(DOWN, entity)
    """ metodo allowHomeAccess de la clase NodeGroup.
        Permite el acceso a una entidad en la casa de Pacman.
        Args:
            entity (Entity): Entidad a la que se le permite el acceso.
        """
    def allowHomeAccess(self, entity):
        self.nodesLUT[self.homekey].allowAccess(DOWN, entity)
    """ metodo denyHomeAccessList de la clase NodeGroup.
        Deniega el acceso a una lista de entidades en la casa de Pacman.
        Args:
            entities (list): Lista de entidades a las que se les deniega el acceso.
        """
    def denyHomeAccessList(self, entities):
        for entity in entities:
            self.denyHomeAccess(entity)
    """ metodo allowHomeAccessList de la clase NodeGroup.
        Permite el acceso a una lista de entidades en la casa de Pacman.
        Args:
            entities (list): Lista de entidades a las que se les permite el acceso.
        """
    def allowHomeAccessList(self, entities):
        for entity in entities:
            self.allowHomeAccess(entity)
    """ metodo render de la clase NodeGroup.
        Dibuja todos los nodos y sus conexiones en la pantalla.
        Args:
            screen (pygame.Surface): Superficie de la pantalla donde se dibujan los nodos.
        """
    def render(self, screen):
        for node in self.nodesLUT.values():
            node.render(screen)
