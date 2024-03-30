import os
import random
import sys
import pygame
import consts
import windows
import boss
import slonik
import hleb
import spriteGroups
from processHelper import load_image


class UltimateAnimPic(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, sprite, *group, speed=2, n=1):
        self.sprites = pygame.transform.scale(load_image(sprite),
                                              (w * n, h))
        super().__init__(*group)
        self.counter = 0
        self.width = w
        self.height = h
        self.frames = self.cut_sheet(self.sprites)
        self.image = self.frames[self.counter]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.waitmark = speed
        self.wait = 0

    def cut_sheet(self, sprites):
        self.rect = pygame.Rect(0, 0, self.width,
                                self.height)
        plist = list()
        for i in range(sprites.get_width() // int(self.width)):
            frame_location = (self.width * i, 0)
            plist.append(sprites.subsurface(pygame.Rect(
                frame_location, self.rect.size)))
        return plist

    def update(self):
        get_shadow(*self.rect)
        spriteGroups.shadowgroup.draw(windows.screen)
        if self.wait % self.waitmark == 0:
            self.counter = (self.counter + 1) % len(self.frames)
            self.image = self.frames[self.counter]
        self.wait += 1


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
        spriteGroups.xwalls.empty()
        spriteGroups.ywalls.empty()
        spriteGroups.triggergroup.empty()
        spriteGroups.toches.empty()
        spriteGroups.platformgroup.empty()
        spriteGroups.untouches.empty()
        spriteGroups.finale.empty()
        spriteGroups.changegroup.empty()
        spriteGroups.thorngroup.empty()
        spriteGroups.breakgroup.empty()
        spriteGroups.anothertoches.empty()
        spriteGroups.hleb.empty()
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[y][x] == '0':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.floor, spriteGroups.toches)
                elif self.board[y][x] == '#':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.wallx, spriteGroups.toches, spriteGroups.ywalls)
                elif self.board[y][x] == '=':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.wally, spriteGroups.toches, spriteGroups.xwalls)
                elif self.board[y][x] == '@':
                    pass
                elif self.board[y][x] == '_':
                    UltimateAnimPic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                                    self.cell_size, consts.plat, spriteGroups.untouches, n=4, speed=6)
                    boss.Pic(self.left + (self.cell_size * x) + self.cell_size // 4, self.top + (self.cell_size * y),
                             self.cell_size - self.cell_size // 2,
                             self.cell_size // 64, consts.placeholder, spriteGroups.platformgroup)
                elif self.board[y][x] == 'F':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.finish, spriteGroups.finale)
                elif self.board[y][x] == 'f':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.closed, spriteGroups.untouches)
                elif self.board[y][x] == 'C':
                    UltimateAnimPic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                                    self.cell_size, consts.change, spriteGroups.untouches, spriteGroups.changegroup,
                                    n=4, speed=8)
                elif self.board[y][x] == '^':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.thorn, spriteGroups.thorngroup, spriteGroups.anothertoches)
                elif self.board[y][x] == 'S':
                    UltimateAnimPic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                                    self.cell_size, consts.boss_door, spriteGroups.changegroup, spriteGroups.untouches,
                                    n=8, speed=8)
                elif self.board[y][x] == '%':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.invis, spriteGroups.breakgroup)
                elif self.board[y][x] == 't':
                    UltimateAnimPic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                                    self.cell_size, consts.trigger, spriteGroups.triggergroup, spriteGroups.untouches,
                                    n=8, speed=8)
                elif self.board[y][x] == '&':
                    boss.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, consts.horizon, spriteGroups.toches)
                elif self.board[y][x] == 'H':
                    hleb.HlebPic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                                 self.cell_size, consts.hleb, spriteGroups.hleb,
                                 koef=windows.k ** windows.fullscreen)
                elif board.board[y][x] == 'k':
                    boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                             board.cell_size, consts.startdoor, spriteGroups.untouches)
                else:
                    pass
        spriteGroups.hleb.draw(sc)
        spriteGroups.triggergroup.draw(sc)
        spriteGroups.breakgroup.draw(sc)
        spriteGroups.thorngroup.draw(sc)
        spriteGroups.anothertoches.draw(sc)
        spriteGroups.changegroup.draw(sc)
        spriteGroups.toches.draw(sc)
        spriteGroups.platformgroup.draw(sc)
        spriteGroups.untouches.draw(sc)
        spriteGroups.finale.draw(sc)

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
        sloniks = pygame.sprite.Group(list(spriteGroups.sloniks)[len(sp) // 2:])
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
        boss.boss_group = pygame.sprite.Group(list(spriteGroups.boss_group)[len(sp) // 2:])

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
        spriteGroups.sloniks.empty()
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if board.board[y][x] == 'e':
                    slonik.Slonik(self.left + (self.cell_size * x), self.top + (self.cell_size * y),
                                  windows.k ** windows.fullscreen, 0, lknrght=random.randint(0, 2),
                                  trtspd=12 * random.randint(0, 8))

    def otris_boss(self):
        spriteGroups.boss_group.empty()
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
        super().__init__(spriteGroups.bgroup)
        self.image = pygame.transform.scale(Background.image_bg, (w * koef, h * koef))
        self.rect = self.image.get_rect()
        self.rect.x = left
        self.rect.y = top

    def update(self, w, h, left, top, koef):
        spriteGroups.bgroup.empty()
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
    spriteGroups.bgroup.update(*windows.size, windows.otstupx * windows.fullscreen,
                               windows.otstupy * windows.fullscreen,
                               windows.k ** windows.fullscreen)
    board.otris_slonik()
    board.otris_boss()
    return board.get_start_end_pos()


def rescreen():
    if windows.fullscreen:
        windows.screen = pygame.display.set_mode(windows.fullsize, pygame.FULLSCREEN)
    else:
        windows.screen = pygame.display.set_mode(windows.size)
    board.set_view(windows.otstupx * windows.fullscreen,
                   -windows.otstupy * windows.k ** windows.fullscreen,
                   64 * windows.k ** windows.fullscreen)
    spriteGroups.bgroup.update(*windows.size, windows.otstupx * windows.fullscreen,
                               windows.otstupy * windows.k * windows.fullscreen,
                               windows.k ** windows.fullscreen)


def updater():
    global board
    spriteGroups.bgroup.draw(windows.screen)
    board.render(windows.screen)
    spriteGroups.hero_health.draw(windows.screen)
    consts.pause_btn.drawPauseBtn(windows.screen, consts.hitNow)


def get_shadow(x, y, w, h):
    spriteGroups.shadowgroup.empty()
    sp = consts.shadow
    boss.Pic(x, y, w, h, sp, spriteGroups.shadowgroup)


def remover(pos, block='.'):
    x, y = pos
    if board.board[int(y)][int(x)] != block:
        board.board[int(y)] = board.board[int(y)][:int(x)] + block + board.board[int(y)][int(x) + 1:]
        if block == '0':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.floor, spriteGroups.toches)
            spriteGroups.toches.draw(windows.screen)
        elif block == '#':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.wallx, spriteGroups.toches)
            spriteGroups.toches.draw(windows.screen)
        elif block == '=':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.wally, spriteGroups.toches)
            spriteGroups.toches.draw(windows.screen)
        elif block == '_':
            UltimateAnimPic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                            board.cell_size, consts.plat, spriteGroups.untouches, n=4, speed=6)
            boss.Pic(board.left + (board.cell_size * x) + board.cell_size // 4, board.top + (board.cell_size * y),
                     board.cell_size - board.cell_size // 2,
                     board.cell_size // 64, consts.placeholder, spriteGroups.platformgroup)
            spriteGroups.platformgroup.draw(windows.screen)
            spriteGroups.untouches.draw(windows.screen)
        elif block == 'F':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.finish, spriteGroups.finale)
            spriteGroups.finale.draw(windows.screen)
        elif block == 'C':
            UltimateAnimPic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                            board.cell_size, consts.change, spriteGroups.changegroup, spriteGroups.untouches, n=4,
                            speed=8)
        elif block == '^':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.thorn, spriteGroups.thorngroup, spriteGroups.anothertoches)
            spriteGroups.anothertoches.draw(windows.screen)
        elif block == 'S':
            UltimateAnimPic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                            board.cell_size, consts.boss_door, spriteGroups.changegroup, spriteGroups.untouches,
                            n=8, speed=8)
        elif block == '%':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.invis, spriteGroups.breakgroup)
            spriteGroups.breakgroup.draw(windows.screen)
        elif block == 't':
            UltimateAnimPic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                            board.cell_size, consts.trigger, spriteGroups.triggergroup, spriteGroups.untouches, n=8,
                            speed=8)
        elif block == '&':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.horizon, spriteGroups.toches)
            spriteGroups.toches.draw(windows.screen)
        elif block == '.':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.shadow, spriteGroups.shadowgroup)
            spriteGroups.shadowgroup.draw(windows.screen)
        elif board.board[y][x] == 'e':
            slonik.Slonik(board.left + (board.cell_size * x), board.top + (board.cell_size * y),
                          windows.k ** windows.fullscreen, 0, lknrght=random.randint(0, 2),
                          trtspd=12 * random.randint(0, 8), hp=1)
            spriteGroups.sloniks.draw(windows.screen)
        elif board.board[y][x] == 'k':
            boss.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, consts.startdoor, spriteGroups.untouches)


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
