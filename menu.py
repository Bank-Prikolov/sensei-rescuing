import pygame
import webbrowser
import windows
import consts
import fileManager
import info
import settings
import levels_menu
import soundManager
import spriteGroups
from processHelper import terminate, transition
from itemCreator import Object, Button
from itemChanger import heroOnScreenChanger


def main_menu():
    soundManager.menu_theme()

    title = Object(windows.width // 2 - 443, windows.height // 2 - 518 // 2, 886, 80,
                   fr"objects\{consts.languageNow}\menu-title-obj.png")

    updates_field = Object(title.x, title.y + 102, 304, 416, fr"objects\{consts.languageNow}\updates-field-obj.png")

    buttons_field = Object(title.x + title.width / 2 - 256 / 2, title.y + 102, 256, 416,
                           r"objects\without text\menu-buttons-field-obj.png")
    start_btn = Button(buttons_field.x + buttons_field.width / 2 - 120, title.y + 110, 240, 100,
                       fr"buttons\{consts.languageNow}\default-start-btn.png",
                       fr"buttons\{consts.languageNow}\hover-start-btn.png",
                       fr"buttons\{consts.languageNow}\press-start-btn.png",
                       r"data\sounds\menu-button-sound.mp3")
    settings_btn = Button(buttons_field.x + buttons_field.width / 2 - 120, title.y + 210, 240, 100,
                          fr"buttons\{consts.languageNow}\default-settings-btn.png",
                          fr"buttons\{consts.languageNow}\hover-settings-btn.png",
                          fr"buttons\{consts.languageNow}\press-settings-btn.png",
                          r"data\sounds\menu-button-sound.mp3")
    info_btn = Button(buttons_field.x + buttons_field.width / 2 - 120, title.y + 310, 240, 100,
                      fr"buttons\{consts.languageNow}\default-info-btn.png",
                      fr"buttons\{consts.languageNow}\hover-info-btn.png",
                      fr"buttons\{consts.languageNow}\press-info-btn.png",
                      r"data\sounds\menu-button-sound.mp3")
    exit_btn = Button(buttons_field.x + buttons_field.width / 2 - 120, title.y + 410, 240, 100,
                      fr"buttons\{consts.languageNow}\default-exit-btn.png",
                      fr"buttons\{consts.languageNow}\hover-exit-btn.png",
                      fr"buttons\{consts.languageNow}\press-exit-btn.png",
                      r"data\sounds\menu-button-sound.mp3")

    hero_field = Object(title.x + title.width - 304, title.y + 102, 304, 416,
                        fr"objects\{consts.languageNow}\hero-field-obj.png")
    choose_btn = Button(hero_field.x + hero_field.width // 2 - 159 // 2, title.y + 410, 159, 48,
                        fr"buttons\{consts.languageNow}\default-choose-btn.png",
                        fr"buttons\{consts.languageNow}\hover-choose-btn.png",
                        fr"buttons\{consts.languageNow}\press-choose-btn.png",
                        r"data\sounds\menu-button-sound.mp3", "", consts.heroNow,
                        fr"buttons\{consts.languageNow}\default-get-btn.png",
                        fr"buttons\{consts.languageNow}\hover-get-btn.png",
                        fr"buttons\{consts.languageNow}\press-get-btn.png")
    arrow_btn = Button(choose_btn.x + choose_btn.width + 5, title.y + 102 + 95 + 241 // 2 - 36 // 2, 36, 40,
                       r"buttons\without text\default-arrow-btn.png", r"buttons\without text\hover-arrow-btn.png",
                       r"buttons\without text\press-arrow-btn.png", r"data\sounds\menu-button-sound.mp3")
    r_arrow_btn = Button(choose_btn.x - 36 - 5, title.y + 102 + 95 + 241 // 2 - 36 // 2, 36, 40,
                         r"buttons\without text\default-r-arrow-btn.png", r"buttons\without text\hover-r-arrow-btn.png",
                         r"buttons\without text\press-r-arrow-btn.png", r"data\sounds\menu-button-sound.mp3")
    field_get = Object(title.x + 582 + 304 // 2 - 159 // 2 - 42, title.y + 302, 243, 105,
                       fr"objects\{consts.languageNow}\how-to-get-obj.png")
    field_ura = Object(title.x + 582, title.y + 102, 304, 416,
                       fr"objects\{consts.languageNow}\hero-field-new-character-obj.png")
    ura_btn = Button(field_ura.x + field_ura.width // 2 - 200 // 2, title.y + 370, 200, 90,
                     fr"buttons\{consts.languageNow}\default-ura-btn.png",
                     fr"buttons\{consts.languageNow}\hover-ura-btn.png",
                     fr"buttons\{consts.languageNow}\press-ura-btn.png",
                     r"data\sounds\menu-button-sound.mp3")

    running = True
    hero = consts.heroNow if not consts.getHero else 2
    current_hero = heroOnScreenChanger(hero, title, hero_field)
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
                        consts.getHero = 1
                fileManager.heroExport(consts.heroNow, consts.isGetHero2, consts.getHero)

            if event.type == pygame.USEREVENT and event.button == ura_btn:
                consts.getHero = 0
                fileManager.heroExport(consts.heroNow, consts.isGetHero2, consts.getHero)

            if event.type == pygame.USEREVENT and (event.button == arrow_btn or event.button == r_arrow_btn):
                if hero == 1:
                    hero = 2
                    current_hero = heroOnScreenChanger(hero, title, hero_field)
                elif hero == 2:
                    hero = 1
                    current_hero = heroOnScreenChanger(hero, title, hero_field)

            for button in [start_btn, settings_btn, info_btn, exit_btn]:
                button.handle_event(event, consts.volS)

            if not consts.getHero:
                for hero_button in [arrow_btn, r_arrow_btn, choose_btn]:
                    hero_button.handle_event(event, consts.volS)

            if consts.getHero:
                ura_btn.handle_event(event, consts.volS)

        for obj in [title, updates_field, buttons_field, hero_field]:
            obj.draw(windows.screen)

        for button in [start_btn, settings_btn, info_btn, exit_btn, arrow_btn, r_arrow_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(windows.screen)

        current_hero.update()
        spriteGroups.animatedHero.draw(windows.screen)

        if not consts.getHero:
            choose_btn.check_hover(pygame.mouse.get_pos())
            choose_btn.draw_heroBtn(windows.screen, hero, consts.heroNow, consts.isGetHero2)
            if choose_btn.rect.collidepoint(pygame.mouse.get_pos()) and hero == 2 and not consts.isGetHero2:
                field_get.draw(windows.screen)

        if consts.getHero:
            field_ura.draw(windows.screen)
            ura_btn.check_hover(pygame.mouse.get_pos())
            ura_btn.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
