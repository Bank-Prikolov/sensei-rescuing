import pygame
import windows
import consts
import menu
import game
import cutscenes
import starsRecorder
from itemChanger import timeChanger
from itemCreator import Object, Button, Stars
from processHelper import terminate, transition


def levels_menu():
    if not windows.fullscreen:
        all_w, all_h = windows.width // 2 - 395, windows.height - 595
    else:
        all_w, all_h = windows.width // 2 - 395, windows.height - 770

    if consts.firstTime:
        pygame.mixer.music.load(r"data\sounds\menu-theme-sound.mp3")
        pygame.mixer.music.play(-1)
        consts.firstTime = False
    pygame.mixer.music.set_volume(consts.wM)

    title = Object(all_w, all_h, 700, 82, fr"objects\{consts.languageNow}\level-menu-title-obj.png")

    cross_btn = Button(all_w + title.width + 18, all_h + 8, 67, 72, r"buttons\without text\default-cross-btn.png",
                       r"buttons\without text\hover-cross-btn.png", r"buttons\without text\press-cross-btn.png",
                       r"data\sounds\menu-button-sound.mp3")
    level1Button = Button(all_w - 58, all_h + 160, 144, 155, r"buttons\without text\default-first-btn.png",
                          r"buttons\without text\hover-first-btn.png", r"buttons\without text\press-first-btn.png",
                          r"data\sounds\menu-button-sound.mp3")
    level2Button = Button(all_w + 317, all_h + 160, 144, 155, r"buttons\without text\default-second-btn.png",
                          r"buttons\without text\hover-second-btn.png", r"buttons\without text\press-second-btn.png",
                          r"data\sounds\menu-button-sound.mp3", r"buttons\without text\no-active-second-btn.png")
    levelBossButton = Button(all_w + 692, all_h + 160, 144, 155, r"buttons\without text\default-boss-btn.png",
                             r"buttons\without text\hover-boss-btn.png", r"buttons\without text\press-boss-btn.png",
                             r"data\sounds\menu-button-sound.mp3", r"buttons\without text\no-active-boss-btn.png")
    info_btn = Button(all_w + 858, all_h + 122.5, 18, 18, r"buttons\without text\default-level-info-btn.png",
                      r"buttons\without text\hover-level-info-btn.png")

    field_d = Object(all_w + 358.5, all_h - 95.5, 498, 218, fr"objects\{consts.languageNow}\level-info-field-obj.png")

    field = Object(all_w - 100, all_h + 111, 987, 252, r"objects\without text\level-menu-field-obj.png")
    level1Field = Object(all_w - 79, all_h + 142, 186, 189, r"objects\without text\start-level-field-obj.png")
    level2Field = Object(all_w + 121, all_h + 142, 360, 189, r"objects\without text\level-field-obj.png",
                         r"objects\without text\hover-level-field-obj.png")
    levelBossField = Object(all_w + 496, all_h + 142, 360, 189,
                            r"objects\without text\level-field-obj.png",
                            r"objects\without text\hover-level-field-obj.png")

    zeroStars, oneStar, twoStars, threeStars = (
        r"objects\without text\stars-zero-obj.png", r"objects\without text\stars-one-obj.png",
        r"objects\without text\stars-two-obj.png", r"objects\without text\stars-three-obj.png")
    level1StarsField = Object(all_w - 79, all_h + 375, 186, 100, r"objects\without text\stars-field-obj.png")
    level1Stars = Stars(all_w - 79 + 186 // 2 - 152 // 2, all_h + 381, 152, 44, zeroStars, oneStar, twoStars,
                        threeStars)
    level2StarsField = Object(all_w + 296, all_h + 375, 186, 100, r"objects\without text\stars-field-obj.png")
    level2Stars = Stars(all_w + 296 + 186 // 2 - 152 // 2, all_h + 381, 152, 44, zeroStars, oneStar, twoStars,
                        threeStars)
    levelBossStarsField = Object(all_w + 673, all_h + 375, 186, 100, r"objects\without text\stars-field-obj.png")
    levelBossStars = Stars(all_w + 673 + 186 // 2 - 152 // 2, all_h + 381, 152, 44, zeroStars, oneStar, twoStars,
                           threeStars)

    ButtonsFont = pygame.font.Font(r"data\fonts\PixelNumbers.ttf", 35)

    running = True
    while running:

        windows.screen.blit(consts.menu_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition()
                    menu.main_menu()

            if event.type == pygame.USEREVENT and event.button == cross_btn:
                transition()
                menu.main_menu()

            if event.type == pygame.USEREVENT and event.button == level1Button:
                consts.lvlNow = 1
                # pygame.mixer.music.stop()
                consts.firstTime = True
                transition()
                cutscenes.start_cutscene()

            if event.type == pygame.USEREVENT and event.button == level2Button:
                consts.lvlNow = 2
                # pygame.mixer.music.stop()
                consts.firstTime = True
                transition()
                game.game_def(2)

            if event.type == pygame.USEREVENT and event.button == levelBossButton:
                consts.lvlNow = 3
                # pygame.mixer.music.stop()
                consts.firstTime = True
                transition()
                game.game_def(3)

            for button in [cross_btn, level1Button, level2Button, levelBossButton]:
                button.handle_event(event, consts.volS)

        for obj in [title, field, level1Field, level2Field, levelBossField]:
            obj.draw(windows.screen)

        for button in [cross_btn, level1Button, level2Button, levelBossButton]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(windows.screen)

        info_btn.check_hover(pygame.mouse.get_pos())
        if info_btn.rect.collidepoint(pygame.mouse.get_pos()):
            field_d.draw(windows.screen)
        info_btn.draw(windows.screen)

        if starsRecorder.check_passing(1):
            level1StarsField.draw(windows.screen)
            level1Stars.draw(windows.screen, starsRecorder.get_record(1))
            level2Field.check_passing(True)
            level2Button.check_passing(True)
            timeChanger(1, ButtonsFont, all_w, all_h, windows.screen)

        if starsRecorder.check_passing(2):
            level2StarsField.draw(windows.screen)
            level2Stars.draw(windows.screen, starsRecorder.get_record(2))
            levelBossField.check_passing(True)
            levelBossButton.check_passing(True)
            timeChanger(2, ButtonsFont, all_w, all_h, windows.screen)

        if starsRecorder.check_passing(3):
            levelBossStarsField.draw(windows.screen)
            levelBossStars.draw(windows.screen, starsRecorder.get_record(3))
            timeChanger(3, ButtonsFont, all_w, all_h, windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
