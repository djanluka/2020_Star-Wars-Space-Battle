import pygame
from pygame import mixer
from source import gui
from source import glob

ABOUT = [
        'This star wars game like Galaga',
        'is made by MATF students:',
        'Boris Cvitak',
        'Ognjen Stamenkovic',
        'Predrag Mitic'
        ]

#DODATO promenljive koje pamte kontrole
CONTROL_LEFT_ORD = ord('a')
CONTROL_LEFT = 'a'
CONTROL_RIGHT_ORD = ord('d')
CONTROL_RIGHT = 'd'
CONTROL_FIRE_ORD = ord('w')
CONTROL_FIRE = 'w'


TWO_CONTROL_LEFT_ORD1 = ord('a')
TWO_CONTROL_LEFT1 = 'a'
TWO_CONTROL_RIGHT_ORD1 = ord('d')
TWO_CONTROL_RIGHT1 = 'd'
TWO_CONTROL_FIRE_ORD1 = ord('w')
TWO_CONTROL_FIRE1 = 'w'

TWO_CONTROL_LEFT_ORD2 = pygame.K_RIGHT
TWO_CONTROL_LEFT2 = 'KEY_RIGHT'
TWO_CONTROL_RIGHT_ORD2 = pygame.K_LEFT
TWO_CONTROL_RIGHT2 = 'KEY_LEFT'
TWO_CONTROL_FIRE_ORD2 = pygame.K_UP
TWO_CONTROL_FIRE2 = 'KEY_UP'

CONTROLS_TEXT = [
                'First player:                                                                                            Second player:',
                f'To left : {CONTROL_LEFT}                                                                                                                  To left : 4',
                f'To right : {CONTROL_RIGHT}                                                                                                               To left : 6',
                f'To shoot : {CONTROL_FIRE}                                                                                                        To shoot : 8'
                ]

VOLUME_VALUES = {
                '0_PERCENT': 0,
                '10_PERCENT': 0.1,
                '30_PERCENT': 0.3,
                '50_PERCENT': 0.5,
                '70_PERCENT': 0.7,
                '100_PERCENT': 1,
                }
emi_fighter = [
                pygame.image.load('images/enm1_40px.png'),
                pygame.image.load('images/enm2_40px.png'),
                pygame.image.load('images/enm3_40px.png'),
                pygame.image.load('images/enm4_40px.png'),
               ]

num_enemies = [
                'Nema enemy-ja za 0 level',
                [76, 76, 76],
                [76, 76, 76],
                [8, 12, 16]
                ]


destroyers = [
                pygame.image.load('images/destroyer.png'),
                pygame.image.load('images/destroyer.png'),
                pygame.image.load('images/destroyer.png')
             ]

stories = [
            'Nema slike za 0 level',
            pygame.image.load('images/story1.png'),
            pygame.image.load('images/story2.png'),
            pygame.image.load('images/story3.png')
          ]

ENEMIES_IMG_30px = [pygame.image.load('images/enm1_30px.png'),
                    pygame.image.load('images/enm2_30px.png'),
                    pygame.image.load('images/enm3_30px.png'),
                    pygame.image.load('images/enm4_30px.png'),
                    ]


#IZMENJENO
#postavio sam LEVEL odmah na 1, da bi se lepo uklopilo sa make_enemies1,2,3
LEVEL_IMAGES = ['', 'images/one.png', 'images/two.png', 'images/three.png']
LEVEL = 1
FIGHT = 0

#TO DO
#postavitii muziku na 0.5
#ja sam se ja sad iskljucio da ne smara svaki put
GAME_VOLUME = 0
MENU_VOLUME = 0

WINDOW_SIZE = (1300, 700)
MENU_SIZE = (500, 450)
START_WARS_LOGO_POS = (100, 600)
PAUSE_ONE_PLAYER_POS = (1265, 665)
PAUSE_TWO_PLAYERS_POS = (634, 5)
BLACK_COLOR = (0, 0, 0)
WALL_START_POS = (650, 700)
WALL_END_POS = (650, 40)
WALL_WIDTH = 15
NUM_PLAYERS = 'ONE_PLAYER'

ENEMIES_IS_READY = False

bullets_enm_list = pygame.sprite.Group()
rockets_list = pygame.sprite.Group()
enemies_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
left_rockets_list = pygame.sprite.Group()
right_rockets_list = pygame.sprite.Group()

game_background = pygame.image.load('images/game_background.jpg')
pause_img_1 = pygame.image.load('images/pause1.png')
pause_img_2 = pygame.image.load('images/pause2.png')

x_wing = pygame.image.load('images/ply6.png')
rocket = pygame.image.load('images/rocket_player.png')


def return_to_main_menu():
    mixer.music.stop()
    gui.main_menu.enable()
    mixer.music.load('sounds/menu_music.mp3')
    mixer.music.play(-1)
    mixer.music.set_volume(glob.MENU_VOLUME)