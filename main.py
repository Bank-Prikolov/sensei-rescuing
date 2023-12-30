from Load_image import load_image
from konst import *
from WINDOWS import *
from lvl_gen import Board, tochesx


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
        if pygame.sprite.spritecollide(self, tochesx, False):
            self.move(0, -yspeed * k ** fullscreen)

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


# class Camera:
#     # зададим начальный сдвиг камеры
#     def __init__(self):
#         self.dx = 0
#         self.dy = 0
#
#     # сдвинуть объект obj на смещение камеры
#     def apply(self, obj):
#         obj.rect.x += self.dx
#         obj.rect.y += self.dy
#
#     # позиционировать камеру на объекте target
#     def update(self, target):
#         self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
#         self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
#
#     def get_apple(self):
#         return self.dx, self.dy
#

characters = pygame.sprite.Group()
wai = load_image(wai)
hero = Hero(wai, 8, 0, height - 173, *wai.get_size(), 1, 0)

bgroup = pygame.sprite.Group()
bg = Background(*size, 0, 0, k)

board = Board(8, 6, 'pp_test_level.txt')
board.set_view(0, 0, 128)

if __name__ == '__main__':
    clock = pygame.time.Clock()
    pygame.display.set_caption('Platformer')
    bgroup.draw(screen)
    characters.draw(screen)
    fullscreen = 0
    running = True
    runright, runleft, lookingup, sitting, shooting = False, False, False, False, False
    lookingright = 1
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
                    lookingright = 1
                    runright = True
                    runleft = False
                elif event.key == pygame.K_w:
                    lookingup = True
                elif event.key == pygame.K_s:
                    sitting = True
                elif event.key == pygame.K_a:
                    hero = hero.change_act('l', hero.get_coords(), k ** fullscreen)
                    lookingright = 0
                    runleft = True
                    runright = False
                elif event.key == pygame.K_F11:
                    if fullscreen:
                        screen = pygame.display.set_mode(size)
                        fullscreen = 0
                        hero.set_coords((hero.get_coords()[0] - otstupx) // k, (hero.get_coords()[1] - otstupy) // k)
                    else:
                        screen = pygame.display.set_mode(fullsize, pygame.FULLSCREEN)
                        fullscreen = 1
                        hero.set_coords(otstupx + hero.get_coords()[0] * k, (otstupy // k + hero.get_coords()[1]) * k)
                    if lookingright:
                        hero = hero.change_act('sr', hero.get_coords(), k ** fullscreen)
                    else:
                        hero = hero.change_act('sl', hero.get_coords(), k ** fullscreen)
                    board.set_view(otstupx * fullscreen, otstupy * fullscreen, 128 * k ** fullscreen)
                    bgroup.update(*size, otstupx * fullscreen, otstupy * fullscreen, k ** fullscreen)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    runright = False
                    if runleft:
                        hero = hero.change_act('l', hero.get_coords(), k ** fullscreen)
                elif event.key == pygame.K_w:
                    lookingup = False
                elif event.key == pygame.K_s:
                    sitting = False
                elif event.key == pygame.K_a:
                    runleft = False
                    if runright:
                        hero = hero.change_act('r', hero.get_coords(), k ** fullscreen)
                if not (runright or runleft or sitting or shooting or lookingup):
                    if lookingright:
                        hero = hero.change_act('sr', hero.get_coords(), k ** fullscreen)
                    else:
                        hero = hero.change_act('sl', hero.get_coords(), k ** fullscreen)
        if runright:
            hero.move(xspeed * k ** fullscreen, 0)
        if runleft:
            hero.move((-1) * xspeed * k ** fullscreen, 0)
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
