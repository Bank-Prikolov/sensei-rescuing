import pygame
from config import consts
import menu
import game
from managing import sounds_managing, stars_managing
from windows.items.item_changing import timeChanger
from windows.items.item_creating import Object, Button, Stars
from misc.specfunctions import terminate, transition


def levels_menu():
    soundManager.menu_theme()

    title = Object(windows.width // 2 - 887 / 2 if consts.languageNow == 'rus' else windows.width // 2 - 907 / 2,
                   windows.height // 2 - 468 // 2,
                   800 if consts.languageNow == 'rus' else 820, 82,
                   fr"objects\{consts.languageNow}\level-menu-title-obj.png")
    cross_btn = Button(title.x + title.width + 20, title.y + 8, 67, 72, r"buttons\without text\default-cross-btn.png",
                       r"buttons\without text\hover-cross-btn.png", r"buttons\without text\press-cross-btn.png",
                       r"data\sounds\menu-button-sound.mp3")

    field = Object(windows.width // 2 - 987 / 2, title.y + 104, 987, 252,
                   r"objects\without text\level-menu-field-obj.png")
    level1Field = Object(field.x + 27, field.y + field.height / 2 - 189 / 2, 186, 189,
                         r"objects\without text\start-level-field-obj.png")
    level2Field = Object(level1Field.x + level1Field.width + 13.5, field.y + field.height / 2 - 189 / 2, 360, 189,
                         r"objects\without text\level-field-obj.png",
                         r"objects\without text\hover-level-field-obj.png")
    levelBossField = Object(level2Field.x + level2Field.width + 13.5, field.y + field.height / 2 - 189 / 2, 360, 189,
                            r"objects\without text\level-field-obj.png",
                            r"objects\without text\hover-level-field-obj.png")
    level1Button = Button(level1Field.x + level1Field.width / 2 - 144 / 2,
                          level1Field.y + level1Field.height / 2 - 155 / 2, 144, 155,
                          r"buttons\without text\default-first-btn.png",
                          r"buttons\without text\hover-first-btn.png", r"buttons\without text\press-first-btn.png",
                          r"data\sounds\menu-button-sound.mp3")
    level2Button = Button(level2Field.x + level2Field.width - level1Field.width / 2 - 144 / 2,
                          level2Field.y + level2Field.height / 2 - 155 / 2, 144, 155,
                          r"buttons\without text\default-second-btn.png",
                          r"buttons\without text\hover-second-btn.png", r"buttons\without text\press-second-btn.png",
                          r"data\sounds\menu-button-sound.mp3", r"buttons\without text\no-active-second-btn.png")
    levelBossButton = Button(levelBossField.x + levelBossField.width - level1Field.width / 2 - 144 / 2,
                             levelBossField.y + levelBossField.height / 2 - 155 / 2, 144, 155,
                             r"buttons\without text\default-boss-btn.png",
                             r"buttons\without text\hover-boss-btn.png", r"buttons\without text\press-boss-btn.png",
                             r"data\sounds\menu-button-sound.mp3", r"buttons\without text\no-active-boss-btn.png")

    info_btn = Button(field.x + field.width - 18 - 11, field.y + 10, 18, 18,
                      r"buttons\without text\default-level-info-btn.png",
                      r"buttons\without text\hover-level-info-btn.png")
    field_d = Object(info_btn.x - 499, info_btn.y - 219, 498, 218,
                     fr"objects\{consts.languageNow}\level-info-field-obj.png")

    zeroStars, oneStar, twoStars, threeStars = (
        r"objects\without text\stars-zero-obj.png", r"objects\without text\stars-one-obj.png",
        r"objects\without text\stars-two-obj.png", r"objects\without text\stars-three-obj.png")
    level1StarsField = Object(level1Field.x, title.y + 368, 186, 100, r"objects\without text\stars-field-obj.png")
    level1Stars = Stars(level1Field.x + level1StarsField.width // 2 - 152 // 2, title.y + 374, 152, 44, zeroStars,
                        oneStar, twoStars,
                        threeStars)
    level2StarsField = Object(level2Field.x + level2Field.width - level1Field.width, title.y + 368, 186, 100,
                              r"objects\without text\stars-field-obj.png")
    level2Stars = Stars(
        (level2Field.x + level2Field.width - level1Field.width) + level2StarsField.width // 2 - 152 // 2, title.y + 374,
        152, 44, zeroStars, oneStar, twoStars,
        threeStars)
    levelBossStarsField = Object(levelBossField.x + levelBossField.width - level1Field.width, title.y + 368, 186, 100,
                                 r"objects\without text\stars-field-obj.png")
    levelBossStars = Stars(
        (levelBossField.x + levelBossField.width - level1Field.width) + levelBossStarsField.width // 2 - 152 // 2,
        title.y + 374, 152, 44, zeroStars, oneStar, twoStars,
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
                consts.playingMenuMusic = True
                soundManager.stop_playback()
                transition()
                game.game_def(1)

            if event.type == pygame.USEREVENT and event.button == level2Button:
                consts.lvlNow = 2
                consts.playingMenuMusic = True
                soundManager.stop_playback()
                transition()
                game.game_def(2)

            if event.type == pygame.USEREVENT and event.button == levelBossButton:
                consts.lvlNow = 3
                consts.playingMenuMusic = True
                soundManager.stop_playback()
                transition()
                game.game_def(3)

            for button in [cross_btn, level1Button, level2Button, levelBossButton]:
                button.handle_event(event, consts.volS)

        if starsRecorder.check_passing(1):
            level1StarsField.draw(windows.screen)
            level1Stars.draw(windows.screen, starsRecorder.get_record(1))
            level2Field.check_passing(True)
            level2Button.check_passing(True)
            timeChanger(1, ButtonsFont, level1StarsField.x, level1StarsField.y, windows.screen)

        if starsRecorder.check_passing(2):
            level2StarsField.draw(windows.screen)
            level2Stars.draw(windows.screen, starsRecorder.get_record(2))
            levelBossField.check_passing(True)
            levelBossButton.check_passing(True)
            timeChanger(2, ButtonsFont, level2StarsField.x, level2StarsField.y, windows.screen)

        if starsRecorder.check_passing(3):
            levelBossStarsField.draw(windows.screen)
            levelBossStars.draw(windows.screen, starsRecorder.get_record(3))
            timeChanger(3, ButtonsFont, levelBossStarsField.x, levelBossStarsField.y, windows.screen)

        for obj in [title, field, level1Field, level2Field, levelBossField]:
            obj.draw(windows.screen)

        for button in [cross_btn, level1Button, level2Button, levelBossButton]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(windows.screen)

        info_btn.check_hover(pygame.mouse.get_pos())
        if info_btn.rect.collidepoint(pygame.mouse.get_pos()):
            field_d.draw(windows.screen)
        info_btn.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
