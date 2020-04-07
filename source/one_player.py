import time as TIME
import pygameMenu
from source import cls
from source import gui
from source import glob
from pygame import mixer
import pygame
import math
import random

player = None
game_timer = None
burst_fire = None

timer_hidden = 0
hidden_enemy = None

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
            if glob.pause_img_1.get_rect(topleft=glob.PAUSE_ONE_PLAYER_POS).collidepoint(pygame.mouse.get_pos()):
                gui.pause_menu.enable()

    # ako su ukljuceni meniji, prikupljamo dogadjaje u njima
    if gui.main_menu.is_enabled():
        gui.main_menu.mainloop(events)
    elif gui.pause_menu.is_enabled():
        gui.pause_menu.mainloop(events)


def check_player_events():
    global game_timer, burst_fire
    cont = cls.Controler()
    movement = 4
    left_margin = 0 + 10
    right_margin = glob.WINDOW_SIZE[0] - 70
    pressed = pygame.key.get_pressed()

    if pressed[cont.get_control('Left')] and player.position_x > left_margin:
        player.position_x -= movement

    if pressed[cont.get_control('Right')] and player.position_x < right_margin:
        player.position_x += movement

    # IZMENJENO burst fire je nejmanje vreme izmedju dve rakete
    burst_fire += 1

    if pressed[cont.get_control('Fire')] and game_timer > 1000:
        # Metak se ispaljuje u svakom 50-tom ciklusu
        if burst_fire > 40:
            # Zvuk pri ispaljivanju metaka
            rocket_sound = mixer.Sound('sounds/laser.wav')
            rocket_sound.play()

            rocket = cls.Rocket()
            rocket.rect.x = player.position_x + 26  # razlika u velicina slika
            rocket.rect.y = player.position_y

            glob.all_sprites_list.add(rocket)
            glob.rockets_list.add(rocket)
            burst_fire = 0

def draw_player():

    if player.health > 0:
        player.show()
        player.show_health()
    else:
        if player.lifes_number >= 0:
            player.lifes_number -= 1
            player.health = 100
            player.show_health()
            pygame.display.update()
            TIME.sleep(0.5)


def draw_destroyer(destroyer, timer_destroyer):
    timer_destroyer += 3
    destroyer.rect.x = glob.WINDOW_SIZE[0] / 2 - 64
    destroyer.rect.y = (int(timer_destroyer / 5) - 240 if timer_destroyer < 1400 else 40)

    if destroyer.health > 0:
        destroyer.show()
        if timer_destroyer > 1000:
            pygame.draw.rect(gui.screen, (200, 10, 10), (150, 10, destroyer.health * 10, 20))
            destroyer.is_ready = True

    return timer_destroyer


def enemies_fire_to_player():
    global timer_hidden, hidden_enemy

    #Ako nema neprijatelja ne pucamo
    if game_timer < 1200 or player.health <= 0:
        glob.bullets_enm_list.draw(gui.screen)
        return

    rand_enm = random.choice(glob.enemies_list.sprites())
    num_enemies = len(glob.enemies_list.sprites())

    #Da ne gadjaju svi metkovi direktno u playera
    frequency = int(500 / num_enemies)

    #Ogranicnje frekvencije paljbe
    if frequency < 100:
        frequency = 100

    frequency -= (glob.LEVEL-1) * 5
    
    fire_mode = game_timer % frequency

    if fire_mode == 0:  # Napad neprijatelja: 400 ucestalost paljbe
        bul = cls.BulletEnemy()
        bul.rect.x = rand_enm.rect.x + 32
        bul.rect.y = rand_enm.rect.y + 32
        intensity = math.sqrt((bul.rect.x - player.position_x) ** 2 + (bul.rect.y - player.position_y) ** 2)
        bul.direction[0] = (player.position_x - bul.rect.x) / intensity + 0.1
        bul.direction[1] = (player.position_y - bul.rect.y) / intensity + 0.1
        glob.bullets_enm_list.add(bul)
        glob.all_sprites_list.add(bul)

    # Svaki drugi ispaljuje metka u pravcu (0,1)
    if fire_mode == int(frequency / 2):
        bul = cls.BulletEnemy()
        bul.rect.x = rand_enm.rect.x + 32
        bul.rect.y = rand_enm.rect.y + 32
        glob.bullets_enm_list.add(bul)
        glob.all_sprites_list.add(bul)

    glob.bullets_enm_list.draw(gui.screen)

    # DODATO
    # mogucnost da enemy bude nevidljiv
    # kada je veci nivo veca je verovatnoca jer je tezi level
    # TO DO
    # mozemo i da napravimo neku listu nevidljivih
    if timer_hidden == 0:
        rand_enm_hidden = random.choice(glob.enemies_list.sprites())
        if random.random() < glob.LEVEL / 30:
            rand_enm_hidden.hidden = True
            hidden_enemy = rand_enm_hidden
            timer_hidden += 1
    elif timer_hidden < 60: # odokativna duzina koliko je nevidljiv
        timer_hidden += 1
    else:
        timer_hidden = 0
        hidden_enemy.hidden = False



def check_bullets_player_collide():
    for bullet in glob.bullets_enm_list:
        if bullet.rect.x in range(player.position_x, player.position_x + 64):
            if bullet.rect.y in range(player.position_y + 20, player.position_y + 64):
                glob.bullets_enm_list.remove(bullet)
                player.health -= 20

        if bullet.rect.y > 1000:
            glob.bullets_enm_list.remove(bullet)


def check_rocket_to_enemise_colide(destroyer):
    global timer_hidden, hidden_enemy

    for r in glob.rockets_list:
        r.show_rocket()

        # Obrada kolizije player vs enemies
        enemy_hit_list = pygame.sprite.spritecollide(r, glob.enemies_list, True)

        for enm in enemy_hit_list:
            #DODATO
            #ako smo uspeli da pogodimo nevidljivog, moramo da ga izbrisemo
            #i da ostavimo mogucnost za biranje sledeceg
            if enm.is_hidden():
                timer_hidden = 0
                hidden_enemy = None
            glob.rockets_list.remove(r)
            glob.all_sprites_list.remove(r)
            glob.enemies_list.remove(enm)

        # ako je destroyer spreman onda mozemo da pucamo na njega i da mu skidamo health-e
        if destroyer.is_ready:
            # Obrada kolizije player vs destroyer
            if r.rect.x in range(destroyer.rect.x, destroyer.rect.x + 120):
                dist = 120 - r.rect.x + destroyer.rect.x
                dist = dist if dist < 64 else 120 - dist
                if r.rect.y < destroyer.rect.y + 3 * dist + 40:
                    glob.rockets_list.remove(r)
                    glob.all_sprites_list.remove(r)

                    # Zvuk eksplozije kada metak pogodi protivnika
                    explosion_sound = mixer.Sound('sounds/explosion.wav')
                    explosion_sound.play()

                    destroyer.health -= 10

        if r.rect.y < -20:
            glob.rockets_list.remove(r)
            glob.all_sprites_list.remove(r)


def make_enemies1(number):
    for n in range(number):
        enm = cls.Enemy(0)
        enm.rect.y = 0.0
        distance = glob.WINDOW_SIZE[0] / number
        enm.rect.x = float(n * distance + (distance - 64) / 2)
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

def make_enemies2(number):
    for n in range(number):
        enm = cls.Enemy(0)
        enm.rect.y = -50.0
        distance = glob.WINDOW_SIZE[0] / number 
        enm.rect.x = float(n * distance + (distance - 64) / 2)  
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

    for n in range(number):
        enm = cls.Enemy(1)
        enm.rect.y = -150.0
        distance = glob.WINDOW_SIZE[0] / number
        enm.rect.x = float(n * distance + (distance - 64) / 2)
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

def make_enemies3(number):
    for n in range(number):
        enm = cls.Enemy(0)
        enm.rect.y = -200.0
        distance = glob.WINDOW_SIZE[0] / number
        enm.rect.x = float(n * distance + (distance - 64) / 2)
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

    for n in range(number):
        enm = cls.Enemy(1)
        enm.rect.y = -120.0
        distance = glob.WINDOW_SIZE[0] / number
        enm.rect.x = float(n * distance + (distance - 64) / 2)
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

    for n in range(number):
        enm = cls.Enemy(2)
        enm.rect.y = -50.0
        distance = glob.WINDOW_SIZE[0] / number
        enm.rect.x = float(n * distance + (distance - 64) / 2)
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

def fight_1():
    for enm in glob.enemies_list:
        if game_timer < 1000:
            enm.rect.x += 0
            enm.rect.y = int(game_timer / 10) - 80


def fight_2():
    i = 0
    for enm in glob.enemies_list:
        i += 1
        if game_timer < 1080:
            enm.rect.y = int(game_timer / 10) - 80
            if i % 2 == 0:
                enm.rect.y += 80
        else:
            enm.rect.x = (enm.rect.x+4) % 1500 


def fight_3():
    n = len(glob.enemies_list.sprites())
    r = 120
    i = 0
    for enm in glob.enemies_list:
        i += 1
        angle_param = i * (360 / n) + game_timer / 100.0
        if game_timer < 1000:
            enm.rect.y = r * math.sin(angle_param) + game_timer / 10
            enm.rect.x = r * math.cos(angle_param) + 200.0
        else:
            enm.rect.y = r * math.sin(angle_param) + 100.0
            enm.rect.x = r * math.cos(angle_param) + math.cos(game_timer / 100) * 400 + 600.0

def fight_4():
    for enm in glob.enemies_list:
        if game_timer < 600:
            enm.rect.x += 0
            enm.rect.y = enm.rect.y + 1


def fight_5():
    for enm in glob.enemies_list:
        if game_timer < 600:
            enm.rect.y = enm.rect.y + 1
        else:   
            if enm.enmType == 0:
                enm.rect.x = (enm.rect.x + 4) % 1500
            else :
                enm.rect.x = (enm.rect.x - 4) % 1500


def fight_6():
   
    for enm in glob.enemies_list:
        if game_timer < 600:
            enm.rect.y = -100
        else:
            if enm.enmType == 0:
                enm.rect.x = (enm.rect.x + 4) % 1500
                enm.rect.y = (enm.rect.x / 4) % 400
            else :
                enm.rect.x = (enm.rect.x - 4) % 1500
                enm.rect.y = (340 - enm.rect.x/4) % 400

def fight_7():
    for enm in glob.enemies_list:
        if game_timer < 600:
            enm.rect.x += 0
            enm.rect.y = enm.rect.y + 1


def fight_8():
    for enm in glob.enemies_list:
        if game_timer < 600:
            enm.rect.y = enm.rect.y + 1
        else:   
            if enm.enmType == 1:
                enm.rect.x = (enm.rect.x + 4) % 1500
            elif enm.enmType == 2 :
                enm.rect.x = (enm.rect.x - 4) % 1500

def fight_9():
    for enm in glob.enemies_list:
        if game_timer < 600:
            if enm.enmType == 0:
                enm.rect.y += 1
            else:
                enm.rect.y = -100
        else:
            if enm.enmType == 1:
                enm.rect.x = (enm.rect.x + 4) % 1500
                enm.rect.y = (enm.rect.x / 4) % 400
            elif enm.enmType == 2:
                enm.rect.x = (enm.rect.x - 4) % 1500
                enm.rect.y = (400 - enm.rect.x/4) % 400

def move_enemies1():
    if glob.FIGHT == 1:
        fight_1()

    if glob.FIGHT == 2:
        fight_2()

    if glob.FIGHT == 3:
        fight_3()

def move_enemies2():
    if glob.FIGHT == 1:
        fight_4()

    if glob.FIGHT == 2:
        fight_5()

    if glob.FIGHT == 3:
        fight_6()

def move_enemies3():
    if glob.FIGHT == 1:
        fight_7()

    if glob.FIGHT == 2:
        fight_8()

    if glob.FIGHT == 3:
        fight_9()

# TO DO: 
# 1) izmeniti kretnja fight_8 fight_9 eventualno i fight_6
# 2) napraviti slike destroyer-a i ubaciti ih u glob
# 3) dodati pucnje za destroyera
# 4) postaviti automatsko vracanje u meni nakon kraja igre
# 5) promeniti background muziku
# 6) napraviti i zameniti story slike
# 7) napistai ovde sta jos treba!

def set_background():
    gui.screen.blit(glob.game_background, (0, 0))

    #DODATO
    #health bar
    gui.screen.blit(pygame.image.load('images/black.png'), (0, 650))
    gui.screen.blit(pygame.image.load('images/yellow1.png'), (10, 650))
    gui.screen.blit(glob.pause_img_1, glob.PAUSE_ONE_PLAYER_POS)
    font = pygameMenu.font.get_font(pygameMenu.font.FONT_PT_SERIF, 30)
    life = font.render('Lifes:', 1, (150, 150, 0))
    gui.screen.blit(life, (75, 655))


def start_game_one_player():

    global player, game_timer, burst_fire

    player = cls.Player()
    destroyer = cls.Destroyer()

    game_timer = 0  # Tajmer igrice
    timer_destroyer = 0  # Tajmer postavljanja destrojera
    burst_fire = 0  # Tajmer rafala
    next_level = True  # da znamo da li igramo igricu ili isrctavamo prelazak nivoa

    while True:
        game_timer += 3

        set_background()

        if next_level:
            # TO DO potrebno je obezbediti da se po zavrsetku igre vrati umeni!!
            if glob.LEVEL == 4:
                glob.return_to_main_menu()
                return
            
            next_level = False
            
            pressed_enter = False
            while not pressed_enter:
                events = pygame.event.get()
                for e in events:
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_RETURN:
                            pressed_enter = True
                
                gui.screen.blit(glob.stories[glob.LEVEL], (150, 20))
                pygame.display.update()

        #DODATO
        #ubijen je igrac vracamo se u meni
        #TO DO
        #obradicemo da zahteva ravans i slicno
        if player.lifes_number < 0:
            glob.return_to_main_menu()
            return

        # Ako ima nepriajtelja, neka ispaljuju metkove:
        num_enemies = len(glob.enemies_list.sprites())
        if num_enemies > 0:
            enemies_fire_to_player()
        else:
            # DODATO Ako nema nepriajatelja pravimo novu flotu u zavisnosti od fighta
            if glob.FIGHT < 3:
                game_timer = 0

                if glob.LEVEL == 1:
                    make_enemies1(glob.num_enemies[glob.LEVEL][glob.FIGHT])
                elif glob.LEVEL == 2:
                    make_enemies2(glob.num_enemies[glob.LEVEL][glob.FIGHT])
                elif glob.LEVEL == 3:
                    make_enemies3(glob.num_enemies[glob.LEVEL][glob.FIGHT])
                    
                glob.FIGHT += 1

            else:
                timer_destroyer = draw_destroyer(destroyer, timer_destroyer)

                if destroyer.health <= 0:
                    if glob.LEVEL == 3:
                        exit()
                    glob.LEVEL += 1
                    glob.FIGHT = 0
                    for r in glob.rockets_list:
                        glob.rockets_list.remove(r)
                        glob.all_sprites_list.remove(r)

                    glob.all_sprites_list.update()
                    start_game_one_player()

        # Funkcije koje prave animaciju kretanja
        if glob.LEVEL == 1:
            move_enemies1()
        elif glob.LEVEL == 2:
            move_enemies2()
        elif glob.LEVEL == 3:
            move_enemies3()

        # Iscrtaj neprijatelje
        for enm in glob.enemies_list:
            enm.show()

        # Funkcija koja proverava da li je pogodjen player
        check_bullets_player_collide()

        # Funkcija za proveru dogadjaja u meniju
        check_menu_events()

        # Funkcija za proveru dogadjaja nad player-om
        check_player_events()

        # Funkcija za proveru pogotka u (sve) neprijatelje
        check_rocket_to_enemise_colide(destroyer)

        # Funkcija za iscrtavanje player-a  ( X-Wing )
        draw_player()

        glob.all_sprites_list.update()
        pygame.display.update()
