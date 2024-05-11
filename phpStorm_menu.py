import pygame
import windows
import consts
import modeSelection
import userRecorder
from itemCreator import Button
from processHelper import terminate, transition


def phpStorm_menu():
    continue_btn = Button(windows.width // 2 - 288 // 2, windows.height // 2 - 112 - 12, 288, 112,
                          fr"buttons\rus\default-continue-btn.png", fr"buttons\rus\hover-continue-btn.png",
                          fr"buttons\rus\press-continue-btn.png", r"data\sounds\menu-button-sound.mp3",
                          "", "", "", "", "",
                          "", "", "", fr"buttons\rus\no-active-continue-btn.png")
    new_game_btn = Button(windows.width // 2 - 288 // 2, windows.height // 2 + 12, 288, 112,
                          fr"buttons\rus\default-newgame-btn.png", fr"buttons\rus\hover-newgame-btn.png",
                          fr"buttons\rus\press-newgame-btn.png", r"data\sounds\menu-button-sound.mp3")
    if userRecorder.get_info()[2] == 0:
        consts.continueChecker = False
    else:
        consts.continueChecker = True
    running = True
    while running:

        windows.screen.blit(consts.menu_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition()
                    modeSelection.modeSelection()

            for button in [new_game_btn]:
                button.handle_event(event, consts.volS)

            for button in [continue_btn]:
                button.handle_event(event, consts.volS, continueCheck=False)

        for button in [new_game_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(windows.screen)

        if consts.continueChecker:
            continue_btn.check_hover(pygame.mouse.get_pos())
        continue_btn.drawContinueBtn(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
