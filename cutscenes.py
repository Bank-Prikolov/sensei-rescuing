import pygame
import windows
import consts
import game_over
import spriteGroups
import soundManager
import levelGenerator
from itemCreator import Button
from processHelper import terminate, load_image
from cutsceneAnimator import AnimatedError, AnimatedDialogue


def hleb_greeting_cutscene():
    dialogueWaiHleb = AnimatedDialogue(consts.WaiHleb,
                                       865, 1,
                                       windows.width // 2 - 697190 / 865 / 2,
                                       18)
    running = True
    consts.hero.change_hero('r', consts.hero.get_coords())
    consts.runright = True
    consts.xspeed = 2
    consts.lookingright = 1
    dialogueStart = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        if consts.hero.get_coords()[0] != 154:
            consts.hero.move(consts.xspeed * windows.k ** windows.fullscreen, 0)
        else:
            consts.xspeed = 0
            consts.runright = False
            dialogueStart = True

        if dialogueStart:
            dialogueWaiHleb.hleb_greeting_update()
            spriteGroups.animatedDialogue.draw(windows.screen)

        spriteGroups.hleb.update()
        spriteGroups.hleb.draw(windows.screen)
        levelGenerator.get_shadow(*consts.hero.get_coords(), *consts.hero.get_size())
        spriteGroups.shadowgroup.draw(windows.screen)
        consts.hero.update()
        spriteGroups.characters.draw(windows.screen)
        consts.clock.tick(consts.fps)
        pygame.display.flip()


def boss_greeting_cutscene():
    dialogueWaiBossGreeting = AnimatedDialogue(consts.WaiBossGreeting,
                                       865, 1,
                                       windows.width // 2 - 697190 / 865 / 2,
                                       18)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        dialogueWaiBossGreeting.hleb_greeting_update()
        spriteGroups.animatedDialogue.draw(windows.screen)
        # levelGenerator.get_shadow(*consts.hero.get_coords(), *consts.hero.get_size())
        # spriteGroups.shadowgroup.draw(windows.screen)
        consts.hero.update()
        spriteGroups.characters.draw(windows.screen)
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


def boss_lose_cutscene():
    pass
