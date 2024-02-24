import game
import levels_menu

# Катсцены недоделаны, так как требуют много ресурсов и времени. Однако на игру это никак не повлияет.
# Проект полностью готов, а катсцены лишь дополнят его для большего погружения в историю.


def start_cutscene():
    game.game_def(1)


def boss_greeting_cutscene():
    pass


def boss_win_cutscene():
    pass


def boss_loose_cutscene():
    pass


def end_cutscene():
    levels_menu.levels_menu()
