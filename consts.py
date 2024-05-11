import pygame
import fileManager
from processHelper import load_image

# menu and game consts
clock = pygame.time.Clock()
fps = 60

# menu consts
pause_field = None
game_state_field = None
backgrBossWin = None
isSliderMusic = False
isSliderSound = False
lvlNow = None
playingMenuMusic = True
heroNow, isGetHero2, getHero = fileManager.heroImport()
wM, wS, volS = fileManager.volumeImport()
languageNow = fileManager.languageImport()
rightNameChecker = None

# game consts
runright, runleft, sitting = False, False, False
jumping = False
falling = False
lookingright = 1
shooting = 0
xspeed = 0
yspeed = 0
hero = None
cheatOn = True
bossHit = 0
heroHit = 0
hitNow = False
tmpHit = 0
heroHP = 3
end_cs = False
final_countdown = False
animend = False
WaiHleb = None
StrongestHleb = None
WaiBossGreeting = None
StrongestBossGreeting = None
WaiBossEnding = None
StrongestBossEnding = None
WaiHleb_FS = None
StrongestHleb_FS = None
WaiBossGreeting_FS = None
StrongestBossGreeting_FS = None
WaiBossEnding_FS = None
StrongestBossEnding_FS = None
nextFrames = True
pause_btn = None


# characters
wai = r'characters\hero-wai.png'
the_strongest = r'characters\hero-the-strongest.png'
shadow = r'characters\shadow.png'
slonik = r'characters\enemy-slonik-php.png'
kowlad = r'characters\enemy-kowlad.png'
hleb = r'characters\hleb.png'
tp = r'characters\boss-tp.png'

# projectiles
php = r'characters\projectile-php.png'
fireball = r'characters\projectile-fireball.png'
hollow_purple = r'characters\projectile-hollow-purple.png'
boos_prjct = r'characters\projectile-php-marker.png'
projectileObj_speed = []
b_projectile_speed = []

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
closed = r'textures\ff-texture.png'
startdoor = r'textures\k-texture.png'
broken = r'textures\C_broken-texture.png'

# levels
lvl1 = r'level-1.txt'
lvl2 = r'endless_1.txt'
# lvl2 = r'level-2.txt'
lvl2_1 = r'level-2-1.txt'
lvl3 = r'level-3.txt'
lvl3_1 = r'level-3-1.txt'
lvl3_2 = r'level-3-2.txt'

endless1 = r'endless_1.txt'
endless2 = r'endless_2.txt'
endless3 = r'endless_3.txt'

# backgrounds
game_bg = r'backgrounds\game-bg.png'
img = load_image(r'backgrounds\main-menu-bg.png')
img_fs = load_image(r"backgrounds\main-menu-fullScreen-bg.png")
menu_bg = None
