from constants import *
""" clase mainMode
    Representa el modo principal del juego Pacman, alternando entre los modos de dispersión y persecución."""
class MainMode(object):
    """ metodo constructor de la clase MainMode.
        Inicializa el temporizador y establece el modo inicial en dispersión.
        atributos:
            timer (float): Temporizador para controlar el tiempo en cada modo.
            time (int): Tiempo asignado para cada modo.
            mode (int): Modo actual (dispersión o persecución)."""
    def __init__(self):
        self.timer = 0
        self.scatter()

    """ metodo update de la clase MainMode.
        Actualiza el temporizador y cambia de modo si se ha alcanzado el tiempo asignado.
        Args:
            dt (float): Delta time para el temporizador.
        """
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()
    """ metodo scatter de la clase MainMode.
        Cambia el modo actual a dispersión y establece el tiempo asignado para este modo.
        attributes:
            mode (int): Modo actual (dispersión).
            time (int): Tiempo asignado para el modo de dispersión.
            timer (float): Temporizador para controlar el tiempo en el modo de dispersión."""
    def scatter(self):
        self.mode = SCATTER
        self.time = SCATTER_TIMELIMIT
        self.timer = 0
    """ metodo chase de la clase MainMode.
        Cambia el modo actual a persecución y establece el tiempo asignado para este modo.
        attributes:
            mode (int): Modo actual (persecución).
            time (int): Tiempo asignado para el modo de persecución.
            timer (float): Temporizador para controlar el tiempo en el modo de persecución."""
    def chase(self):
        self.mode = CHASE
        self.time = CHASE_TIMELIMIT
        self.timer = 0

""" clase ModeController
    Controla los modos de juego y la transición entre ellos."""
class ModeController(object):
    """ metodo constructor de la clase ModeController.
        Inicializa el temporizador y establece el modo inicial en dispersión.
        attributes:     
            timer (float): Temporizador para controlar el tiempo en cada modo.
            time (int): Tiempo asignado para cada modo.
            mainmode (MainMode): Instancia de la clase MainMode para controlar los modos.
            current (int): Modo actual (dispersión o persecución).
            entity (Entity): Entidad asociada al controlador de modos."""
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity 
    """ metodo update de la clase ModeController.
        Actualiza el temporizador y cambia de modo si se ha alcanzado el tiempo asignado.
        Si el modo actual es de dispersión o persecución, actualiza el modo principal.
        Si el modo actual es de carga, verifica si la entidad ha llegado al nodo de inicio.
        Args:
            dt (float): Delta time para el temporizador.
        """
    def update(self, dt):
        self.mainmode.update(dt)
        if self.current is FREIGHT:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.entity.normalMode()
                self.current = self.mainmode.mode
        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode

        if self.current is SPAWN:
            if self.entity.node == self.entity.spawnNode:
                self.entity.normalMode()
                self.current = self.mainmode.mode
    """ metodo setFreightMode de la clase ModeController.
        Cambia el modo actual a carga y establece el tiempo asignado para este modo.
        attributes:
            current (int): Modo actual (carga).
            timer (float): Temporizador para controlar el tiempo en el modo de carga.
            time (int): Tiempo asignado para el modo de carga."""
    def setFreightMode(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.timer = 0
    """ metodo setSpawnMode de la clase ModeController.
        Cambia el modo actual a carga y establece el tiempo asignado para este modo.
        attributes:
            current (int): Modo actual (carga).
            timer (float): Temporizador para controlar el tiempo en el modo de carga.
            time (int): Tiempo asignado para el modo de carga."""
    def setSpawnMode(self):
        if self.current is FREIGHT:
            self.current = SPAWN
