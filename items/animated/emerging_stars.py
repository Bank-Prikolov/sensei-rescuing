import pygame
import spriteGroups
from managing import sounds_managing


class AnimatedStars(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(spriteGroups.animatedStars)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.delay = 0
        self.counter = 0
        self.sound = 1

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, record):
        if self.delay == 20:
            if self.cur_frame != record * 2:
                if self.counter == 13:
                    self.counter = 0
                    if self.sound % 2 != 0:
                        soundManager.star_sound()
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                    self.image = self.frames[self.cur_frame]
                    self.sound += 1
                self.counter += 1
        else:
            self.delay += 1
