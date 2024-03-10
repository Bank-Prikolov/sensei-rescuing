import pygame
import windows
import consts
import threading
import menu
from processHelper import load_image, terminate


def loading_items():
    consts.WaiHleb = load_image(fr"cutscenes\hleb-greeting\hleb-greeting-wai-dialogue.png")
    consts.StrongestHleb = load_image(fr"cutscenes\hleb-greeting\hleb-greeting-thest-dialogue.png")
    consts.WaiBossGreeting = load_image(fr"cutscenes\boss-greeting\boss-greeting-wai-dialogue.png")
    consts.StrongestBossGreeting = load_image(fr"cutscenes\boss-greeting\boss-greeting-thest-dialogue.png")
    consts.WaiBossEnding = load_image(fr"cutscenes\boss-lose\boss-lose-wai-dialogue.png")
    consts.StrongestBossEnding = load_image(fr"cutscenes\boss-lose\boss-lose-thest-dialogue.png")
    consts.WaiHleb_FS = pygame.transform.scale(consts.WaiHleb, (consts.WaiHleb.get_width() * 1.5,
                                                                consts.WaiHleb.get_height() * 1.5))
    consts.StrongestHleb_FS = pygame.transform.scale(consts.StrongestHleb, (consts.StrongestHleb.get_width() * 1.5,
                                                                            consts.StrongestHleb.get_height() * 1.5))
    consts.WaiBossGreeting_FS = pygame.transform.scale(consts.WaiBossGreeting,
                                                       (consts.WaiBossGreeting.get_width() * 1.5,
                                                        consts.WaiBossGreeting.get_height() * 1.5))
    consts.StrongestBossGreeting_FS = pygame.transform.scale(consts.StrongestBossGreeting,
                                                             (consts.StrongestBossGreeting.get_width() * 1.5,
                                                              consts.StrongestBossGreeting.get_height() * 1.5))
    consts.WaiBossEnding_FS = pygame.transform.scale(consts.WaiBossEnding, (consts.WaiBossEnding.get_width() * 1.5,
                                                                            consts.WaiBossEnding.get_height() * 1.5))
    consts.StrongestBossEnding_FS = pygame.transform.scale(consts.StrongestBossEnding,
                                                           (consts.StrongestBossEnding.get_width() * 1.5,
                                                            consts.StrongestBossEnding.get_height() * 1.5))


def loading_menu():
    loadingItems = threading.Thread(target=loading_items)
    loadingItems.start()

    running = True
    while running:

        windows.screen.blit(consts.menu_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        if not loadingItems.is_alive():
            menu.main_menu()

        pygame.display.flip()
