import pygame
import windows
import consts
import menu
import fileManager
from itemCreator import Object, Button
from itemChanger import windowsFullscreenChanger
from processHelper import terminate, transition


def settings_menu():
    if not windows.fullscreen:
        all_w, all_h = windows.width // 2 - 363, windows.height - 619
    else:
        all_w, all_h = windows.width // 2 - 363, windows.height - 820

    title = Object(all_w, all_h, 626, 82, fr"objects\{consts.languageNow}\settings-title-obj.png")

    field_audio = Object(all_w - 87, all_h + 115, 420, 430, fr"objects\{consts.languageNow}\audio-field-obj.png")
    field_video = Object(all_w + 393, all_h + 115, 420, 430, fr"objects\{consts.languageNow}\video-field-obj.png")
    fs_name = Object(all_w + 436, all_h + 235 if consts.languageNow == 'rus' else all_h + 215, 332, 75,
                     fr"objects\{consts.languageNow}\fullscreen-obj.png")
    sound_name = Object(field_audio.x + field_audio.width // 2 - 332 // 2 if consts.languageNow == 'rus'
                        else field_audio.x + field_audio.width // 2 - 359 // 2, all_h + 385,
                        332 if consts.languageNow == 'rus' else 359, 35, fr"objects\{consts.languageNow}\sound-obj.png")
    music_name = Object(
        field_audio.x + field_audio.width // 2 - 332 // 2 if consts.languageNow == 'rus'
        else field_audio.x + field_audio.width // 2 - 359 // 2,
        all_h + 249, 332 if consts.languageNow == 'rus' else 359, 35, fr"objects\{consts.languageNow}\music-obj.png")
    music_slider_obj = Object(all_w - 31, all_h + 308, 302, 16, r"objects\without text\slider-obj.png")
    sound_slider_obj = Object(all_w - 31, all_h + 444, 302, 16, r"objects\without text\slider-obj.png")
    langauge_obj = Object(all_w + 436 + 57.5, all_h + 420, 215, 52,
                          r"objects\rus\language-rus-obj.png", "", r"objects\eng\language-eng-obj.png")

    cross_btn = Button(all_w + 646, all_h + 8, 67, 72, r"buttons\without text\default-cross-btn.png",
                       r"buttons\without text\hover-cross-btn.png",
                       r"buttons\without text\press-cross-btn.png", r"data\sounds\menu-button-sound.mp3")
    fs_btn = Button(fs_name.x + fs_name.width // 2 - 136 // 2, fs_name.y + fs_name.height + 15, 136, 62,
                    fr"buttons\{consts.languageNow}\fullscreen-off-btn.png", "",
                    fr"buttons\{consts.languageNow}\fullscreen-on-btn.png", r"data\sounds\menu-button-sound.mp3")
    arrow_btn = Button(all_w + 732, all_h + 432, 36, 40,
                       r"buttons\without text\default-arrow-btn.png", r"buttons\without text\hover-arrow-btn.png",
                       r"buttons\without text\press-arrow-btn.png", r"data\sounds\menu-button-sound.mp3")
    r_arrow_btn = Button(all_w + 436, all_h + 432, 36, 40,
                         r"buttons\without text\default-r-arrow-btn.png", r"buttons\without text\hover-r-arrow-btn.png",
                         r"buttons\without text\press-r-arrow-btn.png", r"data\sounds\menu-button-sound.mp3")
    if not windows.fullscreen:
        sl = 106 + 300 * consts.wM
    else:
        sl = 553 + 300 * consts.wM
    music_slider_btn = Button(sl, all_h + 302, 26, 28,
                              r"buttons\without text\default-slider-btn.png",
                              r"buttons\without text\hover-slider-btn.png",
                              r"buttons\without text\press-slider-btn.png")
    if not windows.fullscreen:
        sd = 106 + 300 * consts.wS
    else:
        sd = 553 + 300 * consts.wS
    sound_slider_btn = Button(sd, all_h + 438, 26, 28,
                              r"buttons\without text\default-slider-btn.png",
                              r"buttons\without text\hover-slider-btn.png",
                              r"buttons\without text\press-slider-btn.png")

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

            if event.type == pygame.USEREVENT and event.button == fs_btn:
                if windows.fullscreen:
                    windows.fullscreen = 0
                    windowsFullscreenChanger(windows.fullscreen)
                    settings_menu()
                else:
                    windows.fullscreen = 1
                    windowsFullscreenChanger(windows.fullscreen)
                    settings_menu()

            if event.type == pygame.USEREVENT and (event.button == arrow_btn or event.button == r_arrow_btn):
                if consts.languageNow == 'eng':
                    consts.languageNow = 'rus'
                elif consts.languageNow == 'rus':
                    consts.languageNow = 'eng'
                fileManager.languageExport(consts.languageNow)
                settings_menu()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == music_slider_btn:
                consts.isSliderMusic = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == music_slider_btn:
                consts.isSliderMusic = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == sound_slider_btn:
                consts.isSliderSound = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == sound_slider_btn:
                consts.isSliderSound = False

            elif event.type == pygame.MOUSEMOTION:
                if consts.isSliderMusic or consts.isSliderSound:
                    if consts.isSliderMusic:
                        xM = music_slider_btn.rect[0]
                        # 553 853
                        if all_w - 32 < event.pos[0] < all_w + 270:
                            x_cube_M = event.pos[0] - xM
                        else:
                            x_cube_M = 13
                        music_slider_btn.rect = music_slider_btn.rect.move(x_cube_M - 13, 0)
                        if not windows.fullscreen:
                            consts.wM = (music_slider_btn.rect[0] - 106) / 300
                        else:
                            consts.wM = (music_slider_btn.rect[0] - 553) / 300
                        pygame.mixer.music.set_volume(consts.wM)

                    elif consts.isSliderSound:
                        xS = sound_slider_btn.rect[0]
                        if all_w - 32 < event.pos[0] < all_w + 270:
                            x_cube_S = event.pos[0] - xS
                        else:
                            x_cube_S = 13
                        sound_slider_btn.rect = sound_slider_btn.rect.move(x_cube_S - 13, 0)
                        if not windows.fullscreen:
                            consts.wS = (sound_slider_btn.rect[0] - 106) / 300
                            consts.volS = consts.wS
                        else:
                            consts.wS = (sound_slider_btn.rect[0] - 553) / 300
                            consts.volS = consts.wS
                    fileManager.volumeExport(consts.wM, consts.wS)

            for button in [cross_btn, fs_btn, arrow_btn, r_arrow_btn]:
                button.handle_event(event, consts.volS)

            for slider_button in [music_slider_btn, sound_slider_btn]:
                slider_button.handle_event_slider(event)

        for obj in [title, field_audio, field_video, fs_name, sound_name, music_name, music_slider_obj,
                    sound_slider_obj]:
            obj.draw(windows.screen)

        langauge_obj.drawLanguage(windows.screen, consts.languageNow)

        for button in [cross_btn, music_slider_btn, sound_slider_btn, arrow_btn, r_arrow_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(windows.screen)

        fs_btn.check_hover(pygame.mouse.get_pos())
        fs_btn.draw_f11(windows.screen, windows.fullscreen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
