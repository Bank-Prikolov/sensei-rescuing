import pygame
import os
import sys
import screeninfo
from Load_image import load_image

pygame.init()
size = width, height = 1024, 704
fullsize = tuple(map(int, '='.join(
    (str(screeninfo.get_monitors()).lstrip('[Monitor(').rstrip(')]').split(', '))[2: 4]).split('=')[1::2]))
k = fullsize[1] // size[1]
otstupx = (fullsize[0] - size[0] * k) // 2
otstupy = (fullsize[1] - size[1] * k) * k
screen = pygame.display.set_mode(size)
last_screen = pygame.display.Info().current_w, pygame.display.Info().current_h
test = 'pp_test_level.txt'


class Hero(pygame.sprite.Sprite):
    def __init__(self, sprites, rows, x, y, w, h, koef, anim):
        super().__init__(characters)
        self.health = 3
        self.sprites = pygame.transform.scale(sprites, (w * koef, h * koef))
        self.frames = []
        self.cut_sheet(self.sprites, koef, rows, anim)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sprites, koef, rows, kakaya_animacia):
        self.rect = pygame.Rect(0, 0, 108 * koef,
                                108 * koef)
        for j in range(rows):
            frame_location = (self.rect.w * kakaya_animacia, self.rect.h * j)
            for _ in range(6):
                self.frames.append(sprites.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def change_act(self, act, koords, koef):
        global fullscreen
        if act == 'sr':
            hc = koords[0], koords[1]
            characters.empty()
            ho = Hero(wai, 8, *hc, wai.get_width(), wai.get_height(), koef, 0)
        elif act == 'sl':
            hc = koords[0], koords[1]
            characters.empty()
            ho = Hero(wai, 8, *hc, wai.get_width(), wai.get_height(), koef, 3)
        elif act == 'r':
            hc = koords[0], koords[1]
            characters.empty()
            ho = Hero(wai, 8, *hc, wai.get_width(), wai.get_height(), koef, 1)
        elif act == 'l':
            hc = koords[0], koords[1]
            characters.empty()
            ho = Hero(wai, 8, *hc, wai.get_width(), wai.get_height(), koef, 2)
        else:
            ho = None
        return ho

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def get_coords(self):
        return self.rect[0], self.rect[1]

    def set_coords(self, x, y):
        self.rect[:2] = [x, y]


class Background(pygame.sprite.Sprite):
    image_bg = load_image('background1.png')

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


class Board:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.board = [[0] * w for _ in range(h)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, sc):
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(sc, '#F1F1F1', (
                    self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size, self.cell_size),
                                 1)

    def get_cell(self, mouse_pos):
        if self.left < mouse_pos[0] < self.left + (self.cell_size * self.width) and \
                self.top < mouse_pos[1] < self.top + (self.cell_size * self.height):
            return int((mouse_pos[0] - 10) / 30), int((mouse_pos[1] - 10) / 30)
        else:
            return None

    def get_size(self):
        return self.cell_size


def generate_level(txt_file):
    fullname = os.path.join('data\levels', txt_file)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    level = fullname
    level_load = list(map(lambda x: x.rstrip('\n'), open(level).readlines()))
    for y in range(len(level_load)):                # y
        for x in range(len(level_load[y])):         # x
            print(level_load[y][x])


characters = pygame.sprite.Group()
wai = load_image('pp_Wai.png')
hero = Hero(wai, 8, 0, height - 173, *wai.get_size(), 1, 0)

bgroup = pygame.sprite.Group()
bg = Background(*size, 0, 0, k)

board = Board(8, 6)
board.set_view(0, 0, 128)

if __name__ == '__main__':
    clock = pygame.time.Clock()
    pygame.display.set_caption('Platformer')
    bgroup.draw(screen)
    characters.draw(screen)
    fullscreen = 0
    running = True
    runright, runleft, lookingup, sitting, shooting = False, False, False, False, False
    lookingright, lookingleft = True, False
    fps = 60
    xspeed = 4
    yspeed = 3
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    hero = hero.change_act('r', hero.get_coords(), k ** fullscreen)
                    lookingright = True
                    lookingleft = False
                    runright = True
                elif event.key == pygame.K_w:
                    lookingup = True
                elif event.key == pygame.K_s:
                    sitting = True
                elif event.key == pygame.K_a:
                    hero = hero.change_act('l', hero.get_coords(), k ** fullscreen)
                    lookingleft = True
                    lookingright = False
                    runleft = True
                elif event.key == pygame.K_F11:
                    if fullscreen:
                        screen = pygame.display.set_mode(size)
                        fullscreen = 0
                        hero.set_coords((hero.get_coords()[0] - otstupx) // k, (hero.get_coords()[1] - otstupy) // k)
                    else:
                        screen = pygame.display.set_mode(fullsize, pygame.FULLSCREEN)
                        fullscreen = 1
                        hero.set_coords(otstupx + hero.get_coords()[0] * k, (otstupy // k + hero.get_coords()[1]) * k)
                    if lookingleft:
                        hero = hero.change_act('sl', hero.get_coords(), k ** fullscreen)
                    elif lookingright:
                        hero = hero.change_act('sr', hero.get_coords(), k ** fullscreen)
                    board.set_view(otstupx * fullscreen, otstupy * fullscreen, 128 * k ** fullscreen)
                    bgroup.update(*size, otstupx * fullscreen, otstupy * fullscreen, k ** fullscreen)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    lookingright = True
                    lookingleft = False
                    runright = False
                elif event.key == pygame.K_w:
                    lookingup = False
                elif event.key == pygame.K_s:
                    sitting = False
                elif event.key == pygame.K_a:
                    lookingleft = True
                    lookingright = False
                    runleft = False
                if not (runright or runleft or lookingup or sitting or shooting):
                    if lookingleft:
                        hero = hero.change_act('sl', hero.get_coords(), k ** fullscreen)
                    elif lookingright:
                        hero = hero.change_act('sr', hero.get_coords(), k ** fullscreen)
        if runright:
            hero.move(xspeed * k ** fullscreen, 0)
        if runleft:
            hero.move(-xspeed * k ** fullscreen, 0)
        if lookingup:
            hero.move(0, -yspeed * k ** fullscreen)
        if sitting:
            hero.move(0, yspeed * k ** fullscreen)
        hero.update()
        bgroup.draw(screen)
        board.render(screen)
        characters.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
