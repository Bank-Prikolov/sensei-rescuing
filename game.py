import pygame.surface

import boss
import fileManager
import lvl_gen
import game_over
import game_complete
import pause
import consts
import windows
import starsRecorder
from processHelper import load_image, terminate
from itemCreator import Object
from itemChanger import starsChanger

runright, runleft, lookingup, sitting = False, False, False, False
jumping = False
falling = False
lookingright = 1
shooting = 0
xspeed = 0
yspeed = 0


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, koef, hr, anim=0, movement=False, act='sr'):
        super().__init__(lvl_gen.characters)
        if hr == 1:
            self.pic = load_image(consts.wai)
            self.fireball = consts.fireball
        if hr == 2:
            self.pic = load_image(consts.the_strongest)
            self.fireball = consts.hollow_purple
        self.sprites = pygame.transform.scale(
            self.pic, (self.pic.get_width() // 2 * koef, self.pic.get_height() // 2 * koef))
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
        self.projectile_speed = 8

    def cut_sheet(self, sprites, koef, anim):
        self.rect = pygame.Rect(0, 0, 40 * koef,
                                54 * koef)

        for i in range(sprites.get_height() // int(54 * koef)):
            frame_location = (self.rect.w * anim, self.rect.h * i)
            self.frames.append(sprites.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def update(self):
        global yspeed, falling, lookingright, jumping, thing, hero
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
                self.change_hero('fallr', self.get_coords())
            else:
                self.change_hero('falll', self.get_coords())
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
                        checklist = [-1, -13, -12, -15, -21, -47]
                    else:
                        checklist = [-1, -9, -8, -4, -25, -16, -14, -6, -31]
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
                        self.change_hero('sr', self.get_coords())
                    else:
                        self.change_hero('sl', self.get_coords())
                else:
                    if not (self.act == 'r' or self.act == 'l'):
                        if runright:
                            self.change_hero('r', self.get_coords())
                        if runleft:
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
        if pygame.sprite.spritecollide(self, lvl_gen.toches, False):
            self.rect = self.rect.move(-x, -y)

    def get_coords(self):
        return self.rect[0], self.rect[1]

    def set_coords(self, x, y):
        self.rect[:2] = [x, y]

    def get_size(self):
        return self.rect[2:4]

    def shoot(self, spees):
        boss.Pic(self.get_coords()[0] + self.get_size()[0] // 4,
                 self.get_coords()[1] + self.get_size()[1] // 2,
                 40 // 2.5 * windows.k ** windows.fullscreen,
                 40 // 2.5 * windows.k ** windows.fullscreen, self.fireball,
                 lvl_gen.projectilesgroup)
        self.projectilespeed.append(spees)

    def end(self):
        global runright, runleft, jumping, falling, sitting
        sitting = False
        runleft = False
        runright = False
        jumping = False
        falling = False
        self.kill()
        lvl_gen.characters.empty()
        lvl_gen.projectilesgroup.empty()
        self.projectilespeed = []


def game_def(lvl):
    global runright, runleft, lookingup, sitting, shooting, jumping, falling, lookingright, xspeed, yspeed, hero
    start_coords = lvl_gen.generate_level(lvl)
    character = fileManager.heroImport()[0]
    if not windows.fullscreen:
        pause_btn = Object(windows.width - windows.width + 8, windows.height - windows.height + 6, 108, 54,
                           r"objects\without text\pause-button-obj.png")
    else:
        pause_btn = Object(windows.otstupx + 8, windows.height - windows.height + 6, 144, 72,
                           r"objects\without text\pause-button-obj.png")
    lvl_gen.updater()
    hero = Hero(*start_coords, windows.k ** windows.fullscreen, character)
    running = True
    lvl_gen.characters.draw(windows.screen)
    thing = ''
    cheatPanel = False  # cheats
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)
    started = True
    current_seconds = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(windows.fullscreen)
            elif event.type == timer_event and started:
                current_seconds += 1
                # print(current_seconds)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    xspeed = hero.xs
                    if not jumping:
                        hero.change_hero('r', hero.get_coords())
                    else:
                        if not falling:
                            hero.change_hero('jumpr', hero.get_coords())
                        else:
                            hero.change_hero('fallr', hero.get_coords())
                    lookingright = 1
                    runright = True
                    runleft = False
                elif event.key == pygame.K_s:
                    sitting = True
                elif event.key == pygame.K_a:
                    xspeed = hero.xs
                    if not jumping:
                        hero.change_hero('l', hero.get_coords())
                    else:
                        if not falling:
                            hero.change_hero('jumpl', hero.get_coords())
                        else:
                            hero.change_hero('falll', hero.get_coords())
                    lookingright = 0
                    runleft = True
                    runright = False
                elif event.key == pygame.K_SPACE:
                    if sitting:
                        yspeed = 7
                    else:
                        if (not (jumping or falling or sitting)) or cheatPanel:
                            jumping = True
                            yspeed = -9 - 5 * cheatPanel
                            if lookingright:
                                hero.change_hero('jumpr', hero.get_coords())
                            else:
                                hero.change_hero('jumpl', hero.get_coords())
                elif event.key == pygame.K_w:
                    if pygame.sprite.spritecollide(hero, lvl_gen.finale, False):
                        thing = ''
                        hero.end()
                        lvl_gen.updater()
                        started = False
                        record = starsChanger(lvl, current_seconds)
                        if current_seconds < starsRecorder.get_seconds(lvl) or starsRecorder.get_seconds(lvl) == 0:
                            starsRecorder.push_record(lvl, 1, record, current_seconds)
                        starsRecorder.push_lastRecord(lvl, record, current_seconds)
                        game_complete.game_complete()
                    else:
                        if lookingright:
                            shooting = hero.projectile_speed * windows.k ** windows.fullscreen
                        else:
                            shooting = -hero.projectile_speed * windows.k ** windows.fullscreen
                        hero.shoot(shooting)
                elif event.key == pygame.K_ESCAPE:
                    xspeed = 0
                    predpause = hero.get_coords()
                    hero.end()
                    started = False
                    pause.pause(current_seconds, len(list(lvl_gen.sloniks)))
                    started = True
                    hero = Hero(*predpause, windows.k ** windows.fullscreen, character)
                    if lookingright:
                        hero.change_hero('sr', predpause)
                    else:
                        hero.change_hero('sl', predpause)
                    lvl_gen.rescreen()
                    lvl_gen.updater()
            elif event.type == pygame.WINDOWEXPOSED:
                if lookingright:
                    hero.change_hero('sr', hero.get_coords())
                else:
                    hero.change_hero('sl', hero.get_coords())
                lvl_gen.rescreen()
                lvl_gen.updater()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    runright = False
                elif event.key == pygame.K_s:
                    sitting = False
                elif event.key == pygame.K_a:
                    runleft = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:  # cheats
                    cheatPanel = not cheatPanel
                    hero.xs = 3 * 5 ** cheatPanel
                    hero.projectile_speed = 8 * 2 ** cheatPanel

        pause_btn.draw(windows.screen)
        if pygame.sprite.spritecollide(hero, lvl_gen.changegroup, False):
            lvl_gen.projectilesgroup.empty()
            if thing == '':
                thing = 1
            else:
                thing += 1
            hero.set_coords(*lvl_gen.generate_level(lvl + thing / 10))
            windows.screen.fill('#000000')
            lvl_gen.updater()
        lvl_gen.get_shadow(*hero.get_coords(), *hero.get_size())
        lvl_gen.shadowgroup.draw(windows.screen)

        if lvl_gen.projectilesgroup:
            for sprite in range(len(lvl_gen.projectilesgroup)):
                pygame.draw.rect(windows.screen, (36, 34, 52), list(lvl_gen.projectilesgroup)[sprite].rect)
                list(lvl_gen.projectilesgroup)[sprite].rect = list(lvl_gen.projectilesgroup)[sprite].rect.move(
                    hero.projectilespeed[sprite], 0)
                if pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite], lvl_gen.sloniks, False):
                    if (pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite],
                                                    lvl_gen.sloniks, False)[0].get_hit(hero.get_coords()[0]) == 0
                            or cheatPanel):
                        lvl_gen.remover(lvl_gen.board.get_cell(list(
                            pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite], lvl_gen.sloniks, True))[
                                                                   0].rect[:2]))
                    hero.projectilespeed.pop(sprite)
                    list(lvl_gen.projectilesgroup)[sprite].kill()
                    break
                if (pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite], lvl_gen.toches, False)
                        or pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite],
                                                       lvl_gen.anothertoches, False)):
                    hero.projectilespeed.pop(sprite)
                    list(lvl_gen.projectilesgroup)[sprite].kill()
                    break
            lvl_gen.projectilesgroup.draw(windows.screen)

        if lvl_gen.nmeprojectilesgroup:
            for sprite in range(len(lvl_gen.nmeprojectilesgroup)):
                pygame.draw.rect(windows.screen, (36, 34, 52), list(lvl_gen.nmeprojectilesgroup)[sprite].rect)
                list(lvl_gen.nmeprojectilesgroup)[sprite].rect = list(lvl_gen.nmeprojectilesgroup)[sprite].rect.move(
                    lvl_gen.projectilespeed[sprite][0], 0)
                if pygame.sprite.spritecollide(list(lvl_gen.nmeprojectilesgroup)[sprite], lvl_gen.characters,
                                               False) and not cheatPanel:
                    thing = ''
                    hero.end()
                    lvl_gen.projectilespeed = []
                    lvl_gen.nmeprojectilesgroup.empty()
                    lvl_gen.updater()
                    started = False
                    game_over.game_over()
                if (pygame.sprite.spritecollide(list(lvl_gen.nmeprojectilesgroup)[sprite], lvl_gen.toches, False)
                        or pygame.sprite.spritecollide(list(lvl_gen.nmeprojectilesgroup)[sprite],
                                                       lvl_gen.anothertoches, False)):
                    lvl_gen.projectilespeed.pop(sprite)
                    list(lvl_gen.nmeprojectilesgroup)[sprite].kill()
                    break
            lvl_gen.nmeprojectilesgroup.draw(windows.screen)
        if not cheatPanel:
            if (pygame.sprite.spritecollide(hero, lvl_gen.thorngroup, False)
                    or pygame.sprite.spritecollide(hero, lvl_gen.sloniks, False)
                    or pygame.sprite.spritecollide(hero, boss.boss_group, False)):
                thing = ''
                hero.end()
                lvl_gen.projectilespeed = []
                lvl_gen.nmeprojectilesgroup.empty()
                lvl_gen.updater()
                started = False
                game_over.game_over()
        if pygame.sprite.spritecollide(hero, lvl_gen.triggergroup, False):
            if lvl == 2 and thing == 1:
                # lvl_gen.remover(lvl_gen.board.get_cell(hero.get_coords()))
                # hero.set_coords(hero.get_coords()[0], hero.get_coords()[1] - lvl_gen.board.get_size())
                # lvl_gen.remover((8, 5), '=')
                # lvl_gen.remover((9, 5), '=')
                # lvl_gen.remover((10, 5), '=')
                # lvl_gen.remover((11, 5), '=')
                # lvl_gen.remover((12, 5), '=')
                # lvl_gen.remover((13, 5), '=')
                # lvl_gen.remover((14, 5), '=')
                # lvl_gen.remover((7, 4), 'F')
                pass
            elif lvl == 3:
                lvl_gen.remover(lvl_gen.board.get_cell(
                    list(pygame.sprite.spritecollide(hero, lvl_gen.triggergroup, True))[0].rect[:2]))
                lvl_gen.toches.remove(lvl_gen.get_key(lvl_gen.toches.spritedict,
                                                      pygame.rect.Rect(int(lvl_gen.board.rev_get_cell((11, 10))[0]),
                                                                       int(lvl_gen.board.rev_get_cell((11, 10))[1]),
                                                                       lvl_gen.board.get_size(),
                                                                       lvl_gen.board.get_size())))
                lvl_gen.remover((11, 10))

        if not lvl_gen.sloniks:
            if lvl == 2 and thing == '':
                lvl_gen.remover((2, 7), 'C')
            elif lvl == 2 and thing == 1:
                lvl_gen.remover((8, 4), 'F')
            elif lvl == 3 and thing == 1:
                lvl_gen.remover((7, 4), 'S')
            elif lvl == 3 and thing == 2:
                hero.end()
                thing = ''
                lvl_gen.updater()
                started = False
                record = starsChanger(lvl, current_seconds)
                if current_seconds < starsRecorder.get_seconds(lvl) or starsRecorder.get_seconds(lvl) == 0:
                    starsRecorder.push_record(lvl, 1, record, current_seconds)
                starsRecorder.push_lastRecord(lvl, record, current_seconds)
                game_complete.game_complete()

        if runright or runleft:
            if runright:
                hero.move(xspeed * windows.k ** windows.fullscreen, 0)
            if runleft:
                hero.move(-xspeed * windows.k ** windows.fullscreen, 0)
        else:
            xspeed = 0
        hero.update()
        lvl_gen.breakgroup.draw(windows.screen)
        lvl_gen.characters.draw(windows.screen)
        lvl_gen.sloniks.update()
        boss.boss_group.update()
        lvl_gen.sloniks.draw(windows.screen)
        lvl_gen.triggergroup.draw(windows.screen)
        lvl_gen.finale.draw(windows.screen)
        lvl_gen.untouches.draw(windows.screen)
        boss.boss_group.draw(windows.screen)
        pygame.draw.rect(windows.screen, '#000000',
                         (0, 0, windows.otstupx ** windows.fullscreen, windows.fullsize[1] ** windows.fullscreen))
        pygame.draw.rect(windows.screen, '#000000',
                         (windows.fullsize[0] - windows.otstupx, 0, windows.fullsize[0] ** windows.fullscreen,
                          windows.fullsize[1] ** windows.fullscreen))
        consts.clock.tick(consts.fps)
        pygame.display.flip()
