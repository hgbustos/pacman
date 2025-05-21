from constants import *
""" clase MazeBase
    Clase base para representar laberintos en el juego Pacman.
    Atributos:
        portalPairs (dict): Diccionario que almacena pares de portales.
        homeoffset (tuple): Desplazamiento de la posición inicial de Pacman.
        ghostNodeDeny (dict): Diccionario que almacena restricciones de acceso para los fantasmas.
        """
class MazeBase(object):
    """ metodo constructor de la clase MazeBase.
        Inicializa los atributos del laberinto, incluyendo los pares de portales,
        el desplazamiento de la posición inicial de Pacman y las restricciones de acceso para los fantasmas.
        """
    def __init__(self):
        self.portalPairs = {}
        self.homeoffset = (0, 0)
        self.ghostNodeDeny = {UP:(), DOWN:(), LEFT:(), RIGHT:()}

    """ metodo setPortalPairs de la clase MazeBase.
        Establece los pares de portales en el laberinto.
        Args:
            nodes (NodeManager): Gestor de nodos que maneja la creación y conexión de nodos.
        """
    def setPortalPairs(self, nodes):
        for pair in list(self.portalPairs.values()):
            nodes.setPortalPair(*pair)
    """ metodo connectHomeNodes de la clase MazeBase.
        Conecta los nodos de inicio de Pacman en el laberinto.
        Args:
            nodes (NodeManager): Gestor de nodos que maneja la creación y conexión de nodos.
        """
    def connectHomeNodes(self, nodes):
        key = nodes.createHomeNodes(*self.homeoffset)
        nodes.connectHomeNodes(key, self.homenodeconnectLeft, LEFT)
        nodes.connectHomeNodes(key, self.homenodeconnectRight, RIGHT)
    """ metodo addOffset de la clase MazeBase.
        Agrega un desplazamiento a las coordenadas (x, y) de la posición inicial de Pacman.
        Args:
            x (float): Coordenada x.
            y (float): Coordenada y."""
    def addOffset(self, x, y):
        return x+self.homeoffset[0], y+self.homeoffset[1]
    """ metodo denyGhostsAccess de la clase MazeBase.
        Deniega el acceso a los fantasmas en ciertas direcciones y nodos del laberinto.
        Args:
            ghosts (list): Lista de fantasmas a los que se les deniega el acceso.
            nodes (NodeManager): Gestor de nodos que maneja la creación y conexión de nodos.
        """
    def denyGhostsAccess(self, ghosts, nodes):
        nodes.denyAccessList(*(self.addOffset(2, 3) + (LEFT, ghosts)))
        nodes.denyAccessList(*(self.addOffset(2, 3) + (RIGHT, ghosts)))

        for direction in list(self.ghostNodeDeny.keys()):
            for values in self.ghostNodeDeny[direction]:
                nodes.denyAccessList(*(values + (direction, ghosts)))

""" clase Maze1
    Representa el primer laberinto del juego Pacman.
    """
class Maze1(MazeBase):
    """ metodo constructor de la clase Maze1.
        Inicializa los atributos del laberinto, incluyendo los pares de portales,
        el desplazamiento de la posición inicial de Pacman y las restricciones de acceso para los fantasmas.
        atributos:
            name (str): Nombre del laberinto.
            portalPairs (dict): Diccionario que almacena pares de portales.
            homeoffset (tuple): Desplazamiento de la posición inicial de Pacman.
            homenodeconnectLeft (tuple): Coordenadas del nodo de inicio a la izquierda.
            homenodeconnectRight (tuple): Coordenadas del nodo de inicio a la derecha.
            pacmanStart (tuple): Coordenadas iniciales de Pacman.
            fruitStart (tuple): Coordenadas iniciales de la fruta.
            ghostNodeDeny (dict): Diccionario que almacena restricciones de acceso para los fantasmas.
        """
    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze1"
        self.portalPairs = {0:((0, 17), (27, 17))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (12, 14)
        self.homenodeconnectRight = (15, 14)
        self.pacmanStart = (15, 26)
        self.fruitStart = (9, 20)
        self.ghostNodeDeny = {UP:((12, 14), (15, 14), (12, 26), (15, 26)), LEFT:(self.addOffset(2, 3),),
                              RIGHT:(self.addOffset(2, 3),)}

""" clase Maze2
    Representa el segundo laberinto del juego Pacman.
    """
class Maze2(MazeBase):
    """ metodo constructor de la clase Maze2.
        Inicializa los atributos del laberinto, incluyendo los pares de portales,
        el desplazamiento de la posición inicial de Pacman y las restricciones de acceso para los fantasmas.
        atributos:
            name (str): Nombre del laberinto.
            portalPairs (dict): Diccionario que almacena pares de portales.
            homeoffset (tuple): Desplazamiento de la posición inicial de Pacman.
            homenodeconnectLeft (tuple): Coordenadas del nodo de inicio a la izquierda.
            homenodeconnectRight (tuple): Coordenadas del nodo de inicio a la derecha.
            pacmanStart (tuple): Coordenadas iniciales de Pacman.
            fruitStart (tuple): Coordenadas iniciales de la fruta.
            ghostNodeDeny (dict): Diccionario que almacena restricciones de acceso para los fantasmas.
        """
    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze2"
        self.portalPairs = {0:((0, 4), (27, 4)), 1:((0, 26), (27, 26))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (9, 14)
        self.homenodeconnectRight = (18, 14)
        self.pacmanStart = (16, 26)
        self.fruitStart = (11, 20)
        self.ghostNodeDeny = {UP:((9, 14), (18, 14), (11, 23), (16, 23)), LEFT:(self.addOffset(2, 3),),
                              RIGHT:(self.addOffset(2, 3),)}

""" clase MazeData
    Clase que gestiona la carga de laberintos en el juego Pacman.
    Atributos:
        obj (MazeBase): Objeto del laberinto cargado.
        mazedict (dict): Diccionario que almacena los laberintos disponibles.
    """
class MazeData(object):
    """ metodo constructor de la clase MazeData.
        Inicializa el objeto del laberinto y el diccionario de laberintos disponibles.
        """
    def __init__(self):
        self.obj = None
        self.mazedict = {0:Maze1, 1:Maze2}
    """ metodo loadMaze de la clase MazeData.
        Carga un laberinto específico en función del nivel proporcionado.
        Args:
            level (int): Nivel del laberinto a cargar.
        """
    def loadMaze(self, level):
        self.obj = self.mazedict[level%len(self.mazedict)]()
