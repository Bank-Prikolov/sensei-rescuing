import pygame
import phpStorm_menu
import windows
import consts
import api_requests
import modeSelection
import userRecorder
from itemCreator import Object, Button
from processHelper import terminate, transition


def getting_name():
    field = Object(windows.width // 2 - 576 / 2, windows.height // 2 - 260 // 2, 576, 260,
                   fr"objects\without text\name-field-obj.png")

    text_input = Object(field.x + field.width / 2 - 468 / 2, field.y + field.height / 2 - 60 / 2 - 8, 468, 60,
                        fr"objects\without text\input-rect-obj.png")
    screen_text = Object(text_input.x - 4, text_input.y - 26 - 7, 284, 26,
                         fr"objects\rus\name-text-obj.png")
    user_text = ''
    font = pygame.font.Font(r"data\fonts\PixelLetters.otf", 45)

    cross_btn = Button(field.x + field.width // 2 - 48 - 18, text_input.y + text_input.height + 9, 48, 52,
                       fr"buttons\without text\default-cross-btn.png",
                       fr"buttons\without text\hover-cross-btn.png",
                       fr"buttons\without text\press-cross-btn.png", r"data\sounds\menu-button-sound.mp3")
    mark_btn = Button(field.x + field.width // 2 + 18, text_input.y + text_input.height + 9, 48, 52,
                      fr"buttons\without text\default-mark-btn.png",
                      fr"buttons\without text\hover-mark-btn.png",
                      fr"buttons\without text\press-mark-btn.png", r"data\sounds\menu-button-sound.mp3",
                      "", "", "", "", "",
                      "", "", fr"buttons\without text\no-active-mark-btn.png")

    consts.rightNameChecker = False
    running = True
    while running:

        if user_text != "":
            consts.rightNameChecker = True
        else:
            consts.rightNameChecker = False

        windows.screen.blit(consts.menu_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition()
                    modeSelection.modeSelection()
                else:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif len(user_text) < 12 and event.unicode != " ":
                        user_text += event.unicode

            if event.type == pygame.USEREVENT and event.button == cross_btn:
                transition()
                modeSelection.modeSelection()

            if event.type == pygame.USEREVENT and event.button == mark_btn:
                if api_requests.checkUser(user_text):
                    user_text = ''
                else:
                    userRecorder.userIdentity(user_text)
                    u = userRecorder.get_user(user_text)
                    api_requests.registerUser(str(u[0]), str(u[1]), int(u[2]), int(u[3]))
                    transition()
                    phpStorm_menu.phpStorm_menu()

            for button in [cross_btn]:
                button.handle_event(event, consts.volS)

            mark_btn.handle_event(event, consts.volS, False)

        for obj in [field, text_input, screen_text]:
            obj.draw(windows.screen)

        for button in [cross_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(windows.screen)

        if consts.rightNameChecker:
            mark_btn.check_hover(pygame.mouse.get_pos())
        mark_btn.drawMarkBtn(windows.screen)

        text_surface = font.render(user_text, True, (255, 255, 255))
        windows.screen.blit(text_surface, (text_input.x + 12, text_input.y + 1))

        consts.clock.tick(consts.fps)
        pygame.display.flip()
