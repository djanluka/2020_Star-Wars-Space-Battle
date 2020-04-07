from source import cls
from source import gui
from source import glob
from pygame import mixer
import pygame
import math
import random

player1 = None
player2 = None

player_1_health_bar_img = pygame.image.load('images/player1.png')
player_2_health_bar_img = pygame.image.load('images/player2.png')

PLAYER_1_IMG_256px = [pygame.image.load('images/PLY1.png'),
                      pygame.image.load('images/PLY2.png'),
                      pygame.image.load('images/PLY3.png'),
                      pygame.image.load('images/PLY_L_4.png'),
                      pygame.image.load('images/PLY5.png'),
                      pygame.image.load('images/PLY6.png')]

PLAYER_1_IMG_64px = [pygame.image.load('images/ply1.png'),
                      pygame.image.load('images/ply2.png'),
                      pygame.image.load('images/ply3.png'),
                      pygame.image.load('images/ply_l_4.png'),
                      pygame.image.load('images/ply5.png'),
                      pygame.image.load('images/ply6.png')]

PLAYER_2_IMG_256px = [pygame.image.load('images/PLY1.png'),
                      pygame.image.load('images/PLY2.png'),
                      pygame.image.load('images/PLY3.png'),
                      pygame.image.load('images/PLY_R_4.png'),
                      pygame.image.load('images/PLY5.png'),
                      pygame.image.load('images/PLY6.png')]

PLAYER_2_IMG_64px = [pygame.image.load('images/ply1.png'),
                      pygame.image.load('images/ply2.png'),
                      pygame.image.load('images/ply3.png'),
                      pygame.image.load('images/ply_r_4.png'),
                      pygame.image.load('images/ply5.png'),
                      pygame.image.load('images/ply6.png')]
NUM_IMG_PLAYER1 = 0
NUM_IMG_PLAYER2 = 0

def check_menu_events():
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                exit()

        # Ukoliko smo kliknuli na pauzu, otvaramo pause_meni i zaustavljamo muziku
        if e.type == pygame.MOUSEBUTTONDOWN and gui.pause_menu.is_disabled():
            if glob.pause_img_2.get_rect(topleft=glob.PAUSE_TWO_PLAYERS_POS).collidepoint(pygame.mouse.get_pos()):
                gui.pause_menu.enable()

    # ako su ukljuceni meniji, prikupljamo dogadjaje u njima
    if gui.main_menu.is_enabled():
        gui.main_menu.mainloop(events)
    elif gui.pause_menu.is_enabled():
        gui.pause_menu.mainloop(events)


def draw_player(player, num_player):
    if player.health > 0:
        player.show()
        player.show_health(num_player)


def init_players():

    global player1, player2
    
    player1 = cls.twoPlayer()
    player1.position_x = 50
    player1.position_y = glob.WINDOW_SIZE[1] / 2
    
    if NUM_IMG_PLAYER1 == 3:
        player1.image = PLAYER_1_IMG_64px[NUM_IMG_PLAYER1]
    elif NUM_IMG_PLAYER1 == 5:
        player1.image = pygame.transform.rotate(PLAYER_1_IMG_64px[NUM_IMG_PLAYER1], -90)
    else:
        player1.image = pygame.transform.rotate(PLAYER_1_IMG_64px[NUM_IMG_PLAYER1], 90)

    player2 = cls.twoPlayer()
    player2.position_x = glob.WINDOW_SIZE[0] - 50 - 64
    player2.position_y = glob.WINDOW_SIZE[1] / 2

    if NUM_IMG_PLAYER2 == 3:
        player2.image = PLAYER_2_IMG_64px[NUM_IMG_PLAYER2]
    elif NUM_IMG_PLAYER2 == 5:
        # Ispravljen bag oko indeksa
        player2.image = pygame.transform.rotate(PLAYER_2_IMG_64px[NUM_IMG_PLAYER2], 90)
    else:
        player2.image = pygame.transform.rotate(PLAYER_2_IMG_64px[NUM_IMG_PLAYER2], -90)


def check_player_events(burst_fire1, burst_fire2, game_taimer):

    global player1, player2

    cont = cls.Controler()
    movement = 4

    left_margin = 0 + 10
    right_margin = glob.WINDOW_SIZE[1] - 120

    pressed = pygame.key.get_pressed()

    if pressed[cont.get_control('Left1')] and player1.position_y > left_margin:
        player1.position_y -= movement

    if pressed[cont.get_control('Right1')] and player1.position_y < right_margin:
        player1.position_y += movement

    burst_fire1 += 1

    if pressed[cont.get_control('Fire1')] and game_taimer > 100:
        # Metak se ispaljuje u svakom 50-tom ciklusu
        if burst_fire1 > 40:
            # Zvuk pri ispaljivanju metaka
            rocket_sound = mixer.Sound('sounds/laser.wav')
            rocket_sound.play()

            rocket = cls.leftRocket()
            rocket.rect.x = player1.position_x + 20
            rocket.rect.y = player1.position_y + 30

            glob.all_sprites_list.add(rocket)
            glob.left_rockets_list.add(rocket)
            burst_fire1 = 0

    if pressed[cont.get_control('Left2')] and player2.position_y > left_margin:
        player2.position_y -= movement

    if pressed[cont.get_control('Right2')] and player2.position_y < right_margin:
        player2.position_y += movement

    burst_fire2 += 1

    if pressed[cont.get_control('Fire2')] and game_taimer > 100:
        if burst_fire2 > 40:
            rocket_sound = mixer.Sound('sounds/laser.wav')
            rocket_sound.play()

            rocket = cls.rightRocket()
            rocket.rect.x = player2.position_x
            rocket.rect.y = player2.position_y + 26

            glob.all_sprites_list.add(rocket)
            glob.right_rockets_list.add(rocket)
            burst_fire2 = 0

    return burst_fire1, burst_fire2


def check_rocket_colide():

    global player1, player2

    for bullet in glob.left_rockets_list:
        bullet.show_rocket()
        if bullet.rect.x in range(int(player2.position_x), int(player2.position_x + 64)):
            if bullet.rect.y in range(int(player2.position_y), int(player2.position_y + 64)):
                glob.left_rockets_list.remove(bullet)
                glob.all_sprites_list.remove(bullet)
                player2.health -= 20

        if bullet.rect.x > 1400:
            glob.left_rockets_list.remove(bullet)
            glob.all_sprites_list.remove(bullet)

    for bullet in glob.right_rockets_list:
        bullet.show_rocket()
        if bullet.rect.x in range(int(player1.position_x), int(player1.position_x + 64)):
            if bullet.rect.y in range(int(player1.position_y), int(player1.position_y + 64)):
                glob.right_rockets_list.remove(bullet)
                glob.all_sprites_list.remove(bullet)
                player1.health -= 20

        if bullet.rect.x < -100:
            glob.right_rockets_list.remove(bullet)
            glob.all_sprites_list.remove(bullet)

def choose_players():

    global NUM_IMG_PLAYER1, NUM_IMG_PLAYER2

    cont = cls.Controler()
    left1 = pygame.image.load('images/left.png')
    right1 = pygame.image.load('images/right.png')
    left2 = pygame.image.load('images/left.png')
    right2 = pygame.image.load('images/right.png')
    play_img = pygame.image.load('images/play.png')
    back_img = pygame.image.load('images/back.png')
    play = True
    size = len(PLAYER_1_IMG_256px)



    while True:

        gui.screen.blit(gui.background, (0, 0))
        gui.screen.blit(left1, (236, 318))
        gui.screen.blit(left2, (660, 318))
        gui.screen.blit(right1, (576, 318))
        gui.screen.blit(right2, (1000, 318))

        if play:
            gui.screen.blit(play_img, (500, 480))
        else:
            gui.screen.blit(back_img, (500, 480))

        gui.screen.blit(PLAYER_1_IMG_256px[NUM_IMG_PLAYER1], (310, 222))
        gui.screen.blit(PLAYER_2_IMG_256px[NUM_IMG_PLAYER2], (734, 222))

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if left1.get_rect(topleft=(236, 318)).collidepoint(pygame.mouse.get_pos()):
                    NUM_IMG_PLAYER1 = (NUM_IMG_PLAYER1 - 1 + size) % size
                elif left2.get_rect(topleft=(660, 318)).collidepoint(pygame.mouse.get_pos()):
                    NUM_IMG_PLAYER2 = (NUM_IMG_PLAYER2 - 1 + size) % size
                elif right1.get_rect(topleft=(576, 318)).collidepoint(pygame.mouse.get_pos()):
                    NUM_IMG_PLAYER1 = (NUM_IMG_PLAYER1 + 1 + size) % size
                elif right2.get_rect(topleft=(1000, 318)).collidepoint(pygame.mouse.get_pos()):
                    NUM_IMG_PLAYER2 = (NUM_IMG_PLAYER2 + 1 + size) % size

            if e.type == pygame.KEYDOWN:
                if e.key == glob.TWO_CONTROL_LEFT_ORD1:
                    NUM_IMG_PLAYER1 = (NUM_IMG_PLAYER1 - 1 + size) % size
                elif e.key == glob.TWO_CONTROL_RIGHT_ORD1:
                    NUM_IMG_PLAYER1 = (NUM_IMG_PLAYER1 + 1 + size) % size
                elif e.key == glob.TWO_CONTROL_LEFT_ORD2:
                    NUM_IMG_PLAYER2 = (NUM_IMG_PLAYER2 - 1 + size) % size
                elif e.key == glob.TWO_CONTROL_RIGHT_ORD2:
                    NUM_IMG_PLAYER2 = (NUM_IMG_PLAYER2 + 1 + size) % size
                elif e.key == pygame.K_DOWN:
                    play = False
                elif e.key == pygame.K_UP:
                    play = True
                elif pygame.K_RETURN:
                    if play is not True:
                        print('menu')
                        glob.return_to_main_menu()
                        return
                    else:
                        return

        pygame.display.update()
        
     


def start_game_two_player():

    global player1, player2

    choose_players()

    init_players()

    game_timer = 0  # Tajmer igrice
    burst_fire1 = 0  # Tajmer rafala
    burst_fire2 = 0  # Tajmer rafala

    while True:
        game_timer += 3
        gui.screen.blit(glob.game_background, (0, 0))
        gui.screen.blit(glob.pause_img_2, glob.PAUSE_TWO_PLAYERS_POS)
        gui.screen.blit(player_1_health_bar_img, (20, 630))
        gui.screen.blit(player_2_health_bar_img, (glob.WINDOW_SIZE[0] - 20 - 64, 630))

        check_menu_events()

        burst_fire1, burst_fire2 = check_player_events(burst_fire1, burst_fire2, game_timer)

        check_rocket_colide()

        draw_player(player1, 1)
        draw_player(player2, 2)

        glob.all_sprites_list.update()
        pygame.display.update()
