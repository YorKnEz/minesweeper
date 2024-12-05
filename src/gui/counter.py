import pygame


class Counter:
    TEXT_BG_COLOR = pygame.Color("#500000")
    TEXT_COLOR = "firebrick1"
    BG_COLOR = "black"

    def __init__(self, bounds: pygame.Rect, count: int):
        self.font = pygame.font.Font("assets/seven-segment.ttf", 48)

        self.bounds = bounds.copy()
        self.count = count

        self._update_text()

    def _update_text(self):
        self.bg_text = self.font.render("888", True, Counter.TEXT_BG_COLOR)
        self.text = self.font.render(f"{self.count:03}", True, Counter.TEXT_COLOR)

        self.text_rect = self.bg_text.get_rect()
        self.text_rect.height //= 2
        # this font is weird so random constants were added so that i can make sure they're properly aligned
        self.text_rect.center = (self.bounds.centerx + 3, self.bounds.centery - self.text_rect.height - 1)

    def handle_event(self, event):
        raise NotImplementedError()

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, Counter.BG_COLOR, self.bounds)
        screen.blit(self.bg_text, self.text_rect)
        screen.blit(self.text, self.text_rect)

