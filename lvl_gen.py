import pygame
import os
import sys
from load_image import load_image
from consts import *
import windows

all_sprites = list()
toches = pygame.sprite.Group()
bgroup = pygame.sprite.Group()
platformgroup = pygame.sprite.Group()
characters = pygame.sprite.Group()
untouches = pygame.sprite.Group()
finale = pygame.sprite.Group()
shadowgroup = pygame.sprite.Group()
all_sprites.append([toches, bgroup, platformgroup, untouches])

heropic = wai
if not windows.fullscreen:
    screen = pygame.display.set_mode(windows.size)
    windows.fullscreen = 0
else:
    screen = pygame.display.set_mode(windows.fullsize, pygame.FULLSCREEN)
    windows.fullscreen = 1


class Pic(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, sprite, *group):
        sprite = load_image(sprite)
        group = group
        super().__init__(*group)
        self.image = pygame.transform.scale(sprite, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Board:
    def __init__(self, txt):
        self.board = self.read_txt(txt)
        self.left = 10
        self.top = 10
        self.cell_size = 30

    @staticmethod
    def read_txt(txt_file):
        fullname = os.path.join(r'data\levels', txt_file)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        level = fullname
        lis = list(map(lambda w: w.rstrip('\n'), open(level).readlines()))
        return lis

    def set_view(self, left, top, cell_size):
        self.left = left
        self.cell_size = cell_size
        self.top = top

    def render(self, sc):
        toches.empty()
        platformgroup.empty()
        untouches.empty()
        finale.empty()
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[y][x] == '0':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, floor, toches)
                elif self.board[y][x] == '#':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, wallx, toches)
                elif self.board[y][x] == '=':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, wally, toches)
                elif self.board[y][x] == '@':
                    pass
                elif self.board[y][x] == '_':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, plat, untouches)
                    Pic(self.left + (self.cell_size * x) + self.cell_size // 4, self.top + (self.cell_size * y), self.cell_size - self.cell_size // 2,
                        self.cell_size // 64, placeholder, platformgroup)
                elif self.board[y][x] == 'F':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, finish, finale)
                else:
                    pass
        toches.draw(sc)
        platformgroup.draw(sc)
        untouches.draw(sc)
        finale.draw(sc)

    def get_cell(self, mouse_pos):
        if board.left < mouse_pos[0] < board.left + (
                board.cell_size * len(self.board[0])) and \
                board.top < mouse_pos[1] < board.top + (
                board.cell_size * len(self.board)):
            return (mouse_pos[0] - board.left) // board.cell_size, (mouse_pos[1] - board.top) // board.cell_size
        else:
            return None

    def get_size(self):
        return self.cell_size

    def get_start_end_pos(self):
        a = 0
        b = 0
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[y][x] == '@':
                    a = (self.left + (
                            10 * windows.k ** windows.fullscreen + self.cell_size * x),
                         (self.top + (
                            10 * windows.k ** windows.fullscreen + self.cell_size * y)))
                elif self.board[y][x] == 'F':
                    b = x, y
                if bool(a) and bool(b):
                    break
        return a, b


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


board = Board('test2.txt')


def generate_level(lvlnum):
    global board, screen
    if lvlnum == 1:
        level = lvl1
    elif lvlnum == 2:
        level = lvl2
    elif lvlnum == 2.1:
        level = lvl2_1
    elif lvlnum == 3:
        level = lvl3
    elif lvlnum == 3:
        level = lvl3
    elif lvlnum == 3.1:
        level = lvl3_1
    else:
        level = lvl3_2
    Background(*windows.size, 0, 0, windows.k)
    board = Board(level)
    board.set_view(windows.otstupx * windows.fullscreen,
                   - board.cell_size * abs(windows.fullscreen - 1) - windows.otstupy * windows.fullscreen,
                   64 * windows.k ** windows.fullscreen)
    bgroup.update(*windows.size, windows.otstupx * windows.fullscreen, windows.otstupy * windows.fullscreen,
                  windows.k ** windows.fullscreen)
    return board.get_start_end_pos()[0], board.get_start_end_pos()[1]


def otrisovka_urovnya():
    bgroup.draw(screen)
    characters.draw(screen)


def rescreen():
    global screen, board, bgroup
    if windows.fullscreen:
        screen = pygame.display.set_mode(windows.fullsize, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(windows.size)
    board.set_view(windows.otstupx * windows.fullscreen,
                   -windows.otstupy * windows.k ** windows.fullscreen,
                   64 * windows.k ** windows.fullscreen)
    bgroup.update(*windows.size, windows.otstupx * windows.fullscreen, windows.otstupy * windows.k * windows.fullscreen,
                  windows.k ** windows.fullscreen)


def updater():
    global bgroup, screen, board
    bgroup.draw(screen)
    board.render(screen)

def get_shadow(x, y, w, h):
    shadowgroup.empty()
    sp = shadow
    Pic(x, y, w, h, sp, shadowgroup)

