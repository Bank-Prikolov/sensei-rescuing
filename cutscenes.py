import pygame
import windows
import consts
from itemCreator import Object, Button
from processHelper import terminate


def start_cutscene():
    pass


def boss_greeting_cutscene():
    pass


def boss_win_cutscene():
    field = Object(windows.width // 2 - 430 // 2, windows.height // 2 - 342 // 2, 430, 342,
                   fr"objects\without text\hero-lose-boss-field-obj.png")
    backgr = Object(windows.width - 1016, windows.height - 696, 1008, 688,
           r"objects\without text\hero-lose-boss-backgr-obj.png")

    accept_btn = Button(field.x + 20, field.y + 110, 180, 78,
           fr"buttons\rus\default-accept-btn.png",
           "",
           "",
           r"data\sounds\menu-button-sound.mp3")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        backgr.draw(windows.screen)
        field.draw(windows.screen)
        accept_btn.draw(windows.screen)

        pygame.display.flip()


def end_cutscene():
    pass
