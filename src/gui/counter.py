import pygame

from theme import Theme
from utils import draw_border


class Counter:
    """Generic counter component.

    Instance variables:
        - font: The font of the counter. Uses seven-segment.
        - bounds: The bounds of the counter.
        - count: The value of the counter.
        - disabled: Whether the counter is disabled.

    Methods:
        - __init__: Construct a Counter instance.
        - _update_text: Update the display value of the counter.
    """
    def __init__(self, bounds: pygame.Rect, count: int):
        """Initialize the counter.

        If the `count` is zero, then the counter is rendered as disabled.

        :param bounds: The bounds of the counter.
        :param count: The value of the counter.
        """
        self.font = pygame.font.Font("assets/seven-segment.ttf", 48)

        self.bounds = bounds.copy()
        self.count = count
        self.disabled = self.count == 0

        self._update_text()

    def _update_text(self):
        """Update the display value of the counter.

        It prepares two texts, the background text, 888, and the foreground text which is the actual value of the
        counter.
        If the counter is disabled, the foreground text is omitted.
        """
        self.bg_text = self.font.render("888", True, Theme.TIMER_TEXT_COLOR_DISABLED)
        if not self.disabled:
            self.text = self.font.render(f"{self.count:03}", True, Theme.TIMER_TEXT_COLOR)

        self.text_rect = self.bg_text.get_rect()
        self.text_rect.height //= 2
        # this font is weird so random constants were added so that I can make sure they're properly aligned
        self.text_rect.center = (self.bounds.centerx + 3, self.bounds.centery - self.text_rect.height - 1)

    def handle_event(self, event):
        """Event handler.

        :raises NotImplementedError: The derived classes must implement it.
        """
        raise NotImplementedError()

    def draw(self, surface: pygame.Surface):
        """Draw the counter on the screen.

        If the counter is disabled, the foreground text is omitted."""
        pygame.draw.rect(surface, Theme.TIMER_BG_COLOR, self.bounds)
        draw_border(surface, self.bounds, pygame.Color(Theme.BG_COLOR), width=8, depth="down")
        surface.blit(self.bg_text, self.text_rect)
        if not self.disabled:
            surface.blit(self.text, self.text_rect)
