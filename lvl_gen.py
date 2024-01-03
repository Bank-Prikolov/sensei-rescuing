import pygame, os, sys
from load_image import load_image
from const import *


class Pic(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, sprite, *group):
        sprite = load_image(sprite)
        super().__init__(*group)
        self.image = pygame.transform.scale(sprite, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Board:
    def __init__(self, w, h, txt):
        self.width = w
        self.height = h
        self.board = self.read_txt(txt)
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def read_txt(self, txt_file):
        fullname = os.path.join('data\levels', txt_file)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        level = fullname
        lis = list(map(lambda w: w.rstrip('\n'), open(level).readlines()))
        return lis

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, sc):
        toches.empty()
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == '0':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, floor, toches)
                elif self.board[y][x] == '#':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, wallx, toches)
                else:
                    pass

        toches.draw(sc)

    def get_cell(self, mouse_pos, k):
        if self.left * k < mouse_pos[0] < self.left * k + (self.cell_size * self.width * k) and \
                self.top * k < mouse_pos[1] < self.top * k + (self.cell_size * self.height) * k:
            return int((mouse_pos[0] - 10) / self.cell_size), int((mouse_pos[1] - 10) / self.cell_size)
        else:
            return None

    def get_size(self):
        return self.cell_size


class Background(pygame.sprite.Sprite):
    image_bg = load_image(bg1)

    def __init__(self, w, h, left, top, koef):
        super().__init__(bgroup)
        self.image = pygame.transform.scale(Background.image_bg, (w * koef, h * koef))
        self.rect = self.image.get_rect()
        self.rect.x = left
        self.rect.y = top

    def update(self, w, h, left, top, koef):
        bgroup.empty()
        newground = Background(w, h, left, top, koef)
        return newground


toches = pygame.sprite.Group()
bgroup = pygame.sprite.Group()