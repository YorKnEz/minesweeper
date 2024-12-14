"""Provides a variety of utility functions.

Functions:
    - clamp: Clamps a value in a fixed range.
    - adjust_color: Lightens/Darkens a color by a factor.
    - draw_border: Draw a minesweeper-styled border around a rectangle.
"""
import pygame


def clamp(x, a, b):
    """Clamp value x in the interval [a, b].

    It is assumed a <= b.

    :param x: The value to clamp.
    :param a: The lower bound.
    :param b: The upper bound.
    :return: The clamped value.
    """
    return max(a, min(b, x))


def adjust_color(color, factor):
    """Adjust the color by a given factor.

    Typically used for getting a slightly lighter/darker tone of a given color.

    :param color: The color to adjust.
    :param factor: The factor to adjust.
    :return: The adjusted color.
    """
    return tuple(min(255, max(0, int(c * factor))) for c in color)


def draw_border(
        surface: pygame.Surface, bounds: pygame.Rect, border_color: pygame.Color, width=1, depth="up", inner=False
):
    """Draw a minesweeper-styled border around a given rect.

    :param surface: The surface to draw on.
    :param bounds: The bounds around which to draw the border.
    :param border_color: The color of the border.
    :param width: The width of the border (default 1).
    :param depth: The effect of the border: if "up", then the border will look as if raises the level of the rect,
    otherwise it will look as if it lowers the level of the rect (default "up").
    :param inner: Whether the border is inner or outer (i.e. if the border is drawn inside or outside the bounds of the
    rect) (default False).
    """

    lighter_color = adjust_color(border_color, 1.3 if depth == "up" else 0.7)
    darker_color = adjust_color(border_color, 0.7 if depth == "up" else 1.3)

    outer_ring = pygame.Rect(
        bounds.left - (1 - inner) * width,
        bounds.top - (1 - inner) * width,
        bounds.width - 1 + (1 - inner) * 2 * width,
        bounds.height - 1 + (1 - inner) * 2 * width,
    )

    inner_ring = pygame.Rect(
        bounds.left - 1 + inner * width,
        bounds.top - 1 + inner * width,
        bounds.width + 1 - inner * 2 * width,
        bounds.height + 1 - inner * 2 * width,
    )

    # top border
    pygame.draw.polygon(
        surface, lighter_color, [outer_ring.topleft, outer_ring.topright, inner_ring.topright, inner_ring.topleft]
    )

    # right border
    pygame.draw.polygon(
        surface,
        darker_color,
        [
            outer_ring.topright,
            outer_ring.bottomright,
            inner_ring.bottomright,
            inner_ring.topright,
        ],
    )

    # bottom border
    pygame.draw.polygon(
        surface,
        darker_color,
        [
            outer_ring.bottomright,
            outer_ring.bottomleft,
            inner_ring.bottomleft,
            inner_ring.bottomright,
        ],
    )

    # left border
    pygame.draw.polygon(
        surface, lighter_color, [outer_ring.bottomleft, outer_ring.topleft, inner_ring.topleft, inner_ring.bottomleft]
    )
