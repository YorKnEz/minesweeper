import pygame


class WindowBase:
    """Window base class."""

    def __init__(self):
        pass

    def handle_event(self, event: pygame.event.Event) -> "WindowBase":
        """Abastract event handler.

        It returns a WindowBase instance to allow window switching."""
        raise NotImplementedError()

    def draw(self, screen: pygame.Surface):
        """Abstract draw handler."""
        raise NotImplementedError()
