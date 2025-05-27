"""clase Pause
    Controla la pausa del juego y el tiempo de pausa.
    
    Atributos:
        paused (bool): Indica si el juego está en pausa.
        timer (float): Temporizador para controlar el tiempo de pausa.
        pauseTime (float): Tiempo asignado para la pausa.
        func (callable): Función a ejecutar al finalizar la pausa.
"""
class Pause(object):
    """ metodo constructor de la clase Pause.
        Inicializa el estado de pausa, temporizador y función a ejecutar al finalizar la pausa.
        
        Args:
            paused (bool): Indica si el juego está en pausa (por defecto es False).
    """
    def __init__(self, paused=False):
        self.paused = paused
        self.timer = 0
        self.pauseTime = None
        self.func = None
    """ metodo update de la clase Pause.
        Actualiza el temporizador y verifica si se ha alcanzado el tiempo de pausa.
        Si es así, reinicia el temporizador, desactiva la pausa y devuelve la función a ejecutar.
        
        Args:
            dt (float): Delta time para el temporizador.
        
        Returns:
            callable: Función a ejecutar al finalizar la pausa (si corresponde).
    """
    def update(self, dt):
        if self.pauseTime is not None:
            self.timer += dt
            if self.timer >= self.pauseTime:
                self.timer = 0
                self.paused = False
                self.pauseTime = None
                return self.func
        return None
    """ metodo setPause de la clase Pause.
        Establece el estado de pausa, el tiempo de pausa y la función a ejecutar al finalizar la pausa.
        
        Args:
            playerPaused (bool): Indica si el juego está en pausa (por defecto es False).
            pauseTime (float): Tiempo asignado para la pausa.
            func (callable): Función a ejecutar al finalizar la pausa.
    """
    def setPause(self, playerPaused=False, pauseTime=None, func=None):
        self.timer = 0
        self.func = func
        self.pauseTime = pauseTime
        self.flip()
    """flip
        Cambia el estado de pausa del juego.
        
        Cambia el estado de pausa del juego al valor opuesto (de pausado a no pausado o viceversa).
    """
    def flip(self):
        self.paused = not self.paused