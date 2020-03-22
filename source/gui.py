from source import glob
from source import start
import pygame
import pygameMenu

main_menu = None
pause_menu = None
screen = pygame.display.set_mode((1300,700))
background = pygame.image.load('images/background.jpg')

star_wars_logo = pygame.image.load('images/blue.jpg')
pygame.display.set_caption('STAR WARS GAME')

def main_background():
    '''
    Funckija koja iscrtava pozadinu dok je main(pause)_menu ukljucen
    '''
    star_wars_logo = pygame.image.load('images/blue.jpg')   
    if star_wars_logo.get_rect(topleft=glob.START_WARS_LOGO_POS).collidepoint(pygame.mouse.get_pos()):
        star_wars_logo = pygame.image.load('images/yellow.png')
    else:
        star_wars_logo = pygame.image.load('images/blue.jpg')

    screen.blit(background, (0, 0))
    screen.blit(star_wars_logo, glob.START_WARS_LOGO_POS)



def change_player(value, player):
    '''
    Funckija koja interaktivno gleda promenu u biranju one_player/two_players u main_menu
    '''
    glob.NUM_PLAYERS = player

def change_volume_menu(value, vol):
    '''
    Funckija koja  interaktivno odredjuje jacinu zvuka koju korisnik zeli iz main_menu
    '''

    mixer.music.set_volume(glob.VOLUME_VALUES[vol])
    glob.MENU_VOLUME = glob.VOLUME_VALUES[vol]

def change_volume_game(value, vol):
    '''
    Funckija koja  interaktivno odredjuje jacinu zvuka koju korisnik zeli iz pause_menu
    '''
    mixer.music.set_volume(glob.VOLUME_VALUES[vol])
    glob.GAME_VOLUME = glob.VOLUME_VALUES[vol]

def continue_game():
    pause_menu.disable()


def reset_game():

    #zaustavljamo muziku u pozadini igrice
    mixer.music.stop()
    pause_menu.disable()
    #vracamo se u main_menu i pustamo muziku menija
    mixer.music.load('sounds/menu_music.mp3')
    mixer.music.play(-1)
    mixer.music.set_volume(glob.MENU_VOLUME)
    main_menu.enable()




def createPauseMenu():    
    global main_menu
    global pause_menu
    
    #Controls subemenu u settings
    controls_submenu = pygameMenu.TextMenu(screen,
                                           window_width=glob.WINDOW_SIZE[0] - 600,
                                           window_height=glob.WINDOW_SIZE[1] - 100,
                                           font=pygameMenu.font.FONT_FRANCHISE,
                                           title='STAR WARS MENU',
                                           bgfun=main_background,
                                           menu_width=glob.MENU_SIZE[0],
                                           menu_height=glob.MENU_SIZE[1]
                                           )
    controls_submenu.add_line(glob.CONTROLS_TEXT[0])
    controls_submenu.add_line(glob.CONTROLS_TEXT[1])
    controls_submenu.add_line(glob.CONTROLS_TEXT[2])
    controls_submenu.add_line(glob.CONTROLS_TEXT[3])
    controls_submenu.add_option('Back', pygameMenu.events.BACK)

    # Settings menu(SOUND, CONTROLS)
    settings_menu = pygameMenu.Menu(screen,
                                    window_width=glob.WINDOW_SIZE[0] - 600,
                                    window_height=glob.WINDOW_SIZE[1] - 100,
                                    font=pygameMenu.font.FONT_FRANCHISE,
                                    title='STAR WARS MENU',
                                    bgfun=main_background,
                                    menu_width=glob.MENU_SIZE[0],
                                    menu_height=glob.MENU_SIZE[1]
                                    )
    settings_menu.add_selector('Sound volume',
                               [('50 %', '50_PERCENT'),
                                ('70 %', '70_PERCENT'),
                                ('100 %', '100_PERCENT'),
                                ('0 %', '0_PERCENT'),
                                ('10 %', '10_PERCENT'),
                                ('30 %', '30_PERCENT'),
                                ],
                               onchange=change_volume_game
                               )
    settings_menu.add_option('Controls', controls_submenu)
    settings_menu.add_option('Back', pygameMenu.events.BACK)


    pause_menu = pygameMenu.Menu(screen,
                                 window_width=glob.WINDOW_SIZE[0] - 600,
                                 window_height=glob.WINDOW_SIZE[1] - 100,
                                 font=pygameMenu.font.FONT_FRANCHISE,
                                 title='STAR WARS MENU',
                                 bgfun=main_background,
                                 menu_width=glob.MENU_SIZE[0],
                                 menu_height=glob.MENU_SIZE[1] )
    pause_menu.add_option('Continue', continue_game)
    pause_menu.add_option('Settings', settings_menu)
    pause_menu.add_option('Reset', reset_game)
                                 
def createMenu():
    global main_menu
    global pause_menu
    # Controls (spisak kontrola)
    controls_submenu = pygameMenu.TextMenu(screen,
                                           window_width=glob.WINDOW_SIZE[0] - 600,
                                           window_height=glob.WINDOW_SIZE[1] - 100,
                                           font=pygameMenu.font.FONT_FRANCHISE,
                                           title='STAR WARS MENU',
                                           bgfun=main_background,
                                           menu_width=glob.MENU_SIZE[0],
                                           menu_height=glob.MENU_SIZE[1]
                                           )
    controls_submenu.add_line(glob.CONTROLS_TEXT[0])
    controls_submenu.add_line(glob.CONTROLS_TEXT[1])
    controls_submenu.add_line(glob.CONTROLS_TEXT[2])
    controls_submenu.add_line(glob.CONTROLS_TEXT[3])
    controls_submenu.add_option('Back', pygameMenu.events.BACK)

    # Play menu (START , 1/2 PLAYER, CONTROLS, BACK)
    play_menu = pygameMenu.Menu(screen,
                                window_width=glob.WINDOW_SIZE[0] - 600,
                                window_height=glob.WINDOW_SIZE[1] - 100,
                                font=pygameMenu.font.FONT_FRANCHISE,
                                title='STAR WARS MENU',
                                bgfun=main_background,
                                menu_width=glob.MENU_SIZE[0],
                                menu_height=glob.MENU_SIZE[1]
                                )
    play_menu.add_option('Start', start.start_game)
    play_menu.add_selector('',
                           [('1-player', 'ONE_PLAYER'),
                            ('2-players', 'TWO_PLAYERS')],
                           onchange=change_player
                           )
    play_menu.add_option('Controls', controls_submenu)
    play_menu.add_option('Back', pygameMenu.events.BACK)

    #Settings menu(SOUND, CONTROLS)
    settings_menu = pygameMenu.Menu(screen,
                                    window_width=glob.WINDOW_SIZE[0] - 600,
                                    window_height=glob.WINDOW_SIZE[1] - 100,
                                    font=pygameMenu.font.FONT_FRANCHISE,
                                    title='STAR WARS MENU',
                                    bgfun=main_background,
                                    menu_width=glob.MENU_SIZE[0],
                                    menu_height=glob.MENU_SIZE[1]
                                    )
    settings_menu.add_selector('Sound volume',
                               [('50 %', '50_PERCENT'),
                                ('70 %', '70_PERCENT'),
                                ('100 %', '100_PERCENT'),
                                ('0 %', '0_PERCENT'),
                                ('10 %', '10_PERCENT'),
                                ('30 %', '30_PERCENT'),
                                ],
                               onchange=change_volume_menu
                               )
    settings_menu.add_option('Controls', controls_submenu)
    settings_menu.add_option('Back', pygameMenu.events.BACK)


    # About menu
    about_menu = pygameMenu.TextMenu(screen,
                                     window_width=glob.WINDOW_SIZE[0] - 600,
                                     window_height=glob.WINDOW_SIZE[1] - 100,
                                     font=pygameMenu.font.FONT_FRANCHISE,
                                     title='STAR WARS MENU',
                                     bgfun=main_background,
                                     menu_width=glob.MENU_SIZE[0],
                                     menu_height=glob.MENU_SIZE[1]
                                     )
    for about in glob.ABOUT:
        about_menu.add_line(about)
    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    about_menu.add_option('Return to menu', pygameMenu.events.BACK)

    # Main menu (PLAY, SETTINGS, ABOUT, EXIT)
    main_menu = pygameMenu.Menu(screen,
                                window_width=glob.WINDOW_SIZE[0] - 600,
                                window_height=glob.WINDOW_SIZE[1] - 100,
                                font=pygameMenu.font.FONT_FRANCHISE,
                                title='STAR WARS MENU',
                                bgfun=main_background,
                                menu_width=glob.MENU_SIZE[0],
                                menu_height=glob.MENU_SIZE[1]
                                )
    main_menu.add_option('Play', play_menu)
    main_menu.add_option('Settings', settings_menu)
    main_menu.add_option('About', about_menu)
    main_menu.add_option('Exit', pygameMenu.events.EXIT)
    
    return main_menu
                                

def play():
    global main_menu
    global pause_menu
    createPauseMenu()
    pause_menu.disable()
    createMenu()
    main_menu.enable()

