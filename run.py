import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pauser import Pause
from text import TextGroup
from sprites import LifeSprites
from sprites import MazeSprites
from mazedata import MazeData
""" clase GameController
    Controlador principal del juego Pacman."""
class GameController(object):
    """ metodo constructor de la clase GameController.
        Inicializa la pantalla del juego, el fondo, el reloj, los sprites y los grupos de entidades.
        Atributos:
            screen (pygame.Surface): Pantalla del juego.
            background (pygame.Surface): Fondo del juego.
            background_norm (pygame.Surface): Fondo normal del juego.
            background_flash (pygame.Surface): Fondo de parpadeo del juego.
            clock (pygame.time.Clock): Reloj para controlar la velocidad de actualización del juego.
            fruit (Fruit): Fruta en el juego.
            pause (Pause): Controlador de pausa del juego.
            level (int): Nivel actual del juego.
            lives (int): Número de vidas restantes del jugador.
            score (int): Puntuación del jugador.
            textgroup (TextGroup): Grupo de texto para mostrar información en pantalla.
            lifesprites (LifeSprites): Sprites de vida del jugador. 
            flashBG (bool): Indica si el fondo debe parpadear.
            flashTime (float): Tiempo de parpadeo del fondo.
            flashTimer (float): Temporizador para controlar el parpadeo del fondo.
            fruitCaptured (list): Lista de frutas capturadas por el jugador.
            fruitNode (Node): Nodo donde se encuentra la fruta.
            mazedata (MazeData): Datos del laberinto."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []
        self.fruitNode = None
        self.mazedata = MazeData()
    """ metodo setBackground de la clase GameController.
        Establece el fondo del juego, tanto el normal como el de parpadeo.
        Carga los sprites del laberinto y construye el fondo normal y de parpadeo.
        Atributos:
            background_norm (pygame.Surface): Fondo normal del juego.
            background_flash (pygame.Surface): Fondo de parpadeo del juego.
            flashBG (bool): Indica si el fondo debe parpadear.
            background (pygame.Surface): Fondo actual del juego.
            flashTimer (float): Temporizador para controlar el parpadeo del fondo.
            flashTime (float): Tiempo de parpadeo del fondo.            
            """
    def setBackground(self):
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level%5)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        self.flashBG = False
        self.background = self.background_norm
    """ metodo startGame de la clase GameController.
        Inicia el juego cargando los datos del laberinto, creando los sprites y grupos de entidades,
        y configurando los nodos y accesos.
        Atributos:
            mazedata (MazeData): Datos del laberinto.
            mazesprites (MazeSprites): Sprites del laberinto.
            nodes (NodeGroup): Grupo de nodos del laberinto.
            pacman (Pacman): Pacman en el juego.
            pellets (PelletGroup): Grupo de pellets en el juego.
            ghosts (GhostGroup): Grupo de fantasmas en el juego.
            fruit (Fruit): Fruta en el juego.
            fruitNode (Node): Nodo donde se encuentra la fruta.
            ghosts (GhostGroup): Grupo de fantasmas en el juego.
      """
    def startGame(self):      
        self.mazedata.loadMaze(self.level)
        self.mazesprites = MazeSprites(self.mazedata.obj.name+".txt", self.mazedata.obj.name+"_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup(self.mazedata.obj.name+".txt")
        self.mazedata.obj.setPortalPairs(self.nodes)
        self.mazedata.obj.connectHomeNodes(self.nodes)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart))
        self.pellets = PelletGroup(self.mazedata.obj.name+".txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)

        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0)))

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.mazedata.obj.denyGhostsAccess(self.ghosts, self.nodes)
    """ metodo startGame_old de la clase GameController.
        Inicia el juego cargando los datos del laberinto, creando los sprites y grupos de entidades,
        y configurando los nodos y accesos.
        Atributos:
            mazedata (MazeData): Datos del laberinto.
            mazesprites (MazeSprites): Sprites del laberinto.
            nodes (NodeGroup): Grupo de nodos del laberinto.
            pacman (Pacman): Pacman en el juego.
            pellets (PelletGroup): Grupo de pellets en el juego.
            ghosts (GhostGroup): Grupo de fantasmas en el juego.
            fruit (Fruit): Fruta en el juego.
            fruitNode (Node): Nodo donde se encuentra la fruta.
            ghosts (GhostGroup): Grupo de fantasmas en el juego. 
            """
    def startGame_old(self):      
        self.mazedata.loadMaze(self.level)#######
        self.mazesprites = MazeSprites("maze1.txt", "maze1_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup("maze1.txt")
        self.nodes.setPortalPair((0,17), (27,17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
        self.pellets = PelletGroup("maze1.txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.nodes.denyAccessList(12, 14, UP, self.ghosts)
        self.nodes.denyAccessList(15, 14, UP, self.ghosts)
        self.nodes.denyAccessList(12, 26, UP, self.ghosts)
        self.nodes.denyAccessList(15, 26, UP, self.ghosts)

        
    """ metodo update de la clase GameController.
        Actualiza el estado del juego, incluyendo la posición de Pacman, los pellets,
        los fantasmas y la fruta. Verifica eventos de colisión y actualiza la puntuación.
        Args:
            dt (float): Delta time para el temporizador.
        """
    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.ghosts.update(dt)      
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()
    """ metodo checkEvents de la clase GameController.
        Verifica los eventos de entrada del usuario, como teclas presionadas y colisiones.
        Si se presiona la tecla ESPACIO, alterna entre pausar y reanudar el juego.
        Si Pacman come un pellet, actualiza la puntuación y verifica si se ha comido todos los pellets.
        Si Pacman colisiona con un fantasma, verifica el estado del fantasma y actualiza la puntuación o las vidas.
        Si Pacman colisiona con la fruta, actualiza la puntuación y verifica si se ha capturado la fruta."""
    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSETXT)
                            #self.hideEntities()
    """ metodo checkPelletEvents de la clase GameController.
        Verifica si Pacman ha comido un pellet y actualiza la puntuación.
        Si se ha comido un pellet, verifica si es un power pellet y actualiza el estado de los fantasmas.
        Si se han comido todos los pellets, pausa el juego y avanza al siguiente nivel.
        Args:
            self: Instancia de la clase GameController.
        """
    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.startFreight()
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)
    """ metodo checkGhostEvents de la clase GameController.
        Verifica si Pacman ha colisionado con un fantasma y actualiza la puntuación.
        Si el fantasma está en modo FREIGHT, Pacman lo captura y se oculta.
        Si el fantasma no está en modo SPAWN, Pacman pierde una vida y se oculta.
        Si Pacman no tiene vidas restantes, muestra el mensaje de GAME OVER y reinicia el juego.
        Args:
            self: Instancia de la clase GameController.
        """
    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)                  
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -=  1
                        self.lifesprites.removeImage()
                        self.pacman.die()               
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textgroup.showText(GAMEOVERTXT)
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)
    """ metodo checkFruitEvents de la clase GameController.
        Verifica si Pacman ha colisionado con la fruta y actualiza la puntuación.
        Si Pacman ha comido 50 o 140 pellets, genera una fruta en la posición correspondiente.
        Si Pacman colisiona con la fruta, actualiza la puntuación y la lista de frutas capturadas.
        Si la fruta ha sido destruida, la elimina.
        Si la fruta no ha sido capturada, la agrega a la lista de frutas capturadas.
        Si la fruta ha sido destruida, la elimina.
        Si la fruta no ha sido capturada, la agrega a la lista de frutas capturadas.
        Args:
            self: Instancia de la clase GameController.
        """
    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20), self.level)
                print(self.fruit)
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None
    """ metodo showEntities de la clase GameController.
        Muestra las entidades del juego, incluyendo Pacman y los fantasmas.
        Args:
            self: Instancia de la clase GameController.
        """
    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()
    """ metodo hideEntities de la clase GameController.
        Oculta las entidades del juego, incluyendo Pacman y los fantasmas.
        Args:
            self: Instancia de la clase GameController.
        """
    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()
    """ metodo nextLevel de la clase GameController.
        Avanza al siguiente nivel del juego, actualizando la puntuación y el nivel.
        Muestra las entidades del juego y pausa el juego.
        Args:
            self: Instancia de la clase GameController.
        """
    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)
    """ metodo restartGame de la clase GameController.
        Reinicia el juego, restableciendo las vidas, el nivel y la puntuación.
        Pausa el juego y muestra el mensaje de "Listo para jugar".
        Args:
            self: Instancia de la clase GameController.
        """
    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)
        self.fruitCaptured = []
    """ metodo resetLevel de la clase GameController.
        Reinicia el nivel actual del juego, restableciendo la posición de Pacman y los fantasmas.
        Pausa el juego y muestra el mensaje de "Listo para jugar".
        Args:
            self: Instancia de la clase GameController.
        """
    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)

    """ metodo updateScore de la clase GameController.
        Actualiza la puntuación del jugador y el texto en pantalla.
        Args:
            points (int): Puntos a agregar a la puntuación actual.
        """
    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)
    """ metodo render de la clase GameController.
        Dibuja el fondo, los pellets, la fruta, Pacman, los fantasmas y el texto en pantalla.
        Args:
            self: Instancia de la clase GameController.
        """
    def render(self):
        self.screen.blit(self.background, (0, 0))
        #self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        for i in range(len(self.fruitCaptured)):
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1)
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))

        pygame.display.update()

"""funcion de este if es ejecutar el juego.
    Crea una instancia de GameController y llama al método startGame.
    Luego, entra en un bucle infinito para actualizar el juego.
    """
if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()



