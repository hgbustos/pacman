# mainMenu.py
import pygame
import sys

def main_menu(screen):
    import pygame
    import sys
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    font = pygame.font.SysFont(None, 40)
    WIDTH, HEIGHT = screen.get_size()
    enter_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 50)
    exit_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50)
    options = ["Entrar", "Salir"]
    selected = 0

    def draw_button(rect, text, selected):
        color = (150, 150, 255) if selected else GRAY
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        label = font.render(text, True, BLACK)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    while True:
        screen.fill(YELLOW)
        draw_button(enter_button, "Entrar", selected == 0)
        draw_button(exit_button, "Salir", selected == 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if enter_button.collidepoint(event.pos):
                    return
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_LEFT]:
                    selected = (selected - 1) % 2
                elif event.key in [pygame.K_DOWN, pygame.K_RIGHT]:
                    selected = (selected + 1) % 2
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected == 0:
                        return
                    else:
                        pygame.quit()
                        sys.exit()
        pygame.display.flip()

def game_over_menu(screen):
    import pygame
    import sys
    font = pygame.font.SysFont(None, 50)
    button_font = pygame.font.SysFont(None, 30)
    WIDTH, HEIGHT = screen.get_size()
    continue_button = pygame.Rect(WIDTH//2 - 120, HEIGHT//2, 110, 50)
    exit_button = pygame.Rect(WIDTH//2 + 10, HEIGHT//2, 110, 50)
    options = ["Continuar", "Salir"]
    selected = 0
    while True:
        screen.fill((0, 0, 0))
        label = font.render("GAME OVER", True, (255, 255, 0))
        screen.blit(label, (WIDTH//2 - label.get_width()//2, HEIGHT//2 - 100))
        # Dibuja botones con selección
        color1 = (150, 150, 255) if selected == 0 else (200, 200, 200)
        color2 = (150, 150, 255) if selected == 1 else (200, 200, 200)
        pygame.draw.rect(screen, color1, continue_button)
        pygame.draw.rect(screen, color2, exit_button)
        pygame.draw.rect(screen, (0, 0, 0), continue_button, 2)
        pygame.draw.rect(screen, (0, 0, 0), exit_button, 2)
        cont_label = button_font.render("Continuar", True, (0, 0, 0))
        exit_label = button_font.render("Salir", True, (0, 0, 0))
        screen.blit(cont_label, (continue_button.x + 5, continue_button.y + 5))
        screen.blit(exit_label, (exit_button.x + 20, exit_button.y + 5))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    return "continue"
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_UP]:
                    selected = (selected - 1) % 2
                elif event.key in [pygame.K_RIGHT, pygame.K_DOWN]:
                    selected = (selected + 1) % 2
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected == 0:
                        return "continue"
                    else:
                        pygame.quit()
                        sys.exit()
        pygame.display.flip()