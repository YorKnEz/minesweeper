import pygame

FPS = 60

BOARD_REVEAL = pygame.USEREVENT + 1
BOARD_FLAG = pygame.USEREVENT + 2
TIMER_TICK = pygame.USEREVENT + 3
BOARD_FLAG_PLACED = pygame.USEREVENT + 4
BOARD_FLAG_REMOVED = pygame.USEREVENT + 5

GAME_START = pygame.USEREVENT + 6
GAME_RESTART = pygame.USEREVENT + 7
GAME_HOME = pygame.USEREVENT + 8
GAME_OVER = pygame.USEREVENT + 9

BOARD_UP = pygame.USEREVENT + 10
BOARD_DOWN = pygame.USEREVENT + 11
BOARD_LEFT = pygame.USEREVENT + 12
BOARD_RIGHT = pygame.USEREVENT + 13

MOUSEBUTTONLEFT = 1
MOUSEBUTTONMIDDLE = 2
MOUSEBUTTONRIGHT = 3
