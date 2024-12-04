import pygame

from constants import BOARD_FLAG_EVENT, BOARD_REVEAL_EVENT, FPS
from gui import Board
from state import GameState

pygame.init()
pygame.display.set_caption("Minesweeper")

size = width, height = 800, 800
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
running = True
dt = 0

font = pygame.font.Font("assets/mine-sweeper.ttf", 16)

state = GameState(size=(32, 32))

board_bounds = pygame.Rect((width - 512) / 2, 64 + (height - 512) / 2, 512, 512)

board = Board(board_bounds, state, font)


def render(_):
    screen.fill("grey20")

    board.draw(screen)

    pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == BOARD_REVEAL_EVENT:
            l, c = event.dict.values()
            state = state.reveal_zone(l, c)
            board.update(state)
        elif event.type == BOARD_FLAG_EVENT:
            l, c = event.dict.values()
            state = state.flag_zone(l, c)
            board.update(state)

        board.handle_event(event)

    if state.is_over():
        pass


    render(dt)

    dt = clock.tick(FPS) / 1000

pygame.quit()
