import pygame

import consts
import soundManager
import spriteGroups


class AnimatedError(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(spriteGroups.animatedError)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.x = x
        self.y = y
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.counter = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.counter == 60:
            self.counter = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.counter += 1


class AnimatedDialogue(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(spriteGroups.animatedDialogue)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.x = x
        self.y = y
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.counter = 0
        self.tmp = 0
        self.talksWithHleb = [13, 39, 105, 145, 195, 206, 255, 333, 406, 444, 497, 531, 548, 610, 635, 663, 728, 784,
                              810, 827, 854, 864]
        self.talksWithBossGreeting = [13, 38, 52, 78]
        self.talksWithBossEnding = [27, 41, 73, 123, 159, 170]
        consts.nextFrames = True

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def dialogue_update(self, whatCS):
        if consts.nextFrames:
            if self.counter == 5:
                soundManager.talking_sound()
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.counter = 0
            self.counter += 1
        if consts.nextFrames:
            if whatCS == 'hg':
                if self.cur_frame == self.talksWithHleb[self.tmp]:
                    self.counter = 5
                    self.tmp += 1
                    consts.nextFrames = False
            if whatCS == 'bg':
                if self.cur_frame == self.talksWithBossGreeting[self.tmp]:
                    self.counter = 5
                    self.tmp += 1
                    consts.nextFrames = False
            if whatCS == 'be':
                if self.cur_frame == self.talksWithBossEnding[self.tmp]:
                    self.counter = 5
                    self.tmp += 1
                    consts.nextFrames = False
