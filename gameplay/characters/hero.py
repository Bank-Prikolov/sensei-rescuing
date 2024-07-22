import pygame
from config import consts
from gameplay.objects import boss
import spriteGroups
from misc.utils import load_image


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, koef, hr, anim=0, movement=False, act='sr'):
        super().__init__(spriteGroups.characters)
        if hr == 1:
            self.pic = load_image(consts.wai)
            self.fireball = consts.fireball
        if hr == 2:
            self.pic = load_image(consts.the_strongest)
            self.fireball = consts.hollow_purple
        self.sprites = pygame.transform.scale(
            self.pic, (self.pic.get_width() * 2 * koef, self.pic.get_height() * 2 * koef))
        self.k = koef
        self.frames = []
        self.cut_sheet(self.sprites, koef, anim)
        self.anim = anim
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.xs = 3
        self.ys = -0.5
        self.movement = movement
        self.act = act
        self.counter = 0
        self.projectilespeed = []
        self.projectile_speed = 10
        self.shoot_counter = 9
        self.shooting = False
        self.step = 0
        self.hitick = 0

    def cut_sheet(self, sprites, koef, anim):
        self.rect = pygame.Rect(0, 0, 40 * koef,
                                54 * koef)

        for i in range(sprites.get_height() // int(54 * koef)):
            frame_location = (self.rect.w * anim, self.rect.h * i)
            self.frames.append(sprites.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def get_hit(self):
        consts.heroHP -= 1
        self.step = 2
        return consts.heroHP

    def update(self):
        self.image = self.frames[self.cur_frame]
        self.set_coords(*self.get_coords())
        if self.counter == 5:
            self.cur_frame = (self.cur_frame + 1) % 8
            self.counter = 0
        self.counter += 1

        self.image = self.frames[self.cur_frame]
        self.set_coords(*self.get_coords())
        if not self.step:
            if self.counter == 5:
                self.cur_frame = (self.cur_frame + 1) % 8
        else:
            if self.counter % (self.step * 3) in range(0, 3):
                if self.hitick != 4:
                    a = pygame.transform.scale(load_image(consts.shadow), (self.rect.w, self.rect.h))
                    self.image = a
                    self.hitick += 1
                else:
                    self.hitick = 0
                    self.step = 0
        self.counter = (self.counter + 1) % 5

        if self.shooting:
            if self.shoot_counter == 10:
                self.shooting = False
                self.shoot_counter = 0
            else:
                self.shoot_counter += 1

        consts.yspeed -= self.ys
        self.rect = self.rect.move(0, consts.yspeed * windows.k ** windows.fullscreen)
        if consts.falling and self.act not in ['falll', 'fallr']:
            if consts.lookingright:
                self.change_hero('fallr', self.get_coords())
            else:
                self.change_hero('falll', self.get_coords())
        elif not consts.falling and consts.yspeed > 0.5:
            consts.falling = True

        if (consts.yspeed >= 0) and (consts.yspeed + self.ys) < 0:
            consts.jumping = False
            consts.falling = True
        heropos = [self.get_coords()[0], self.get_coords()[1] + self.get_size()[1]]

        if consts.jumping:
            touchable = False
        elif consts.falling:
            if pygame.sprite.spritecollide(self, spriteGroups.platformgroup, False):
                # print(list(pygame.sprite.spritecollide(self,
                # spriteGroups.platformgroup, False))[0].rect[1] - heropos[1])
                if windows.k == 1.5:
                    if windows.fullscreen:
                        checklist = [-1, -13, -12, -15, -21, -47, -8, -2, -6, -24]
                    else:
                        checklist = [-1, -9, -8, -4, -25, -16, -14, -6, -31]
                else:
                    checklist = list(
                        map(lambda x: int(x * windows.k ** windows.fullscreen),
                            [-1, -9, -8, -4, -25, -16, -14, -6])
                    )
                if not (list(pygame.sprite.spritecollide(self, spriteGroups.platformgroup, False))[0].rect[1] - heropos[
                    1]
                        in checklist):
                    touchable = False
                else:
                    touchable = True
            else:
                touchable = True
        else:
            touchable = True

        if pygame.sprite.spritecollide(self, spriteGroups.toches, False) or (
                pygame.sprite.spritecollide(self, spriteGroups.platformgroup, False) and touchable):
            if pygame.sprite.spritecollide(self, spriteGroups.toches, False):
                if (pygame.sprite.spritecollide(self, spriteGroups.toches, False)[0].rect[1]
                        > consts.hero.get_coords()[1] - consts.yspeed):
                    self.rect = self.rect.move(0, pygame.sprite.spritecollide(
                        self, spriteGroups.toches, False)[0].rect[1] - self.get_coords()[1] - self.get_size()[1])
                else:
                    self.rect = self.rect.move(0, -consts.yspeed * windows.k)
            else:
                self.rect = self.rect.move(0, pygame.sprite.spritecollide(
                    self, spriteGroups.platformgroup, False)[0].rect[1] - consts.hero.get_coords()[1]
                                           - consts.hero.get_size()[1])

            consts.yspeed = 0
            consts.jumping = False
            consts.falling = False
            if self.movement and consts.yspeed == 0:
                if consts.xspeed == 0:
                    if consts.lookingright:
                        self.change_hero('sr', self.get_coords())
                    else:
                        self.change_hero('sl', self.get_coords())
                else:
                    if not (self.act == 'r' or self.act == 'l'):
                        if consts.runright:
                            self.change_hero('r', self.get_coords())
                        if consts.runleft:
                            self.change_hero('l', self.get_coords())

    def change_hero(self, act, coords):
        pos = coords
        self.act = act
        self.frames = []
        self.cur_frame = 0
        if act == 'sr':
            self.movement = False
            self.anim = 0
            self.cut_sheet(self.sprites, self.k, self.anim)
        elif act == 'sl':
            self.movement = False
            self.anim = 3
            self.cut_sheet(self.sprites, self.k, self.anim)
        elif act == 'r':
            self.movement = True
            self.anim = 1
            self.cut_sheet(self.sprites, self.k, self.anim)
        elif act == 'l':
            self.movement = True
            self.anim = 2
            self.cut_sheet(self.sprites, self.k, self.anim)
        elif act == 'jumpr':
            self.movement = True
            self.anim = 4
            self.cut_sheet(self.sprites, self.k, self.anim)
        elif act == 'fallr':
            self.movement = True
            self.anim = 5
            self.cut_sheet(self.sprites, self.k, self.anim)
        elif act == 'jumpl':
            self.movement = True
            self.anim = 6
            self.cut_sheet(self.sprites, self.k, self.anim)
        elif act == 'falll':
            self.movement = True
            self.anim = 7
            self.cut_sheet(self.sprites, self.k, self.anim)
        else:
            pass
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(*pos)

    def move(self, x, y):
        self.rect = self.rect.move(x, y)
        if pygame.sprite.spritecollide(self, spriteGroups.toches, False):
            self.rect = self.rect.move(-x, -y)

    def get_coords(self):
        return self.rect[0], self.rect[1]

    def set_coords(self, x, y):
        self.rect[:2] = [x, y]

    def get_size(self):
        return self.rect[2:4]

    def shoot(self, spees):
        if not self.shooting:
            boss.Pic(self.get_coords()[0] + self.get_size()[0] // 4,
                     self.get_coords()[1] + self.get_size()[1] // 2,
                     16 * windows.k ** windows.fullscreen,
                     16 * windows.k ** windows.fullscreen, self.fireball,
                     spriteGroups.projectilesgroup)
            self.projectilespeed.append(spees)
            self.shooting = True

    def end(self):
        consts.sitting = False
        consts.runleft = False
        consts.runright = False
        consts.jumping = False
        consts.falling = False
        self.kill()
        spriteGroups.characters.empty()


class AnimatedHeroHealth(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(spriteGroups.hero_health)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.counter = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, hit):
        if hit == 0 and self.cur_frame == 2:
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
        if self.cur_frame != hit:
            if self.counter == 10:
                self.counter = 0
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
            self.counter += 1
