import pygame
import sys
from load_image import load_image

pygame.init()

size = WIDTH, HEIGHT = 1024, 704
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sensei Rescuing')
clock = pygame.time.Clock()


def transition():
    running = True
    transition_level = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        transition_surface = pygame.Surface((WIDTH, HEIGHT))
        transition_surface.fill((0, 0, 0))
        transition_surface.set_alpha(transition_level)
        screen.blit(transition_surface, (0, 0))

        transition_level += 5
        if transition_level >= 105:
            transition_level = 255
            running = False

        pygame.display.flip()
        clock.tick(65)
