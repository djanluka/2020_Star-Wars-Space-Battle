import pygame
import pygameMenu
from pygame import mixer

ABOUT = ['This star wars game like Galaga',
         'is made by MATF students:',
         'Boris Cvitak',
         'Ognjen Stamenkovic',
         'Predrag Mitic']

CONTROLS_TEXT = [
    'First player:                                                                                            Second player:',
    'To left : A                                                                                                                  To left : 4',
    'To right : D                                                                                                               To left : 6',
    'To shoot : W                                                                                                        To shoot : 8']

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


class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([5, 10])
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


rockets_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()


def start_game_one_player():
    global screen
    global main_menu
    global pause_menu

    game_background = pygame.image.load('images/game_background.png')
    playerImg = pygame.image.load('images/player.png')
    pauseImg = pygame.image.load('images/pause.png')
    rocketImg = pygame.image.load('images/rocket-launch.png')
    destroyerImg = pygame.image.load('images/destroyer.png')

    plane_position_y = 500
    plane_position_x = 250
    left_margin = 0 + 10
    right_margin = WINDOW_SIZE[0] - 70  # Ovo je zavisno od sirine slike aviona
    time = 0  # timer za animaciju sa raketicama
    destroyer = Destroyer()

    while True:
        time += 10
        screen.blit(game_background, (0, 0))
        screen.blit(pauseImg, PAUSE_ONE_PLAYER_POS)

        destroyer.rect.x = WINDOW_SIZE[0] / 2 - 50
        destroyer.rect.y = (int(time / 5) - 150 if time < 1000 else 50)
        if destroyer.health > 0:
            destroyer.show(destroyerImg)
            if time > 1000:  #
                pygame.draw.rect(screen, (200, 10, 10), (150, 20, destroyer.health * 10, 20))

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
                    mixer.music.pause()
                    pause_menu.enable()

        #Za kretanje ne mogu koristi events jer treba da se krece i kada se samo drzi taster
        pressed = pygame.key.get_pressed()
        movement = 2

        if pressed[pygame.K_a] and plane_position_x > left_margin:
            plane_position_x -= movement

        if pressed[pygame.K_d] and plane_position_x < right_margin:
            plane_position_x += movement

        if pressed[pygame.K_w] and time % 10 is 0 and time > 1000:

            #Zvuk pri ispaljivanju metaka
            rocket_sound = mixer.Sound('sounds/laser.wav')
            rocket_sound.play()

            rocket = Rocket()
            rocket.rect.x = plane_position_x + 16  # razlika u velicina slika
            rocket.rect.y = plane_position_y

            all_sprites_list.add(rocket)
            rockets_list.add(rocket)

        for r in rockets_list:
            r.show_rocket(rocketImg)

            #Obrada kolizije
            if r.rect.x in range(destroyer.rect.x, destroyer.rect.x + 110):

                dist = 110 - r.rect.x + destroyer.rect.x
                if r.rect.y < destroyer.rect.y + dist:
                    rockets_list.remove(r)
                    all_sprites_list.remove(r)

                    #Zvuk eksplozije kada metak pogodi protivnika
                    explosion_sound = mixer.Sound('sounds/explosion.wav')
                    explosion_sound.play()

                    destroyer.health -= 1

            if r.rect.y < -20:
                rockets_list.remove(r)
                all_sprites_list.remove(r)

        # Ovde iscrtavamo avion zbog toga sto raketa izlazi (pre) ispod njega
        screen.blit(playerImg, (plane_position_x, plane_position_y))

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

    if NUM_PLAYERS == 'ONE_PLAYER':
        mixer.music.stop() #zaustavljamo muziku menija
        main_menu.disable()
        mixer.music.load('sounds/background.wav')
        mixer.music.play() #pustamo muziku igrice
        start_game_one_player()
    else:
        mixer.music.stop() #zaustavljamo muziku menija
        main_menu.disable()
        mixer.music.load('sounds/background.wav')
        mixer.music.play() #pustamo muziku igrice
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


def createMenu():
    global main_menu

    # Controls (spisak kontrola)
    controls_submenu_play = pygameMenu.TextMenu(screen,
                                                window_width=WINDOW_SIZE[0] - 600,
                                                window_height=WINDOW_SIZE[1] - 100,
                                                font=pygameMenu.font.FONT_FRANCHISE,
                                                title='STAR WARS MENU',
                                                bgfun=main_background,
                                                menu_width=MENU_SIZE[0],
                                                menu_height=MENU_SIZE[1]
                                                )
    controls_submenu_play.add_line(CONTROLS_TEXT[0])
    controls_submenu_play.add_line(CONTROLS_TEXT[1])
    controls_submenu_play.add_line(CONTROLS_TEXT[2])
    controls_submenu_play.add_line(CONTROLS_TEXT[3])
    controls_submenu_play.add_option('Back', pygameMenu.events.BACK)

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
    play_menu.add_option('Controls', controls_submenu_play)
    play_menu.add_option('Back', pygameMenu.events.BACK)

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
    main_menu.add_option('Settings', about_menu)
    main_menu.add_option('About', about_menu)
    main_menu.add_option('Exit', pygameMenu.events.EXIT)


def continue_game():
    global pause_menu
    #vracamo se u igricu i pustamo muziku u pozadini
    mixer.music.unpause()
    pause_menu.disable()


def reset_game():
    global pause_menu
    global main_menu
    #zaustavljamo muziku u pozadini igrice
    mixer.music.stop()
    pause_menu.disable()
    #vracamo se main_menu i pustamo muziku menija
    mixer.music.load('sounds/menu_music.mp3')
    mixer.music.play()
    main_menu.enable()


def createPauseMenu():
    global pause_menu
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
    pause_menu.add_option('Settings', about_menu)
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

    #Pustamo muziku menija
    mixer.music.load('sounds/menu_music.mp3')
    mixer.music.play()

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
