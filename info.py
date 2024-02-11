import pygame
import windows
import consts
import menu
import webbrowser
from itemCreator import Object, Button
from processHelper import terminate, transition


def info_menu():
    if not windows.fullscreen:
        all_w, all_h = windows.width // 2 - 364, windows.height - 619
    else:
        all_w, all_h = windows.width // 2 - 364, windows.height - 820

    title = Object(all_w, all_h, 640, 82, fr"objects\{consts.languageNow}\info-title-obj.png")

    cross_btn = Button(all_w + 660, all_h + 8, 67, 72, r"buttons\without text\default-cross-btn.png",
                       r"buttons\without text\hover-cross-btn.png", r"buttons\without text\press-cross-btn.png",
                       r"data\sounds\menu-button-sound.mp3")
    github_left_btn = Button(all_w + 19, all_h + 449, 67, 72, r"buttons\without text\default-github-btn.png",
                             r"buttons\without text\hover-github-btn.png", r"buttons\without text\press-github-btn.png",
                             r"data\sounds\menu-button-sound.mp3")
    github_right_btn = Button(all_w + 464, all_h + 449, 67, 72, r"buttons\without text\default-github-btn.png",
                              r"buttons\without text\hover-github-btn.png",
                              r"buttons\without text\press-github-btn.png",
                              r"data\sounds\menu-button-sound.mp3")

    field = Object(all_w - 86, all_h + 115, 900, 430, fr"objects\{consts.languageNow}\info-field-obj.png")
    alexandr = Object(all_w + 99, all_h + 462, 269, 46, fr"objects\{consts.languageNow}\alexandr-obj.png")
    igor = Object(all_w + 544, all_h + 462, 142, 45, fr"objects\{consts.languageNow}\igor-obj.png")

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

            if event.type == pygame.USEREVENT and event.button == github_left_btn:
                webbrowser.open('https://github.com/mikhalexandr')

            if event.type == pygame.USEREVENT and event.button == github_right_btn:
                webbrowser.open('https://github.com/WaizorSote')

            for button in [github_left_btn, github_right_btn, cross_btn]:
                button.handle_event(event, consts.volS)

        for obj in [title, field, alexandr, igor]:
            obj.draw(windows.screen)

        for button in [github_left_btn, github_right_btn, cross_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
