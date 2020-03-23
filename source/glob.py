import pygame 

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
CONTROL_SHOOT_ORD = ord('w')
CONTROL_SHOOT = 'w'

CONTROLS_TEXT = [
                'First player:                                                                                            Second player:',
                f'To left : {CONTROL_LEFT}                                                                                                                  To left : 4',
                f'To right : {CONTROL_RIGHT}                                                                                                               To left : 6',
                f'To shoot : {CONTROL_SHOOT}                                                                                                        To shoot : 8'
                ]

VOLUME_VALUES = {
                '0_PERCENT': 0,
                '10_PERCENT': 0.1,
                '30_PERCENT': 0.3,
                '50_PERCENT': 0.5,
                '70_PERCENT': 0.7,
                '100_PERCENT': 1,
                }

LEVEL_IMAGES = ['images/one.png', 'images/two.png', 'images/three.png']
LEVEL = 0

GAME_VOLUME = 0.5
MENU_VOLUME = 0.5

WINDOW_SIZE = (1300, 700)
MENU_SIZE = (500, 450)
START_WARS_LOGO_POS = (100, 600)
PAUSE_ONE_PLAYER_POS = (1260, 5)
PAUSE_TWO_PLAYERS_POS = (634, 5)
BLACK_COLOR = (0, 0, 0)
WALL_START_POS = (650, 700)
WALL_END_POS = (650, 40)
WALL_WIDTH = 15
NUM_PLAYERS = 'ONE_PLAYER'


bullets_enm_list = pygame.sprite.Group()
rockets_list = pygame.sprite.Group()
enemies_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

game_background = pygame.image.load('images/game_background.jpg')
pause_img = pygame.image.load('images/pause.png')