import pygame
import consts
import levels_menu
import game
import windows
from processHelper import terminate, transition
from itemCreator import Object, Button


def pause(time, sloniks):
    title = Object(windows.width // 2 - 176, windows.height // 2 - 190, 352, 116,
                   fr"objects\{consts.languageNow}\pause-title-obj.png")

    sound_name = Object(windows.width // 2 + 28, windows.height // 2 + 124, 434, 50,
                        fr"objects\{consts.languageNow}\sound-obj.png")
    music_name = Object(windows.width // 2 - 28 - 434, windows.height // 2 + 124, 434, 50,
                        fr"objects\{consts.languageNow}\music-obj.png")
    music_slider_obj = Object(music_name.x + 434 // 2 - 422 // 2, windows.height // 2 + 200, 422, 16,
                              r"objects\without text\slider-obj.png")
    sound_slider_obj = Object(sound_name.x + 434 // 2 - 422 // 2, windows.height // 2 + 200, 422, 16,
                              r"objects\without text\slider-obj.png")
    sound_field = Object(sound_name.x + 434 // 2 - 470 // 2, windows.height // 2 + 110, 470, 128,
                         fr"objects\without text\volume-field-obj.png")
    music_field = Object(music_name.x + 434 // 2 - 470 // 2, windows.height // 2 + 110, 470, 128,
                         fr"objects\without text\volume-field-obj.png")
    music_slider_btn = Button(music_slider_obj.x + 422 - 15, music_slider_obj.y - 6, 26, 28,
                              r"buttons\without text\default-slider-btn.png",
                              r"buttons\without text\hover-slider-btn.png",
                              r"buttons\without text\press-slider-btn.png")
    sound_slider_btn = Button(sound_slider_obj.x + 422 - 15, sound_slider_obj.y - 6, 26, 28,
                              r"buttons\without text\default-slider-btn.png",
                              r"buttons\without text\hover-slider-btn.png",
                              r"buttons\without text\press-slider-btn.png")

    repeat_btn = Button(title.x + title.width // 2 - 94 // 2, title.y + title.height + 18, 94, 104,
                        r"buttons\without text\default-repeat-btn.png",
                        r"buttons\without text\hover-repeat-btn.png",
                        r"buttons\without text\press-repeat-btn.png", r"data\sounds\menu-button-sound.mp3")
    to_lvlmenu_btn = Button(title.x + title.width - 94 - 15, title.y + title.height + 18, 94, 104,
                            r"buttons\without text\default-tolvlmenu-btn.png",
                            r"buttons\without text\hover-tolvlmenu-btn.png",
                            r"buttons\without text\press-tolvlmenu-btn.png", r"data\sounds\menu-button-sound.mp3")
    play_btn = Button(title.x + 15, title.y + title.height + 18, 94, 104,
                      r"buttons\without text\default-play-btn.png",
                      r"buttons\without text\hover-play-btn.png",
                      r"buttons\without text\press-play-btn.png", r"data\sounds\menu-button-sound.mp3")

    pause_field = Object(windows.width // 2 - 430 // 2, windows.height // 2 - 246, 430, 342,
                         fr"objects\without text\pause-field-obj.png")
    left_field = Object(music_name.x + 434 // 2 - 470 // 2, windows.height // 2 - 246, 252, 342,
                        fr"objects\without text\left-field-obj.png")
    time_title = Object(left_field.x + left_field.width // 2 - 196 // 2, windows.height // 2 - 185, 196, 34,
                        fr"objects\{consts.languageNow}\pause-time-obj.png")
    sloniks_title = Object(left_field.x + left_field.width // 2 - 234 // 2, windows.height // 2 - 50, 234, 37,
                           fr"objects\{consts.languageNow}\pause-sloniks-obj.png")
    right_field = Object(sound_name.x + 434 // 2 - 470 // 2 + 470 - 252, windows.height // 2 - 246, 252, 342,
                         fr"objects\{consts.languageNow}\right-field-obj.png")

    TimeFont = pygame.font.Font(r"data\fonts\PixelNumbers.ttf", 50)
    time_sorted = f"{time // 60:02}:{time % 60:02}"
    levelTime = TimeFont.render(time_sorted, True, "#ffffff")
    levelTimeRect = levelTime.get_rect(
        center=(time_title.x + time_title.width // 2, time_title.y + time_title.height + 40))

    SloniksFont = pygame.font.Font(r"data\fonts\PixelNumbers.ttf", 50)
    levelSloniks = SloniksFont.render(str(sloniks), True, "#ffffff")
    levelSloniksRect = levelSloniks.get_rect(
        center=(sloniks_title.x + sloniks_title.width // 2, sloniks_title.y + sloniks_title.height + 40))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                transition()
                levels_menu.levels_menu()

            if event.type == pygame.USEREVENT and event.button == repeat_btn:
                transition()
                game.game_def(consts.lvlNow)

            if event.type == pygame.USEREVENT and event.button == play_btn:
                running = False

            for button in [repeat_btn, to_lvlmenu_btn, play_btn]:
                button.handle_event(event, consts.volS)

        for obj in [consts.pause_field, left_field, time_title, sloniks_title, pause_field, right_field, sound_field,
                    music_field,
                    title, sound_slider_obj, music_slider_obj, music_slider_btn, sound_slider_btn, sound_name,
                    music_name]:
            obj.draw(windows.screen)

        for button in [repeat_btn, to_lvlmenu_btn, play_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(windows.screen)

        windows.screen.blit(levelTime, levelTimeRect)
        windows.screen.blit(levelSloniks, levelSloniksRect)

        pygame.display.flip()
