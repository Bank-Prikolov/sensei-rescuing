import os
import sys
from consts import *
import windows
import B055

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

    def __init__(self, x, y, koef, act=0):
        super().__init__(sloniks)
        self.sprites = pygame.transform.scale(
            Slonik.pic, (Slonik.pic.get_width() // 2 * koef, Slonik.pic.get_height() // 2 * koef))
        self.k = koef
        self.frames = []
        self.cut_sheet(self.sprites, koef, act)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.counter = 0
        self.xspeed = 4
        self.moving = False
        self.act = act
        self.looking_right = True
        self.hp = 6
        self.bulletspeed = 10
        self.acter = 0
        self.step = 0
        self.hitick = 0
        self.shoot_counter = 35
        self.turn_speed = 0
        self.dontseeme = True

    def cut_sheet(self, sprites, koef, act):
        self.rect = pygame.Rect(0, 0, 64 * koef,
                                64 * koef)

        for i in range(sprites.get_height() // int(64 * koef)):
            frame_location = (self.rect.w * act, self.rect.h * i)
            self.frames.append(sprites.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def update(self):
        if self.turn_speed == 95 and self.dontseeme:
            if self.looking_right:
                self.looking_right = False
            else:
                self.looking_right = True
        self.turn_speed = (self.turn_speed + 1) % 96
        hrop = board.get_cell(list(characters)[0].get_coords())
        enep = board.get_cell(self.get_coords())
        if ((board.get_cell((list(characters)[0].rect.x,
                             list(characters)[0].rect.centery))[1] - board.get_cell(self.rect[:2])[1] in [0])
                and (('=' not in board.board[enep[1]][min(enep[0], hrop[0]) + 1: max(enep[0], hrop[0])])
                     and ('#' not in board.board[enep[1]][min(enep[0], hrop[0]) + 1: max(enep[0], hrop[0])])
                     and ('&' not in board.board[enep[1]][min(enep[0], hrop[0]) + 1: max(enep[0], hrop[0])]))):
            if ((list(characters)[0].rect.x < self.rect.x and not self.looking_right)
                    or (list(characters)[0].rect.x > self.rect.x and self.looking_right)):
                self.dontseeme = False
                self.turn_speed = 1
                if self.shoot_counter == 35:
                    self.shoot()
                self.shoot_counter = (self.shoot_counter + 1) % 36
        else:
            if self.turn_speed == 0 and not self.dontseeme:
                self.shoot_counter = 35
                self.dontseeme = True
        if self.moving:
            pass
        else:
            if self.looking_right:
                if self.act != 0:
                    self.change_act(0, self.get_coords())
            else:
                if self.act != 1:
                    self.change_act(1, self.get_coords())
        self.image = self.frames[self.cur_frame]
        self.set_coords(*self.get_coords())
        if not self.step:
            if self.counter == 11:
                self.cur_frame = (self.cur_frame + 1) % 2
        else:
            if self.counter % (self.step * 3) in range(0, 3):
                if self.hitick != 4:
                    a = pygame.transform.scale(load_image(shadow), (self.rect.w, self.rect.h))
                    self.image = a
                    self.hitick += 1
                else:
                    self.hitick = 0
                    self.step = 0
        self.counter = (self.counter + 1) % 12

    def get_coords(self):
        return self.rect[0], self.rect[1]

    def set_coords(self, x, y):
        self.rect[:2] = [x, y]

    def get_size(self):
        return self.rect[2:4]

    def shoot(self):
        B055.Pic(self.get_coords()[0] + self.get_size()[0] // 2,
                 self.get_coords()[1] + self.get_size()[1] // 2.5,
                 Slonik.php.get_width() // 2 * windows.k ** windows.fullscreen,
                 Slonik.php.get_height() // 2 * windows.k ** windows.fullscreen, php,
                 nmeprojectilesgroup)
        if self.looking_right:
            projectilespeed.append((self.bulletspeed * self.k ** windows.fullscreen, self))
        else:
            projectilespeed.append((-self.bulletspeed * self.k ** windows.fullscreen, self))

    def get_hit(self, herox):
        self.hp -= 1
        self.step = 2
        self.turn_speed = 1
        if self.get_coords()[0] - herox < 0:
            if not self.looking_right:
                self.looking_right = True
        else:
            if self.looking_right:
                self.looking_right = False
        return self.hp

    def change_act(self, act, coords):
        pos = coords
        self.act = act
        self.frames = []
        self.cur_frame = 0
        if act == 0:
            self.moving = False
            self.cut_sheet(self.sprites, self.k, self.act)
        elif act == 1:
            self.moving = False
            self.cut_sheet(self.sprites, self.k, self.act)
        else:
            pass
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(*pos)


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
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[y][x] == '0':
                    B055.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, floor, toches)
                elif self.board[y][x] == '#':
                    B055.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, wallx, toches)
                elif self.board[y][x] == '=':
                    B055.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, wally, toches)
                elif self.board[y][x] == '@':
                    pass
                elif self.board[y][x] == '_':
                    B055.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, plat, untouches)
                    B055.Pic(self.left + (self.cell_size * x) + self.cell_size // 4, self.top + (self.cell_size * y),
                             self.cell_size - self.cell_size // 2,
                             self.cell_size // 64, placeholder, platformgroup)
                elif self.board[y][x] == 'F':
                    B055.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, finish, finale)
                elif self.board[y][x] == 'C':
                    B055.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, change, changegroup, untouches)
                elif self.board[y][x] == '^':
                    B055.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, thorn, thorngroup, anothertoches)
                elif self.board[y][x] == 'S':
                    B055.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, boss_door, changegroup, untouches)
                elif self.board[y][x] == '%':
                    B055.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, invis, breakgroup)
                elif self.board[y][x] == 't':
                    B055.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, trigger, triggergroup)
                elif self.board[y][x] == '&':
                    B055.Pic(self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size,
                             self.cell_size, horizon, toches)
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

    def pereres_slon(self, spisokslonikoff):
        global sloniks
        sp = spisokslonikoff
        for slon in sp:
            if not windows.fullscreen:
                new = ((slon.get_coords()[0] - windows.otstupx) // windows.k,
                       (slon.get_coords()[1] - windows.otstupy + 16) // windows.k)
            else:
                new = (windows.otstupx + slon.get_coords()[0] * windows.k,
                       (windows.otstupy + slon.get_coords()[1] - 18) * windows.k)
            a = Slonik(*new, windows.k ** windows.fullscreen, slon.act)
            a.hp = slon.hp
            a.looking_right = slon.looking_right
        sloniks = pygame.sprite.Group(list(sloniks)[len(sp) // 2:])
        sloniks.draw(screen)

    def pereres_boss(self, spisokslonikoff):
        sp = spisokslonikoff
        for boss in sp:
            if not windows.fullscreen:
                new = ((boss.get_coords()[0] - windows.otstupx) // windows.k,
                       (boss.get_coords()[1] - windows.otstupy) // windows.k)
            else:
                new = (windows.otstupx + boss.get_coords()[0] * windows.k,
                       (windows.otstupy + boss.get_coords()[1] - 18) * windows.k)
            a = B055.Boss(*new, windows.k ** windows.fullscreen, boss.act)
            a.hp = boss.hp
        B055.boss_group = pygame.sprite.Group(list(B055.boss_group)[len(sp) // 2:])

    def rev_get_cell(self, mouse_pos):
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
                    Slonik(self.left + (self.cell_size * x), self.top + (self.cell_size * y),
                           windows.k ** windows.fullscreen, 0)

    def otris_boss(self):
        B055.boss_group.empty()
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[y][x] == 'B':
                    B055.Boss(self.left + (self.cell_size * x),
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
    board.otris_slonik()
    board.otris_boss()
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
    B055.Pic(x, y, w, h, sp, shadowgroup)


def remover(pos, block='.'):
    x, y = pos
    if board.board[int(y)][int(x)] != block:
        board.board[int(y)] = board.board[int(y)][:int(x)] + block + board.board[int(y)][int(x) + 1:]
        if block == '0':
            B055.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, floor, toches)
            toches.draw(screen)
        elif block == '#':
            B055.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, wallx, toches)
            toches.draw(screen)
        elif block == '=':
            B055.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, wally, toches)
            toches.draw(screen)
        elif block == '_':
            B055.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, plat, untouches)
            B055.Pic(board.left + (board.cell_size * x) + board.cell_size // 4, board.top + (board.cell_size * y),
                     board.cell_size - board.cell_size // 2,
                     board.cell_size // 64, placeholder, platformgroup)
            platformgroup.draw(screen)
            untouches.draw(screen)
        elif block == 'F':
            B055.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, finish, finale)
            finale.draw(screen)
        elif block == 'C':
            B055.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, change, changegroup, untouches)
            untouches.draw(screen)
        elif block == '^':
            B055.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, thorn, thorngroup, anothertoches)
            anothertoches.draw(screen)
        elif block == 'S':
            B055.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, boss_door, changegroup, untouches)
            untouches.draw(screen)
        elif block == '%':
            B055.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, invis, breakgroup)
            breakgroup.draw(screen)
        elif block == 't':
            B055.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, trigger, triggergroup)
            triggergroup.draw(screen)
        elif block == '&':
            B055.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, horizon, toches)
            toches.draw(screen)
        elif block == '.':
            B055.Pic(board.left + (board.cell_size * x), board.top + (board.cell_size * y), board.cell_size,
                     board.cell_size, shadow, shadowgroup)
            shadowgroup.draw(screen)


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
