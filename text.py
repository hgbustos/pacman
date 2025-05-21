import pygame
from vector import Vector2
from constants import *
"""clase text
    Representa un texto en la pantalla del juego Pacman."""
class Text(object):
    """ metodo constructor de la clase Text.
        Inicializa los atributos del texto, incluyendo su posición, color,
        tamaño, tiempo de vida, visibilidad y temporizador.
        Args:
            text (str): Texto a mostrar.
            color (tuple): Color del texto.
            x (int): Posición x del texto.
            y (int): Posición y del texto.
            size (int): Tamaño de la fuente del texto.
            time (float, opcional): Tiempo de vida del texto en segundos. Por defecto es None.
            id (int, opcional): Identificador del texto. Por defecto es None.
            visible (bool, opcional): Indica si el texto es visible o no. Por defecto es True.
        atributos:
            id (int): Identificador del texto.
            text (str): Texto a mostrar.
            color (tuple): Color del texto.
            size (int): Tamaño de la fuente del texto.
            visible (bool): Indica si el texto es visible o no.
            position (Vector2): Posición del texto en la pantalla.
            timer (float): Temporizador para controlar el tiempo de vida del texto.
            lifespan (float): Tiempo de vida del texto en segundos.
            label (pygame.Surface): Superficie donde se renderiza el texto.
            destroy (bool): Indica si el texto debe ser destru
            font (pygame.font.Font): Fuente del texto.
            createLabel (callable): Método para crear la etiqueta del texto.
            setupFont (callable): Método para configurar la fuente del texto."""
    def __init__(self, text, color, x, y, size, time=None, id=None, visible=True):
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        self.position = Vector2(x, y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        self.setupFont("PressStart2P-Regular.ttf")
        self.createLabel()
    """ metodo setupFont de la clase Text.
        Configura la fuente del texto utilizando el archivo de fuente especificado.
        Args:
            fontpath (str): Ruta del archivo de fuente.
        """
    def setupFont(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.size)
    """ metodo createLabel de la clase Text.
        Crea la etiqueta del texto utilizando la fuente y el color especificados.
        """
    def createLabel(self):
        self.label = self.font.render(self.text, 1, self.color)
    """metodo setText de la clase Text.
        Establece el nuevo texto y crea la etiqueta correspondiente.
        Args:
            newtext (str): Nuevo texto a mostrar.
        """
    def setText(self, newtext):
        self.text = str(newtext)
        self.createLabel()
    """metodo update de la clase Text.
        Actualiza el temporizador del texto y verifica si ha alcanzado su tiempo de vida.
        Si es así, marca el texto para ser destruido.
        Args:
            dt (float): Delta time para el temporizador.
        """
    def update(self, dt):
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True
    """ metodo render de la clase Text.
        Dibuja el texto en la pantalla si es visible.
        Args:
            screen (pygame.Surface): Superficie de la pantalla donde se dibuja el texto.
        """
    def render(self, screen):
        if self.visible:
            x, y = self.position.asTuple()
            screen.blit(self.label, (x, y))

""" clase TextGroup
    Representa un grupo de textos en el juego Pacman."""
class TextGroup(object):
    """ metodo constructor de la clase TextGroup.
        Inicializa el grupo de textos y configura los textos iniciales.
        Atributos:
            nextid (int): Identificador del siguiente texto a agregar.
            alltext (dict): Diccionario que almacena todos los textos.
            setupText (callable): Método para configurar los textos iniciales.
            showText (callable): Método para mostrar un texto específico."""
    def __init__(self):
        self.nextid = 10
        self.alltext = {}
        self.setupText()
        self.showText(READYTXT)

    """ metodo addText de la clase TextGroup.
        Agrega un nuevo texto al grupo de textos y devuelve su identificador.
        Args:
            text (str): Texto a mostrar.
            color (tuple): Color del texto.
            x (int): Posición x del texto.
            y (int): Posición y del texto.
            size (int): Tamaño de la fuente del texto.
            time (float, opcional): Tiempo de vida del texto en segundos. Por defecto es None.
            id (int, opcional): Identificador del texto. Por defecto es None."""
    def addText(self, text, color, x, y, size, time=None, id=None):
        self.nextid += 1
        self.alltext[self.nextid] = Text(text, color, x, y, size, time=time, id=id)
        return self.nextid
    """ metodo removeText de la clase TextGroup.
        Elimina un texto del grupo de textos utilizando su identificador.
        Args:
            id (int): Identificador del texto a eliminar.
        """
    def removeText(self, id):
        self.alltext.pop(id)
    """ setupText de la clase TextGroup.
        Configura los textos iniciales del juego, incluyendo el puntaje, nivel,
        mensajes de estado (listo, pausado, game over) y sus posiciones.
        """
    def setupText(self):
        size = TILEHEIGHT
        self.alltext[SCORETXT] = Text("0".zfill(8), WHITE, 0, TILEHEIGHT, size)
        self.alltext[LEVELTXT] = Text(str(1).zfill(3), WHITE, 23*TILEWIDTH, TILEHEIGHT, size)
        self.alltext[READYTXT] = Text("READY!", YELLOW, 11.25*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[PAUSETXT] = Text("PAUSED!", YELLOW, 10.625*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[GAMEOVERTXT] = Text("GAMEOVER!", YELLOW, 10*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.addText("SCORE", WHITE, 0, 0, size)
        self.addText("LEVEL", WHITE, 23*TILEWIDTH, 0, size)
    """ metodo update de la clase TextGroup.
        Actualiza todos los textos en el grupo y verifica si alguno debe ser destruido.
        Args:
            dt (float): Delta time para el temporizador.
        """
    def update(self, dt):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.removeText(tkey)
    """ metodo showText de la clase TextGroup.
        Muestra un texto específico en la pantalla utilizando su identificador.
        Args:
            id (int): Identificador del texto a mostrar.
        """
    def showText(self, id):
        self.hideText()
        self.alltext[id].visible = True
    """ metodo hideText de la clase TextGroup.
        Oculta todos los textos en el grupo, excepto el texto de puntaje y nivel.
        """
    def hideText(self):
        self.alltext[READYTXT].visible = False
        self.alltext[PAUSETXT].visible = False
        self.alltext[GAMEOVERTXT].visible = False

    """ metoodo updateScore de la clase TextGroup.
        Actualiza el puntaje mostrado en la pantalla.
        Args:
            score (int): Nuevo puntaje a mostrar.
        """
    def updateScore(self, score):
        self.updateText(SCORETXT, str(score).zfill(8))

    """ metodo updateLevel de la clase TextGroup.
        Actualiza el nivel mostrado en la pantalla.
        Args:
            level (int): Nuevo nivel a mostrar.
        """
    def updateLevel(self, level):
        self.updateText(LEVELTXT, str(level + 1).zfill(3))
    """ metodo updateText de la clase TextGroup.
        Actualiza el texto mostrado en la pantalla utilizando su identificador.
        Args:
            id (int): Identificador del texto a actualizar.
            value (str): Nuevo valor a mostrar.
        """
    def updateText(self, id, value):
        if id in self.alltext.keys():
            self.alltext[id].setText(value)
    """ metodo render de la clase TextGroup.    
        Dibuja todos los textos en la pantalla.
        Args:
            screen (pygame.Surface): Superficie de la pantalla donde se dibujan los textos.
        """
    def render(self, screen):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)
