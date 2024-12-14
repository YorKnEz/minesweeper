"""Contains all the theme-related variables.

Classes:
    - Theme: The main theme-related variables.
"""
import pygame


class Theme:
    """The main theme-related variables."""

    BG_COLOR = "grey20"
    TEXT_COLOR = "white"

    TIMER_TEXT_COLOR = "firebrick1"
    TIMER_TEXT_COLOR_DISABLED = pygame.Color("#500000")
    TIMER_BG_COLOR = "black"

    REVEALED_BG_COLOR = "grey50"
    UNREVEALED_BG_COLOR = "grey30"
    REVEALED_BOMB_BG_COLOR = "darkred"

    CELL_COLORS = ["blue", "green", "red", "purple", "darkgoldenrod1", "deepskyblue", "deeppink1", "darkolivegreen1"]
