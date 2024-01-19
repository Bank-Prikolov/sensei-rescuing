import pygame
import sys
from load_image import load_image
from itemCreator import Button, Object
import menu

pygame.init()

size = WIDTH, HEIGHT = 1024, 704
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption('Sensei Rescuing')

cursor = load_image(r'objects\cursor-obj.png')
pygame.mouse.set_visible(False)

title = Object(WIDTH // 2 - 150, HEIGHT - 520, 300, 100, r"objects\pause-title-obj.png")
field = Object(WIDTH - 1016, HEIGHT - 696, 1008, 688, r"objects\windows-field-obj.png")

repeat_btn = Button(WIDTH // 2 - 150 + 102, HEIGHT // 2 - 30, 94, 104, r"buttons\default-repeat-btn.png", r"buttons\hover-repeat-btn.png",
                r"buttons\press-repeat-btn.png", r"data\sounds\menu-button-sound.mp3")
to_lvlmenu_btn = Button(WIDTH // 2 - 150 + 212, HEIGHT // 2 - 30, 94, 104, r"buttons\default-tolvlmenu-btn.png",
                 r"buttons\hover-tolvlmenu-btn.png",
                 r"buttons\press-tolvlmenu-btn.png", r"data\sounds\menu-button-sound.mp3")
play_btn = Button(WIDTH // 2 - 150 - 7, HEIGHT // 2 - 30, 94, 104, r"buttons\default-play-btn.png",
                 r"buttons\hover-play-btn.png",
                 r"buttons\press-play-btn.png", r"data\sounds\menu-button-sound.mp3")


def game_pause():
    running = True
    fps = 60
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                menu.levels_menu()

            for button in [repeat_btn, to_lvlmenu_btn, play_btn]:
                button.handle_event(event)
                button.handle_event(event)

        for obj in [field, title]:
            obj.draw(screen)

        for button in [repeat_btn, to_lvlmenu_btn, play_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)

        clock.tick(fps)

        x_c, y_c = pygame.mouse.get_pos()
        if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
            screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


game_pause()
