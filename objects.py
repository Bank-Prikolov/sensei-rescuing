import pygame
from load_image import *


class Object:
    def __init__(self, x, y, width, height, image_path, hover_image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = load_image(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.is_hovered = False

    def draw(self, screen):
        current_image = self.image
        screen.blit(current_image, self.rect.topleft)

    def check_passing(self, checkPassing):
        if checkPassing:
            self.is_hovered = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
