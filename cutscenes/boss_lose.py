import pygame
import time

from config import MenuGameConsts, GameConsts, CharacterConsts, GameSprites, MenuSprites, WindowsSettings
from items.scenes.dialogue import AnimatedDialogue
from misc import terminate


def boss_lose_cutscene(character):
    if not WindowsSettings.fullscreen:
        dialogueWaiBossLose = AnimatedDialogue(
            (GameConsts.WaiBossEnding if character == 1 else GameConsts.StrongestBossEnding),
            171, 1,
            WindowsSettings.width // 2 - 137826 / 171 / 2,
            18)
    else:
        dialogueWaiBossLose = AnimatedDialogue(
            (GameConsts.WaiBossEnding_FS if character == 1 else GameConsts.StrongestBossEnding_FS),
            171, 1,
            WindowsSettings.width // 2 - 137826 * 1.5 / 171 / 2,
            18 * 1.5)
    GameConsts.runright = False
    GameConsts.runleft = False
    GameConsts.xspeed = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                levelGenerator.updater()
                running = False
                MenuSprites.animatedDialogue.empty()

            if (event.type == pygame.KEYDOWN
                    and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and not GameConsts.nextFrames):
                GameConsts.nextFrames = True

            elif (event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and GameConsts.nextFrames
                  and dialogueWaiBossLose.cur_frame <= dialogueWaiBossLose.talksWithBossEnding[-2]):
                dialogueWaiBossLose.cur_frame = dialogueWaiBossLose.talksWithBossEnding[dialogueWaiBossLose.tmp] + 1
                dialogueWaiBossLose.tmp += 1

            elif (event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and GameConsts.nextFrames
                  and dialogueWaiBossLose.cur_frame >= dialogueWaiBossLose.talksWithBossEnding[-2]):
                levelGenerator.updater()
                GameConsts.xspeed = 0
                running = False
                MenuSprites.animatedDialogue.empty()

            if event.type == pygame.WINDOWEXPOSED:
                levelGenerator.rescreen()
                levelGenerator.updater()

        if dialogueWaiBossLose.cur_frame == dialogueWaiBossLose.talksWithBossEnding[-1]:
            time.sleep(0.6)
            levelGenerator.updater()
            GameConsts.xspeed = 0
            running = False
            MenuSprites.animatedDialogue.empty()

        if dialogueWaiBossLose.cur_frame == dialogueWaiBossLose.talksWithBossEnding[-2]:
            time.sleep(0.6)
            levelGenerator.updater()
            GameConsts.xspeed = 0
            running = False
            MenuSprites.animatedDialogue.empty()

        GameSprites.un_touches.update()
        GameSprites.un_touches.draw(WindowsSettings.screen)
        levelGenerator.get_shadow(*CharacterConsts.hero.get_coords(), *CharacterConsts.hero.get_size())
        GameSprites.shadow_group.draw(WindowsSettings.screen)
        CharacterConsts.hero.update()
        GameSprites.characters.draw(WindowsSettings.screen)
        dialogueWaiBossLose.dialogue_update('be')
        GameSprites.break_group.draw(WindowsSettings.screen)
        MenuSprites.animatedDialogue.draw(WindowsSettings.screen)
        GameSprites.boss_group.update()
        GameSprites.boss_group.draw(WindowsSettings.screen)
        MenuGameConsts.clock.tick(MenuGameConsts.fps)
        pygame.display.flip()
