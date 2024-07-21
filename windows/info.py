import pygame
from config import consts
import menu
import webbrowser
from windows.items.item_creating import Object, Button
from misc.specfunctions import terminate, transition


def info_menu():
    title = Object(windows.width // 2 - 771 / 2 if consts.languageNow == 'rus' else windows.width // 2 - 629 / 2,
                   windows.height // 2 - 534 // 2,
                   684 if consts.languageNow == 'rus' else 542, 82, fr"objects\{consts.languageNow}\info-title-obj.png")
    cross_btn = Button(title.x + title.width + 20, title.y + 8, 67, 72, r"buttons\without text\default-cross-btn.png",
                       r"buttons\without text\hover-cross-btn.png", r"buttons\without text\press-cross-btn.png",
                       r"data\sounds\menu-button-sound.mp3")

    field = Object(windows.width // 2 - 900 / 2, title.y + 104, 900, 430,
                   fr"objects\{consts.languageNow}\info-field-obj.png")
    github_left_btn = Button(windows.width // 2 - 333.5, title.y + 438, 67, 72,
                             r"buttons\without text\default-github-btn.png",
                             r"buttons\without text\hover-github-btn.png",
                             r"buttons\without text\press-github-btn.png",
                             r"data\sounds\menu-button-sound.mp3")
    github_right_btn = Button(windows.width // 2 + 111.5, title.y + 438, 67, 72,
                              r"buttons\without text\default-github-btn.png",
                              r"buttons\without text\hover-github-btn.png",
                              r"buttons\without text\press-github-btn.png",
                              r"data\sounds\menu-button-sound.mp3")
    alexandr = Object(github_left_btn.x + github_left_btn.width + 13, title.y + 451, 269, 46,
                      fr"objects\{consts.languageNow}\alexandr-obj.png")
    igor = Object(github_right_btn.x + github_right_btn.width + 13, title.y + 451, 142, 45,
                  fr"objects\{consts.languageNow}\igor-obj.png")

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
