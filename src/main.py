import pygame

from constants import FPS
from gui.windows.window import Window
from theme import Theme

pygame.init()
pygame.display.set_caption("Minesweeper")

size = width, height = 800, 800
screen = pygame.display.set_mode(size)

font = pygame.font.Font("assets/mine-sweeper.ttf", 16)

clock = pygame.time.Clock()
running = True
dt = 0

window = Window(width, height, font)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        window.handle_event(event)

    screen.fill(Theme.BG_COLOR)

    window.draw(screen)

    pygame.display.flip()

    dt = clock.tick(FPS) / 1000

pygame.quit()
