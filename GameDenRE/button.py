import pygame

class Button:
    def __init__(self, rect: pygame.Rect):
        self.rect = rect

    def is_hovering(self, mouse_position: tuple) -> bool:
        """If the position inputed is on top of the button, it'll return True"""
        return self.rect.collidepoint(mouse_position)

    def pygame_render(self, surface: pygame.Surface, image_path: str):
        image = pygame.image.load(image)
        image = pygame.transform.scale(
            self.image,
            (
                self.image.get_width() * self.render_size,
                self.image.get_height() * self.render_size,
            ),
        )
        surface.blit(image, (self.rect.x, self.rect.y))