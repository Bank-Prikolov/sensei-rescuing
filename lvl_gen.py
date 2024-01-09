import os
import sys
from load_image import load_image
from consts import *
from windows import *

toches = pygame.sprite.Group()
bgroup = pygame.sprite.Group()
platformgroup = pygame.sprite.Group()
characters = pygame.sprite.Group()
heropic = wai
if not fullscreen:
    screen = pygame.display.set_mode(size)
    fullscreen = 0
else:
    screen = pygame.display.set_mode(fullsize, pygame.FULLSCREEN)
    fullscreen = 1


class Pic(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, sprite, *group):
        sprite = load_image(sprite)
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
        self.top = top
        self.cell_size = cell_size

    def render(self, sc):
        toches.empty()
        platformgroup.empty()
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
                        self.cell_size, plat, platformgroup)
                else:
                    pass
        toches.draw(sc)
        platformgroup.draw(sc)

    def get_cell(self, mouse_pos):
        if self.left * k < mouse_pos[0] < self.left * k + (self.cell_size * len(self.board[0]) * k) and \
                self.top * k < mouse_pos[1] < self.top * k + (self.cell_size * len(self.board)) * k:
            return int((mouse_pos[0] - 10) / self.cell_size), int((mouse_pos[1] - 10) / self.cell_size)
        else:
            return None

    def get_size(self):
        return self.cell_size

    def get_start_pos(self):
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[y][x] == '@':
                    return otstupx * fullscreen + (20 + self.cell_size * x) * k ** fullscreen, otstupy * fullscreen + (
                                20 + self.cell_size * y) * k ** fullscreen


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


board = Board('pp_test_level.txt')
board.set_view(0, 0, 128)
start_coords = board.get_start_pos()
bg = Background(*size, 0, 0, k)


def generate_level(lvlnum):
    global board, screen, start_coords, bg
    if lvlnum == 1:
        level = lvl1
        # bground = 1
    else:
        level = lvl2
        # bground = 2
    bg = Background(*size, 0, 0, k)
    board = Board(level)
    board.set_view(otstupx * fullscreen, otstupy * fullscreen, 128 * k ** fullscreen)
    bgroup.update(*size, otstupx * fullscreen, otstupy * fullscreen, k ** fullscreen)
    start_coords = board.get_start_pos()


def otrisovka_urovnya():
    bgroup.draw(screen)
    characters.draw(screen)


def rescreen(fs):
    global screen, board, bgroup
    if fs:
        screen = pygame.display.set_mode(fullsize, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(size)
    board.set_view(otstupx * fs, otstupy * fs, 128 * k ** fs)
    bgroup.update(*size, otstupx * fs, otstupy * fs, k ** fs)


def updater():
    global bgroup, screen, board
    bgroup.draw(screen)
    board.render(screen)
