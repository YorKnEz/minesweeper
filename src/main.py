import pygame

from constants import BOARD_FLAG, BOARD_REVEAL, FPS, TIMER_TICK
from gui import Board, BombCounter, Timer
from state import GameState
from utils import draw_border

pygame.init()
pygame.display.set_caption("Minesweeper")

size = width, height = 800, 800
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
running = True
dt = 0

font = pygame.font.Font("assets/mine-sweeper.ttf", 16)

state = GameState(size=(16, 16), max_bombs=32, time=100)

board_bounds = pygame.Rect((width - 512) / 2, 64 + (height - 512) / 2, 512, 512)
board = Board(board_bounds, state, font)

timer_bounds = pygame.Rect(board_bounds.left, board_bounds.top - 96, 100, 64)
timer = Timer(timer_bounds, state)

bomb_cnt_bounds = pygame.Rect(board_bounds.right - 100, board_bounds.top - 96, 100, 64)
bomb_cnt = BombCounter(bomb_cnt_bounds, state)


def render(_):
    screen.fill("grey20")

    board.draw(screen)
    timer.draw(screen)
    bomb_cnt.draw(screen)

    draw_border(screen, screen.get_rect(), pygame.Color("grey20"), width=8, depth="up", inner=True)
    pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == BOARD_REVEAL:
            l, c = event.dict.values()
            state = state.reveal_zone(l, c)
            board.update(state)
        elif event.type == BOARD_FLAG:
            l, c = event.dict.values()
            state = state.flag_zone(l, c)
            board.update(state)
        elif event.type == TIMER_TICK:
            state = state.timer_ticked()

        board.handle_event(event)
        timer.handle_event(event)
        bomb_cnt.handle_event(event)

    if state.is_over():
        pass

    render(dt)

    dt = clock.tick(FPS) / 1000

pygame.quit()
