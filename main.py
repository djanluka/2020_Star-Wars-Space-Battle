import pygame
import pygameMenu
from pygame import mixer
import math
import random

ABOUT = [
        'This star wars game like Galaga',
        'is made by MATF students:',
        'Boris Cvitak',
        'Ognjen Stamenkovic',
        'Predrag Mitic'
        ]

CONTROLS_TEXT = [
                'First player:                                                                                            Second player:',
                'To left : A                                                                                                                  To left : 4',
                'To right : D                                                                                                               To left : 6',
                'To shoot : W                                                                                                        To shoot : 8'
                ]

VOLUME_VALUES = {
                '10_PERCENT': 0.1,
                '30_PERCENT': 0.3,
                '50_PERCENT': 0.5,
                '70_PERCENT': 0.7,
                '100_PERCENT': 1,
                }
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

screen = None
background = None
star_wars_logo = None
main_menu = None
pause_menu = None


class Player():
    def __init__(self):
        self.position_x = 0
        self.position_x = 0
        self.score = 100

    def show(self, img):
        screen.blit(img, (self.position_x, self.position_y))

class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([5, 100])
        self.rect = self.image.get_rect()

    def show_rocket(self, rocket):
        screen.blit(rocket, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y -= 4

class Destroyer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([100, 50])
        self.rect = self.image.get_rect()
        self.health = 100

    def show(self, img):
        screen.blit(img, (self.rect.x, self.rect.y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40,40])
        self.rect = self.image.get_rect()

    def show(self, img):
        screen.blit(img, (self.rect.x, self.rect.y))

class BulletEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([8, 8])
        self.image.fill((100,200,255))
        self.rect = self.image.get_rect()
        self.direction = [0, 6]
   
    def show_rocket(self, rocket):
        screen.blit(rocket, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x += self.direction[0] * 8
        self.rect.y += self.direction[1] * 8


bullets_enm_list = pygame.sprite.Group()
rockets_list = pygame.sprite.Group()
enemies_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

def make_enemies(number):
    for n in range(number):
        enm = Enemy()
        enm.rect.y = 60
        distance = WINDOW_SIZE[0]/number
        enm.rect.x = n * distance  + distance / 2 
        enemies_list.add(enm)
        all_sprites_list.add(enm)

def start_game_one_player():
    global screen
    global main_menu
    global pause_menu

    game_background = pygame.image.load('images/game_background.png')
    playerImg = pygame.image.load('images/player.png')
    pauseImg = pygame.image.load('images/pause.png')
    rocketImg = pygame.image.load('images/rocket-launch.png')
    destroyerImg = pygame.image.load('images/destroyer.png')
    enemyImg = pygame.image.load('images/enemy1.png')

    player = Player()

    player.position_y = 600
    player.position_x = 250
    player.score = 100
    left_margin = 0 + 10
    right_margin = WINDOW_SIZE[0] - 70  # Ovo je zavisno od sirine slike aviona
    time = 0  # timer za animaciju sa raketicama
    timer_destroyer = 0
    destroyer = Destroyer()
    rafal_timer = 0

    make_enemies(9)
    while True:
        time += 3
        screen.blit(game_background, (0, 0))
        screen.blit(pauseImg, PAUSE_ONE_PLAYER_POS)


        for enm in enemies_list:
            enm.rect.x
            enm.show(enemyImg)
        
        num_enemies = len(enemies_list.sprites())
            
        if num_enemies > 0:
            rand_enm = random.choice(enemies_list.sprites())        
            
            if time % 80/num_enemies == 0: # Napad neprijatelja: 80 ucestalost paljbe 
                bul = BulletEnemy()
                bul.rect.x = rand_enm.rect.x + 20
                bul.rect.y = rand_enm.rect.y + 20
                seanse = math.sqrt( (bul.rect.x - player.position_x)**2 + (bul.rect.y - player.position_y)**2)
                bul.direction[0] = (player.position_x - bul.rect.x) / seanse + 0.1  
                bul.direction[1] = (player.position_y - bul.rect.y) / seanse + 0.1  
                bullets_enm_list.add(bul)
                all_sprites_list.add(bul)

            bullets_enm_list.draw(screen)

        else:
            timer_destroyer += 3
            destroyer.rect.x = WINDOW_SIZE[0] / 2 - 50
            destroyer.rect.y = (int(timer_destroyer/ 5) - 150 if timer_destroyer < 1000 else 50)
            if destroyer.health > 0:
                destroyer.show(destroyerImg)
                if time > 1000:  #
                    pygame.draw.rect(screen, (200, 10, 10), (150, 10, destroyer.health * 10, 20))
                

        for bullet in bullets_enm_list:
            #kolizija sa playerom
            if bullet.rect.x in range(player.position_x, player.position_x + 64):
                if bullet.rect.y in range(player.position_y+20, player.position_y + 64):
                    bullets_enm_list.remove(bullet) 
                    player.score -= 10


            if bullet.rect.y > 1000:
                bullets_enm_list.remove(bullet)

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    exit()

            #Ukoliko smo kliknuli na pauzu, otvaramo pause_meni i zaustavljamo muziku
            if e.type == pygame.MOUSEBUTTONDOWN and pause_menu.is_disabled():
                if pauseImg.get_rect(topleft=PAUSE_ONE_PLAYER_POS).collidepoint(pygame.mouse.get_pos()):
                    pause_menu.enable()

        #Za kretanje ne mogu koristi events jer treba da se krece i kada se samo drzi taster
        pressed = pygame.key.get_pressed()
        movement = 4

        if pressed[pygame.K_a] and player.position_x > left_margin:
            player.position_x -= movement

        if pressed[pygame.K_d] and player.position_x < right_margin:
            player.position_x += movement
        
        if pressed[pygame.K_w]: 
            if rafal_timer % 50 is 0:     
                #Zvuk pri ispaljivanju metaka
                rocket_sound = mixer.Sound('sounds/laser.wav')
                rocket_sound.play()

                rocket = Rocket()
                rocket.rect.x = player.position_x + 16  # razlika u velicina slika
                rocket.rect.y = player.position_y

                all_sprites_list.add(rocket)
                rockets_list.add(rocket)
            rafal_timer += 1
        else:
            rafal_timer = 0
        
        for r in rockets_list:
            r.show_rocket(rocketImg)
            
            # Obrada kolizije player vs enemies
            
            enemy_hit_list = pygame.sprite.spritecollide(r, enemies_list, True)

            for enm in enemy_hit_list:
                rockets_list.remove(r)
                all_sprites_list.remove(r)
                enemies_list.remove(enm)

                # Obrada kolizije player vs destroyer
            if r.rect.x in range(destroyer.rect.x, destroyer.rect.x + 110):
                dist = 110 - r.rect.x + destroyer.rect.x
                if r.rect.y < destroyer.rect.y + dist:
                    rockets_list.remove(r)
                    all_sprites_list.remove(r)

                    #Zvuk eksplozije kada metak pogodi protivnika
                    explosion_sound = mixer.Sound('sounds/explosion.wav')
                    explosion_sound.play()

                    destroyer.health -= 5

            if r.rect.y < -20:
                rockets_list.remove(r)
                all_sprites_list.remove(r)

        # Ovde iscrtavamo x-wing zbog toga sto raketa izlazi (pre) ispod njega
        if player.score > 0:
            player.show(playerImg)
            pygame.draw.rect(screen, (0,100,100), (150, WINDOW_SIZE[1]-30, player.score * 10, 20))

        if main_menu.is_enabled():
            main_menu.mainloop(events)
        elif pause_menu.is_enabled():
            pause_menu.mainloop(events)

        all_sprites_list.update()
        pygame.display.update()


def start_game_two_player():
    global screen
    global main_menu
    global pause_menu

    game_background = pygame.image.load('images/game_background.png')
    playerImg = pygame.image.load('images/player.png')
    pauseImg = pygame.image.load('images/pause.png')

    while True:
        screen.blit(game_background, (0, 0))
        pygame.draw.line(screen, BLACK_COLOR, WALL_START_POS, WALL_END_POS, WALL_WIDTH)
        screen.blit(playerImg, (280, 600))
        screen.blit(playerImg, (950, 600))
        screen.blit(pauseImg, PAUSE_TWO_PLAYERS_POS)

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    exit()

            #Ukoliko smo kliknuli na pauzu, otvaramo pause_meni i zaustavljamo muziku
            if e.type == pygame.MOUSEBUTTONDOWN and pause_menu.is_disabled():
                if pauseImg.get_rect(topleft=PAUSE_TWO_PLAYERS_POS).collidepoint(pygame.mouse.get_pos()):
                    mixer.music.pause()
                    pause_menu.enable()

        if main_menu.is_enabled():
            main_menu.mainloop(events)
        elif pause_menu.is_enabled():
            pause_menu.mainloop(events)

        pygame.display.update()


def start_game():

    global main_menu
    global GAME_VOLUME

    if NUM_PLAYERS == 'ONE_PLAYER':
        mixer.music.stop() #zaustavljamo muziku menija
        main_menu.disable()
        mixer.music.load('sounds/background.wav')
        mixer.music.play(-1) #pustamo muziku igrice
        mixer.music.set_volume(GAME_VOLUME)
        start_game_one_player()
    else:
        mixer.music.stop() #zaustavljamo muziku menija
        main_menu.disable()
        mixer.music.load('sounds/background.wav')
        mixer.music.play(-1) #pustamo muziku igrice
        mixer.music.set_volume(GAME_VOLUME)
        start_game_two_player()


def main_background():
    '''
    Funckija koja iscrtava pozadinu dok je main(pause)_menu ukljucen
    '''
    global screen
    global star_wars_logo

    if star_wars_logo.get_rect(topleft=START_WARS_LOGO_POS).collidepoint(pygame.mouse.get_pos()):
        star_wars_logo = pygame.image.load('images/yellow.png')
    else:
        star_wars_logo = pygame.image.load('images/blue.jpg')

    screen.blit(background, (0, 0))
    screen.blit(star_wars_logo, START_WARS_LOGO_POS)


def change_player(value, player):
    '''
    Funckija koja interaktivno gleda promenu u biranju one_player/two_players u main_menu
    '''
    global NUM_PLAYERS
    NUM_PLAYERS = player

def change_volume_menu(value, vol):
    '''
    Funckija koja  interaktivno odredjuje jacinu zvuka koju korisnik zeli iz main_menu
    '''

    global MENU_VOLUME
    mixer.music.set_volume(VOLUME_VALUES[vol])
    MENU_VOLUME = VOLUME_VALUES[vol]

def change_volume_game(value, vol):
    '''
    Funckija koja  interaktivno odredjuje jacinu zvuka koju korisnik zeli iz pause_menu
    '''
    global GAME_VOLUME
    mixer.music.set_volume(VOLUME_VALUES[vol])
    GAME_VOLUME = VOLUME_VALUES[vol]


def createMenu():
    global main_menu

    # Controls (spisak kontrola)
    controls_submenu = pygameMenu.TextMenu(screen,
                                           window_width=WINDOW_SIZE[0] - 600,
                                           window_height=WINDOW_SIZE[1] - 100,
                                           font=pygameMenu.font.FONT_FRANCHISE,
                                           title='STAR WARS MENU',
                                           bgfun=main_background,
                                           menu_width=MENU_SIZE[0],
                                           menu_height=MENU_SIZE[1]
                                           )
    controls_submenu.add_line(CONTROLS_TEXT[0])
    controls_submenu.add_line(CONTROLS_TEXT[1])
    controls_submenu.add_line(CONTROLS_TEXT[2])
    controls_submenu.add_line(CONTROLS_TEXT[3])
    controls_submenu.add_option('Back', pygameMenu.events.BACK)

    # Play menu (START , 1/2 PLAYER, CONTROLS, BACK)
    play_menu = pygameMenu.Menu(screen,
                                window_width=WINDOW_SIZE[0] - 600,
                                window_height=WINDOW_SIZE[1] - 100,
                                font=pygameMenu.font.FONT_FRANCHISE,
                                title='STAR WARS MENU',
                                bgfun=main_background,
                                menu_width=MENU_SIZE[0],
                                menu_height=MENU_SIZE[1]
                                )
    play_menu.add_option('Start', start_game)
    play_menu.add_selector('',
                           [('1-player', 'ONE_PLAYER'),
                            ('2-players', 'TWO_PLAYERS')],
                           onchange=change_player
                           )
    play_menu.add_option('Controls', controls_submenu)
    play_menu.add_option('Back', pygameMenu.events.BACK)

    #Settings menu(SOUND, CONTROLS)
    settings_menu = pygameMenu.Menu(screen,
                                    window_width=WINDOW_SIZE[0] - 600,
                                    window_height=WINDOW_SIZE[1] - 100,
                                    font=pygameMenu.font.FONT_FRANCHISE,
                                    title='STAR WARS MENU',
                                    bgfun=main_background,
                                    menu_width=MENU_SIZE[0],
                                    menu_height=MENU_SIZE[1]
                                    )
    settings_menu.add_selector('Sound volume',
                               [('50 %', '50_PERCENT'),
                                ('70 %', '70_PERCENT'),
                                ('100 %', '100_PERCENT'),
                                ('10 %', '10_PERCENT'),
                                ('30 %', '30_PERCENT'),
                                ],
                               onchange=change_volume_menu
                               )
    settings_menu.add_option('Controls', controls_submenu)
    settings_menu.add_option('Back', pygameMenu.events.BACK)


    # About menu
    about_menu = pygameMenu.TextMenu(screen,
                                     window_width=WINDOW_SIZE[0] - 600,
                                     window_height=WINDOW_SIZE[1] - 100,
                                     font=pygameMenu.font.FONT_FRANCHISE,
                                     title='STAR WARS MENU',
                                     bgfun=main_background,
                                     menu_width=MENU_SIZE[0],
                                     menu_height=MENU_SIZE[1]
                                     )
    for about in ABOUT:
        about_menu.add_line(about)
    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    about_menu.add_option('Return to menu', pygameMenu.events.BACK)

    # Main menu (PLAY, SETTINGS, ABOUT, EXIT)
    main_menu = pygameMenu.Menu(screen,
                                window_width=WINDOW_SIZE[0] - 600,
                                window_height=WINDOW_SIZE[1] - 100,
                                font=pygameMenu.font.FONT_FRANCHISE,
                                title='STAR WARS MENU',
                                bgfun=main_background,
                                menu_width=MENU_SIZE[0],
                                menu_height=MENU_SIZE[1]
                                )
    main_menu.add_option('Play', play_menu)
    main_menu.add_option('Settings', settings_menu)
    main_menu.add_option('About', about_menu)
    main_menu.add_option('Exit', pygameMenu.events.EXIT)


def continue_game():
    global pause_menu
    pause_menu.disable()


def reset_game():
    global pause_menu
    global main_menu
    global MENU_VOLUME

    #zaustavljamo muziku u pozadini igrice
    mixer.music.stop()
    pause_menu.disable()
    #vracamo se u main_menu i pustamo muziku menija
    mixer.music.load('sounds/menu_music.mp3')
    mixer.music.play(-1)
    mixer.music.set_volume(MENU_VOLUME)
    main_menu.enable()


def createPauseMenu():
    global pause_menu

    #Controls subemenu u settings
    controls_submenu = pygameMenu.TextMenu(screen,
                                           window_width=WINDOW_SIZE[0] - 600,
                                           window_height=WINDOW_SIZE[1] - 100,
                                           font=pygameMenu.font.FONT_FRANCHISE,
                                           title='STAR WARS MENU',
                                           bgfun=main_background,
                                           menu_width=MENU_SIZE[0],
                                           menu_height=MENU_SIZE[1]
                                           )
    controls_submenu.add_line(CONTROLS_TEXT[0])
    controls_submenu.add_line(CONTROLS_TEXT[1])
    controls_submenu.add_line(CONTROLS_TEXT[2])
    controls_submenu.add_line(CONTROLS_TEXT[3])
    controls_submenu.add_option('Back', pygameMenu.events.BACK)

    # Settings menu(SOUND, CONTROLS)
    settings_menu = pygameMenu.Menu(screen,
                                    window_width=WINDOW_SIZE[0] - 600,
                                    window_height=WINDOW_SIZE[1] - 100,
                                    font=pygameMenu.font.FONT_FRANCHISE,
                                    title='STAR WARS MENU',
                                    bgfun=main_background,
                                    menu_width=MENU_SIZE[0],
                                    menu_height=MENU_SIZE[1]
                                    )
    settings_menu.add_selector('Sound volume',
                               [('50 %', '50_PERCENT'),
                                ('70 %', '70_PERCENT'),
                                ('100 %', '100_PERCENT'),
                                ('10 %', '10_PERCENT'),
                                ('30 %', '30_PERCENT'),
                                ],
                               onchange=change_volume_game
                               )
    settings_menu.add_option('Controls', controls_submenu)
    settings_menu.add_option('Back', pygameMenu.events.BACK)


    pause_menu = pygameMenu.Menu(screen,
                                 window_width=WINDOW_SIZE[0] - 600,
                                 window_height=WINDOW_SIZE[1] - 100,
                                 font=pygameMenu.font.FONT_FRANCHISE,
                                 title='STAR WARS MENU',
                                 bgfun=main_background,
                                 menu_width=MENU_SIZE[0],
                                 menu_height=MENU_SIZE[1]
                                 )
    pause_menu.add_option('Continue', continue_game)
    pause_menu.add_option('Settings', settings_menu)
    pause_menu.add_option('Reset', reset_game)


def main():
    global main_menu
    global pause_menu
    global screen
    global background
    global star_wars_logo

    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)
    background = pygame.image.load('images/background.jpg')

    star_wars_logo = pygame.image.load('images/blue.jpg')
    pygame.display.set_caption('STAR WARS GAME')

    createPauseMenu()
    pause_menu.disable()
    createMenu()
    main_menu.enable()

    #pustamo menu_music
    mixer.music.load('sounds/menu_music.mp3')
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)

    while True:
        # menu.screen.blit(menu.background, (0, 0))
        # menu.screen.blit(menu.star_wars_logo, menu.START_WARS_LOGO_POS)

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()

        if main_menu.is_enabled():
            main_menu.mainloop(events)
        elif pause_menu.is_enabled():
            pause_menu.mainloop(events)

        pygame.display.update()


if __name__ == '__main__':
    main()
