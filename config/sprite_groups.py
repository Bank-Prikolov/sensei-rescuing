import pygame


class MenuSprites:
    animatedTypedText = pygame.sprite.Group()
    animatedIntro = pygame.sprite.Group()
    animatedHero = pygame.sprite.Group()
    animatedStars = pygame.sprite.Group()
    animatedDots = pygame.sprite.Group()
    animatedError = pygame.sprite.Group()
    animatedFight = pygame.sprite.Group()
    animatedDialogue = pygame.sprite.Group()


class GameSprites:
    touches = pygame.sprite.Group()
    bgroup = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    characters = pygame.sprite.Group()
    un_touches = pygame.sprite.Group()
    finale = pygame.sprite.Group()
    projectiles_group = pygame.sprite.Group()
    shadow_group = pygame.sprite.Group()
    change_group = pygame.sprite.Group()
    thorn_group = pygame.sprite.Group()
    break_group = pygame.sprite.Group()
    trigger_group = pygame.sprite.Group()
    sloniks = pygame.sprite.Group()
    nme_projectiles_group = pygame.sprite.Group()
    another_touches = pygame.sprite.Group()
    x_walls = pygame.sprite.Group()
    y_walls = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()
    boss_projectile_group = pygame.sprite.Group()
    health_bar = pygame.sprite.Group()
    hero_health = pygame.sprite.Group()
    hleb = pygame.sprite.Group()
