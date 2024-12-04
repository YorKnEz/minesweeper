import pygame

from constants import FPS

pygame.init()
pygame.display.set_caption("Minesweeper")

size = width, height = 800, 800
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
running = True
dt = 0

font = pygame.font.Font("assets/mine-sweeper.ttf", 16)


def render(_):
    screen.fill("purple")
    pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    render(dt)

    dt = clock.tick(FPS) / 1000

pygame.quit()
