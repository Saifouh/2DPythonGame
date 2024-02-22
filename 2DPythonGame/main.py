
### constants file with size for screen, resource folder paths and more
### configuration related stuff
from CONSTANTS import *  
import pygame as pg
import sys
from states.menu import menu 
from states.game import gameplay
from states.end import endgame 
from behaviours.player import player
from behaviours.levels import level 

pg.init()
pg.font.init()
pg.mixer.init()
pg.display.init()

# A small and simple window class
class pe_win:
    def __init__(self, size, caption = "pg game", flags = 0, icon = None):
        self.size = size 
        self.caption = caption
        self.flags = flags
        self.icon = icon
        self.screen = pg.display.set_mode(self.size, self.flags)

        pg.display.set_caption(caption)

        self.fps = pg.time.Clock()

        if icon is not None:
            pg.display.set_icon(pg.image.load(self.icon).convert())
    
        self.display_size = pg.display.get_surface().get_size()

    # clears the screen
    def cls(self, color = (0, 0, 0)):
        self.screen.fill(color)

    def get_current_size(self):
        self.display_size = pg.display.get_surface().get_size()
        return self.display_size

    # Draws a smaller surface which contains the main game, 
    # helps in making the game faster and more efficient
    # since you are drawing to a smaller surface and scaling it
    # up, also allows you to draw smaller art which can then be
    # scaled by the game
    def draw(self, main_surf=None, pos=[0, 0], scale=0, fps=60):
        self.screen.fill((0, 0, 255))

        self.display_size = pg.display.get_surface().get_size()
        if main_surf is not None and scale:
            pg.transform.scale(main_surf, self.display_size, dest_surface=self.screen)

        if main_surf is not None and not scale:
            self.screen.blit(main_surf, pos)

        pg.display.update()
        self.fps.tick(fps)

    # Closes pygame and the program
    def close(self):
        pg.quit()
        sys.exit()

class pe_mouse:
    def __init__(self, img = None, visible = True):
        self.visible = visible
        pg.mouse.set_visible(self.visible)
        self.pos = pg.mouse.get_pos()

    # If you use a smaller surface than the original display, this function is very important
    # It returns the relative position of the mouse on the smaller surface rather than on the actual screen
    def get_scaled_coords(self, win_size, surf_size):
        self.pos = pg.mouse.get_pos()
        return (self.pos[0] / (win_size[0] / surf_size[0]), self.pos[1] / (win_size[1] / surf_size[1]))

class game_state:
    def __init__(self):
        self.window = pe_win(WINDOW_SIZE, TITLE)
        # a smaller display surface which is then scaled up
        self.display = pg.Surface(DISPLAY_SIZE)

        self.running = 1
        self.lmbtn_down = 0
        self.mouse = pe_mouse()
        self.mouse_pos = [0, 0]
        self.helping = 0
        # storing the pygame events
        self.events = 0

        self.play_button = pg.Rect(DISPLAY_CENTER[0] - 50, 
                                   DISPLAY_CENTER[1] - 15, 
                                   100, 30)
        self.help_button = pg.Rect(DISPLAY_CENTER[0] - 50, 
                                   DISPLAY_CENTER[1] + 50 - 15, 
                                   100, 30)

        self.lvls_button = pg.Rect(DISPLAY_CENTER[0] - 50, 
                                   DISPLAY_CENTER[1] + 100 - 15, 
                                   100, 30)

        self.exit_button = pg.Rect(DISPLAY_CENTER[0] - 50, 
                                   DISPLAY_CENTER[1] + 150 - 15,
                                   100, 30)
        self.selecting_lvls = 0



        # the map tiles are 32, 32 and map is contained in maps folder
        self.lvls = level(LVLS, LVL_FOLDER, [32, 32], TILE_NUMS, TILES)

        self.player = player(self.lvls.get_player_pos(), PLAYER_IMG_FOLDER, 
                             PLAYER_STATES, PLAYER_STATE_LIST, 
                             PLAYER_SIZE)

        self.lvls.get_rects()

    # this function handles different game states like menu..etc..
    def handle_states(self):
        while self.running:
            # menu
            while self.running == 1:
                self.mouse_pos = self.mouse.get_scaled_coords(self.window.get_current_size(), DISPLAY_SIZE)
                menu(self)

            # main game
            while self.running == 2:
                self.mouse_pos = self.mouse.get_scaled_coords(self.window.get_current_size(), DISPLAY_SIZE)
                gameplay(self)

            # game end
            while self.running == 3:
                self.mouse_pos = self.mouse.get_scaled_coords(self.window.get_current_size(), DISPLAY_SIZE)
                endgame(self)


    # closing
    def destroy(self):
        self.window.close()

if __name__ == '__main__':
    game_s = game_state()
    game_s.handle_states()
    # save file
    game_s.lvls.save("res/lvls/save.txt")
    game_s.destroy()


