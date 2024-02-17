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
import soundManager
from hero import Hero
from processHelper import terminate
from itemChanger import starsChanger, pauseButtonChanger


def game_def(lvl):
    boss.boss_projectile_group.empty()
    boss.b_projectile_speed = []
    soundManager.game_theme()
    start_coords = lvl_gen.generate_level(lvl)
    character = fileManager.heroImport()[0]
    pause_btn = pauseButtonChanger()
    lvl_gen.updater()
    lvl_gen.characters.empty()
    consts.hero = Hero(*start_coords, windows.k ** windows.fullscreen, character)
    consts.jumping = False
    consts.yspeed = 0
    running = True
    lvl_gen.characters.draw(windows.screen)
    thing = ''
    cheatPanel = False  # cheats
    normalize = True
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)
    started = True
    current_seconds = 0
    lvl_gen.projectilesgroup.empty()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == timer_event and started:
                current_seconds += 1
                # print(current_seconds)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    consts.xspeed = consts.hero.xs
                    if not consts.jumping:
                        consts.hero.change_hero('r', consts.hero.get_coords())
                    else:
                        if not consts.falling:
                            consts.hero.change_hero('jumpr', consts.hero.get_coords())
                        else:
                            consts.hero.change_hero('fallr', consts.hero.get_coords())
                    consts.lookingright = 1
                    consts.runright = True
                    consts.runleft = False
                elif event.key == pygame.K_s:
                    consts.sitting = True
                elif event.key == pygame.K_a:
                    consts.xspeed = consts.hero.xs
                    if not consts.jumping:
                        consts.hero.change_hero('l', consts.hero.get_coords())
                    else:
                        if not consts.falling:
                            consts.hero.change_hero('jumpl', consts.hero.get_coords())
                        else:
                            consts.hero.change_hero('falll', consts.hero.get_coords())
                    consts.lookingright = 0
                    consts.runleft = True
                    consts.runright = False
                elif event.key == pygame.K_SPACE:
                    if consts.sitting:
                        consts.yspeed = 7
                    else:
                        if (not (consts.jumping or consts.falling or consts.sitting)) or cheatPanel:
                            if normalize:
                                consts.yspeed = -9
                                consts.jumping = True
                            else:
                                consts.yspeed = -9 - 2
                            if consts.lookingright:
                                consts.hero.change_hero('jumpr', consts.hero.get_coords())
                            else:
                                consts.hero.change_hero('jumpl', consts.hero.get_coords())
                elif event.key == pygame.K_w:
                    if pygame.sprite.spritecollide(consts.hero, lvl_gen.finale, False):
                        thing = ''
                        consts.hero.end()
                        lvl_gen.updater()
                        started = False
                        record = starsChanger(lvl, current_seconds)
                        if current_seconds < starsRecorder.get_seconds(lvl) or starsRecorder.get_seconds(lvl) == 0:
                            starsRecorder.push_record(lvl, 1, record, current_seconds)
                        starsRecorder.push_lastRecord(lvl, record, current_seconds)
                        game_complete.game_complete()
                    else:
                        if consts.lookingright:
                            consts.shooting = consts.hero.projectile_speed * windows.k ** windows.fullscreen
                        else:
                            consts.shooting = -consts.hero.projectile_speed * windows.k ** windows.fullscreen
                        consts.hero.shoot(consts.shooting)
                elif event.key == pygame.K_e:
                    for b in boss.boss_group:
                        b.shoot()
            elif event.type == pygame.WINDOWEXPOSED:
                if consts.lookingright:
                    consts.hero.change_hero('sr', consts.hero.get_coords())
                else:
                    consts.hero.change_hero('sl', consts.hero.get_coords())
                lvl_gen.rescreen()
                lvl_gen.updater()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    consts.runright = False
                elif event.key == pygame.K_s:
                    consts.sitting = False
                elif event.key == pygame.K_a:
                    consts.runleft = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:  # cheats
                    cheatPanel = not cheatPanel
                    consts.hero.xs = 3 * 5 ** cheatPanel
                    consts.hero.projectile_speed = 8 * 2 ** cheatPanel
                    normalize = not normalize
                if cheatPanel and event.button == 4:
                    normalize = not normalize
                    if normalize:
                        consts.hero.xs = 3
                        consts.hero.projectile_speed = 8
                    else:
                        consts.hero.xs = 3 * 5
                        consts.hero.projectile_speed = 8 * 2
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or
                    (event.type == pygame.USEREVENT and event.button == pause_btn)):
                consts.xspeed = 0
                predpause = consts.hero.get_coords()
                proj = consts.hero.projectilespeed
                pause.pause(current_seconds, len(list(lvl_gen.sloniks)))
                lvl_gen.characters.empty()
                consts.hero = Hero(*predpause, windows.k ** windows.fullscreen, character)
                consts.hero.projectilespeed = proj
                if consts.lookingright:
                    consts.hero.change_hero('sr', predpause)
                else:
                    consts.hero.change_hero('sl', predpause)
                lvl_gen.rescreen()
                lvl_gen.updater()

            pause_btn.handle_event(event, consts.volS)

        pause_btn.check_hover(pygame.mouse.get_pos())
        pause_btn.draw(windows.screen)

        if pygame.sprite.spritecollide(consts.hero, lvl_gen.changegroup, False):
            lvl_gen.projectilesgroup.empty()
            lvl_gen.nmeprojectilesgroup.empty()
            lvl_gen.projectilespeed = []
            boss.boss_projectile_group.empty()
            boss.b_projectile_speed = []
            if thing == '':
                thing = 1
            else:
                thing += 1
            consts.hero.set_coords(*lvl_gen.generate_level(lvl + thing / 10))
            consts.hero.projectilespeed = []
            windows.screen.fill('#000000')
            lvl_gen.updater()
        lvl_gen.get_shadow(*consts.hero.get_coords(), *consts.hero.get_size())
        lvl_gen.shadowgroup.draw(windows.screen)

        if lvl_gen.projectilesgroup:
            for sprite in range(len(lvl_gen.projectilesgroup)):
                pygame.draw.rect(windows.screen, (36, 34, 52), list(lvl_gen.projectilesgroup)[sprite].rect)
                list(lvl_gen.projectilesgroup)[sprite].rect = list(lvl_gen.projectilesgroup)[sprite].rect.move(
                    consts.hero.projectilespeed[sprite], 0)
                if pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite], lvl_gen.sloniks, False):
                    if (pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite],
                                                    lvl_gen.sloniks, False)[0].get_hit(consts.hero.get_coords()[0]) == 0
                            or cheatPanel):
                        lvl_gen.remover(lvl_gen.board.get_cell(list(
                            pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite], lvl_gen.sloniks, True))[
                                                                   0].rect[:2]))
                    consts.hero.projectilespeed.pop(sprite)
                    list(lvl_gen.projectilesgroup)[sprite].kill()
                    break

                if pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite], boss.boss_group, False):
                    if (pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite],
                                                    boss.boss_group, False)[0].get_hit() == 0):
                        boss.boss_group.empty()
                    consts.hero.projectilespeed.pop(sprite)
                    list(lvl_gen.projectilesgroup)[sprite].kill()
                    break

                if (pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite], lvl_gen.toches, False)
                        or pygame.sprite.spritecollide(list(lvl_gen.projectilesgroup)[sprite],
                                                       lvl_gen.anothertoches, False)):
                    consts.hero.projectilespeed.pop(sprite)
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
                    consts.hero.end()
                    lvl_gen.projectilespeed = []
                    lvl_gen.nmeprojectilesgroup.empty()
                    lvl_gen.updater()
                    boss.boss_projectile_group.empty()
                    boss.b_projectile_speed = []
                    started = False
                    game_over.game_over()
                if (pygame.sprite.spritecollide(list(lvl_gen.nmeprojectilesgroup)[sprite], lvl_gen.toches, False)
                        or pygame.sprite.spritecollide(list(lvl_gen.nmeprojectilesgroup)[sprite],
                                                       lvl_gen.anothertoches, False)):
                    lvl_gen.projectilespeed.pop(sprite)
                    list(lvl_gen.nmeprojectilesgroup)[sprite].kill()
                    break
            lvl_gen.nmeprojectilesgroup.draw(windows.screen)

        if boss.boss_projectile_group:
            for sprite in range(len(boss.boss_projectile_group)):
                list(boss.boss_projectile_group)[sprite].rect = list(boss.boss_projectile_group)[sprite].rect.move(
                    boss.b_projectile_speed[sprite][0][0], boss.b_projectile_speed[sprite][0][1])
                if pygame.sprite.spritecollide(list(boss.boss_projectile_group)[sprite], lvl_gen.characters,
                                               False) and not cheatPanel:
                    thing = ''
                    consts.hero.end()
                    lvl_gen.projectilespeed = []
                    lvl_gen.nmeprojectilesgroup.empty()
                    boss.boss_projectile_group.empty()
                    boss.b_projectile_speed = []
                    lvl_gen.updater()
                    started = False
                    game_over.game_over()
                else:
                    if (pygame.sprite.spritecollide(list(boss.boss_projectile_group)[sprite], lvl_gen.xwalls,
                                                    False)
                            or pygame.sprite.spritecollide(
                                list(boss.boss_projectile_group)[sprite], lvl_gen.thorngroup, False)):

                        list(boss.boss_projectile_group)[sprite].rect = list(boss.boss_projectile_group)[
                            sprite].rect.move(
                            -boss.b_projectile_speed[sprite][0][0], -boss.b_projectile_speed[sprite][0][1])
                        if boss.b_projectile_speed[sprite][1] == 1:
                            pygame.draw.rect(windows.screen, (36, 34, 52), (
                                list(boss.boss_projectile_group)[sprite].rect))
                            list(boss.boss_projectile_group)[sprite].kill()
                            boss.b_projectile_speed.pop(sprite)
                            break
                        else:
                            pygame.draw.rect(windows.screen, (36, 34, 52), (
                                list(boss.boss_projectile_group)[sprite].rect))
                            boss.b_projectile_speed[sprite] = ((boss.b_projectile_speed[sprite][0][0],
                                                                -boss.b_projectile_speed[sprite][0][1]),
                                                               boss.b_projectile_speed[sprite][1] + 1)

                    elif pygame.sprite.spritecollide(list(boss.boss_projectile_group)[sprite], lvl_gen.ywalls,
                                                     False):
                        list(boss.boss_projectile_group)[sprite].rect = list(boss.boss_projectile_group)[
                            sprite].rect.move(
                            -boss.b_projectile_speed[sprite][0][0], -boss.b_projectile_speed[sprite][0][1])
                        if boss.b_projectile_speed[sprite][1] == 1:
                            pygame.draw.rect(windows.screen, (36, 34, 52), (
                                list(boss.boss_projectile_group)[sprite].rect))
                            list(boss.boss_projectile_group)[sprite].kill()
                            boss.b_projectile_speed.pop(sprite)
                            break
                        else:
                            pygame.draw.rect(windows.screen, (36, 34, 52), (
                                list(boss.boss_projectile_group)[sprite].rect))
                            boss.b_projectile_speed[sprite] = ((-boss.b_projectile_speed[sprite][0][0],
                                                                boss.b_projectile_speed[sprite][0][1]),
                                                               boss.b_projectile_speed[sprite][1] + 1)
                    else:
                        pygame.draw.rect(windows.screen, (36, 34, 52), (
                            list(boss.boss_projectile_group)[sprite].rect[0] - boss.b_projectile_speed[sprite][0][0],
                            list(boss.boss_projectile_group)[sprite].rect[1] - boss.b_projectile_speed[sprite][0][1],
                            *list(boss.boss_projectile_group)[sprite].rect[2:]))
                list(boss.boss_projectile_group)[sprite].update()
            lvl_gen.boss.boss_projectile_group.draw(windows.screen)

        if not cheatPanel:
            if (pygame.sprite.spritecollide(consts.hero, lvl_gen.thorngroup, False)
                    or pygame.sprite.spritecollide(consts.hero, lvl_gen.sloniks, False)
                    or pygame.sprite.spritecollide(consts.hero, boss.boss_group, False)):
                thing = ''
                consts.hero.end()
                lvl_gen.projectilespeed = []
                lvl_gen.nmeprojectilesgroup.empty()
                boss.boss_projectile_group.empty()
                boss.b_projectile_speed = []
                lvl_gen.updater()
                started = False
                game_over.game_over()
        if pygame.sprite.spritecollide(consts.hero, lvl_gen.triggergroup, False):
            if lvl == 3:
                lvl_gen.remover(lvl_gen.board.get_cell(
                    list(pygame.sprite.spritecollide(consts.hero, lvl_gen.triggergroup, True))[0].rect[:2]))
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
                consts.hero.end()
                boss.boss_projectile_group.empty()
                boss.b_projectile_speed = []
                thing = ''
                lvl_gen.updater()
                started = False
                record = starsChanger(lvl, current_seconds)
                if current_seconds < starsRecorder.get_seconds(lvl) or starsRecorder.get_seconds(lvl) == 0:
                    starsRecorder.push_record(lvl, 1, record, current_seconds)
                starsRecorder.push_lastRecord(lvl, record, current_seconds)
                game_complete.game_complete()

        if consts.runright or consts.runleft:
            if consts.runright:
                consts.hero.move(consts.xspeed * windows.k ** windows.fullscreen, 0)
            if consts.runleft:
                consts.hero.move(-consts.xspeed * windows.k ** windows.fullscreen, 0)
        else:
            consts.xspeed = 0
        consts.hero.update()
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
