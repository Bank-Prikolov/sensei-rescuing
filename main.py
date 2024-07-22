import pygame

from misc import load_image
from windows import start_screen


pygame.init()
pygame.display.set_caption('Sensei Rescuing')
pygame.display.set_icon(load_image(r"objects\without text\ico-obj.png"))

if __name__ == '__main__':
    start_screen()
