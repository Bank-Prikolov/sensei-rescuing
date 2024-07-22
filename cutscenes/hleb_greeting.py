import pygame
import time
from config import consts
import spriteGroups
import levelGenerator
from misc.utils import terminate
from items.scenes.dialogue import AnimatedDialogue


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






