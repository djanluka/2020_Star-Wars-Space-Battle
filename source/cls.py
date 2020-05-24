from source import glob
from source import gui
import random
import pygame

class Player():
    ''' Player class '''
    def __init__(self):
        self.position_x = int(glob.WINDOW_SIZE[0]/2)
        self.position_y = int(glob.WINDOW_SIZE[1] - 120)
        self.health = 100
        self.lives_number = 0
        self.image = glob.x_wing

    def show_health(self):
        for i in range(self.lives_number):
            gui.screen.blit(glob.life_image, (150 + i*35, glob.WINDOW_SIZE[1]-40))

        pygame.draw.rect(gui.screen, (200, 150, 0), (glob.WINDOW_SIZE[0]-400, glob.WINDOW_SIZE[1]-35, -self.health * 6, 20))

    def show_player(self):
        gui.screen.blit(self.image, (self.position_x, self.position_y))

class twoPlayer():
    def __init__(self):
        self.position_x = int(glob.WINDOW_SIZE[0]/2)
        self.position_y = int(glob.WINDOW_SIZE[1] - 120)
        self.health = 100
        self.image = glob.x_wing
   
    def show_health(self, num_player):
        if gui.main_menu.is_enabled() or gui.pause_menu.is_enabled():
            return None

        if num_player == 2:
            pygame.draw.rect(gui.screen, (0, 0, 255), (glob.WINDOW_SIZE[0]-20-64, glob.WINDOW_SIZE[1]-40, -self.health * 4,20))
        if num_player == 1:
            pygame.draw.rect(gui.screen, (180, 0, 0), (20+64, glob.WINDOW_SIZE[1]-40, self.health * 4,20))
    
    def show_players(self):
        gui.screen.blit(self.image, (self.position_x, self.position_y))

class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = glob.rocket
        self.rect = self.image.get_rect()

    def show_rocket(self):
        gui.screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y = self.rect.y - 10
        
class leftRocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotate(glob.rocket, -90)
        self.rect = self.image.get_rect()

    def show_left_rocket(self):
        gui.screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x += 10

class rightRocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotate(glob.rocket, 90)
        self.rect = self.image.get_rect()

    def show_rocket(self):
        gui.screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x -= 10

class Destroyer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.dstType = 0
        self.image = pygame.Surface([100, 50])
        self.rect = self.image.get_rect()
        self.health = 100
        self.is_ready = False
        self.image = glob.destroyers[glob.LEVEL-1]

    def show_destroyer(self):
        gui.screen.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(pygame.sprite.Sprite):
    ''' Enemy class '''
    def __init__(self, enmType):
        super().__init__()
        self.enmType = enmType
        self.image = pygame.transform.scale(glob.fighters[enmType], (50,50))
        self.rect = self.image.get_rect()
        self.hidden = False

    def is_hidden(self):
        return self.hidden

    def show(self):
        if not self.hidden:
            gui.screen.blit(self.image, (self.rect.x, self.rect.y))

class BulletEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/rocket_enemy.png')
        self.rect = self.image.get_rect()
        self.direction = [0, 1]

    def set_direction(self, player_pos_x, player_pos_y, intensity):
        self.direction[0] = (player_pos_x - self.rect.x) / intensity + 0.1
        self.direction[1] = (player_pos_y - self.rect.y) / intensity + 0.1

        direct = self.direction[0]
        if 0.1 <= direct and direct <= 0.2:
            self.image = pygame.transform.rotate(self.image, 8)
        elif 0.2 < direct and direct <= 0.4:
            self.image = pygame.transform.rotate(self.image, 18)
        elif 0.4 < direct and direct <= 0.6:
            self.image = pygame.transform.rotate(self.image, 30)
        elif 0.6 < direct and direct <= 0.8:
            self.image = pygame.transform.rotate(self.image, 45)
        elif dir > 0.8:
            self.image = pygame.transform.rotate(self.image, 55)
        elif -0.2 < direct and direct <= 0.1:
            self.image = pygame.transform.rotate(self.image, -8)
        elif -0.4 <= direct and direct < -0.2:
            self.image = pygame.transform.rotate(self.image, -18)
        elif -0.6 <= direct and direct < -0.4:
            self.image = pygame.transform.rotate(self.image, -30)
        elif -0.8 <= direct and direct < -0.6 :
            self.image = pygame.transform.rotate(self.image, -45)
        elif dir < -0.8:
            self.image = pygame.transform.rotate(self.image, -55)


    def show_rocket(self, rocket):
        gui.screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x += self.direction[0] * 10
        self.rect.y += self.direction[1] * 10


class BulletDestroyer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([6, 6])
        self.image.fill((255, 10, 10))
        self.rect = self.image.get_rect()
        self.direction = [0, 1]

    def show_rocket(self, rocket):
        gui.screen.blit(rocket, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x += self.direction[0] * 10
        self.rect.y += self.direction[1] * 10


class Controler():
    def __init__(self):
        self.Left = glob.CONTROL_LEFT_ORD
        self.Right = glob.CONTROL_RIGHT_ORD
        self.Fire = glob.CONTROL_FIRE_ORD
        self.Left1 = glob.TWO_CONTROL_LEFT_ORD1
        self.Right1 = glob.TWO_CONTROL_RIGHT_ORD1
        self.Fire1 = glob.TWO_CONTROL_FIRE_ORD1
        self.Left2 = glob.TWO_CONTROL_LEFT_ORD2
        self.Right2 = glob.TWO_CONTROL_RIGHT_ORD2
        self.Fire2 = glob.TWO_CONTROL_FIRE_ORD2
