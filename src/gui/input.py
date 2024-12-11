import pygame

from theme import Theme
from utils import draw_border


class Input:
    def __init__(self, bounds, font, max_length, text_color=(255, 255, 255), bg_color=(0, 0, 0)):
        """Initialize a single-line text input."""
        self.bounds = pygame.Rect(bounds)
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.max_length = max_length

        self.text = ""
        self.cursor_pos = 0

        self.active = False  # Input box starts active by default

    def handle_event(self, event):
        """Handle keyboard events for the text input."""
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = self.text[: self.cursor_pos - 1] + self.text[self.cursor_pos :]
                    self.cursor_pos -= 1
            elif event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.text):
                    self.text = self.text[: self.cursor_pos] + self.text[self.cursor_pos + 1 :]
            elif event.key == pygame.K_LEFT:
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1
            elif event.key == pygame.K_RIGHT:
                if self.cursor_pos < len(self.text):
                    self.cursor_pos += 1
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
            else:
                # Add new character if within max_length and the character is a digit
                if event.unicode.isdigit() and len(self.text) < self.max_length:
                    self.text = self.text[: self.cursor_pos] + event.unicode + self.text[self.cursor_pos :]
                    self.cursor_pos += 1
        elif event.type == pygame.MOUSEBUTTONUP and event.button == MOUSEBUTTONLEFT:
            # activate the input if it's been clicked
            if self.bounds.collidepoint(pygame.mouse.get_pos()):
                self.active = True
            else:
                self.active = False

    def draw(self, surface):
        """Render the text input box and its content."""
        # Draw the background rectangle
        pygame.draw.rect(surface, self.bg_color, self.bounds)

        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        surface.blit(
            text_surface, (self.bounds.x + 5, self.bounds.y + (self.bounds.height - text_surface.get_height()) // 2)
        )

        # Draw the cursor
        if self.active:
            cursor_x = self.font.size(self.text[: self.cursor_pos])[0] + self.bounds.x + 5
            cursor_y = self.bounds.y + (self.bounds.height - text_surface.get_height()) // 2
            pygame.draw.line(
                surface, self.text_color, (cursor_x, cursor_y), (cursor_x, cursor_y + text_surface.get_height()), 2
            )

        draw_border(surface, self.bounds, pygame.Color(Theme.BG_COLOR), width=8, depth="down", inner=False)

    def set_active(self, active):
        """Set whether the text box is active."""
        self.active = active
