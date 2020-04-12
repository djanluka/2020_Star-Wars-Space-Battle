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
destroyer = None
game_timer = 0
burst_fire = 0
timer_destroyer = 0

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

    if pressed[cont.get_control('Fire')] and (glob.ENEMIES_IS_READY or destroyer.is_ready):
        # Metak se ispaljuje u svakom 20-tom ciklusu
        if burst_fire > 10:
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

def draw_destroyer():
    global destroyer, timer_destroyer
    timer_destroyer += 3
    destroyer.rect.x = glob.WINDOW_SIZE[0] / 2 - 64
    destroyer.rect.y = (int(timer_destroyer / 5) - 240 if timer_destroyer < 1400 else 40)

    if destroyer.health > 0:
        destroyer.show()
        if timer_destroyer > 1000:
            pygame.draw.rect(gui.screen, (200, 10, 10), (150, 10, destroyer.health * 10, 20))
        if timer_destroyer > 1200:
            destroyer.is_ready = True
            destroyer_fire_to_player()


def destroyer_battle():

    if destroyer.health <= 0:
        destroyer.is_ready = False
        if glob.LEVEL == 3:
            exit()
        glob.LEVEL += 1
        glob.FIGHT = 0
        for r in glob.rockets_list:
            glob.rockets_list.remove(r)
            glob.all_sprites_list.remove(r)
        for b in glob.bullets_enm_list:
            glob.bullets_enm_list.remove(b)
            glob.all_sprites_list.remove(b)

        glob.all_sprites_list.update()
        start_game_one_player()
    else:
        draw_destroyer()

def set_hidden_enemys():
    global timer_hidden, hidden_enemy
    '''
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
    elif timer_hidden < 60:  # odokativna duzina koliko je nevidljiv
        timer_hidden += 1
    else:
        timer_hidden = 0
        hidden_enemy.hidden = False
    '''
    # OVO JE KOD GDE MI SVI ENEMYJI POSTAJU NEVIDLJIVI NA 150 MILISEKUDNI
    # KOD IZNAD OVOG JE KAD MI SMAO JEDAN ENEMY POSTAJE NEVIDLJIV
    # OVO NE MORAJU DA BUDU KONACNE FUNCKIJE
    # IDEJA MI JE DA NAPRAVIMO JEDNU POSEBNU FUNKCIJU GDE CEMO U ZAVISNOSTI OD LEVELA I FIGHTA
    # DA BIRAMO NA KOJI CE NACIN ENEMY-JI DA BUDU NEVIDLJIVI
    if hidden_enemy is True: #glob.LEVEL == 1 and glob.FIGHT == 3:
        if timer_hidden == 0:
            for enm in glob.enemies_list:
                enm.hidden = True
                timer_hidden += 1
        elif timer_hidden < 150:  # odokativna duzina koliko je nevidljiv
            timer_hidden += 1
        else:
            timer_hidden = -150
            for enm in glob.enemies_list:
                enm.hidden = False


def enemies_fire_to_player():

    #Ako nema neprijatelja ne pucamo
    if glob.ENEMIES_IS_READY is False or player.health <= 0:
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

    set_hidden_enemys()


def destroyer_fire_to_player():

    global timer_destroyer
    if player.health <= 0:
        glob.bullets_enm_list.draw(gui.screen)
        return

    #ODOKATIVNO 99, STAVICEMO NESTO STO JE U ZAVISNOSTI OD LEVELA
    if timer_destroyer % 99 == 0:
        for i in range(3):
            bul = cls.BulletDestroyer()
            bul.rect.x = destroyer.rect.x + 32*(i+1)
            bul.rect.y = destroyer.rect.y + 115
            intensity = math.sqrt((bul.rect.x - player.position_x) ** 2 + (bul.rect.y - player.position_y) ** 2)
            bul.direction[0] = (player.position_x - bul.rect.x) / intensity + i/10
            bul.direction[1] = (player.position_y - bul.rect.y) / intensity + i/10
            glob.bullets_enm_list.add(bul)
            glob.all_sprites_list.add(bul)

    glob.bullets_enm_list.draw(gui.screen)

    '''
    bul1 = cls.BulletEnemy()
    bul1.rect.x = rand_enm.rect.x + 32
    bul1.rect.y = rand_enm.rect.y + 32
    glob.bullets_enm_list.add(bul1)
    glob.all_sprites_list.add(bul1)
    '''


def check_bullets_player_collide():
    for bullet in glob.bullets_enm_list:
        if bullet.rect.x in range(player.position_x, player.position_x + 64):
            if bullet.rect.y in range(player.position_y + 20, player.position_y + 64):
                glob.bullets_enm_list.remove(bullet)
                if destroyer.is_ready:
                    player.health -= 15
                else:
                    player.health -= 7

        if bullet.rect.y > glob.WINDOW_SIZE[1] - 55:
            glob.bullets_enm_list.remove(bullet)


def check_rocket_to_enemise_colide():
    global destroyer, timer_hidden, hidden_enemy

    for r in glob.rockets_list:
        r.show_rocket()

        if glob.ENEMIES_IS_READY:
            # Obrada kolizije player vs enemies
            enemy_hit_list = pygame.sprite.spritecollide(r, glob.enemies_list, True)

            for enm in enemy_hit_list:
                #DODATO
                #ako smo uspeli da pogodimo nevidljivog, moramo da ga izbrisemo
                #i da ostavimo mogucnost za biranje sledeceg
                #if enm.is_hidden():
                 #   timer_hidden = 0
                 #   hidden_enemy = None
                glob.rockets_list.remove(r)
                glob.all_sprites_list.remove(r)
                glob.enemies_list.remove(enm)

        # ako je destroyer spreman onda mozemo da pucamo na njega i da mu skidamo health-e
        if destroyer.is_ready:
            print("usaoooo")
            # Obrada kolizije player vs destroyer
            if r.rect.x in range(destroyer.rect.x, destroyer.rect.x + 120):
                dist = 120 - r.rect.x + destroyer.rect.x
                dist = dist if dist < 64 else 120 - dist
                if r.rect.y < destroyer.rect.y + 3 * dist + 40:
                    glob.rockets_list.remove(r)
                    glob.all_sprites_list.remove(r)
                    # Zvuk eksplozije kada metak pogodi protivnika
                    #explosion_sound = mixer.Sound('sounds/explosion.wav')
                    #explosion_sound.play()
                    destroyer.health -= 7

        if r.rect.y < -20:
            glob.rockets_list.remove(r)
            glob.all_sprites_list.remove(r)

def make_new_enemies():
    global game_timer
    game_timer = 0

    if glob.LEVEL == 1:
        make_enemies4(glob.num_enemies[glob.LEVEL][glob.FIGHT])
    elif glob.LEVEL == 2:
        make_enemies2(glob.num_enemies[glob.LEVEL][glob.FIGHT])
    elif glob.LEVEL == 3:
        make_enemies3(glob.num_enemies[glob.LEVEL][glob.FIGHT])

    glob.FIGHT += 1

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

def make_enemies4(number):

    for i in range(1, 5):
        for n in range(1, 20):
            if i % 2 == 0:
                enm = cls.Enemy(0)
            else:
                enm = cls.Enemy(1)
            enm.rect.y = -(30 * i + 60 * (i-1))
            distance = int((glob.WINDOW_SIZE[0] - 20*40) / 21)
            enm.rect.x = float(n * distance + n*40)
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)


def fight_1():
    if game_timer < 1000:
        for enm in glob.enemies_list:
                enm.rect.x += 0
                enm.rect.y = int(game_timer / 10) - 80
    else:
        glob.ENEMIES_IS_READY = True

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

    glob.ENEMIES_IS_READY = True


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
    glob.ENEMIES_IS_READY = True


def fight_4():
    if game_timer < 600:
        for enm in glob.enemies_list:
                enm.rect.x += 0
                enm.rect.y = enm.rect.y + 1
    else:
        glob.ENEMIES_IS_READY = True


def fight_5():
    for enm in glob.enemies_list:
        if game_timer < 600:
            enm.rect.y = enm.rect.y + 1
        else:   
            if enm.enmType == 0:
                enm.rect.x = (enm.rect.x + 4) % 1500
            else :
                enm.rect.x = (enm.rect.x - 4) % 1500
    glob.ENEMIES_IS_READY = True


def fight_6():
   
    for enm in glob.enemies_list:
        if game_timer < 600:
            enm.rect.y = -100
        else:
            if enm.enmType == 0:
                enm.rect.x = (enm.rect.x + 4) % 1500
                enm.rect.y = (enm.rect.x / 4) % 400
            else:
                enm.rect.x = (enm.rect.x - 4) % 1500
                enm.rect.y = (340 - enm.rect.x/4) % 400
    glob.ENEMIES_IS_READY = True

def fight_7():
    for enm in glob.enemies_list:
        if game_timer < 600:
            enm.rect.x += 0
            enm.rect.y = enm.rect.y + 1
    glob.ENEMIES_IS_READY = True


def fight_8():
    for enm in glob.enemies_list:
        if game_timer < 600:
            enm.rect.y = enm.rect.y + 1
        else:   
            if enm.enmType == 1:
                enm.rect.x = (enm.rect.x + 4) % 1500
            elif enm.enmType == 2 :
                enm.rect.x = (enm.rect.x - 4) % 1500
    glob.ENEMIES_IS_READY = True

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
    glob.ENEMIES_IS_READY = True

def fight_10():
    if game_timer < 500:
        for enm in glob.enemies_list:
            enm.rect.y += 2
    else:
        glob.ENEMIES_IS_READY = True


def fight_11():

    if game_timer < 500:
        for enm in glob.enemies_list:
            enm.rect.y += 2
    else:
        glob.ENEMIES_IS_READY = True
        for enm in glob.enemies_list:
            if enm.enmType == 0:
                enm.rect.x = (enm.rect.x-4) % glob.WINDOW_SIZE[0]
            elif enm.enmType == 1:
                enm.rect.x = (enm.rect.x+4) % glob.WINDOW_SIZE[0]

def fight_12():
    global hidden_enemy
    if game_timer < 500:
        for enm in glob.enemies_list:
            enm.rect.y += 2
    else:
        glob.ENEMIES_IS_READY = True
        hidden_enemy = True
        for enm in glob.enemies_list:
            if enm.enmType == 0:
                enm.rect.x = (enm.rect.x - 4) % glob.WINDOW_SIZE[0]
            elif enm.enmType == 1:
                enm.rect.x = (enm.rect.x + 4) % glob.WINDOW_SIZE[0]


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


def move_enemies4():
    if glob.FIGHT == 1:
        fight_10()

    if glob.FIGHT == 2:
        fight_11()

    if glob.FIGHT == 3:
        fight_12()


def move_enemies():

    #Samo ako postoje neprijatelji
    if len(glob.enemies_list) > 0:
        if glob.LEVEL == 1:
            move_enemies4()
        elif glob.LEVEL == 2:
            move_enemies2()
        elif glob.LEVEL == 3:
            move_enemies3()

def set_background():
    gui.screen.blit(glob.game_background, (0, 0))

    #DODATO
    #health bar
    gui.screen.blit(pygame.image.load('images/black.png'), (0, 650))
    gui.screen.blit(pygame.image.load('images/yellow1.png'), (10, 650))
    gui.screen.blit(glob.pause_img_1, glob.PAUSE_ONE_PLAYER_POS)
    font = pygameMenu.font.get_font(pygameMenu.font.FONT_PT_SERIF, 30)
    lifes = font.render('Lifes:', 1, (150, 150, 0))
    gui.screen.blit(lifes, (75, 655))


def set_background_num_enemies():
    #DODATO
    #iscrtavanje koliko nam je enmija ostalo da bismo presli na naredbi fight
    font = pygameMenu.font.get_font(pygameMenu.font.FONT_PT_SERIF, 30)
    enm1 = 0
    enm2 = 0
    for enm in glob.enemies_list:
        if enm.enmType == 0:
            enm1 += 1
        elif enm.enmType == 1:
            enm2 += 1
    enm1 = font.render(f':{enm1}', 1, (150, 150, 0))
    enm2 = font.render(f':{enm2}', 1, (150, 150, 0))
    gui.screen.blit(enm1, (1130, 655))
    gui.screen.blit(enm2, (1210, 655))
    gui.screen.blit(pygame.image.load('images/enm1_30px.png'), (1095, 660))
    gui.screen.blit(pygame.image.load('images/enm2_30px.png'), (1175, 660))

# TO DO:
# 1) izmeniti kretnja fight_8 fight_9 eventualno i fight_6
# 2) napraviti slike destroyer-a i ubaciti ih u glob
# 3) dodati pucnje za destroyera
# 4) postaviti automatsko vracanje u meni nakon kraja igre
# 5) promeniti background muziku
# 6) napraviti i zameniti story slike
# 7) napistai ovde sta jos treba!
# GORE SAM OSTAVIO KOMENTAR ZA NEVIDLJIVOST ENEMYJA
# ALI TAKODJE MISLIM DA  UMESTO SAMO JEDNOG RANDOOM ENEMYJA BIRAMO VISE NJIH DA PUCA ISTOVREMENO
# DODAO SAM DVE NOVE SLIKE ENM1_40PX, ENM2_40PX JER SA MANJIM ENEYJIMA MOZE DOSTA VISE DA IH BUDE
#ZATO SAM I NAPRAVIO MAKE_ENEMIES_4 DA VIDIMO KOLIKO JE BOLJE KAD IMAMO VISE PROTIVNIKA
#PROBAO SAM I SLIAKAMA OD 30PX ALI TU SU MI ONDA NEKAKO PREVISE SITNI




def start_game_one_player():

    global player, destroyer, game_timer, timer_destroyer, burst_fire

    player = cls.Player()
    destroyer = cls.Destroyer()

    game_timer = 0
    timer_destroyer = 0
    burst_fire = 0
    next_level = True  # da znamo da li igramo igricu ili isrctavamo prelazak nivoa

    while True:
        game_timer += 3
        set_background()

        if next_level:
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

        if player.lifes_number < 0:
            glob.return_to_main_menu()
            return

        # Ako ima nepriajtelja, neka ispaljuju metkove i neka se krecu:
        num_enemies = len(glob.enemies_list.sprites())
        if num_enemies > 0:
            enemies_fire_to_player()
            move_enemies()
        else:
            glob.ENEMIES_IS_READY = False
            if glob.FIGHT < 3:
                make_new_enemies()
            else:
                #Zavrsili smo fight 3, vreme je za destroyera
                destroyer_battle()

        # Iscrtaj neprijatelje
        for enm in glob.enemies_list:
            enm.show()

        #ispisuje broj preostalih enemyja u health-baru
        set_background_num_enemies()

        # Funkcija koja proverava da li je pogodjen player
        check_bullets_player_collide()

        # Funkcija za proveru dogadjaja u meniju
        check_menu_events()

        # Funkcija za proveru dogadjaja nad player-om
        check_player_events()

        # Funkcija za proveru pogotka u (sve) neprijatelje
        check_rocket_to_enemise_colide()

        # Funkcija za iscrtavanje player-a  ( X-Wing )
        draw_player()

        glob.all_sprites_list.update()
        pygame.display.update()
