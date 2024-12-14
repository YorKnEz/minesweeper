import pygame


class WindowBase:
    """Window base class."""

    def __init__(self):
        pass

    def enter(self):
        """Method called by the Window Manager upon choosing a window as the current window."""
        raise NotImplementedError()

    def handle_event(self, event: pygame.event.Event):
        """Abstract event handler."""
        raise NotImplementedError()

    def draw(self, screen: pygame.Surface):
        """Abstract draw handler."""
        raise NotImplementedError()
