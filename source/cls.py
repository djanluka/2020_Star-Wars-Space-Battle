from source import glob
from source import gui
import pygame

class Player():
    def __init__(self):
        self.position_x = int(glob.WINDOW_SIZE[0]/2)
        self.position_y = int(glob.WINDOW_SIZE[1] - 120)
        self.health = 100
        self.lifes_number = 3
        self.image = pygame.image.load('images/player.png')
   
    def show_health(self):

        if gui.main_menu.is_enabled() or gui.pause_menu.is_enabled():
            return None

        for i in range(self.lifes_number):
            gui.screen.blit(self.image, (10 + i*70, glob.WINDOW_SIZE[1]-60))
        	
        pygame.draw.rect(gui.screen, (0, 100, 100), (glob.WINDOW_SIZE[0]-20, glob.WINDOW_SIZE[1]-40, -self.health * 10,20))
    
    def show(self):

        if gui.main_menu.is_enabled() or gui.pause_menu.is_enabled():
            return None

        gui.screen.blit(self.image, (self.position_x, self.position_y))
        self.show_health()


class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/rocket-launch.png')
        self.rect = self.image.get_rect()

    def show_rocket(self):

        if gui.main_menu.is_enabled() or gui.pause_menu.is_enabled():
            return None

        gui.screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y -= 10

class Destroyer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([100, 50])
        self.rect = self.image.get_rect()
        self.health = 100
        self.is_ready = False
        self.image = pygame.image.load('images/destroyer.png')

    def show(self):

        if gui.main_menu.is_enabled() or gui.pause_menu.is_enabled():
            return None

        gui.screen.blit(self.image, (self.rect.x, self.rect.y))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/enemy1.png')
        self.rect = self.image.get_rect()

    def show(self):

        if gui.main_menu.is_enabled() or gui.pause_menu.is_enabled():
            return None

        gui.screen.blit(self.image, (self.rect.x, self.rect.y))

class BulletEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([5, 5])
        self.image.fill((100, 255, 200))
        self.rect = self.image.get_rect()
        self.direction = [0, 1]
   
    def show_rocket(self, rocket):

        if gui.main_menu.is_enabled() or gui.pause_menu.is_enabled():
            return None

        gui.screen.blit(rocket, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x += self.direction[0] * 6
        self.rect.y += self.direction[1] * 6

class Controler():
    def __init__(self):
        self.control = {}
        self.set_controls()

    def set_controls(self):
        self.control['Left'] = glob.CONTROL_LEFT_ORD
        self.control['Right'] = glob.CONTROL_RIGHT_ORD
        self.control['Fire'] = glob.CONTROL_FIRE_ORD

    def get_control(self, eve):
        return self.control[eve]
