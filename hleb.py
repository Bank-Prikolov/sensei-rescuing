import pygame
from processHelper import load_image


class HlebPic(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, sprite, *group, koef):
        self.sprites = pygame.transform.scale(load_image(sprite),
                                              (w, h * 2))
        super().__init__(*group)
        self.counter = 0
        self.frames = self.cut_sheet(self.sprites, koef)
        self.image = self.frames[self.counter]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.wait = 0

    def cut_sheet(self, sprites, koef):
        self.rect = pygame.Rect(0, 0, 64 * koef,
                                64 * koef)
        plist = list()
        for i in range(sprites.get_height() // int(64 * koef)):
            frame_location = (0, self.rect.h * i)
            plist.append(sprites.subsurface(pygame.Rect(
                frame_location, self.rect.size)))
        return plist

    def update(self):
        if self.wait % 12 == 0:
            self.counter = (self.counter + 1) % len(self.frames)
            self.image = self.frames[self.counter]
        self.wait += 1
