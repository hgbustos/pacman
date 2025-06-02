def main_menu():
    """
    Muestra un menú de inicio con dos botones: 'Entrar' y 'Salir'.
    Al hacer clic en 'Entrar', se imprime un mensaje y se puede iniciar el juego.
    Al hacer clic en 'Salir', se cierra el programa.
    """ 

import pygame
import sys

# Inicializar Pygame
pygame.init()
WIDTH, HEIGHT = 600, 800
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menú de Inicio - Pacman")

# Colores
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fuente
font = pygame.font.SysFont(None, 40)

# Crear botones como rectángulos
enter_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 50)
exit_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50)

def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)  # borde
    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def main_menu():
    while True:
        screen.fill(YELLOW)

        # Dibujar botones
        draw_button(enter_button, "Entrar")
        draw_button(exit_button, "Salir")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if enter_button.collidepoint(event.pos):
                    print("Entrar al juego...")
                    return  # aquí terminarías el menú y comenzarías el juego
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()