import pygame
import time
import windows
import consts
import game_over
import spriteGroups
import soundManager
import levelGenerator
from itemCreator import Button
from processHelper import terminate, load_image
from cutsceneAnimator import AnimatedError, AnimatedDialogue


def hleb_greeting_cutscene(character):
    if not windows.fullscreen:
        dialogueWaiHleb = AnimatedDialogue((consts.WaiHleb if character == 1 else consts.StrongestHleb),
                                           865, 1,
                                           windows.width // 2 - 697190 / 865 / 2,
                                           18)
    else:
        dialogueWaiHleb = AnimatedDialogue((consts.WaiHleb_FS if character == 1 else consts.StrongestHleb_FS),
                                           865, 1,
                                           windows.width // 2 - 697190 * 1.5 / 865 / 2,
                                           18 * 1.5)
    running = True
    consts.hero.change_hero('r', consts.hero.get_coords())
    consts.runright = True
    consts.xspeed = 1.6
    consts.lookingright = 1
    dialogueStart = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                levelGenerator.updater()
                consts.xspeed = 0
                running = False
                spriteGroups.animatedDialogue.empty()

            if event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and not consts.nextFrames:
                consts.nextFrames = True

            elif (event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and consts.nextFrames
                  and dialogueWaiHleb.cur_frame <= dialogueWaiHleb.talksWithHleb[-2]):
                dialogueWaiHleb.cur_frame = dialogueWaiHleb.talksWithHleb[dialogueWaiHleb.tmp] + 1
                dialogueWaiHleb.tmp += 1

            elif (event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and consts.nextFrames
                  and dialogueWaiHleb.cur_frame >= dialogueWaiHleb.talksWithHleb[-2]):
                levelGenerator.updater()
                consts.xspeed = 0
                running = False
                spriteGroups.animatedDialogue.empty()

            if event.type == pygame.WINDOWEXPOSED:
                levelGenerator.rescreen()
                levelGenerator.updater()

        if dialogueWaiHleb.cur_frame == dialogueWaiHleb.talksWithHleb[-1]:
            time.sleep(0.6)
            levelGenerator.updater()
            consts.xspeed = 0
            running = False
            spriteGroups.animatedDialogue.empty()

        if consts.hero.get_coords()[0] <= (154 if not windows.fullscreen else 425):
            consts.hero.move(consts.xspeed * windows.k ** windows.fullscreen, 0)
        else:
            consts.xspeed = 0
            consts.runright = False
            dialogueStart = True

        spriteGroups.sloniks.update()
        spriteGroups.sloniks.draw(windows.screen)
        spriteGroups.breakgroup.draw(windows.screen)
        spriteGroups.hleb.update()
        spriteGroups.hleb.draw(windows.screen)
        levelGenerator.get_shadow(*consts.hero.get_coords(), *consts.hero.get_size())
        spriteGroups.shadowgroup.draw(windows.screen)
        spriteGroups.untouches.update()
        spriteGroups.untouches.draw(windows.screen)
        if dialogueStart:
            dialogueWaiHleb.dialogue_update('hg')
            spriteGroups.animatedDialogue.draw(windows.screen)
        consts.hero.update()
        spriteGroups.characters.draw(windows.screen)
        consts.clock.tick(consts.fps)
        pygame.display.flip()


def boss_greeting_cutscene(character):
    if not windows.fullscreen:
        dialogueWaiBossGreeting = AnimatedDialogue(
            (consts.WaiBossGreeting if character == 1 else consts.StrongestBossGreeting),
            79, 1,
            windows.width // 2 - 63674 / 79 / 2,
            18)
    else:
        dialogueWaiBossGreeting = AnimatedDialogue(
            (consts.WaiBossGreeting_FS if character == 1 else consts.StrongestBossGreeting_FS),
            79, 1,
            windows.width // 2 - 63674 * 1.5 / 79 / 2,
            18 * 1.5)
    consts.hero.change_hero('r', consts.hero.get_coords())
    consts.lookingright = 1
    list(spriteGroups.boss_group)[0].change_act(1, list(spriteGroups.boss_group)[0].get_coords())
    turning = False
    counter = 0
    d_counter = 0
    consts.runright = False
    consts.xspeed = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                levelGenerator.updater()
                list(spriteGroups.boss_group)[0].change_act(0, list(spriteGroups.boss_group)[0].get_coords())
                spriteGroups.health_bar.draw(windows.screen)
                running = False
                spriteGroups.animatedDialogue.empty()

            if (event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and not consts.nextFrames
                    and turning):
                consts.nextFrames = True

            elif (event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and consts.nextFrames
                  and dialogueWaiBossGreeting.cur_frame <= dialogueWaiBossGreeting.talksWithBossGreeting[
                      -2]) and (
                    turning or dialogueWaiBossGreeting.cur_frame < dialogueWaiBossGreeting.talksWithBossGreeting[0]
                    and d_counter >= 60):
                if (dialogueWaiBossGreeting.cur_frame < dialogueWaiBossGreeting.talksWithBossGreeting[0]
                        and d_counter >= 60):
                    dialogueWaiBossGreeting.cur_frame = dialogueWaiBossGreeting.talksWithBossGreeting[0] - 1
                else:
                    dialogueWaiBossGreeting.cur_frame = dialogueWaiBossGreeting.talksWithBossGreeting[
                                                            dialogueWaiBossGreeting.tmp] + 1
                dialogueWaiBossGreeting.tmp += 1

            elif (event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and consts.nextFrames
                  and dialogueWaiBossGreeting.cur_frame >= dialogueWaiBossGreeting.talksWithBossGreeting[
                      -2]) and turning:
                levelGenerator.updater()
                spriteGroups.health_bar.draw(windows.screen)
                consts.xspeed = 0
                running = False
                spriteGroups.animatedDialogue.empty()

            if event.type == pygame.WINDOWEXPOSED:
                levelGenerator.rescreen()
                levelGenerator.updater()

        if dialogueWaiBossGreeting.cur_frame == dialogueWaiBossGreeting.talksWithBossGreeting[0]:
            counter += 1
            spriteGroups.animatedDialogue.draw(windows.screen)
            if counter == 60:
                list(spriteGroups.boss_group)[0].change_act(0, list(spriteGroups.boss_group)[0].get_coords())
            if counter == 90:
                turning = True
                consts.nextFrames = True

        if dialogueWaiBossGreeting.cur_frame == dialogueWaiBossGreeting.talksWithBossGreeting[-1]:
            time.sleep(0.6)
            levelGenerator.updater()
            spriteGroups.health_bar.draw(windows.screen)
            consts.xspeed = 0
            running = False
            spriteGroups.animatedDialogue.empty()

        if (turning or dialogueWaiBossGreeting.cur_frame < dialogueWaiBossGreeting.talksWithBossGreeting[0]
                and d_counter >= 60):
            dialogueWaiBossGreeting.dialogue_update('bg')
            spriteGroups.animatedDialogue.draw(windows.screen)
        spriteGroups.untouches.update()
        spriteGroups.untouches.draw(windows.screen)
        levelGenerator.get_shadow(*consts.hero.get_coords(), *consts.hero.get_size())
        spriteGroups.shadowgroup.draw(windows.screen)
        consts.hero.update()
        spriteGroups.characters.draw(windows.screen)
        spriteGroups.boss_group.update()
        spriteGroups.boss_group.draw(windows.screen)
        d_counter += 1
        consts.clock.tick(consts.fps)
        pygame.display.flip()


def boss_win_cutscene():
    field = AnimatedError(load_image(fr"cutscenes\boss-win\boss-win-field-obj.png"), 2, 1,
                          windows.width // 2 - 1290 / 4,
                          windows.height // 2 - 448 / 2)
    yes_btn = Button(field.x + 645 / 2 - 118, field.y + 374, 92, 38,
                     fr"cutscenes\boss-win\default-yes-btn.png",
                     fr"cutscenes\boss-win\hover-yes-btn.png",
                     "",
                     r"data\sounds\revive-sound.mp3")
    no_btn = Button(field.x + 645 / 2 + 20, field.y + 374, 92, 38,
                    fr"cutscenes\boss-win\default-no-btn.png",
                    fr"cutscenes\boss-win\hover-no-btn.png")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.USEREVENT and event.button == yes_btn:
                running = False
                spriteGroups.animatedError.empty()
                soundManager.boss_theme()

            if event.type == pygame.USEREVENT and event.button == no_btn:
                spriteGroups.animatedError.empty()
                game_over.game_over()

            if event.type == pygame.WINDOWEXPOSED:
                levelGenerator.rescreen()
                levelGenerator.updater()

            for button in [yes_btn, no_btn]:
                button.handle_event(event, consts.volS)

        consts.backgrBossWin.draw(windows.screen)
        field.update()
        spriteGroups.animatedError.draw(windows.screen)

        for button in [yes_btn, no_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()


def boss_lose_cutscene(character):
    if not windows.fullscreen:
        dialogueWaiBossLose = AnimatedDialogue(
            (consts.WaiBossEnding if character == 1 else consts.StrongestBossEnding),
            171, 1,
            windows.width // 2 - 137826 / 171 / 2,
            18)
    else:
        dialogueWaiBossLose = AnimatedDialogue(
            (consts.WaiBossEnding_FS if character == 1 else consts.StrongestBossEnding_FS),
            171, 1,
            windows.width // 2 - 137826 * 1.5 / 171 / 2,
            18 * 1.5)
    consts.runright = False
    consts.runleft = False
    consts.xspeed = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                levelGenerator.updater()
                running = False
                spriteGroups.animatedDialogue.empty()

            if event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and not consts.nextFrames:
                consts.nextFrames = True

            elif (event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and consts.nextFrames
                  and dialogueWaiBossLose.cur_frame <= dialogueWaiBossLose.talksWithBossEnding[-2]):
                dialogueWaiBossLose.cur_frame = dialogueWaiBossLose.talksWithBossEnding[dialogueWaiBossLose.tmp] + 1
                dialogueWaiBossLose.tmp += 1

            elif (event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and consts.nextFrames
                  and dialogueWaiBossLose.cur_frame >= dialogueWaiBossLose.talksWithBossEnding[-2]):
                levelGenerator.updater()
                consts.xspeed = 0
                running = False
                spriteGroups.animatedDialogue.empty()

            if event.type == pygame.WINDOWEXPOSED:
                levelGenerator.rescreen()
                levelGenerator.updater()

        if dialogueWaiBossLose.cur_frame == dialogueWaiBossLose.talksWithBossEnding[-1]:
            time.sleep(0.6)
            levelGenerator.updater()
            consts.xspeed = 0
            running = False
            spriteGroups.animatedDialogue.empty()

        if dialogueWaiBossLose.cur_frame == dialogueWaiBossLose.talksWithBossEnding[-2]:
            time.sleep(0.6)
            levelGenerator.updater()
            consts.xspeed = 0
            running = False
            spriteGroups.animatedDialogue.empty()

        spriteGroups.untouches.update()
        spriteGroups.untouches.draw(windows.screen)
        levelGenerator.get_shadow(*consts.hero.get_coords(), *consts.hero.get_size())
        spriteGroups.shadowgroup.draw(windows.screen)
        consts.hero.update()
        spriteGroups.characters.draw(windows.screen)
        dialogueWaiBossLose.dialogue_update('be')
        spriteGroups.breakgroup.draw(windows.screen)
        spriteGroups.animatedDialogue.draw(windows.screen)
        spriteGroups.boss_group.update()
        spriteGroups.boss_group.draw(windows.screen)
        consts.clock.tick(consts.fps)
        pygame.display.flip()
