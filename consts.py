import pygame
from processHelper import load_image

# game consts
test = r'test2.txt'
wai = r'characters\hero.png'
floor = r'textures\0-texture.png'
wallx = r'textures\#-texture.png'
wally = r'textures\=-texture.png'
lvl1 = r'lvl_1.txt'
lvl2 = r'lvl_2.txt'
lvl2_1 = r'lvl_2_1.txt'
lvl3 = r'lvl_3.txt'
lvl3_1 = r'lvl_3_1.txt'
lvl3_2 = r'lvl_3_2.txt'
plat = r'textures\_-texture.png'
placeholder = r'textures\_invisiblethingcausethisthingissostupidijustdontgetit-texture.png'
finish = r'textures\F-texture.png'
bg1 = r'backgrounds\game-bg.png'
shadow = r'characters\shadow.png'
fireball = r'characters\fireball.png'
change = r'textures\C-texture.png'
thorn = r'textures\^-texture.png'
boss_door = r'textures\S-texture.png'
trigger = r'textures\t-texture.png'
slonik = r'characters\slonik_php.png'
php = r'characters\php.png'
invis = r'textures\%-texture.png'
horizon = r'textures\&-texture.png'

# menu and game consts
cursor = load_image(r'objects\without text\cursor-obj.png')
clock = pygame.time.Clock()
fps = 60

# menu animated sprite groups
bg_group_start_screen = pygame.sprite.Group()
bg_group_intro = pygame.sprite.Group()
bg_group_over = pygame.sprite.Group()
bg_group_complete = pygame.sprite.Group()
