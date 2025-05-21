    
""" metodo checkEvents de la clase Game.
        Verifica los eventos del juego, como el cierre de la ventana o la pausa del juego.
        Si se presiona la tecla de espacio, alterna entre pausar y reanudar el juego.
        """
from pygame import K_SPACE, KEYDOWN, QUIT
import pygame


def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            #newtext::self.textgroup.hideText()
                            self.showEntities()
                        else:
                            #newtext::self.textgroup.showText(PAUSETXT)
                            self.hideEntities()