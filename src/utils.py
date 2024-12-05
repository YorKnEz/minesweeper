import pygame


def clamp(x, a, b):
    """Clamp value x in interval [a, b].

    It is assumed a <= b.
    """
    return max(a, min(b, x))


def draw_border(
    surface: pygame.Surface, bounds: pygame.Rect, border_color: pygame.Color, width=1, depth="up", inner=False
):
    """Draw a minesweeper-styled border around a given rect.

    Depth parameter can be either "up" or "down" specifying the effect the border will have.
    """

    def adjust_color(color, factor):
        return tuple(min(255, max(0, int(c * factor))) for c in color)

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
