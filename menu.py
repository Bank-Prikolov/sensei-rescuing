import pygame
import webbrowser
import windows
import consts
import fileManager
import info
import settings
import levels_menu
from processHelper import terminate, transition
from itemCreator import Object, Button
from itemChanger import fullscreenChanger


def main_menu():
    if consts.firstTime:
        fullscreenChanger(windows.fullscreen, True)
        pygame.mixer.music.load(r"data\sounds\menu-theme-sound.mp3")
        pygame.mixer.music.play(-1)
        consts.firstTime = False
    pygame.mixer.music.set_volume(consts.wM)

    if not windows.fullscreen:
        all_w, all_h = windows.width // 2 - 443, windows.height - 619
    else:
        all_w, all_h = windows.width // 2 - 443, windows.height - 820

    title = Object(all_w, all_h, 886, 80, fr"objects\{consts.languageNow}\menu-title-obj.png")

    updates_field = Object(all_w, all_h + 102, 304, 416, fr"objects\{consts.languageNow}\updates-field-obj.png")
    buttons_field = Object(all_w + 315, all_h + 102, 256, 416, r"objects\without text\menu-buttons-field-obj.png")
    hero_field = Object(all_w + 582, all_h + 102, 304, 416, fr"objects\{consts.languageNow}\hero-field-obj.png")

    start_btn = Button(all_w + 323, all_h + 110, 240, 100, fr"buttons\{consts.languageNow}\default-start-btn.png",
                       fr"buttons\{consts.languageNow}\hover-start-btn.png",
                       fr"buttons\{consts.languageNow}\press-start-btn.png",
                       r"data\sounds\menu-button-sound.mp3")
    settings_btn = Button(all_w + 323, all_h + 210, 240, 100, fr"buttons\{consts.languageNow}\default-settings-btn.png",
                          fr"buttons\{consts.languageNow}\hover-settings-btn.png",
                          fr"buttons\{consts.languageNow}\press-settings-btn.png",
                          r"data\sounds\menu-button-sound.mp3")
    info_btn = Button(all_w + 323, all_h + 310, 240, 100, fr"buttons\{consts.languageNow}\default-info-btn.png",
                      fr"buttons\{consts.languageNow}\hover-info-btn.png",
                      fr"buttons\{consts.languageNow}\press-info-btn.png",
                      r"data\sounds\menu-button-sound.mp3")
    exit_btn = Button(all_w + 323, all_h + 410, 240, 100, fr"buttons\{consts.languageNow}\default-exit-btn.png",
                      fr"buttons\{consts.languageNow}\hover-exit-btn.png",
                      fr"buttons\{consts.languageNow}\press-exit-btn.png",
                      r"data\sounds\menu-button-sound.mp3")

    hero_choose = Object(all_w + 582 + 304 // 2 - 107 // 2, all_h + 102 + 95, 107, 204,
                         r"objects\without text\hero-wai-obj.png", "",
                         r"objects\without text\hero-the-strongest-wai-obj.png")

    arrow_btn = Button(all_w + 582 + 304 // 2 - 173 // 2 + 180, all_h + 102 + 95 + 241 // 2 - 36 // 2, 36, 40,
                       r"buttons\without text\default-arrow-btn.png", r"buttons\without text\hover-arrow-btn.png",
                       r"buttons\without text\press-arrow-btn.png", r"data\sounds\menu-button-sound.mp3")
    r_arrow_btn = Button(all_w + 582 + 304 // 2 - 173 // 2 - 43, all_h + 102 + 95 + 241 // 2 - 36 // 2, 36, 40,
                         r"buttons\without text\default-r-arrow-btn.png", r"buttons\without text\hover-r-arrow-btn.png",
                         r"buttons\without text\press-r-arrow-btn.png", r"data\sounds\menu-button-sound.mp3")
    choose_btn = Button(all_w + 582 + 304 // 2 - 159 // 2, all_h + 410, 159, 48,
                        fr"buttons\{consts.languageNow}\default-choose-btn.png",
                        fr"buttons\{consts.languageNow}\hover-choose-btn.png",
                        fr"buttons\{consts.languageNow}\press-choose-btn.png",
                        r"data\sounds\menu-button-sound.mp3", "", consts.heroNow,
                        fr"buttons\{consts.languageNow}\default-get-btn.png",
                        fr"buttons\{consts.languageNow}\hover-get-btn.png",
                        fr"buttons\{consts.languageNow}\press-get-btn.png")

    field_get = Object(all_w + 582 + 304 // 2 - 159 // 2 - 42, all_h + 302, 243, 105,
                       fr"objects\{consts.languageNow}\how-to-get-obj.png")

    running = True
    hero = consts.heroNow
    while running:

        windows.screen.blit(consts.menu_bg, (0, 0))

        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.USEREVENT and event.button == exit_btn):
                terminate()

            if event.type == pygame.USEREVENT and event.button == start_btn:
                transition()
                levels_menu.levels_menu()

            if event.type == pygame.USEREVENT and event.button == settings_btn:
                transition()
                settings.settings_menu()

            if event.type == pygame.USEREVENT and event.button == info_btn:
                transition()
                info.info_menu()

            if event.type == pygame.USEREVENT and event.button == choose_btn:
                if hero == 1 and hero != consts.heroNow:
                    consts.heroNow = 1
                elif hero == 2 and hero != consts.heroNow:
                    if consts.isGetHero2:
                        consts.heroNow = 2
                    else:
                        webbrowser.open('https://t.me/smoladventurebot')
                        consts.isGetHero2 = 1
                fileManager.heroExport(consts.heroNow, consts.isGetHero2)

            if event.type == pygame.USEREVENT and (event.button == arrow_btn or event.button == r_arrow_btn):
                if hero == 1:
                    hero = 2
                elif hero == 2:
                    hero = 1

            for button in [start_btn, settings_btn, info_btn, exit_btn, arrow_btn, r_arrow_btn, choose_btn]:
                button.handle_event(event, consts.volS)

        for obj in [title, updates_field, buttons_field, hero_field]:
            obj.draw(windows.screen)

        hero_choose.draw(windows.screen, hero)

        for button in [start_btn, settings_btn, info_btn, exit_btn, arrow_btn, r_arrow_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(windows.screen)

        choose_btn.check_hover(pygame.mouse.get_pos())
        choose_btn.draw_heroBtn(windows.screen, hero, consts.heroNow, consts.isGetHero2)
        if choose_btn.rect.collidepoint(pygame.mouse.get_pos()) and hero == 2 and not consts.isGetHero2:
            field_get.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
