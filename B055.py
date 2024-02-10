import pygame
import consts
import windows
from processHelper import load_image


class Pic(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, sprite, *group):
        sprite = load_image(sprite)
        group = group
        super().__init__(*group)
        self.image = pygame.transform.scale(sprite, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


boss_group = pygame.sprite.Group()
boss_projectile_group = pygame.sprite.Group()


class Boss(pygame.sprite.Sprite):
    pic = load_image(consts.boss)
    # php = load_image('пуля')

    def __init__(self, x, y, koef, act=0):
        super().__init__(boss_group)
        self.sprites = pygame.transform.scale(
            Boss.pic, (Boss.pic.get_width() * koef, Boss.pic.get_height() * koef))
        self.k = koef
        self.frames = []
        self.cut_sheet(self.sprites, koef, act)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.counter = 0
        self.act = act
        self.looking_right = False
        self.hp = 100
        self.bulletspeed = 6
        self.step = 0
        self.hitick = 0
        self.projectile_speed = []

    def cut_sheet(self, sprites, koef, act):
        self.rect = pygame.Rect(0, 0, 64 * koef,
                                64 * koef)

        for i in range(sprites.get_height() // int(64 * koef)):
            frame_location = (self.rect.w * act, self.rect.h * i)
            self.frames.append(sprites.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def update(self):
        self.image = self.frames[self.cur_frame]
        self.set_coords(*self.get_coords())
        if self.counter == 11:
            self.cur_frame = (self.cur_frame + 1) % 2

    def get_coords(self):
        return self.rect[0], self.rect[1]

    def set_coords(self, x, y):
        self.rect[:2] = [x, y]

    def get_size(self):
        return self.rect[2:4]

    def shoot(self):
        Pic(self.get_coords()[0] + self.get_size()[0] // 2,
            self.get_coords()[1] + self.get_size()[1] // 2.5,
            Boss.php.get_width() // 2 * windows.k ** windows.fullscreen,
            Boss.php.get_height() // 2 * windows.k ** windows.fullscreen, marker,
            boss_projectile_group)
        if self.looking_right:
            self.projectile_speed.append((self.bulletspeed * self.k ** windows.fullscreen, self))
        else:
            self.projectile_speed.append((-self.bulletspeed * self.k ** windows.fullscreen, self))

    def get_hit(self):
        self.hp -= 1
        self.step = 2
        return self.hp

    def change_act(self, act, coords):
        pos = coords
        self.act = act
        self.frames = []
        self.cur_frame = 0
        if act == 0:
            self.cut_sheet(self.sprites, self.k, self.act)
        elif act == 1:
            self.cut_sheet(self.sprites, self.k, self.act)
        else:
            pass
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(*pos)