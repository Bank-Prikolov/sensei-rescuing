import pygame.surface
import fileManager
import levelGenerator
import game_over
import game_complete
import pause
import consts
import windows
import cutscenes
import starsRecorder
import soundManager
import spriteGroups
from hero import Hero
from processHelper import terminate
from itemChanger import starsChanger, pauseButtonChanger, healthBossBarChanger, heroHeartsChanger
from AI_lvl import  new_lvls

def game_def(lvl, endless=False):
    spriteGroups.boss_projectile_group.empty()
    consts.b_projectile_speed = []
    spriteGroups.nmeprojectilesgroup.empty()
    consts.projectileObj_speed = []
    consts.end_cs = False
    soundManager.game_theme()
    greeting = False
    start_coords, end_coords, mark = levelGenerator.generate_level(lvl, endless=endless)
    character = fileManager.heroImport()[0]
    consts.pause_btn = pauseButtonChanger()
    levelGenerator.updater()
    spriteGroups.characters.empty()
    consts.hero = Hero(*start_coords, windows.k ** windows.fullscreen, character)
    consts.jumping = False
    consts.final_countdown = False
    consts.animend = False
    consts.yspeed = 0
    running = True
    keyboardUnlock = False if lvl == 1 else True
    spriteGroups.characters.draw(windows.screen)
    if not endless:
        if lvl == 1:
            levelGenerator.remover((1, 10), block='k')
    thing = ''
    doorCounter = 0
    healthBossBar = healthBossBarChanger()
    heroHearts = heroHeartsChanger()
    cheatPanel = False  # cheats
    consts.bossHit = 0
    consts.heroHit = 0
    consts.hitNow = False
    consts.tmpHit = 0
    consts.heroHP = 3
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)
    started = True
    current_seconds = 0
    spriteGroups.projectilesgroup.empty()
    checkLevel = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == timer_event and started:
                current_seconds += 1
            elif event.type == pygame.KEYDOWN and keyboardUnlock:
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
                    if not (consts.jumping or consts.falling):
                        consts.yspeed = 7
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
                    if (not (consts.jumping or consts.falling)) or cheatPanel:
                        consts.jumping = True
                        consts.yspeed = -9 - 2 * cheatPanel
                        if consts.lookingright:
                            consts.hero.change_hero('jumpr', consts.hero.get_coords())
                        else:
                            consts.hero.change_hero('jumpl', consts.hero.get_coords())
                elif event.key == pygame.K_w:
                    if pygame.sprite.spritecollide(consts.hero, spriteGroups.finale, False):
                        if not endless:
                            thing = ''
                            consts.hero.end()
                            levelGenerator.updater()
                            started = False
                            record = starsChanger(lvl, current_seconds)
                            if current_seconds < starsRecorder.get_seconds(lvl) or starsRecorder.get_seconds(lvl) == 0:
                                starsRecorder.push_record(lvl, 1, record, current_seconds)
                                starsRecorder.push_lastRecord(lvl, record, current_seconds)
                            soundManager.stop_playback()
                            game_complete.game_complete()
                        else:
                            doorCounter = 0
                            new_lvls()
                            spriteGroups.projectilesgroup.empty()
                            spriteGroups.nmeprojectilesgroup.empty()
                            consts.projectileObj_speed = []
                            spriteGroups.boss_projectile_group.empty()
                            consts.b_projectile_speed = []
                            start_coords, end_coords, mark = levelGenerator.generate_level(1, endless=endless)
                            levelGenerator.updater()
                            consts.hero.set_coords(*start_coords)
                    else:
                        if consts.lookingright:
                            consts.shooting = consts.hero.projectile_speed * windows.k ** windows.fullscreen
                        else:
                            consts.shooting = -consts.hero.projectile_speed * windows.k ** windows.fullscreen
                        consts.hero.shoot(consts.shooting)
            elif event.type == pygame.WINDOWEXPOSED:
                if consts.lookingright:
                    consts.hero.change_hero('sr', consts.hero.get_coords())
                else:
                    consts.hero.change_hero('sl', consts.hero.get_coords())
                levelGenerator.rescreen()
                levelGenerator.updater()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    consts.runright = False
                elif event.key == pygame.K_a:
                    consts.runleft = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5 and consts.cheatOn:  # cheats
                    cheatPanel = not cheatPanel
                    consts.hero.xs = 3 * 5 ** cheatPanel
                    consts.hero.projectile_speed = 8 * 2 ** cheatPanel
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or
                    (event.type == pygame.USEREVENT and event.button == consts.pause_btn)):
                consts.xspeed = 0
                predpause = consts.hero.get_coords()
                proj = consts.hero.projectilespeed
                pause.pause(current_seconds, len(list(spriteGroups.sloniks)), lvl, thing, endless)
                spriteGroups.characters.empty()
                consts.hero = Hero(*predpause, windows.k ** windows.fullscreen, character)
                consts.hero.projectilespeed = proj
                if consts.lookingright:
                    consts.hero.change_hero('sr', predpause)
                else:
                    consts.hero.change_hero('sl', predpause)
                levelGenerator.rescreen()
                levelGenerator.updater()

            consts.pause_btn.handle_event(event, consts.volS)

        if pygame.sprite.spritecollide(consts.hero, spriteGroups.changegroup, False):
            soundManager.teleport_sound()
            doorCounter = 0
            if thing == '':
                thing = 1
            else:
                thing += 1
            spriteGroups.projectilesgroup.empty()
            spriteGroups.nmeprojectilesgroup.empty()
            consts.projectileObj_speed = []
            spriteGroups.boss_projectile_group.empty()
            consts.b_projectile_speed = []
            start_coords, end_coords, mark = levelGenerator.generate_level(lvl + thing / 10, endless=endless)
            consts.hero.set_coords(*start_coords)
            if lvl == 3 and thing == 2:
                checkLevel = True
                soundManager.stop_playback()
                soundManager.boss_theme()
            consts.hero.projectilespeed = []
            windows.screen.fill('#000000')
            levelGenerator.updater()
        levelGenerator.get_shadow(*consts.hero.get_coords(), *consts.hero.get_size())
        spriteGroups.shadowgroup.draw(windows.screen)

        if spriteGroups.projectilesgroup:
            for sprite in range(len(spriteGroups.projectilesgroup)):
                pygame.draw.rect(windows.screen, (36, 34, 52), list(spriteGroups.projectilesgroup)[sprite].rect)
                list(spriteGroups.projectilesgroup)[sprite].rect = list(spriteGroups.projectilesgroup)[
                    sprite].rect.move(
                    consts.hero.projectilespeed[sprite], 0)
                if pygame.sprite.spritecollide(list(spriteGroups.projectilesgroup)[sprite], spriteGroups.sloniks,
                                               False):
                    if (pygame.sprite.spritecollide(list(spriteGroups.projectilesgroup)[sprite],
                                                    spriteGroups.sloniks, False)[0].get_hit(
                        consts.hero.get_coords()[0]) == 0
                            or cheatPanel):
                        levelGenerator.remover(levelGenerator.board.get_cell(list(
                            pygame.sprite.spritecollide(list(spriteGroups.projectilesgroup)[sprite],
                                                        spriteGroups.sloniks, True))[
                                                                                 0].rect[:2]))
                    consts.hero.projectilespeed.pop(sprite)
                    list(spriteGroups.projectilesgroup)[sprite].kill()
                    break

                if pygame.sprite.spritecollide(list(spriteGroups.projectilesgroup)[sprite], spriteGroups.boss_group,
                                               False):
                    if not consts.final_countdown:
                        if (pygame.sprite.spritecollide(list(spriteGroups.projectilesgroup)[sprite],
                                                        spriteGroups.boss_group, False)[0].get_hit() <= 0):
                            consts.final_countdown = True
                            spriteGroups.sloniks.empty()
                            consts.projectileObj_speed = []
                            bo55 = pygame.sprite.spritecollide(list(spriteGroups.projectilesgroup)[sprite],
                                                               spriteGroups.boss_group, False)[0]
                            bo55.change_act(8, bo55.get_coords())

                            spriteGroups.nmeprojectilesgroup.empty()
                            soundManager.stop_playback()
                            soundManager.boss_lose_sound()
                            spriteGroups.boss_projectile_group.empty()
                            levelGenerator.updater()
                        consts.hero.projectilespeed.pop(sprite)
                        list(spriteGroups.projectilesgroup)[sprite].kill()
                        break

                if (pygame.sprite.spritecollide(list(spriteGroups.projectilesgroup)[sprite], spriteGroups.toches, False)
                        or pygame.sprite.spritecollide(list(spriteGroups.projectilesgroup)[sprite],
                                                       spriteGroups.anothertoches, False)):
                    consts.hero.projectilespeed.pop(sprite)
                    list(spriteGroups.projectilesgroup)[sprite].kill()
                    break

        if spriteGroups.nmeprojectilesgroup:
            for sprite in range(len(spriteGroups.nmeprojectilesgroup)):
                pygame.draw.rect(windows.screen, (36, 34, 52), list(spriteGroups.nmeprojectilesgroup)[sprite].rect)
                list(spriteGroups.nmeprojectilesgroup)[sprite].rect = list(spriteGroups.nmeprojectilesgroup)[
                    sprite].rect.move(
                    consts.projectileObj_speed[sprite][0], 0)
                if pygame.sprite.spritecollide(list(spriteGroups.nmeprojectilesgroup)[sprite], spriteGroups.characters,
                                               False) and not cheatPanel:
                    soundManager.hero_take_hit_sound()
                    consts.heroHit += 2
                    consts.hitNow = True
                    consts.tmpHit = 5
                    if consts.hero.get_hit() == 0:
                        if not (lvl == 3 and thing == 2):
                            thing = ''
                            consts.hero.end()
                            consts.projectileObj_speed = []
                            spriteGroups.nmeprojectilesgroup.empty()
                            levelGenerator.updater()
                            spriteGroups.boss_projectile_group.empty()
                            consts.b_projectile_speed = []
                            started = False
                            soundManager.stop_playback()
                            game_over.game_over(endless)
                        else:
                            spriteGroups.projectilesgroup.empty()
                            spriteGroups.nmeprojectilesgroup.empty()
                            consts.projectileObj_speed = []
                            spriteGroups.boss_projectile_group.empty()
                            consts.b_projectile_speed = []
                            start_coords, end_coords, mark = levelGenerator.generate_level(lvl + thing / 10, endless=endless)
                            consts.hero.set_coords(*start_coords)
                            consts.hero.move(0, -8)
                            consts.runleft = False
                            consts.runright = False
                            consts.jumping = False
                            consts.falling = False
                            consts.hero.rect.move(0, -16)
                            consts.heroHP = 3
                            soundManager.hero_take_hit_sound()
                            consts.heroHit = 0
                            consts.bossHit = 0
                            soundManager.stop_playback()
                            soundManager.hero_lose_boss_sound()
                            consts.hero.projectilespeed = []
                            cutscenes.boss_win_cutscene()
                            windows.screen.fill('#000000')
                            levelGenerator.updater()
                        break
                    else:
                        consts.projectileObj_speed.pop(sprite)
                        list(spriteGroups.nmeprojectilesgroup)[sprite].kill()
                        break
                if (pygame.sprite.spritecollide(list(spriteGroups.nmeprojectilesgroup)[sprite], spriteGroups.toches,
                                                False)
                        or pygame.sprite.spritecollide(list(spriteGroups.nmeprojectilesgroup)[sprite],
                                                       spriteGroups.anothertoches, False)):
                    consts.projectileObj_speed.pop(sprite)
                    list(spriteGroups.nmeprojectilesgroup)[sprite].kill()
                    break

        if spriteGroups.boss_projectile_group:
            for sprite in range(len(spriteGroups.boss_projectile_group)):
                list(spriteGroups.boss_projectile_group)[sprite].rect = list(spriteGroups.boss_projectile_group)[
                    sprite].rect.move(
                    consts.b_projectile_speed[sprite][0][0], consts.b_projectile_speed[sprite][0][1])
                if pygame.sprite.spritecollide(list(spriteGroups.boss_projectile_group)[sprite],
                                               spriteGroups.characters,
                                               False) and not cheatPanel:
                    soundManager.hero_take_hit_sound()
                    consts.heroHit += 2
                    consts.hitNow = True
                    consts.tmpHit = 5
                    if consts.heroHit == 6:
                        consts.heroHit = 0
                        consts.bossHit = 0
                        soundManager.stop_playback()
                        soundManager.hero_lose_boss_sound()
                    if consts.hero.get_hit() == 0:
                        consts.yspeed = 0
                        spriteGroups.projectilesgroup.empty()
                        spriteGroups.nmeprojectilesgroup.empty()
                        consts.projectileObj_speed = []
                        spriteGroups.boss_projectile_group.empty()
                        consts.b_projectile_speed = []

                        start_coords, end_coords, mark = levelGenerator.generate_level(lvl + thing / 10, endless=endless)
                        consts.hero.set_coords(*start_coords)
                        consts.runleft = False
                        consts.runright = False
                        consts.jumping = False
                        consts.falling = False
                        consts.hero.projectilespeed = []
                        cutscenes.boss_win_cutscene()
                        windows.screen.fill('#000000')
                        consts.heroHP = 3
                        levelGenerator.updater()
                        break
                    else:
                        pygame.draw.rect(windows.screen, (36, 34, 52), (
                            list(spriteGroups.boss_projectile_group)[sprite].rect[0] -
                            consts.b_projectile_speed[sprite][0][0],
                            list(spriteGroups.boss_projectile_group)[sprite].rect[1] -
                            consts.b_projectile_speed[sprite][0][1],
                            *list(spriteGroups.boss_projectile_group)[sprite].rect[2:]))
                        list(spriteGroups.boss_projectile_group)[sprite].kill()
                        consts.b_projectile_speed.pop(sprite)
                        break
                else:
                    if (pygame.sprite.spritecollide(list(spriteGroups.boss_projectile_group)[sprite],
                                                    spriteGroups.xwalls,
                                                    False)
                            or pygame.sprite.spritecollide(
                                list(spriteGroups.boss_projectile_group)[sprite], spriteGroups.thorngroup, False)):

                        list(spriteGroups.boss_projectile_group)[sprite].rect = \
                            list(spriteGroups.boss_projectile_group)[
                                sprite].rect.move(
                                -consts.b_projectile_speed[sprite][0][0], -consts.b_projectile_speed[sprite][0][1])
                        if consts.b_projectile_speed[sprite][1] == 1:
                            pygame.draw.rect(windows.screen, (36, 34, 52), (
                                list(spriteGroups.boss_projectile_group)[sprite].rect))
                            list(spriteGroups.boss_projectile_group)[sprite].kill()
                            consts.b_projectile_speed.pop(sprite)
                            break
                        else:
                            pygame.draw.rect(windows.screen, (36, 34, 52), (
                                list(spriteGroups.boss_projectile_group)[sprite].rect))
                            consts.b_projectile_speed[sprite] = ((consts.b_projectile_speed[sprite][0][0],
                                                                  -consts.b_projectile_speed[sprite][0][1]),
                                                                 consts.b_projectile_speed[sprite][1] + 1)

                    elif pygame.sprite.spritecollide(list(spriteGroups.boss_projectile_group)[sprite],
                                                     spriteGroups.ywalls,
                                                     False):
                        list(spriteGroups.boss_projectile_group)[sprite].rect = \
                            list(spriteGroups.boss_projectile_group)[
                                sprite].rect.move(
                                -consts.b_projectile_speed[sprite][0][0], -consts.b_projectile_speed[sprite][0][1])
                        if consts.b_projectile_speed[sprite][1] == 1:
                            pygame.draw.rect(windows.screen, (36, 34, 52), (
                                list(spriteGroups.boss_projectile_group)[sprite].rect))
                            list(spriteGroups.boss_projectile_group)[sprite].kill()
                            consts.b_projectile_speed.pop(sprite)
                            break
                        else:
                            pygame.draw.rect(windows.screen, (36, 34, 52), (
                                list(spriteGroups.boss_projectile_group)[sprite].rect))
                            consts.b_projectile_speed[sprite] = ((-consts.b_projectile_speed[sprite][0][0],
                                                                  consts.b_projectile_speed[sprite][0][1]),
                                                                 consts.b_projectile_speed[sprite][1] + 1)
                    else:
                        pygame.draw.rect(windows.screen, (36, 34, 52), (
                            list(spriteGroups.boss_projectile_group)[sprite].rect[0] -
                            consts.b_projectile_speed[sprite][0][0],
                            list(spriteGroups.boss_projectile_group)[sprite].rect[1] -
                            consts.b_projectile_speed[sprite][0][1],
                            *list(spriteGroups.boss_projectile_group)[sprite].rect[2:]))
                list(spriteGroups.boss_projectile_group)[sprite].update()

        if not cheatPanel:
            if (pygame.sprite.spritecollide(consts.hero, spriteGroups.thorngroup, False)
                    or pygame.sprite.spritecollide(consts.hero, spriteGroups.sloniks, False)
                    or pygame.sprite.spritecollide(consts.hero, spriteGroups.boss_group, False)):
                if pygame.sprite.spritecollide(consts.hero, spriteGroups.boss_group, False) and consts.final_countdown:
                    pass
                else:
                    if lvl == 3 and thing == 2:
                        consts.final_countdown = False
                        consts.yspeed = 0
                        spriteGroups.projectilesgroup.empty()
                        spriteGroups.nmeprojectilesgroup.empty()
                        consts.projectileObj_speed = []
                        spriteGroups.boss_projectile_group.empty()
                        consts.b_projectile_speed = []
                        start_coords, end_coords, mark = levelGenerator.generate_level(lvl + thing / 10, endless=endless)
                        consts.hero.set_coords(*start_coords)
                        consts.hero.move(0, -8)
                        consts.runleft = False
                        consts.runright = False
                        consts.jumping = False
                        consts.falling = False
                        consts.hero.rect.move(0, -16)
                        consts.heroHP = 3
                        soundManager.hero_take_hit_sound()
                        consts.heroHit = 0
                        consts.bossHit = 0
                        soundManager.stop_playback()
                        soundManager.hero_lose_boss_sound()
                        consts.hero.projectilespeed = []
                        cutscenes.boss_win_cutscene()
                        windows.screen.fill('#000000')
                        levelGenerator.updater()
                    else:
                        thing = ''
                        consts.hero.end()
                        consts.projectileObj_speed = []
                        spriteGroups.nmeprojectilesgroup.empty()
                        levelGenerator.updater()
                        spriteGroups.boss_projectile_group.empty()
                        consts.b_projectile_speed = []
                        started = False
                        soundManager.stop_playback()
                        game_over.game_over(endless)
        if pygame.sprite.spritecollide(consts.hero, spriteGroups.triggergroup, False):
            if lvl == 3:
                levelGenerator.remover(levelGenerator.board.get_cell(
                    list(pygame.sprite.spritecollide(consts.hero, spriteGroups.triggergroup, True))[0].rect[:2]))
                spriteGroups.toches.remove(levelGenerator.get_key(spriteGroups.toches.spritedict,
                                                                  pygame.rect.Rect(
                                                                      int(levelGenerator.board.rev_get_cell((11, 10))[
                                                                              0]),
                                                                      int(levelGenerator.board.rev_get_cell((11, 10))[
                                                                              1]),
                                                                      levelGenerator.board.get_size(),
                                                                      levelGenerator.board.get_size())))
                soundManager.get_key_sound()
                levelGenerator.remover((11, 10))

        if not spriteGroups.boss_group or consts.end_cs:
            if lvl == 3 and thing == 2:
                list(spriteGroups.boss_group)[0].cutscene = 1
                cutscenes.boss_lose_cutscene(character)
                list(spriteGroups.boss_group)[0].cutscene = 0
                consts.hero.end()
                spriteGroups.boss_projectile_group.empty()
                consts.b_projectile_speed = []
                thing = ''
                if not endless:
                    started = False
                    record = starsChanger(lvl, current_seconds)
                    if current_seconds < starsRecorder.get_seconds(lvl) or starsRecorder.get_seconds(lvl) == 0:
                        starsRecorder.push_record(lvl, 1, record, current_seconds)
                    starsRecorder.push_lastRecord(lvl, record, current_seconds)
                    soundManager.stop_playback()
                    game_complete.game_complete()
            elif not spriteGroups.sloniks:
                if end_coords:
                    if doorCounter == 0:
                        if mark == 'f':
                            levelGenerator.remover(end_coords, 'F')
                            soundManager.door_open_sound()
                            doorCounter += 1
                        elif mark == 'c':
                            levelGenerator.remover(end_coords, 'C')
                            soundManager.tp_activated()
                            doorCounter += 1
                else:
                    if lvl == 3 and thing == 1:
                        levelGenerator.remover((9, 6),  'S')

        if consts.runright or consts.runleft:
            if consts.runright:
                consts.hero.move(consts.xspeed * windows.k ** windows.fullscreen, 0)
            if consts.runleft:
                consts.hero.move(-consts.xspeed * windows.k ** windows.fullscreen, 0)
        else:
            consts.xspeed = 0

        consts.pause_btn.check_hover(pygame.mouse.get_pos())
        consts.pause_btn.drawPauseBtn(windows.screen, consts.hitNow)
        if consts.tmpHit == 0:
            consts.hitNow = False
        else:
            consts.tmpHit -= 1
        spriteGroups.untouches.update()
        spriteGroups.boss_group.update()
        spriteGroups.boss_group.draw(windows.screen)
        spriteGroups.telep_group.update()
        spriteGroups.telep_group.draw(windows.screen)
        spriteGroups.untouches.draw(windows.screen)
        levelGenerator.spriteGroups.boss_projectile_group.draw(windows.screen)
        spriteGroups.nmeprojectilesgroup.draw(windows.screen)
        spriteGroups.hleb.update()
        spriteGroups.hleb.draw(windows.screen)
        consts.hero.update()
        spriteGroups.breakgroup.draw(windows.screen)
        spriteGroups.finale.draw(windows.screen)
        spriteGroups.projectilesgroup.draw(windows.screen)
        spriteGroups.characters.draw(windows.screen)
        spriteGroups.sloniks.update()
        spriteGroups.sloniks.draw(windows.screen)
        heroHearts.update(consts.heroHit)
        spriteGroups.hero_health.draw(windows.screen)
        if checkLevel:
            healthBossBar.update(consts.bossHit)
            spriteGroups.health_bar.draw(windows.screen)
        spriteGroups.triggergroup.draw(windows.screen)
        pygame.draw.rect(windows.screen, '#000000',
                         (0, 0, windows.otstupx ** windows.fullscreen, windows.fullsize[1] ** windows.fullscreen))
        pygame.draw.rect(windows.screen, '#000000',
                         (windows.fullsize[0] - windows.otstupx, 0, windows.fullsize[0] ** windows.fullscreen,
                          windows.fullsize[1] ** windows.fullscreen))
        if not endless:
            if lvl == 1 and consts.hero.get_coords() == start_coords and not keyboardUnlock:
                cutscenes.hleb_greeting_cutscene(character)
                keyboardUnlock = True
                levelGenerator.remover((1, 10), block='.')
                levelGenerator.remover((1, 10), block='k')
        else:
            keyboardUnlock = True

        if lvl == 3 and thing == 2 and not greeting:
            list(spriteGroups.boss_group)[0].cutscene = 1
            cutscenes.boss_greeting_cutscene(character)
            list(spriteGroups.boss_group)[0].cutscene = 0
            greeting = True

        consts.clock.tick(consts.fps)
        pygame.display.flip()
