import pygame
import fileManager
from processHelper import load_image

# menu and game consts
clock = pygame.time.Clock()
fps = 60

# menu animated sprite groups
bg_group_start_screen = pygame.sprite.Group()
bg_group_intro = pygame.sprite.Group()
bg_group_over = pygame.sprite.Group()
bg_group_complete = pygame.sprite.Group()

# menu consts
img = load_image(r'backgrounds\main-menu-bg.png')
img_fs = load_image(r"backgrounds\main-menu-fullScreen-bg.png")
menu_bg = None
pause_field = None
game_state_filed = None
isSliderMusic = False
isSliderSound = False
isPauseSliderMusic = False
isPauseSliderSound = False
lvlNow = None
firstTime = True
heroNow, isGetHero2 = fileManager.heroImport()
wM, wS, volS = fileManager.volumeImport()
languageNow = fileManager.languageImport()

# characters
wai = r'characters\hero-wai.png'
the_strongest = r'characters\hero-the-strongest.png'
shadow = r'characters\shadow.png'
slonik = r'characters\enemy-slonik-php.png'
kowlad = r'characters\enemy-kowlad.png'

# projectiles
php = r'characters\projectile-php.png'
fireball = r'characters\projectile-fireball.png'
hollow_purple = r'characters\projectile-hollow-purple.png'

# textures
floor = r'textures\0-texture.png'
wallx = r'textures\#-texture.png'
wally = r'textures\=-texture.png'
plat = r'textures\_-texture.png'
placeholder = r'textures\_invisiblethingcausethisthingissostupidijustdontgetit-texture.png'
finish = r'textures\F-texture.png'
change = r'textures\C-texture.png'
thorn = r'textures\^-texture.png'
boss_door = r'textures\S-texture.png'
trigger = r'textures\t-texture.png'
invis = r'textures\%-texture.png'
horizon = r'textures\&-texture.png'

# levels
lvl1 = r'lvl_1.txt'
lvl2 = r'lvl_2.txt'
lvl2_1 = r'lvl_2_1.txt'
lvl3 = r'lvl_3.txt'
lvl3_1 = r'lvl_3_1.txt'
lvl3_2 = r'lvl_3_2.txt'

# backgrounds
game_bg = r'backgrounds\game-bg.png'
