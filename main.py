from pygame import mixer
from source import gui
from source import glob
import pygame

def main():  
    pygame.init()
    gui.play()

    #pustamo menu_music
    mixer.music.load('sounds/menu_music.mp3')
    mixer.music.set_volume(glob.MENU_VOLUME)
    mixer.music.play(-1)

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()

        if gui.main_menu.is_enabled():
            gui.main_menu.mainloop(events)

        pygame.display.update()

if __name__ == '__main__':
    main()
