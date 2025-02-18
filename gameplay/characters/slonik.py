import pygame
from gameplay.objects import boss
from config import consts
import levelGenerator
import spriteGroups
from misc.utils import load_image


class Slonik(pygame.sprite.Sprite):
    pic = load_image(consts.slonik)
    php = load_image(consts.php)

    def __init__(self, x, y, koef, act=0, lknrght=True, trtspd=0, hp=3, zaderzhka=False):
        super().__init__(spriteGroups.sloniks)
        self.sprites = pygame.transform.scale(
            Slonik.pic, (Slonik.pic.get_width() * 2 * koef, Slonik.pic.get_height() * 2 * koef))
        self.k = koef
        self.frames = []
        self.cut_sheet(self.sprites, koef, act)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.counter = 0
        self.xspeed = 4
        self.act = act
        self.looking_right = lknrght
        self.hp = hp
        self.bulletspeed = 8
        self.acter = 0
        self.step = 0
        self.hitick = 0
        if zaderzhka:
            self.shoot_counter = 0
        else:
            self.shoot_counter = 35
        self.turn_speed = trtspd
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
        hrop = levelGenerator.board.get_cell(list(spriteGroups.characters)[0].get_coords())
        enep = levelGenerator.board.get_cell(self.get_coords())
        if ((levelGenerator.board.get_cell((list(spriteGroups.characters)[0].rect.x,
                                            list(spriteGroups.characters)[0].rect.centery))[1] -
             levelGenerator.board.get_cell(self.rect[:2])[1]
             in [0])
                and (('=' not in levelGenerator.board.board[enep[1]][min(enep[0], hrop[0]) + 1: max(enep[0], hrop[0])])
                     and ('#' not in levelGenerator.board.board[enep[1]][
                                     min(enep[0], hrop[0]) + 1: max(enep[0], hrop[0])])
                     and ('&' not in levelGenerator.board.board[enep[1]][
                                     min(enep[0], hrop[0]) + 1: max(enep[0], hrop[0])]))):
            if ((list(spriteGroups.characters)[0].rect.x < self.rect.x and not self.looking_right)
                    or (list(spriteGroups.characters)[0].rect.x > self.rect.x and self.looking_right)):
                self.dontseeme = False
                self.turn_speed = 1
                if self.shoot_counter == 35:
                    self.shoot()
                self.shoot_counter = (self.shoot_counter + 1) % 36
        else:
            if self.turn_speed == 0 and not self.dontseeme:
                self.shoot_counter = 35
                self.dontseeme = True
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
                    a = pygame.transform.scale(load_image(consts.shadow), (self.rect.w, self.rect.h))
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
        boss.Pic(self.get_coords()[0] + self.get_size()[0] // 2,
                 self.get_coords()[1] + self.get_size()[1] // 2.5,
                 Slonik.php.get_width() // 2 * windows.k ** windows.fullscreen,
                 Slonik.php.get_height() // 2 * windows.k ** windows.fullscreen, consts.php,
                 spriteGroups.nmeprojectilesgroup)
        if self.looking_right:
            consts.projectileObj_speed.append((self.bulletspeed * self.k ** windows.fullscreen, self))
        else:
            consts.projectileObj_speed.append((-self.bulletspeed * self.k ** windows.fullscreen, self))

    def get_hit(self, herox):
        self.hp -= 1
        self.step = 2
        self.turn_speed = 1
        soundManager.slonik_take_hit_sound()
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
            self.cut_sheet(self.sprites, self.k, self.act)
        elif act == 1:
            self.cut_sheet(self.sprites, self.k, self.act)
        else:
            pass
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(*pos)
