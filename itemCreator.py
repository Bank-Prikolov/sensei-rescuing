import pygame
from processHelper import load_image


class Object:
    def __init__(self, x, y, width, height, image_path, no_active_image_path=None, image_path2=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

        if image_path2:
            self.image2 = load_image(image_path2)
            self.image2 = pygame.transform.scale(self.image2, (width, height))

        self.no_active_image = self.image
        if no_active_image_path:
            self.is_no_active = True
            self.no_active_image = load_image(no_active_image_path)
            self.no_active_image = pygame.transform.scale(self.no_active_image, (width, height))
        else:
            self.is_no_active = False

        self.rect = self.image.get_rect(topleft=(x, y))

    def check_passing(self, isActive=False):
        if isActive:
            self.is_no_active = False

    def draw(self, screen):
        current_image = self.image
        if self.is_no_active:
            current_image = self.no_active_image
        screen.blit(current_image, self.rect.topleft)

    def drawLanguage(self, screen, languageNow):
        current_image = self.image
        if languageNow == 'rus':
            current_image = self.image
        elif languageNow == 'eng':
            current_image = self.image2
        screen.blit(current_image, self.rect.topleft)


class Button:
    def __init__(self, x, y, width, height, image_path, hover_image_path=None, press_image_path=None, sound_path=None,
                 no_active_image_path=None, hero=None, image_get_path=None, hover_image_get_path=None,
                 press_image_get_path=None, hover_2_image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = load_image(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))

        self.hover_image_2 = self.image
        if hover_2_image_path:
            self.hover_image_2 = load_image(hover_2_image_path)
            self.hover_image_2 = pygame.transform.scale(self.hover_image_2, (width, height))

        self.press_image = self.image
        if press_image_path:
            self.press_image = load_image(press_image_path)
            self.press_image = pygame.transform.scale(self.press_image, (width, height))

        self.no_active_image = self.image
        if no_active_image_path:
            self.is_no_active = True
            self.no_active_image = load_image(no_active_image_path)
            self.no_active_image = pygame.transform.scale(self.no_active_image, (width, height))
        else:
            self.is_no_active = False

        if image_get_path:
            self.get_image = load_image(image_get_path)
            self.get_image = pygame.transform.scale(self.get_image, (width, height))

            self.hover_get_image = load_image(hover_image_get_path)
            self.hover_get_image = pygame.transform.scale(self.hover_get_image, (width, height))

            self.press_get_image = load_image(press_image_get_path)
            self.press_get_image = pygame.transform.scale(self.press_get_image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))

        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)

        self.is_hovered = False
        self.is_pressed = False
        self.is_slider = False

        self.hero = hero

    def check_passing(self, isActive=False):
        if isActive:
            self.is_no_active = False

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw_f11(self, screen, fs=None):
        if fs:
            if self.is_hovered:
                current_image = self.hover_image_2
            else:
                current_image = self.press_image
        else:
            if self.is_hovered:
                current_image = self.hover_image
            else:
                current_image = self.image
        screen.blit(current_image, self.rect.topleft)

    def draw_heroBtn(self, screen, hero, heroNow, isGetHero2):
        if heroNow == hero:
            current_image = self.press_image
        else:
            if isGetHero2:
                current_image = self.image
                if self.is_hovered:
                    current_image = self.hover_image
            else:
                current_image = self.get_image
                if self.is_hovered:
                    current_image = self.hover_get_image
                if self.is_pressed:
                    current_image = self.press_get_image
        screen.blit(current_image, self.rect.topleft)

    def draw(self, screen):
        current_image = self.image
        if self.is_no_active:
            current_image = self.no_active_image
        else:
            if self.is_hovered:
                current_image = self.hover_image
            if self.is_pressed:
                current_image = self.press_image
        screen.blit(current_image, self.rect.topleft)

    def handle_event(self, event, volS=1):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered and not self.is_no_active:
            self.is_pressed = True
            if self.sound:
                pygame.mixer.Sound.set_volume(self.sound, volS)
                self.sound.play()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_pressed:
            self.is_pressed = False
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

    def handle_event_slider(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered and not self.is_no_active:
            self.is_pressed = True
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=self))
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_pressed:
            self.is_pressed = False
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, button=self))


class Stars:
    def __init__(self, x, y, width, height, zeroStars_path, oneStar_path, twoStar_path, threeStar_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.zeroStar_image = load_image(zeroStars_path)
        self.zeroStar_image = pygame.transform.scale(self.zeroStar_image, (width, height))

        self.oneStar_image = load_image(oneStar_path)
        self.oneStar_image = pygame.transform.scale(self.oneStar_image, (width, height))

        self.twoStar_image = load_image(twoStar_path)
        self.twoStar_image = pygame.transform.scale(self.twoStar_image, (width, height))

        self.threeStar_image = load_image(threeStar_path)
        self.threeStar_image = pygame.transform.scale(self.threeStar_image, (width, height))

        self.rect = self.zeroStar_image.get_rect(topleft=(x, y))

    def draw(self, screen, record):
        current_image = load_image(r"objects\without text\stars-none-obj.png")
        if record == 0:
            current_image = self.zeroStar_image
        if record == 1:
            current_image = self.oneStar_image
        if record == 2:
            current_image = self.twoStar_image
        if record == 3:
            current_image = self.threeStar_image
        screen.blit(current_image, self.rect.topleft)
