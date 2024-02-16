import os
import random
import sys
import pygame
import consts
import windows
import boss
import slonik
from processHelper import load_image

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

projectilespeed = []

heropic = consts.wai


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
        triggergroup.empty()
        toches.empty()
        platformgroup.empty()
        untouches.empty()
        finale.empty()
        changegroup.empty()
        thorngroup.empty()
        breakgroup.empty()
        anothertoches.empty()
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[y][x] == '0':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.floor, toches)
                elif self.board[y][x] == '#':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.wallx, toches)
                elif self.board[y][x] == '=':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.wally, toches)
                elif self.board[y][x] == '@':
                    pass
                elif self.board[y][x] == '_':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.plat, untouches)
                    boss.Pic(self.left + (self.cell_size * x) + self.cell_size // 4, self.top + (self.cell_size * y),
                             self.cell_size - self.cell_size // 2,
                             self.cell_size // 64, consts.placeholder, platformgroup)
                elif self.board[y][x] == 'F':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.finish, finale)
                elif self.board[y][x] == 'C':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.change, changegroup, untouches)
                elif self.board[y][x] == '^':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.thorn, thorngroup, anothertoches)
                elif self.board[y][x] == 'S':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.boss_door, changegroup, untouches)
                elif self.board[y][x] == '%':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.invis, breakgroup)
                elif self.board[y][x] == 't':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.trigger, triggergroup)
                elif self.board[y][x] == '&':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.horizon, toches)
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
            return int((mouse_pos[0] - board.left) // board.cell_size), int(
                (mouse_pos[1] - board.top) // board.cell_size)
        else:
            return None

    @staticmethod
    def pereres_slon(spisokslonikoff):
        global sloniks
        sp = spisokslonikoff
        for slon in sp:
            if not windows.fullscreen:
                new = ((slon.get_coords()[0] - windows.otstupx) // windows.k,
                       (slon.get_coords()[1] - windows.otstupy + 16) // windows.k)
            else:
                new = (windows.otstupx + slon.get_coords()[0] * windows.k,
                       (windows.otstupy + slon.get_coords()[1] - 18) * windows.k)
            a = slonik.Slonik(*new, windows.k ** windows.fullscreen, slon.act)
            a.hp = slon.hp
            a.looking_right = slon.looking_right
        sloniks = pygame.sprite.Group(list(sloniks)[len(sp) // 2:])
        sloniks.draw(windows.screen)

    @staticmethod
    def pereres_boss(spisokslonikoff):
        sp = spisokslonikoff
        for bs in sp:
            if not windows.fullscreen:
                new = ((bs.get_coords()[0] - windows.otstupx) // windows.k,
                       (bs.get_coords()[1] - windows.otstupy) // windows.k)
            else:
                new = (windows.otstupx + bs.get_coords()[0] * windows.k,
                       (windows.otstupy + bs.get_coords()[1] - 18) * windows.k)
            a = boss.Boss(*new, windows.k ** windows.fullscreen, bs.act)
            a.hp = bs.hp
        boss.boss_group = pygame.sprite.Group(list(boss.boss_group)[len(sp) // 2:])

    @staticmethod
    def rev_get_cell(mouse_pos):
        if 0 < mouse_pos[0] < len(board.board[0]) and \
                0 < mouse_pos[1] < len(board.board):
            return mouse_pos[0] * board.cell_size + board.left, mouse_pos[1] * board.cell_size + board.top
        else:
            return None

    def get_size(self):
        return self.cell_size

    def otris_slonik(self):
        sloniks.empty()
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if board.board[y][x] == 'e':
                    slonik.Slonik(self.left + (self.cell_size * x), self.top + (self.cell_size * y),
                                  windows.k ** windows.fullscreen, 0, lknrght=random.randint(0, 2),
                                  trtspd=12 * random.randint(0, 8))

    def otris_boss(self):
        boss.boss_group.empty()
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[y][x] == 'B':
                    boss.Boss(self.left + (self.cell_size * x),
                              self.top + (self.cell_size * y) - 44 * windows.k ** windows.fullscreen,
                              windows.k ** windows.fullscreen)

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
    image_bg = load_image(consts.game_bg)

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
    global board
    if lvlnum == 1:
        level = consts.lvl1
    elif lvlnum == 2:
        level = consts.lvl2
    elif lvlnum == 2.1:
        level = consts.lvl2_1
    elif lvlnum == 3:
        level = consts.lvl3
    elif lvlnum == 3:
        level = consts.lvl3
    elif lvlnum == 3.1:
        level = consts.lvl3_1
    else:
        level = consts.lvl3_2
    Background(*windows.size, 0, 0, windows.k)
    board = Board(level)
    board.set_view(windows.otstupx * windows.fullscreen,
                   -windows.otstupy * windows.k ** windows.fullscreen,
                   64 * windows.k ** windows.fullscreen)
    bgroup.update(*windows.size, windows.otstupx * windows.fullscreen, windows.otstupy * windows.fullscreen,
                  windows.k ** windows.fullscreen)
    board.otris_slonik()
    board.otris_boss()
    return board.get_start_end_pos()


def rescreen():
    global bgroup
    if windows.fullscreen:
        windows.screen = pygame.display.set_mode(windows.fullsize, pygame.FULLSCREEN)
    else:
        windows.screen = pygame.display.set_mode(windows.size)
    board.set_view(windows.otstupx * windows.fullscreen,
                   -windows.otstupy * windows.k ** windows.fullscreen,
                   64 * windows.k ** windows.fullscreen)
    bgroup.update(*windows.size, windows.otstupx * windows.fullscreen, windows.otstupy * windows.k * windows.fullscreen,
                  windows.k ** windows.fullscreen)


def updater():
    global bgroup, board
    bgroup.draw(windows.screen)
    board.render(windows.screen)


def get_shadow(x, y, w, h):
    shadowgroup.empty()
    sp = consts.shadow
    boss.Pic(x, y, w, h, sp, shadowgroup)


def remover(pos, block='.'):
    x, y = pos
    if board.board[int(y)][int(x)] != block:
        board.board[int(y)] = board.board[int(y)][:int(x)] + block + board.board[int(y)][int(x) + 1:]
        if block == '0':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.floor, toches)
            toches.draw(windows.screen)
        elif block == '#':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.wallx, toches)
            toches.draw(windows.screen)
        elif block == '=':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.wally, toches)
            toches.draw(windows.screen)
        elif block == '_':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.plat, untouches)
            boss.Pic(board.left + (board.cell_size * x) + board.cell_size // 4, board.top + (board.cell_size * y),
                     board.cell_size - board.cell_size // 2,
                     board.cell_size // 64, consts.placeholder, platformgroup)
            platformgroup.draw(windows.screen)
            untouches.draw(windows.screen)
        elif block == 'F':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.finish, finale)
            finale.draw(windows.screen)
        elif block == 'C':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.change, changegroup, untouches)
            untouches.draw(windows.screen)
        elif block == '^':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.thorn, thorngroup, anothertoches)
            anothertoches.draw(windows.screen)
        elif block == 'S':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.boss_door, changegroup, untouches)
            untouches.draw(windows.screen)
        elif block == '%':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.invis, breakgroup)
            breakgroup.draw(windows.screen)
        elif block == 't':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.trigger, triggergroup)
            triggergroup.draw(windows.screen)
        elif block == '&':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.horizon, toches)
            toches.draw(windows.screen)
        elif block == '.':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.shadow, shadowgroup)
            shadowgroup.draw(windows.screen)


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
