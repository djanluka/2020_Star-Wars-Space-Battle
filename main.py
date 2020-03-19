import pygame
import pygameMenu

ABOUT = ['This star wars game like Galaga',
         'is made by MATF students:',
         'Boris Cvitak',
         'Ognjen Stamenkovic',
         'Predrag Mitic']

CONTROLS_TEXT = ['First player:                                                                                            Second player:',
                 'To left : A                                                                                                                  To left : 4',
                 'To right : D                                                                                                               To left : 6',
                 'To shoot : space                                                                                  To shoot : enter']

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


def start_game_one_player():
    global screen
    global main_menu
    global pause_menu

    game_background = pygame.image.load('game_background.png')
    playerImg = pygame.image.load('player.png')
    pauseImg = pygame.image.load('pause.png')

    while True:
        screen.blit(game_background, (0, 0))
        screen.blit(playerImg, (580, 600))
        screen.blit(pauseImg, PAUSE_ONE_PLAYER_POS)

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    exit()

            if e.type == pygame.MOUSEBUTTONDOWN and pause_menu.is_disabled():
                x, y = PAUSE_ONE_PLAYER_POS
                if pauseImg.get_rect(topleft=(x, y)).collidepoint(pygame.mouse.get_pos()):
                    pause_menu.enable()

        if main_menu.is_enabled():
            main_menu.mainloop(events)
        elif pause_menu.is_enabled():
            pause_menu.mainloop(events)

        pygame.display.update()


def start_game_two_player():
    global screen
    global main_menu
    global pause_menu

    game_background = pygame.image.load('game_background.png')
    playerImg = pygame.image.load('player.png')
    pauseImg = pygame.image.load('pause.png')

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

            if e.type == pygame.MOUSEBUTTONDOWN and pause_menu.is_disabled():
                x, y = PAUSE_TWO_PLAYERS_POS
                if pauseImg.get_rect(topleft=(x, y)).collidepoint(pygame.mouse.get_pos()):
                    pause_menu.enable()

        if main_menu.is_enabled():
            main_menu.mainloop(events)
        elif pause_menu.is_enabled():
            pause_menu.mainloop(events)

        pygame.display.update()


def start_game():
    global main_menu

    if NUM_PLAYERS == 'ONE_PLAYER':
        main_menu.disable()
        start_game_one_player()
    else:
        main_menu.disable()
        start_game_two_player()


def main_background():

    global screen
    global star_wars_logo

    if star_wars_logo.get_rect(topleft=START_WARS_LOGO_POS).collidepoint(pygame.mouse.get_pos()):
        star_wars_logo = pygame.image.load('yellow.png')
    else:
        star_wars_logo = pygame.image.load('blue.jpg')

    screen.blit(background, (0, 0))
    screen.blit(star_wars_logo, START_WARS_LOGO_POS)

def change_player(value, player):
    global NUM_PLAYERS
    NUM_PLAYERS = player


def createMenu():

    global main_menu

    #Controls submenu in Play Menu
    controls_submenu_play = pygameMenu.TextMenu(screen,
                                                window_width=WINDOW_SIZE[0] - 600,
                                                window_height=WINDOW_SIZE[1] - 100,
                                                font=pygameMenu.font.FONT_FRANCHISE,
                                                title='STAR WARS MENU',
                                                bgfun=main_background,
                                                menu_width= MENU_SIZE[0],
                                                menu_height= MENU_SIZE[1]
                                                )
    controls_submenu_play.add_line(CONTROLS_TEXT[0])
    controls_submenu_play.add_line(CONTROLS_TEXT[1])
    controls_submenu_play.add_line(CONTROLS_TEXT[2])
    controls_submenu_play.add_line(CONTROLS_TEXT[3])
    controls_submenu_play.add_option('Back', pygameMenu.events.BACK)

    #Play Menu
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

    #About menu
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

    #Main menu
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
    pause_menu.disable()

def reset_game():
    global pause_menu
    global main_menu
    pause_menu.disable()
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
    background = pygame.image.load('background.jpg')
    star_wars_logo = pygame.image.load('blue.jpg')
    pygame.display.set_caption('STAR WARS GAME')

    createPauseMenu()
    pause_menu.disable()
    createMenu()
    main_menu.enable()

    running = True
    while running:
        #menu.screen.blit(menu.background, (0, 0))
        #menu.screen.blit(menu.star_wars_logo, menu.START_WARS_LOGO_POS)

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                running = False

        if main_menu.is_enabled():
            main_menu.mainloop(events)
        elif pause_menu.is_enabled():
            pause_menu.mainloop(events)

        pygame.display.update()


if __name__ == '__main__':
    main()