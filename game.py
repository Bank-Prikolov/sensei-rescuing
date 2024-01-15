import pygame.sprite
from lvl_gen import *


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

        yspeed -= (self.ys // 20)
        self.rect = self.rect.move(0, yspeed * k ** fullscreen)
        if falling and not pygame.sprite.spritecollide(self, toches, False):
            if not (self.act == 'falll' or self.act == 'fallr'):
                if lookingright:
                    hero = self.change_hero('fallr', self.get_coords(), k ** fullscreen)
                else:
                    hero = self.change_hero('falll', self.get_coords(), k ** fullscreen)

        if ((yspeed >= 0) and (yspeed + (self.ys // 20)) < 0) or (yspeed > 6 and not falling):
            if not (self.act == 'falll' or self.act == 'fallr'):
                if lookingright:
                    hero = self.change_hero('fallr', self.get_coords(), k ** fullscreen)
                else:
                    hero = self.change_hero('falll', self.get_coords(), k ** fullscreen)
            jumping = False
            falling = True

        heropos = [self.get_coords()[0], self.get_coords()[1] + self.get_size()[1]]
        if jumping:
            touchable = False
        elif falling:
            if pygame.sprite.spritecollide(self, platformgroup, False):
                if k == 1.5:
                    if fullscreen:
                        checklist = [-6, -25, -16, -24, -26, -18, -12, -22]
                    else:
                        checklist = [-2, -17, -8, -12, -20, -22, -14, -18, -16]
                else:
                    checklist = list(
                        map(lambda x: int(x * k ** fullscreen), [-2, -17, -8, -12, -20, -22, -14, -18, -16])
                    )
                if not (list(pygame.sprite.spritecollide(self, platformgroup, False))[0].rect[1] - heropos[1]
                        in checklist):
                    touchable = False
                else:
                    touchable = True
            else:
                touchable = True
        else:
            touchable = True
        if pygame.sprite.spritecollide(self, toches, False) or (
                (pygame.sprite.spritecollide(self, platformgroup, False)) and touchable):
            self.rect = self.rect.move(0, -yspeed * k ** fullscreen)
            yspeed = 0
            self.ys = -16
            jumping = False
            falling = False
            if self.movement and yspeed == 0:
                if xspeed == 0:
                    if lookingright:
                        hero = self.change_hero('sr', hero.get_coords(), k ** fullscreen)
                    else:
                        hero = self.change_hero('sl', hero.get_coords(), k ** fullscreen)
                else:
                    if not (self.act == 'r' or self.act == 'l'):
                        if runright:
                            hero = self.change_hero('r', hero.get_coords(), k ** fullscreen)
                        if runleft:
                            hero = self.change_hero('l', hero.get_coords(), k ** fullscreen)

    @staticmethod
    def change_hero(act, koords, koef):
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

    # def shoot(self, coords):
    #     radius = 40
    #     image = pygame.Surface((2 * radius, 2 * radius),
    #                                 pygame.SRCALPHA, 32)
    #     pygame.draw.circle(image, pygame.Color("red"),
    #                        (radius, radius), radius)
    #     rect = pygame.Rect(coords[0] + hero.get_size()[0] // 2, coords[1] + hero.get_size()[1] // 2, 2 * radius, 2 * radius)
    #     vx = 2
    #     vy = 2

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = width // 2
        self.dy = height // 2

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

    def get_apple(self):
        return self.dx, self.dy


generate_level(2)
updater()
wai = load_image(wai)
hero = Hero(wai, 8, *start_coords, *wai.get_size(), k ** fullscreen, 0)
end_coords = end_coords
camera = Camera()
if __name__ == '__main__':
    clock = pygame.time.Clock()
    pygame.display.set_caption('Platformer')
    running = True
    runright, runleft, lookingup, sitting, shooting = False, False, False, False, False
    lookingright = 1
    jumping = False
    falling = False
    platstand = False
    winning = False
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
                    if sitting:
                        falling = True
                    else:
                        if not (jumping or falling or sitting):
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
                        fullscreen = 0
                        hero.set_coords((hero.get_coords()[0] - otstupx) // k, (hero.get_coords()[1] - otstupy) // k)
                    else:
                        fullscreen = 1
                        hero.set_coords(otstupx + hero.get_coords()[0] * k, (otstupy // k + hero.get_coords()[1]) * k)
                    if lookingright:
                        hero = hero.change_hero('sr', hero.get_coords(), k ** fullscreen)
                    else:
                        hero = hero.change_hero('sl', hero.get_coords(), k ** fullscreen)
                    rescreen(fullscreen)
                    updater()
            elif event.type == pygame.MOUSEMOTION:
                if pygame.sprite.spritecollide(hero, finale, False):
                    winning = True
                else:
                    winning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == 1025 and board.get_cell(event.pos) == end_coords and winning:
                    running = False
                if event.type == 1025:
                    if not shooting:
                        shooting = True
                        hero.shoot(event.pos)
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
        # camera.update(hero)
        # for sprite in all_sprites:
        #     print(camera.get_apple())
        #     camera.apply(sprite)
        bgd = pygame.Surface(hero.get_size())
        hero.update()
        characters.draw(screen)
        clock.tick(fps)
        pygame.display.update()
    pygame.quit()
