import pygame
import sys
import webbrowser

import windows
import game

from load_image import load_image
from itemCreator import Object, Button, Stars, checkFullscreen

pygame.init()

size = WIDTH, HEIGHT = 1024, 704
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sensei Rescuing')
clock = pygame.time.Clock()
fps = 60

cursor = load_image(r'objects\cursor-obj.png')
pygame.mouse.set_visible(False)

img = load_image(r'backgrounds\main-menu-bg.png')
bg = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))

checkIsActive2 = True
checkIsActiveBoss = True
isSliderMusic = False
isSliderSound = False

checkIsPassing1 = True
checkIsPassing2 = True
checkIsPassingBoss = True

record1 = 0
record2 = 0
record3 = 0

b = open(r"data/savings/hero-settings.txt", "r", encoding="utf-8")
checkHero = list(map(lambda x: float(x.rstrip('\n')), b))
hero = int(checkHero[0])
heroNow = hero

lvlNow = 1

a = open(r"data/savings/volume-settings.txt", "r", encoding="utf-8")
checkActDet = list(map(lambda x: float(x.rstrip('\n')), a))
wM = checkActDet[0]
wS = checkActDet[1]
volS = wS

pygame.mixer.music.load(r"data\sounds\menu-sound.wav")
ft = True


def main_menu():
    global checkActDet, wM, wS, ft, hero, heroNow

    if ft:
        pygame.mixer.music.play(-1)
        ft = False
    pygame.mixer.music.set_volume(wM)

    if not windows.fullscreen:
        change_fullScreen(1024, 704)
        all_w, all_h = WIDTH // 2 - 443, HEIGHT - 619
    else:
        change_fullScreen(1920, 1080, pygame.FULLSCREEN)
        all_w, all_h = WIDTH // 2 - 443, HEIGHT - 820

    title = Object(all_w, all_h, 886, 80, r"objects\menu-title-obj.png")

    updates_field = Object(all_w, all_h + 102, 304, 416, r"objects\updates-field-obj.png")
    buttons_field = Object(all_w + 315, all_h + 102, 256, 416, r"objects\menu-buttons-field-obj.png")
    hero_field = Object(all_w + 582, all_h + 102, 304, 416, r"objects\hero-field-obj.png")

    start_btn = Button(all_w + 323, all_h + 110, 240, 100, r"buttons\default-start-btn.png",
                       r"buttons\hover-start-btn.png", r"buttons\press-start-btn.png",
                       r"data\sounds\menu-button-sound.mp3")
    settings_btn = Button(all_w + 323, all_h + 210, 240, 100, r"buttons\default-settings-btn.png",
                          r"buttons\hover-settings-btn.png", r"buttons\press-settings-btn.png",
                          r"data\sounds\menu-button-sound.mp3")
    info_btn = Button(all_w + 323, all_h + 310, 240, 100, r"buttons\default-info-btn.png",
                      r"buttons\hover-info-btn.png", r"buttons\press-info-btn.png",
                      r"data\sounds\menu-button-sound.mp3")
    exit_btn = Button(all_w + 323, all_h + 410, 240, 100, r"buttons\default-exit-btn.png",
                      r"buttons\hover-exit-btn.png", r"buttons\press-exit-btn.png",
                      r"data\sounds\menu-button-sound.mp3")

    hero_choose = Object(all_w + 582 + 304 // 2 - 107 // 2, all_h + 102 + 95, 107, 204,
                         r"objects\hero-wai-obj.png", "", r"objects\hero-sato-obj.png")

    arrow_btn = Button(all_w + 582 + 304 // 2 - 173 // 2 + 180, all_h + 102 + 95 + 241 // 2 - 36 // 2, 36, 40,
                       r"buttons\default-arrow-btn.png", r"buttons\hover-arrow-btn.png",
                       r"buttons\press-arrow-btn.png", r"data\sounds\menu-button-sound.mp3")
    r_arrow_btn = Button(all_w + 582 + 304 // 2 - 173 // 2 - 43, all_h + 102 + 95 + 241 // 2 - 36 // 2, 36, 40,
                         r"buttons\default-r-arrow-btn.png", r"buttons\hover-r-arrow-btn.png",
                         r"buttons\press-r-arrow-btn.png", r"data\sounds\menu-button-sound.mp3")
    choose_btn = Button(all_w + 582 + 304 // 2 - 159 // 2, all_h + 410, 159, 48, r"buttons\default-choose-btn.png",
                      r"buttons\hover-choose-btn.png", r"buttons\press-choose-btn.png",
                      r"data\sounds\menu-button-sound.mp3", "", hero)

    running = True
    hero = heroNow
    while running:
        clock.tick(fps)
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.USEREVENT and event.button == exit_btn):
                checkFullscreen(windows.fullscreen)
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == start_btn:
                transition()
                levels_menu()

            if event.type == pygame.USEREVENT and event.button == settings_btn:
                transition()
                settings_menu()

            if event.type == pygame.USEREVENT and event.button == info_btn:
                transition()
                info_menu()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if windows.fullscreen:
                    windows.fullscreen = 0
                    change_fullScreen(1024, 704)
                    main_menu()
                else:
                    windows.fullscreen = 1
                    change_fullScreen(1920, 1080, pygame.FULLSCREEN)
                    main_menu()

            if event.type == pygame.USEREVENT and event.button == choose_btn:
                checkHeroRewrite = open(r"data/savings/hero-settings.txt", "w")
                if hero == 1 and hero != heroNow:
                    heroNow = 1
                    print('hero WAI is chosen')
                elif hero == 2 and hero != heroNow:
                    heroNow = 2
                    print('hero SATO is chosen')
                checkHeroRewrite.writelines(str(hero))

            if event.type == pygame.USEREVENT and (event.button == arrow_btn or event.button == r_arrow_btn):
                if hero == 1:
                    hero = 2
                elif hero == 2:
                    hero = 1

            for button in [start_btn, settings_btn, info_btn, exit_btn, arrow_btn, r_arrow_btn, choose_btn]:
                button.handle_event(event, volS)

        for obj in [title, updates_field, buttons_field, hero_field]:
            obj.draw(screen)

        hero_choose.draw(screen, hero)

        for button in [start_btn, settings_btn, info_btn, exit_btn, arrow_btn, r_arrow_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)

        choose_btn.check_hover(pygame.mouse.get_pos())
        choose_btn.draw_heroBtn(screen, hero, heroNow)

        x_c, y_c = pygame.mouse.get_pos()
        if not windows.fullscreen:
            if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
                screen.blit(cursor, (x_c, y_c))
        else:
            screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


def levels_menu():
    global lvlNow, ft
    if not windows.fullscreen:
        change_fullScreen(1024, 704)
        all_w, all_h = WIDTH // 2 - 395, HEIGHT - 582
    else:
        change_fullScreen(1920, 1080, pygame.FULLSCREEN)
        all_w, all_h = WIDTH // 2 - 395, HEIGHT - 770

    if ft:
        pygame.mixer.music.play(-1)
        ft = False
    pygame.mixer.music.set_volume(wM)

    title = Object(all_w, all_h, 700, 82, r"objects\level-menu-title-obj.png")

    cross_btn = Button(all_w + title.width + 18, all_h + 8, 67, 72, r"buttons\default-cross-btn.png",
                       r"buttons\hover-cross-btn.png", r"buttons\press-cross-btn.png",
                       r"data\sounds\menu-button-sound.mp3")
    level1Button = Button(all_w - 58, all_h + 160, 144, 155, r"buttons\default-first-btn.png",
                          r"buttons\hover-first-btn.png", r"buttons\press-first-btn.png",
                          r"data\sounds\menu-button-sound.mp3")
    level2Button = Button(all_w + 317, all_h + 160, 144, 155, r"buttons\default-second-btn.png",
                          r"buttons\hover-second-btn.png", r"buttons\press-second-btn.png",
                          r"data\sounds\menu-button-sound.mp3", r"buttons\no-active-second-btn.png")
    levelBossButton = Button(all_w + 692, all_h + 160, 144, 155, r"buttons\default-boss-btn.png",
                             r"buttons\hover-boss-btn.png", r"buttons\press-boss-btn.png",
                             r"data\sounds\menu-button-sound.mp3", r"buttons\no-active-boss-btn.png")
    info_btn = Button(all_w + 858, all_h + 122.5, 18, 18, r"buttons\default-level-info-btn.png",
                      r"buttons\hover-level-info-btn.png")

    field = Object(all_w - 100, all_h + 111, 987, 252, r"objects\level-menu-field-obj.png")
    level1Field = Object(all_w - 79, all_h + 142, 186, 189, r"objects\start-level-field-obj.png")
    level2Field = Object(all_w + 121, all_h + 142, 360, 189, r"objects\level-field-obj.png",
                         r"objects\hover-level-field-obj.png")
    levelBossField = Object(all_w + 496, all_h + 142, 360, 189,
                            r"objects\level-field-obj.png", r"objects\hover-level-field-obj.png")

    zeroStars, oneStar, twoStars, threeStars = (r"objects\stars-zero-obj.png", r"objects\stars-one-obj.png",
                                                r"objects\stars-two-obj.png", r"objects\stars-three-obj.png")
    level1StarsField = Object(all_w - 79, all_h + 375, 186, 56, r"objects\stars-field-obj.png")
    level1Stars = Stars(all_w - 79 + 186 // 2 - 152 // 2, all_h + 380, 152, 44, zeroStars, oneStar, twoStars,
                        threeStars)
    level2StarsField = Object(all_w + 296, all_h + 375, 186, 56, r"objects\stars-field-obj.png")
    level2Stars = Stars(all_w + 296 + 186 // 2 - 152 // 2, all_h + 380, 152, 44, zeroStars, oneStar, twoStars,
                        threeStars)
    levelBossStarsField = Object(all_w + 673, all_h + 375, 186, 56, r"objects\stars-field-obj.png")
    levelBossStars = Stars(all_w + 673 + 186 // 2 - 152 // 2, all_h + 380, 152, 44, zeroStars, oneStar, twoStars,
                           threeStars)

    running = True
    while running:
        clock.tick(fps)
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                checkFullscreen(windows.fullscreen)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition()
                    main_menu()

            if event.type == pygame.USEREVENT and event.button == cross_btn:
                transition()
                main_menu()

            if event.type == pygame.USEREVENT and event.button == level1Button:
                lvlNow = 1
                pygame.mixer.music.stop()
                ft = True
                transition()
                game.game_def(1)

            if event.type == pygame.USEREVENT and event.button == level2Button and checkIsActive2:
                lvlNow = 2
                pygame.mixer.music.stop()
                ft = True
                transition()
                game.game_def(2)

            if event.type == pygame.USEREVENT and event.button == levelBossButton and checkIsActiveBoss:
                lvlNow = 3
                pygame.mixer.music.stop()
                ft = True
                transition()
                game.game_def(3)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if windows.fullscreen:
                    windows.fullscreen = 0
                    change_fullScreen(1024, 704)
                    levels_menu()
                else:
                    windows.fullscreen = 1
                    change_fullScreen(1920, 1080, pygame.FULLSCREEN)
                    levels_menu()

            for button in [cross_btn, level1Button, level2Button, levelBossButton]:
                button.handle_event(event, volS)

        for obj in [title, field, level1Field]:
            obj.draw(screen)

        level2Field.check_passing(checkIsActive2)
        level2Field.draw(screen)
        levelBossField.check_passing(checkIsActiveBoss)
        levelBossField.draw(screen)

        for button in [cross_btn, level1Button, level2Button, levelBossButton]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)

        info_btn.check_hover(pygame.mouse.get_pos())
        if info_btn.rect.collidepoint(pygame.mouse.get_pos()):
            field_d = Object(all_w + 358.5, all_h - 95.5, 498, 218, r"objects\level-info-field-obj.png")
            field_d.draw(screen)
        info_btn.draw(screen)

        level2Button.check_passing(checkIsActive2)
        levelBossButton.check_passing(checkIsActiveBoss)

        if checkIsPassing1:
            level1StarsField.draw(screen)
            level1Stars.draw(screen, record1)
        if checkIsPassing2:
            level2StarsField.draw(screen)
            level2Stars.draw(screen, record2)
        if checkIsPassingBoss:
            levelBossStarsField.draw(screen)
            levelBossStars.draw(screen, record3)

        x_c, y_c = pygame.mouse.get_pos()
        if not windows.fullscreen:
            if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
                screen.blit(cursor, (x_c, y_c))
        else:
            screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


def settings_menu():
    global isSliderMusic, isSliderSound, volS, wM, wS, checkActDet
    if not windows.fullscreen:
        all_w, all_h = WIDTH // 2 - 363, HEIGHT - 619
    else:
        all_w, all_h = WIDTH // 2 - 363, HEIGHT - 820

    title = Object(all_w, all_h, 626, 82, r"objects\settings-title-obj.png")

    field_audio = Object(all_w - 87, all_h + 115, 420, 430, r"objects\audio-field-obj.png")
    field_video = Object(all_w + 393, all_h + 115, 420, 430, r"objects\video-field-obj.png")
    fs_name = Object(all_w + 436, all_h + 245, 332, 75, r"objects\fullscreen-obj.png")
    sound_name = Object(all_w - 46, all_h + 385, 332, 35, r"objects\sound-obj.png")
    music_name = Object(all_w - 46, all_h + 249, 332, 35, r"objects\music-obj.png")

    cross_btn = Button(all_w + 646, all_h + 8, 67, 72, r"buttons\default-cross-btn.png", r"buttons\hover-cross-btn.png",
                       r"buttons\press-cross-btn.png", r"data\sounds\menu-button-sound.mp3")
    fs_btn = Button(all_w + 534, all_h + 335, 136, 62, r"buttons\fullscreen-off-btn.png", "",
                    r"buttons\fullscreen-on-btn.png", r"data\sounds\menu-button-sound.mp3")

    if not windows.fullscreen:
        sl = 106 + 300 * wM
    else:
        sl = 553 + 300 * wM
    music_slider_btn = Button(sl, all_h + 302, 26, 28,
                              r"buttons\default-slider-btn.png", r"buttons\hover-slider-btn.png",
                              r"buttons\press-slider-btn.png")

    if not windows.fullscreen:
        sd = 106 + 300 * wS
    else:
        sd = 553 + 300 * wS
    sound_slider_btn = Button(sd, all_h + 438, 26, 28,
                              r"buttons\default-slider-btn.png", r"buttons\hover-slider-btn.png",
                              r"buttons\press-slider-btn.png")

    music_slider_obj = Object(all_w - 31, all_h + 308, 302, 16, r"objects\slider-obj.png")
    sound_slider_obj = Object(all_w - 31, all_h + 444, 302, 16, r"objects\slider-obj.png")
    running = True
    while running:
        clock.tick(fps)
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                checkFullscreen(windows.fullscreen)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition()
                    main_menu()

            if event.type == pygame.USEREVENT and event.button == cross_btn:
                transition()
                main_menu()

            if ((event.type == pygame.USEREVENT and event.button == fs_btn) or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_F11)):
                if windows.fullscreen:
                    windows.fullscreen = 0
                    change_fullScreen(1024, 704)
                    settings_menu()
                else:
                    windows.fullscreen = 1
                    change_fullScreen(1920, 1080, pygame.FULLSCREEN)
                    settings_menu()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == music_slider_btn:
                isSliderMusic = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == music_slider_btn:
                isSliderMusic = False

            elif event.type == pygame.MOUSEMOTION:
                if isSliderMusic or isSliderSound:
                    checkActDet = open(r"data/savings/volume-settings.txt", "w")
                    if isSliderMusic:
                        xM = music_slider_btn.rect[0]
                        # 553 853
                        if all_w - 32 < event.pos[0] < all_w + 270:
                            x_cube_M = event.pos[0] - xM
                        else:
                            x_cube_M = 13
                        music_slider_btn.rect = music_slider_btn.rect.move(x_cube_M - 13, 0)
                        if not windows.fullscreen:
                            wM = (music_slider_btn.rect[0] - 106) / 300
                        else:
                            wM = (music_slider_btn.rect[0] - 553) / 300
                        pygame.mixer.music.set_volume(wM)

                    elif isSliderSound:
                        xS = sound_slider_btn.rect[0]
                        if all_w - 32 < event.pos[0] < all_w + 270:
                            x_cube_S = event.pos[0] - xS
                        else:
                            x_cube_S = 13
                        sound_slider_btn.rect = sound_slider_btn.rect.move(x_cube_S - 13, 0)
                        if not windows.fullscreen:
                            wS = (sound_slider_btn.rect[0] - 106) / 300
                            volS = wS
                        else:
                            wS = (sound_slider_btn.rect[0] - 553) / 300
                            volS = wS
                    checkActDet.writelines([str(wM) + '\n', str(wS)])

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == sound_slider_btn:
                isSliderSound = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == sound_slider_btn:
                isSliderSound = False

            for button in [cross_btn, fs_btn]:
                button.handle_event(event, volS)

            for slider_button in [music_slider_btn, sound_slider_btn]:
                slider_button.handle_event_slider(event)

        for obj in [title, field_audio, field_video, fs_name, sound_name, music_name, music_slider_obj,
                    sound_slider_obj]:
            obj.draw(screen)

        for slider_button in [cross_btn, music_slider_btn, sound_slider_btn]:
            slider_button.check_hover(pygame.mouse.get_pos())
            slider_button.draw(screen)

        fs_btn.check_hover(pygame.mouse.get_pos())
        fs_btn.draw_f11(screen, windows.fullscreen)

        x_c, y_c = pygame.mouse.get_pos()
        if not windows.fullscreen:
            if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
                screen.blit(cursor, (x_c, y_c))
        else:
            screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


def info_menu():
    if not windows.fullscreen:
        all_w, all_h = WIDTH // 2 - 364, HEIGHT - 619
    else:
        all_w, all_h = WIDTH // 2 - 364, HEIGHT - 820

    title = Object(all_w, all_h, 640, 82, r"objects\info-title-obj.png")

    cross_btn = Button(all_w + 660, all_h + 8, 67, 72, r"buttons\default-cross-btn.png",
                       r"buttons\hover-cross-btn.png", r"buttons\press-cross-btn.png",
                       r"data\sounds\menu-button-sound.mp3")
    github_left_btn = Button(all_w + 19, all_h + 449, 67, 72, r"buttons\default-github-btn.png",
                             r"buttons\hover-github-btn.png", r"buttons\press-github-btn.png",
                             r"data\sounds\menu-button-sound.mp3")
    github_right_btn = Button(all_w + 464, all_h + 449, 67, 72, r"buttons\default-github-btn.png",
                              r"buttons\hover-github-btn.png", r"buttons\press-github-btn.png",
                              r"data\sounds\menu-button-sound.mp3")

    field = Object(all_w - 86, all_h + 115, 900, 430, r"objects\info-field-obj.png")
    alexandr = Object(all_w + 99, all_h + 462, 269, 46, r"objects\alexandr-obj.png")
    igor = Object(all_w + 544, all_h + 462, 142, 45, r"objects\igor-obj.png")

    running = True
    while running:
        clock.tick(fps)
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                checkFullscreen(windows.fullscreen)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition()
                    main_menu()

            if event.type == pygame.USEREVENT and event.button == cross_btn:
                transition()
                main_menu()

            if event.type == pygame.USEREVENT and event.button == github_left_btn:
                webbrowser.open('https://github.com/mikhalexandr')

            if event.type == pygame.USEREVENT and event.button == github_right_btn:
                webbrowser.open('https://github.com/WaizorSote')

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if windows.fullscreen:
                    windows.fullscreen = 0
                    change_fullScreen(1024, 704)
                    info_menu()
                else:
                    windows.fullscreen = 1
                    change_fullScreen(1920, 1080, pygame.FULLSCREEN)
                    info_menu()

            for button in [github_left_btn, github_right_btn, cross_btn]:
                button.handle_event(event, volS)

        for obj in [title, field, alexandr, igor]:
            obj.draw(screen)

        for button in [github_left_btn, github_right_btn, cross_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        if not windows.fullscreen:
            if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
                screen.blit(cursor, (x_c, y_c))
        else:
            screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


def transition():
    running = True
    transition_level = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        transition_surface = pygame.Surface((WIDTH, HEIGHT))
        transition_surface.fill((0, 0, 0))
        transition_surface.set_alpha(transition_level)
        screen.blit(transition_surface, (0, 0))

        transition_level += 5
        if transition_level >= 105:
            transition_level = 255
            running = False

        pygame.display.flip()
        clock.tick(70)


def change_fullScreen(width, height, fullScreen=0):
    global WIDTH, HEIGHT, screen, img, bg
    WIDTH, HEIGHT = width, height
    screen = pygame.display.set_mode((WIDTH, HEIGHT), fullScreen)
    if windows.fullscreen:
        tmp_img = load_image(r"backgrounds\main-menu-fullScreen-bg.png")
        bg = pygame.transform.scale(tmp_img, (tmp_img.get_width(), tmp_img.get_height()))
    else:
        bg = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
