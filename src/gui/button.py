import pygame

from constants import MOUSEBUTTONLEFT
from utils import draw_border


class Button:
    """The Button component.

    Instance variables:
        - bounds: The bounds of the button.
        - bg_color: The background color of the button.
        - text: The text of the button.
        - text_rect: The bounds of the text.
        - click_event: The event to emit upon clicking.

    Methods:
        - __init__: Initialize the input.
        - handle_event: Handle input events.
        - draw: Draw the input.
    """

    def __init__(self, bounds: pygame.Rect, bg_color, text, text_color, font: pygame.font.Font, click_event):
        """Initialize a button.

        Describe the look of the button and provide the event to post upon clicking it.

        :param bounds: The bounds of the button.
        :param bg_color: The background color of the button.
        :param text: The text of the button.
        :param text_color: The text color of the button.
        :param font: The font of the button.
        :param click_event: The event to emit upon clicking the button.
        """
        self.bounds = bounds.copy()
        self.bg_color = bg_color

        self.text = font.render(text, True, text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.bounds.center

        self.click_event = click_event

    def handle_event(self, event):
        """Event handler."""
        # check if the user clicked the button and fire the given event
        if (
                event.type == pygame.MOUSEBUTTONUP
                and event.button == MOUSEBUTTONLEFT
                and self.bounds.collidepoint(pygame.mouse.get_pos())
        ):
            pygame.event.post(pygame.event.Event(self.click_event))

    def draw(self, screen: pygame.Surface):
        """Draw handler."""
        pygame.draw.rect(screen, self.bg_color, self.bounds)
        screen.blit(self.text, self.text_rect)

        draw_border(screen, self.bounds, pygame.Color(self.bg_color), width=8, depth="up", inner=False)
