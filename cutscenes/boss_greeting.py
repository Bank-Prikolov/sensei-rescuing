import pygame
import time

from config import MenuGameConsts, GameConsts, CharacterConsts, GameSprites, MenuSprites, WindowsSettings
from items.scenes.dialogue import AnimatedDialogue
from misc import terminate


def boss_greeting_cutscene(character):
    if not WindowsSettings.fullscreen:
        dialogueWaiBossGreeting = AnimatedDialogue(
            (GameConsts.WaiBossGreeting if character == 1 else GameConsts.StrongestBossGreeting),
            79, 1,
            WindowsSettings.width // 2 - 63674 / 79 / 2,
            18)
    else:
        dialogueWaiBossGreeting = AnimatedDialogue(
            (GameConsts.WaiBossGreeting_FS if character == 1 else GameConsts.StrongestBossGreeting_FS),
            79, 1,
            WindowsSettings.width // 2 - 63674 * 1.5 / 79 / 2,
            18 * 1.5)
    CharacterConsts.hero.change_hero('r', CharacterConsts.hero.get_coords())
    GameConsts.lookingright = 1
    list(GameSprites.boss_group)[0].change_act(1, list(GameSprites.boss_group)[0].get_coords())
    turning = False
    counter = 0
    d_counter = 0
    GameConsts.runright = False
    GameConsts.xspeed = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                levelGenerator.updater()
                list(GameSprites.boss_group)[0].change_act(0, list(GameSprites.boss_group)[0].get_coords())
                GameSprites.health_bar.draw(WindowsSettings.screen)
                running = False
                MenuSprites.animatedDialogue.empty()

            if (event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and not GameSprites.nextFrames
                    and turning):
                GameSprites.nextFrames = True

            elif (event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and GameConsts.nextFrames
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
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and GameConsts.nextFrames
                  and dialogueWaiBossGreeting.cur_frame >= dialogueWaiBossGreeting.talksWithBossGreeting[
                      -2]) and turning:
                levelGenerator.updater()
                GameSprites.health_bar.draw(WindowsSettings.screen)
                GameConsts.xspeed = 0
                running = False
                MenuSprites.animatedDialogue.empty()

            if event.type == pygame.WINDOWEXPOSED:
                levelGenerator.rescreen()
                levelGenerator.updater()

        if dialogueWaiBossGreeting.cur_frame == dialogueWaiBossGreeting.talksWithBossGreeting[0]:
            counter += 1
            MenuSprites.animatedDialogue.draw(WindowsSettings.screen)
            if counter == 60:
                list(GameSprites.boss_group)[0].change_act(0, list(GameSprites.boss_group)[0].get_coords())
            if counter == 90:
                turning = True
                GameConsts.nextFrames = True

        if dialogueWaiBossGreeting.cur_frame == dialogueWaiBossGreeting.talksWithBossGreeting[-1]:
            time.sleep(0.6)
            levelGenerator.updater()
            GameSprites.health_bar.draw(WindowsSettings.screen)
            GameConsts.xspeed = 0
            running = False
            MenuSprites.animatedDialogue.empty()

        if (turning or dialogueWaiBossGreeting.cur_frame < dialogueWaiBossGreeting.talksWithBossGreeting[0]
                and d_counter >= 60):
            dialogueWaiBossGreeting.dialogue_update('bg')
            MenuSprites.animatedDialogue.draw(WindowsSettings.screen)
        GameSprites.un_touches.update()
        GameSprites.un_touches.draw(WindowsSettings.screen)
        levelGenerator.get_shadow(*CharacterConsts.hero.get_coords(), *CharacterConsts.hero.get_size())
        GameSprites.shadow_group.draw(WindowsSettings.screen)
        CharacterConsts.hero.update()
        GameSprites.characters.draw(WindowsSettings.screen)
        GameSprites.boss_group.update()
        GameSprites.boss_group.draw(WindowsSettings.screen)
        d_counter += 1
        MenuGameConsts.clock.tick(MenuGameConsts.fps)
        pygame.display.flip()
