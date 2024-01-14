import pygame
from load_image import load_image


class Object:
    def __init__(self, x, y, width, height, image_path, no_active_image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

        self.no_active_image = self.image
        if no_active_image_path:
            self.no_active_image = load_image(no_active_image_path)
            self.no_active_image = pygame.transform.scale(self.no_active_image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))

        self.is_no_active = True

    def check_passing(self, isActive=False):
        if isActive:
            self.is_no_active = False

    def draw(self, screen):
        if self.is_no_active:
            current_image = self.no_active_image
        else:
            current_image = self.image
        screen.blit(current_image, self.rect.topleft)


class Button:
    def __init__(self, x, y, width, height, image_path, hover_image_path=None, press_image_path=None, sound_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

        self.hover_image = self.image
        self.push_image = self.image
        if hover_image_path:
            self.hover_image = load_image(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        if press_image_path:
            self.push_image = load_image(press_image_path)
            self.push_image = pygame.transform.scale(self.push_image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))

        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)

        self.is_hovered = False
        self.is_pushed = False

    def draw(self, screen):
        current_image = self.image
        if self.is_hovered:
            current_image = self.hover_image
        if self.is_pushed:
            current_image = self.push_image
        screen.blit(current_image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            self.is_pushed = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_pushed:
            self.is_pushed = False
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
