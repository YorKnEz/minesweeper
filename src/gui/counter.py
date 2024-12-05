import pygame

from utils import draw_border


class Counter:
    TEXT_BG_COLOR = pygame.Color("#500000")
    TEXT_COLOR = "firebrick1"
    BG_COLOR = "black"

    def __init__(self, bounds: pygame.Rect, count: int):
        """Initialize the counter.

        If the `count` is zero, then the counter is rendered as disabled.
        """
        self.font = pygame.font.Font("assets/seven-segment.ttf", 48)

        self.bounds = bounds.copy()
        self.count = count
        self.disabled = self.count == 0

        self._update_text()

    def _update_text(self):
        self.bg_text = self.font.render("888", True, Counter.TEXT_BG_COLOR)
        if not self.disabled:
            self.text = self.font.render(f"{self.count:03}", True, Counter.TEXT_COLOR)

        self.text_rect = self.bg_text.get_rect()
        self.text_rect.height //= 2
        # this font is weird so random constants were added so that i can make sure they're properly aligned
        self.text_rect.center = (self.bounds.centerx + 3, self.bounds.centery - self.text_rect.height - 1)

    def handle_event(self, event):
        """Event handler.

        Raises `NotImplementedError` since the derived classes must implement it.
        """
        raise NotImplementedError()

    def draw(self, screen: pygame.Surface):
        """Draw the counter on the screen."""
        pygame.draw.rect(screen, Counter.BG_COLOR, self.bounds)
        draw_border(screen, self.bounds, pygame.Color("grey20"), width=8, depth="down")
        screen.blit(self.bg_text, self.text_rect)
        if not self.disabled:
            screen.blit(self.text, self.text_rect)
