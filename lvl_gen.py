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
projectilesgroup = pygame.sprite.Group()
changegroup = pygame.sprite.Group()
thorngroup = pygame.sprite.Group()
breakgroup = pygame.sprite.Group()
triggergroup = pygame.sprite.Group()
sloniks = pygame.sprite.Group()
nmeprojectilesgroup = pygame.sprite.Group()
anothertoches = pygame.sprite.Group()

heropic = wai

if not windows.fullscreen:
    screen = pygame.display.set_mode(windows.size)
    windows.fullscreen = 0
else:
    screen = pygame.display.set_mode(windows.fullsize, pygame.FULLSCREEN)
    windows.fullscreen = 1


class Slonik(pygame.sprite.Sprite):
    pic = load_image(slonik)
    php = load_image(php)

    def __init__(self, x, y, koef, flip=True):
        super().__init__(sloniks)
        self.sprites = pygame.transform.scale(
            Slonik.pic, (Slonik.pic.get_width() // 2 * koef, Slonik.pic.get_height() // 2 * koef))
        # if flip:
        #     pygame.transform.flip(Slonik.pic, True, False)
        self.k = koef
        self.frames = []
        self.cut_sheet(self.sprites, koef)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.counter = 0

    def cut_sheet(self, sprites, koef):
        self.rect = pygame.Rect(0, 0, 64 * koef,
                                64 * koef)

        for i in range(sprites.get_height() // int(64 * koef)):
            frame_location = (0, self.rect.h * i)
            self.frames.append(sprites.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def update(self):
        self.image = self.frames[self.cur_frame]
        self.set_coords(*self.get_coords())
        if self.counter == 12:
            self.cur_frame = (self.cur_frame + 1) % 2
            self.counter = 0
        self.counter += 1

    def get_coords(self):
        return self.rect[0], self.rect[1]

    def set_coords(self, x, y):
        self.rect[:2] = [x, y]

    def get_size(self):
        return self.rect[2:4]

    def shoot(self):
        Pic(self.get_coords()[0] + self.get_size()[0] // 4,
            self.get_coords()[1] + self.get_size()[1] // 2,
            Slonik.php.get_width() // 2.5 * windows.k ** windows.fullscreen,
            Slonik.php.get_height() // 2.5 * windows.k ** windows.fullscreen, php,
            nmeprojectilesgroup)

    def set_angle(self, right=True):
        if right:
            for n in self.frames:
                pygame.transform.flip(n, True, False)


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
    def __init__(self, txt=None):
        if txt:
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
        changegroup.empty()
        thorngroup.empty()
        breakgroup.empty()
        anothertoches.empty()
        sloniks.empty()
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
                    Pic(self.left + (self.cell_size * x) + self.cell_size // 4, self.top + (self.cell_size * y),
                        self.cell_size - self.cell_size // 2,
                        self.cell_size // 64, placeholder, platformgroup)
                elif self.board[y][x] == 'F':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, finish, finale)
                elif self.board[y][x] == 'C':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, change, changegroup, untouches)
                elif self.board[y][x] == '^':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, thorn, thorngroup, anothertoches)
                elif self.board[y][x] == 'S':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, boss_door, changegroup, untouches)
                elif self.board[y][x] == '%':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, invis, breakgroup)
                elif self.board[y][x] == 't':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, trigger, triggergroup)
                elif self.board[y][x] == '&':
                    Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                        self.cell_size, horizon, toches)
                elif self.board[y][x] == 'e':
                    for z in range(len(board.board)):
                        if '@' in board.board[z]:
                            if board.board[z].find('@') - x > 0:
                                endth = True
                            else:
                                endth = False
                    Slonik(self.left + (self.cell_size * x), self.top + (self.cell_size * y),
                           windows.k ** windows.fullscreen, endth)
                else:
                    pass
        triggergroup.draw(sc)
        breakgroup.draw(sc)
        thorngroup.draw(sc)
        anothertoches.draw(sc)
        changegroup.draw(sc)
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

    def rev_get_cell(self, mouse_pos):
        if 0 < mouse_pos[0] < len(board.board[0]) and \
                0 < mouse_pos[1] < len(board.board):
            return mouse_pos[0] * board.cell_size + board.left, mouse_pos[1] * board.cell_size + board.top
        else:
            return None

    def get_size(self):
        return self.cell_size

    def get_start_end_pos(self):
        a = 0
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[y][x] == '@':
                    a = (self.left + (
                            10 * windows.k ** windows.fullscreen + self.cell_size * x),
                         (self.top + (
                                 10 * windows.k ** windows.fullscreen + self.cell_size * y)))
                    break
        return a


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


board = Board()


def generate_level(lvlnum):
    global screen, board
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
                   -windows.otstupy * windows.k ** windows.fullscreen,
                   64 * windows.k ** windows.fullscreen)
    bgroup.update(*windows.size, windows.otstupx * windows.fullscreen, windows.otstupy * windows.fullscreen,
                  windows.k ** windows.fullscreen)
    return board.get_start_end_pos()


def rescreen():
    global screen, bgroup
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


def remover(pos, block='.'):
    x, y = pos
    if board.board[int(y)][int(x)] != block:
        board.board[int(y)] = board.board[int(y)][:int(x)] + block + board.board[int(y)][int(x) + 1:]
        if block == '0':
            Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                board.cell_size, floor, toches)
            toches.draw(screen)
        elif block == '#':
            Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                board.cell_size, wallx, toches)
            toches.draw(screen)
        elif block == '=':
            Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                board.cell_size, wally, toches)
            toches.draw(screen)
        elif block == '_':
            Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                board.cell_size, plat, untouches)
            Pic(board.left + (board.cell_size * x) + board.cell_size // 4, board.top + (board.cell_size * y),
                board.cell_size - board.cell_size // 2,
                board.cell_size // 64, placeholder, platformgroup)
            platformgroup.draw(screen)
            untouches.draw(screen)
        elif block == 'F':
            Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                board.cell_size, finish, finale)
            finale.draw(screen)
        elif block == 'C':
            Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                board.cell_size, change, changegroup, untouches)
            untouches.draw(screen)
        elif block == '^':
            Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                board.cell_size, thorn, thorngroup, anothertoches)
            anothertoches.draw(screen)
        elif block == 'S':
            Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                board.cell_size, boss_door, changegroup, untouches)
            untouches.draw(screen)
        elif block == '%':
            Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                board.cell_size, invis, breakgroup)
            breakgroup.draw(screen)
        elif block == 't':
            Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                board.cell_size, trigger, triggergroup)
            triggergroup.draw(screen)
        elif block == '&':
            Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                board.cell_size, horizon, toches)
            toches.draw(screen)
        elif block == '.':
            Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                board.cell_size, shadow, shadowgroup)
            shadowgroup.draw(screen)


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
