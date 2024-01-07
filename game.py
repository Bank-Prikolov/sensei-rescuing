from load_image import load_image
from consts import *
from windows import *
from lvl_gen import Board, toches


class Hero(pygame.sprite.Sprite):
    def __init__(self, sprites, rows, x, y, w, h, koef, anim, movement=False, act='sr'):
        super().__init__(characters)
        self.health = 3
        self.sprites = pygame.transform.scale(sprites, (w * koef, h * koef))
        self.frames = []
        self.cut_sheet(self.sprites, koef, rows, anim)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.xs = 5
        self.ys = -16
        self.movement = movement
        self.act = act

    def cut_sheet(self, sprites, koef, rows, kakaya_animacia):
        self.rect = pygame.Rect(0, 0, 80 * koef,
                                108 * koef)
        for j in range(rows):
            frame_location = (self.rect.w * kakaya_animacia, self.rect.h * j)
            for _ in range(6):
                self.frames.append(sprites.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

        global yspeed, xspeed, jumping, hero, falling

        if (yspeed - (self.ys // 20) >= 0) and yspeed < 0:
            falling = True
            if lookingright:
                hero = hero.change_hero('fallr', hero.get_coords(), k ** fullscreen)
            else:
                hero = hero.change_hero('falll', hero.get_coords(), k ** fullscreen)

        yspeed -= (self.ys // 20)
        self.rect = self.rect.move(0, yspeed * k ** fullscreen)

        if pygame.sprite.spritecollide(self, toches, False):
            self.rect = self.rect.move(0, -yspeed * k ** fullscreen)
            yspeed = 0
            self.ys = -16
            jumping = False
            falling = False
            if self.movement and yspeed == 0:
                if xspeed == 0:
                    if lookingright:
                        hero = hero.change_hero('sr', hero.get_coords(), k ** fullscreen)
                    else:
                        hero = hero.change_hero('sl', hero.get_coords(), k ** fullscreen)
                else:
                    if not (self.act == 'r' or self.act == 'l'):
                        if runright:
                            hero = hero.change_hero('r', hero.get_coords(), k ** fullscreen)
                        if runleft:
                            hero = hero.change_hero('l', hero.get_coords(), k ** fullscreen)
        if yspeed > 6 and not falling:
            if not (self.act == 'falll' or self.act == 'fallr'):
                if lookingright:
                    hero = hero.change_hero('fallr', hero.get_coords(), k ** fullscreen)
                else:
                    hero = hero.change_hero('falll', hero.get_coords(), k ** fullscreen)
                    falling = True

    def change_hero(self, act, koords, koef):
        global fullscreen
        characters.empty()
        hc = koords[0], koords[1]
        if act == 'sr':
            ho = Hero(wai, 8, *hc, wai.get_width(), wai.get_height(), koef, 0, act=act)
        elif act == 'sl':
            ho = Hero(wai, 8, *hc, wai.get_width(), wai.get_height(), koef, 3, act=act)
        elif act == 'r':
            ho = Hero(wai, 8, *hc, wai.get_width(), wai.get_height(), koef, 1, movement=True, act=act)
        elif act == 'l':
            ho = Hero(wai, 8, *hc, wai.get_width(), wai.get_height(), koef, 2, movement=True, act=act)
        elif act == 'jumpr':
            ho = Hero(wai, 8, *hc, wai.get_width(), wai.get_height(), koef, 4, movement=True, act=act)
        elif act == 'fallr':
            ho = Hero(wai, 8, *hc, wai.get_width(), wai.get_height(), koef, 5, movement=True, act=act)
        elif act == 'jumpl':
            ho = Hero(wai, 8, *hc, wai.get_width(), wai.get_height(), koef, 6, movement=True, act=act)
        elif act == 'falll':
            ho = Hero(wai, 8, *hc, wai.get_width(), wai.get_height(), koef, 7, movement=True, act=act)
        else:
            ho = None
        return ho

    def move(self, x, y):
        self.rect = self.rect.move(x, y)
        if pygame.sprite.spritecollide(self, toches, False):
            self.rect = self.rect.move(-x, -y)

    def get_coords(self):
        return self.rect[0], self.rect[1]

    def set_coords(self, x, y):
        self.rect[:2] = [x, y]

    def get_size(self):
        return self.rect[2:4]


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
hero = Hero(wai, 8, 1 + 256, height - 172 - 128 - 128, *wai.get_size(), 1, 0)

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
    jumping = False
    falling = False
    fps = 60
    xspeed = 0
    yspeed = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    xspeed = hero.xs
                    if not jumping:
                        hero = hero.change_hero('r', hero.get_coords(), k ** fullscreen)
                    else:
                        if not falling:
                            hero = hero.change_hero('jumpr', hero.get_coords(), k ** fullscreen)
                        else:
                            hero = hero.change_hero('fallr', hero.get_coords(), k ** fullscreen)
                    lookingright = 1
                    runright = True
                    runleft = False
                elif event.key == pygame.K_w:
                    lookingup = True
                elif event.key == pygame.K_s:
                    sitting = True
                elif event.key == pygame.K_a:
                    xspeed = hero.xs
                    if not jumping:
                        hero = hero.change_hero('l', hero.get_coords(), k ** fullscreen)
                    else:
                        if not falling:
                            hero = hero.change_hero('jumpl', hero.get_coords(), k ** fullscreen)
                        else:
                            hero = hero.change_hero('falll', hero.get_coords(), k ** fullscreen)
                    lookingright = 0
                    runleft = True
                    runright = False
                elif event.key == pygame.K_SPACE:
                    if not (jumping or falling):
                        jumping = True
                        yspeed = -17
                        hero.ys = -8
                        if lookingright:
                            hero = hero.change_hero('jumpr', hero.get_coords(), k ** fullscreen)
                            pass
                        else:
                            hero = hero.change_hero('jumpl', hero.get_coords(), k ** fullscreen)
                            pass
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
                        hero = hero.change_hero('sr', hero.get_coords(), k ** fullscreen)
                    else:
                        hero = hero.change_hero('sl', hero.get_coords(), k ** fullscreen)
                    board.set_view(otstupx * fullscreen, otstupy * fullscreen, 128 * k ** fullscreen)
                    bgroup.update(*size, otstupx * fullscreen, otstupy * fullscreen, k ** fullscreen)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    runright = False
                elif event.key == pygame.K_w:
                    lookingup = False
                elif event.key == pygame.K_s:
                    sitting = False
                elif event.key == pygame.K_a:
                    runleft = False
        if runright or runleft:
            if runright:
                hero.move(xspeed * k ** fullscreen, 0)
            if runleft:
                hero.move(-xspeed * k ** fullscreen, 0)
        else:
            xspeed = 0
            if sitting:
                hero.move(0, 0)
            elif lookingup:
                hero.move(0, 0)
        bgroup.draw(screen)
        board.render(screen)
        hero.update()
        characters.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
