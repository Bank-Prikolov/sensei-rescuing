import pygame
import consts
import windows
import lvl_gen
from processHelper import load_image
import random


class Pic(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, sprite, *group):
        sprite = load_image(sprite)
        group = group
        super().__init__(*group)
        self.image = pygame.transform.scale(sprite, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Animpic(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, sprite, *group, koef):
        self.sprites = pygame.transform.scale(sprite,
                                              (w, h))
        super().__init__(*group)
        self.counter = 0
        self.frames = self.cut_sheet(self.sprites, koef)
        self.image = self.frames[self.counter]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.wait = 2

    def cut_sheet(self, sprites, koef):
        self.rect = pygame.Rect(0, 0, 24 * koef,
                                24 * koef)
        plist = list()
        for i in range(sprites.get_height() // int(32 * koef)):
            frame_location = (0, self.rect.h * i)
            plist.append(sprites.subsurface(pygame.Rect(
                frame_location, self.rect.size)))
        return plist

    def update(self):
        if self.wait % 2 == 0:
            self.counter = (self.counter + 1) % len(self.frames)
            self.image = self.frames[self.counter]
        self.wait += 1


boss_shoot_list = []
boss_group = pygame.sprite.Group()
boss_projectile_group = pygame.sprite.Group()
b_projectile_speed = []


class Boss(pygame.sprite.Sprite):
    pic = load_image(consts.kowlad)
    php = load_image(consts.boos_prjct)

    def __init__(self, x, y, koef, act=0):
        super().__init__(boss_group)
        self.sprites = pygame.transform.scale(
            Boss.pic, (Boss.pic.get_width() * koef, Boss.pic.get_height() * koef))
        self.k = koef
        self.frames = self.cut_sheet(self.sprites, koef, act)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.counter = 0
        self.act = act
        self.looking_right = False
        self.hp = ord('p') + ord('h') + ord('p') - 96 * 3
        self.bullet_speed = 7
        self.step = 0
        self.hitick = 0
        self.pospoint = 0
        self.herocords = [list(lvl_gen.characters)[0].rect[0] - list(lvl_gen.characters)[0].rect[2] // 2,
                          list(lvl_gen.characters)[0].rect[1] - list(lvl_gen.characters)[0].rect[3] // 2]
        self.attack = 0
        self.attack_counter = -59

    def cut_sheet(self, sprites, koef, act):
        self.rect = pygame.Rect(0, 0, 64 * koef,
                                108 * koef)
        plist = list()
        for i in range(sprites.get_height() // int(108 * koef)):
            frame_location = (self.rect.w * act, self.rect.h * i)
            plist.append(sprites.subsurface(pygame.Rect(
                frame_location, self.rect.size)))
        return plist

    def update(self):
        if self.herocords[0] < self.rect.x:
            if self.looking_right:
                self.looking_right = False
                self.change_act(0, self.get_coords())
        else:
            if not self.looking_right:
                self.looking_right = True
                self.change_act(1, self.get_coords())
        self.herocords = [list(lvl_gen.characters)[0].rect[0] - list(lvl_gen.characters)[0].rect[2] // 2,
                          list(lvl_gen.characters)[0].rect[1] - list(lvl_gen.characters)[0].rect[3] // 2]
        lvl_gen.get_shadow(*self.rect)
        lvl_gen.shadowgroup.draw(windows.screen)
        self.image = self.frames[self.cur_frame]
        if not self.step:
            if self.counter == 7:
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
        self.counter = (self.counter + 1) % 8
        if self.attack_counter == 0:
            self.attack = self.make_attack()
        elif self.attack_counter == 359:
            self.attack = 0
            self.make_move()
        if self.attack == 1:
            if self.attack_counter in [40, 80, 120]:
                self.shoot()
            elif self.attack_counter > 120 and self.step:
                self.attack_counter = 358
        elif self.attack == 2:
            if self.attack_counter in [120, 200]:
                self.make_move()
            elif self.attack_counter in [60, 140, 220]:
                self.shoot()
            elif self.attack_counter > 220 and self.step:
                self.attack_counter = 358
        elif self.attack == 3:
            if self.attack_counter in [120]:
                self.shoot_circle()
            elif self.attack_counter > 120 and self.step:
                self.attack_counter = 358
        else:
            pass
        self.attack_counter = (self.attack_counter + 1) % 360

    def set_coords(self, x, y):
        self.rect[:2] = [x, y]

    def get_coords(self):
        return self.rect[0], self.rect[1]

    def shoot(self):
        naborx = self.herocords[0], self.rect[0]
        nabory = self.herocords[1], self.rect[1]
        a, b = max(naborx) - min(naborx), max(nabory) - min(nabory)
        bxs, bys = (self.bullet_speed * a / (a + b)).__round__(0), (self.bullet_speed * b / (a + b)).__round__(0)
        Animpic(self.get_coords()[0] + self.get_size()[0] // 2,
                self.get_coords()[1] + self.get_size()[1] // 2,
                Boss.php.get_width() * 3 // 8 * windows.k ** windows.fullscreen,
                Boss.php.get_height() * 3 // 8 * windows.k ** windows.fullscreen, Boss.php,
                boss_projectile_group, koef=self.k)
        if self.looking_right:
            xz = 1
        else:
            xz = -1
        if self.rect[1] - self.rect[3] // 2 < self.herocords[1]:
            yz = 1
        else:
            yz = -1
        b_projectile_speed.append(((int(xz * bxs * self.k ** windows.fullscreen),
                                    int(yz * bys * self.k ** windows.fullscreen)), 0))

    def shoot_circle(self):
        if self.pospoint == 0: # [896, 66], [480, 66]]
            xrange = [-1]
            yrange = [-1]
        elif self.pospoint == 1:
            xrange = [1]
            yrange = [-1]
        elif self.pospoint == 2:
            xrange = [1]
            yrange = [1]
        elif self.pospoint == 3:
            xrange = [-1]
            yrange = [1]
        else:
            xrange = [-1, 1]
            yrange = [1]
        for xcoef in xrange:
            for ycoef in yrange:
                for xb in range(8):
                    yb = self.bullet_speed - xb
                    if yb != 0 and xb != 0:
                        Animpic(self.get_coords()[0] + self.get_size()[0] // 2,
                                self.get_coords()[1] + self.get_size()[1] // 2,
                                Boss.php.get_width() * 3 // 8 * windows.k ** windows.fullscreen,
                                Boss.php.get_height() * 3 // 8 * windows.k ** windows.fullscreen, Boss.php,
                                boss_projectile_group, koef=self.k)
                        b_projectile_speed.append(((int(xcoef * xb * self.k ** windows.fullscreen),
                                                    int(ycoef * yb * self.k ** windows.fullscreen)), 0))

    def get_hit(self):
        self.hp -= 2
        self.step = 2
        return self.hp

    def change_act(self, act, coords):
        pos = coords
        self.act = act
        self.frames = []
        self.cur_frame = 0
        if act == 0:
            self.frames = self.cut_sheet(self.sprites, self.k, self.act)
        elif act == 1:
            self.frames = self.cut_sheet(self.sprites, self.k, self.act)
        else:
            pass
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(*pos)

    def get_size(self):
        return self.rect[2:4]

    def make_move(self):
        cordi = [[896, 322], [64, 322], [64, 66], [896, 66], [480, 66]]
        a = random.randint(0, 4)
        lvl_gen.get_shadow(*self.rect)
        lvl_gen.shadowgroup.draw(windows.screen)
        while a == self.pospoint:
            a = random.randint(0, 4)
        self.set_coords(windows.otstupx * windows.fullscreen + cordi[a][0] * self.k, cordi[a][1] * self.k)
        if a in [0, 3]:
            self.change_act(0, self.get_coords())
            self.looking_right = False
        elif a in [1, 2]:
            self.change_act(1, self.get_coords())
            self.looking_right = True
        self.pospoint = a

    def make_attack(self):
        return random.randint(1, 3)


    def rain_attack(self):
        pass
