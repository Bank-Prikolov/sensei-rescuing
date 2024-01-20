import sys

import lvl_gen
import pygame

import game_over
import game_complete
import menu
from consts import *
import windows
from load_image import load_image

runright, runleft, lookingup, sitting = False, False, False, False
jumping = False
falling = False
lookingright = 1
shooting = 0
xspeed = 0
yspeed = 0


class Hero(pygame.sprite.Sprite):
    pic = load_image(wai)
    fiball = load_image(fireball)

    def __init__(self, x, y, koef, anim=0, movement=False, act='sr'):
        super().__init__(lvl_gen.characters)
        self.sprites = pygame.transform.scale(
            Hero.pic, (Hero.pic.get_width() // 2 * koef, Hero.pic.get_height() // 2 * koef))
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

    def cut_sheet(self, sprites, koef, anim):
        self.rect = pygame.Rect(0, 0, 40 * koef,
                                54 * koef)

        for i in range(sprites.get_height() // int(54 * koef)):
            frame_location = (self.rect.w * anim, self.rect.h * i)
            self.frames.append(sprites.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def update(self):
        global yspeed, falling, lookingright, hero, jumping, thing
        self.image = self.frames[self.cur_frame]
        self.set_coords(*self.get_coords())
        if self.counter == 5:
            self.cur_frame = (self.cur_frame + 1) % 8
            self.counter = 0
        self.counter += 1

        yspeed -= self.ys
        self.rect = self.rect.move(0, yspeed * windows.k ** windows.fullscreen)
        if falling and self.act not in ['falll', 'fallr']:
            if lookingright:
                hero = self.change_hero('fallr', self.get_coords())
            else:
                hero = self.change_hero('falll', self.get_coords())
        elif not falling and yspeed > 0.5:
            falling = True

        if (yspeed >= 0) and (yspeed + self.ys) < 0:
            jumping = False
            falling = True
        heropos = [self.get_coords()[0], self.get_coords()[1] + self.get_size()[1]]

        if jumping:
            touchable = False
        elif falling:
            if pygame.sprite.spritecollide(self, lvl_gen.platformgroup, False):
                if windows.k == 1.5:
                    if windows.fullscreen:
                        checklist = [-1, -13, -12, -15, -21]
                    else:
                        checklist = [-1, -9, -8, -4, -25, -16, -14, -6]
                else:
                    checklist = list(
                        map(lambda x: int(x * windows.k ** windows.fullscreen),
                            [-1, -9, -8, -4, -25, -16, -14, -6])
                    )
                if not (list(pygame.sprite.spritecollide(self, lvl_gen.platformgroup, False))[0].rect[1] - heropos[1]
                        in checklist):
                    touchable = False
                else:
                    touchable = True
            else:
                touchable = True
        else:
            touchable = True

        if pygame.sprite.spritecollide(self, lvl_gen.toches, False) or (
                pygame.sprite.spritecollide(self, lvl_gen.platformgroup, False) and touchable):
            if pygame.sprite.spritecollide(self, lvl_gen.toches, False):
                if pygame.sprite.spritecollide(self, lvl_gen.toches, False)[0].rect[1] > hero.get_coords()[1] - yspeed:
                    self.rect = self.rect.move(0, pygame.sprite.spritecollide(
                        self, lvl_gen.toches, False)[0].rect[1] - self.get_coords()[1] - self.get_size()[1])
                else:
                    self.rect = self.rect.move(0, -yspeed * windows.k)
            else:
                self.rect = self.rect.move(0, pygame.sprite.spritecollide(
                    self, lvl_gen.platformgroup, False)[0].rect[1] - hero.get_coords()[1] - hero.get_size()[1])

            yspeed = 0
            jumping = False
            falling = False
            if self.movement and yspeed == 0:
                if xspeed == 0:
                    if lookingright:
                        hero = self.change_hero('sr', self.get_coords())
                    else:
                        hero = self.change_hero('sl', self.get_coords())
                else:
                    if not (self.act == 'r' or self.act == 'l'):
                        if runright:
                            hero = self.change_hero('r', self.get_coords())
                        if runleft:
                            hero = self.change_hero('l', self.get_coords())

    def change_hero(self, act, coords):
        lvl_gen.characters.empty()
        pos = coords
        if act == 'sr':
            hr = Hero(*pos, windows.k ** windows.fullscreen, 0, act='sr')
        elif act == 'sl':
            hr = Hero(*pos, windows.k ** windows.fullscreen, 3, act='sl')
        elif act == 'r':
            hr = Hero(*pos, windows.k ** windows.fullscreen, 1, movement=True, act='r')
        elif act == 'l':
            hr = Hero(*pos, windows.k ** windows.fullscreen, 2, movement=True, act='l')
        elif act == 'jumpr':
            hr = Hero(*pos, windows.k ** windows.fullscreen, 4, movement=True, act='jumpr')
        elif act == 'fallr':
            hr = Hero(*pos, windows.k ** windows.fullscreen, 5, movement=True, act='fallr')
        elif act == 'jumpl':
            hr = Hero(*pos, windows.k ** windows.fullscreen, 6, movement=True, act='jumpr')
        elif act == 'falll':
            hr = Hero(*pos, windows.k ** windows.fullscreen, 7, movement=True, act='falll')
        else:
            pass
        return hr

    def move(self, x, y):
        self.rect = self.rect.move(x, y)
        if pygame.sprite.spritecollide(self, lvl_gen.toches, False):
            self.rect = self.rect.move(-x, -y)

    def get_coords(self):
        return self.rect[0], self.rect[1]

    def set_coords(self, x, y):
        self.rect[:2] = [x, y]

    def get_size(self):
        return self.rect[2:4]

    def shoot(self):
        lvl_gen.Pic(self.get_coords()[0] + self.get_size()[0] // 4,
                    self.get_coords()[1] + self.get_size()[1] // 2,
                    Hero.fiball.get_width() // 2.5 * windows.k ** windows.fullscreen,
                    Hero.fiball.get_height() // 2.5 * windows.k ** windows.fullscreen, fireball,
                    lvl_gen.projectilesgroup)


def game_def(lvl):
    global runright, runleft, lookingup, sitting, shooting, jumping, falling, lookingright, xspeed, yspeed, hero
    start_coords = lvl_gen.generate_level(lvl)
    lvl_gen.updater()
    hero = Hero(*start_coords, windows.k ** windows.fullscreen)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Sensei Rescuing')
    running = True
    projectile_speed = 8
    fps = 60
    lvl_gen.characters.draw(lvl_gen.screen)
    thing = ''
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    xspeed = hero.xs
                    if not jumping:
                        hero = hero.change_hero('r', hero.get_coords())
                    else:
                        if not falling:
                            hero = hero.change_hero('jumpr', hero.get_coords())
                        else:
                            hero = hero.change_hero('fallr', hero.get_coords())
                    lookingright = 1
                    runright = True
                    runleft = False
                elif event.key == pygame.K_s:
                    sitting = True
                elif event.key == pygame.K_a:
                    xspeed = hero.xs
                    if not jumping:
                        hero = hero.change_hero('l', hero.get_coords())
                    else:
                        if not falling:
                            hero = hero.change_hero('jumpl', hero.get_coords())
                        else:
                            hero = hero.change_hero('falll', hero.get_coords())
                    lookingright = 0
                    runleft = True
                    runright = False
                elif event.key == pygame.K_SPACE:
                    if sitting:
                        yspeed = 7
                    else:
                        if not (jumping or falling or sitting):
                            jumping = True
                            yspeed = -9
                            if lookingright:
                                hero = hero.change_hero('jumpr', hero.get_coords())
                                pass
                            else:
                                hero = hero.change_hero('jumpl', hero.get_coords())
                                pass
                elif event.key == pygame.K_F11:
                    if windows.fullscreen:
                        windows.fullscreen = 0
                        new = ((hero.get_coords()[0] - windows.otstupx) // windows.k,
                               (hero.get_coords()[1] - windows.otstupy + 6) // windows.k)
                    else:
                        windows.fullscreen = 1
                        new = (windows.otstupx + hero.get_coords()[0] * windows.k,
                               (windows.otstupy // windows.k + hero.get_coords()[1]) * windows.k)
                    if lookingright:
                        hero = hero.change_hero('sr', new)
                    else:
                        hero = hero.change_hero('sl', new)
                    lvl_gen.rescreen()
                    lvl_gen.updater()
                elif event.key == pygame.K_w:
                    if pygame.sprite.spritecollide(hero, lvl_gen.finale, False):
                        menu.levels_menu()
                    elif not lvl_gen.projectilesgroup:
                        if lookingright:
                            shooting = projectile_speed * windows.k ** windows.fullscreen
                        else:
                            shooting = -projectile_speed * windows.k ** windows.fullscreen
                        hero.shoot()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     # if event.button == 1:
            #     #     for x in lvl_gen.sloniks:
            #     #         x.shoot()
            elif event.type == pygame.WINDOWEXPOSED:
                if lookingright:
                    hero = hero.change_hero('sr', hero.get_coords())
                else:
                    hero = hero.change_hero('sl', hero.get_coords())
                lvl_gen.rescreen()
                lvl_gen.updater()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    runright = False
                elif event.key == pygame.K_w:
                    lookingup = False
                elif event.key == pygame.K_s:
                    sitting = False
                elif event.key == pygame.K_a:
                    runleft = False
        if pygame.sprite.spritecollide(hero, lvl_gen.changegroup, False):
            if thing == '':
                thing = 1
            else:
                thing += 1
            hero.set_coords(*lvl_gen.generate_level(lvl + thing / 10))
            lvl_gen.screen.fill('#000000')
            lvl_gen.updater()
        lvl_gen.get_shadow(*hero.get_coords(), *hero.get_size())
        lvl_gen.shadowgroup.draw(lvl_gen.screen)

        for sprite in range(len(lvl_gen.projectilesgroup)):
            pygame.draw.rect(lvl_gen.screen, (36, 34, 52), list(lvl_gen.projectilesgroup)[sprite].rect)
            list(lvl_gen.projectilesgroup)[sprite].rect = list(lvl_gen.projectilesgroup)[sprite].rect.move(shooting, 0)
            if pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite], lvl_gen.sloniks, True):
                    lvl_gen.remover(lvl_gen.board.get_cell((list(lvl_gen.projectilesgroup)[sprite].rect.right,
                                                           list(lvl_gen.projectilesgroup)[sprite].rect[1])))
                    lvl_gen.remover(lvl_gen.board.get_cell(list(lvl_gen.projectilesgroup)[sprite].rect[:2]))
                    list(lvl_gen.projectilesgroup)[sprite].kill()
                    lvl_gen.updater()
            if lvl_gen.projectilesgroup:
                if (pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite], lvl_gen.toches, False)
                        or pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite], lvl_gen.anothertoches, False)):
                    list(lvl_gen.projectilesgroup)[sprite].kill()
        lvl_gen.projectilesgroup.draw(lvl_gen.screen)

        for sprite in range(len(lvl_gen.nmeprojectilesgroup)):
            pygame.draw.rect(lvl_gen.screen, (36, 34, 52), list(lvl_gen.nmeprojectilesgroup)[sprite].rect)
            list(lvl_gen.nmeprojectilesgroup)[sprite].rect = list(lvl_gen.nmeprojectilesgroup)[sprite].rect.move(shooting * 1.5, 0)

            if pygame.sprite.spritecollide(list(lvl_gen.nmeprojectilesgroup)[sprite], lvl_gen.toches, False):
                list(lvl_gen.nmeprojectilesgroup)[sprite].kill()
        lvl_gen.nmeprojectilesgroup.draw(lvl_gen.screen)

        if pygame.sprite.spritecollide(hero, lvl_gen.thorngroup, False) or pygame.sprite.spritecollide(hero, lvl_gen.sloniks, False):
            runleft = False
            runright = False
            hero.kill()
            thing = ''
            lvl_gen.generate_level(lvl)
            lvl_gen.updater()
            hero.set_coords(*start_coords)
            game_over.game_over()
        if pygame.sprite.spritecollide(hero, lvl_gen.triggergroup, True):
            if lvl == 2 and thing == 1:
                lvl_gen.remover(lvl_gen.board.get_cell(hero.get_coords()))
                hero.set_coords(hero.get_coords()[0], hero.get_coords()[1] - lvl_gen.board.get_size())
                lvl_gen.remover((8, 5), '=')
                lvl_gen.remover((9, 5), '=')
                lvl_gen.remover((10, 5), '=')
                lvl_gen.remover((11, 5), '=')
                lvl_gen.remover((12, 5), '=')
                lvl_gen.remover((13, 5), '=')
                lvl_gen.remover((14, 5), '=')
                lvl_gen.remover((7, 4), 'F')
            elif lvl == 3:
                lvl_gen.remover(lvl_gen.board.get_cell(hero.get_coords()))
                lvl_gen.remover((11, 10))

        if not lvl_gen.sloniks:
            if lvl == 2 and thing == '':
                lvl_gen.remover((2, 7), 'C')
            elif lvl == 2 and thing == 1:
                lvl_gen.remover((8, 4), 'F')
            elif lvl == 3 and thing == 1:
                lvl_gen.remover((7, 4), 'S')
            elif lvl == 3 and thing == 2:
                runleft = False
                runright = False
                hero.kill()
                game_complete.game_complete()

        if runright or runleft:
            if runright:
                hero.move(xspeed * windows.k ** windows.fullscreen, 0)
            if runleft:
                hero.move(-xspeed * windows.k ** windows.fullscreen, 0)
        else:
            xspeed = 0
        hero.update()
        lvl_gen.sloniks.update()
        lvl_gen.characters.draw(lvl_gen.screen)
        lvl_gen.sloniks.draw(lvl_gen.screen)
        lvl_gen.finale.draw(lvl_gen.screen)
        lvl_gen.untouches.draw(lvl_gen.screen)
        clock.tick(fps)
        pygame.display.flip()

# game_def(1)
