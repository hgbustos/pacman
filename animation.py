from constants import *
""" class Animator
    Representa un animador que gestiona la animación de sprites en el juego.
    
    Atributos:
        frames (list): Lista de imágenes para la animación.
        current_frame (int): Índice de la imagen actual en la animación.
        speed (int): Velocidad de la animación (frames por segundo).
        loop (bool): Indica si la animación debe repetirse al finalizar.
        dt (float): Delta time acumulado para controlar el tiempo entre frames.
        finished (bool): Indica si la animación ha terminado.
    """
class Animator(object):
    """ metodo constructor de la clase Animator.
        Inicializa los atributos del animador, incluyendo la lista de frames, velocidad,
        bucle y estado de finalización.
        
        Args:
            frames (list): Lista de imágenes para la animación.
            speed (int): Velocidad de la animación (frames por segundo).
            loop (bool): Indica si la animación debe repetirse al finalizar.
    """
    def __init__(self, frames=[], speed=20, loop=True):
        self.frames = frames
        self.current_frame = 0
        self.speed = speed
        self.loop = loop
        self.dt = 0
        self.finished = False
    """ metodo reset de la clase Animator.
        Reinicia la animación estableciendo el índice del frame actual en 0
        y el estado de finalización en False.
    """
    def reset(self):
        self.current_frame = 0
        self.finished = False
    """ metodo update de la clase Animator.
        Actualiza la animación en función del tiempo transcurrido (dt).
        Si la animación ha terminado y el bucle está habilitado, reinicia la animación.
        
        Args:
            dt (float): Delta time para la actualización de la animación.
        
        Returns:
            Image: Imagen actual de la animación.
    """
    def update(self, dt):
        if not self.finished:
            self.nextFrame(dt)
        if self.current_frame == len(self.frames):
            if self.loop:
                self.current_frame = 0
            else:
                self.finished = True
                self.current_frame -= 1
   
        return self.frames[self.current_frame]
    """ metodo nextFrame de la clase Animator.
        Avanza al siguiente frame de la animación en función del tiempo transcurrido (dt).
        Si se ha alcanzado el tiempo necesario para avanzar, incrementa el índice del frame actual.
        
        Args:
            dt (float): Delta time para la actualización de la animación.
    """
    def nextFrame(self, dt):
        self.dt += dt
        if self.dt >= (1.0 / self.speed):
            self.current_frame += 1
            self.dt = 0





                        
