from re import I
import pygame as pg

fonts = {}
### draw centered text
### returns the width and height of the text as well
def text(text, color, size, x, y, font, surface):
    if size not in fonts:
        fonts[size] = pg.font.Font(font, size)
    surf = fonts[size].render(text, False, color)  
    x = x - surf.get_rect().width / 2
    y = y - surf.get_rect().height / 2

    surface.blit(surf, (x, y))
    return (surf.get_rect().width, surf.get_rect().height)

def load_map(path):
    return [list(row) for row in open(path + ".txt", "r").read().split("\n")]

WHITE = (255, 255, 255)
GRAY = (10, 10, 15)
BLACK = (0, 0, 0)
FONT = "res/m5x7.ttf"

def menu_events(game):
    game.events = pg.event.get()
    for e in game.events:
        if e.type == pg.QUIT:
            game.running = 0
        if e.type == pg.KEYDOWN:
            if e.key != pg.K_h and not game.helping:
                game.running = 2
            if e.key == pg.K_ESCAPE and game.helping:
                game.helping = 0
            if e.key == pg.K_h:
                game.helping = 1

        if e.type == pg.MOUSEBUTTONDOWN:
            game.lmbtn_down = 1

        if e.type == pg.MOUSEBUTTONUP:
            game.lmbtn_down = 0


def menu_update(game):
    pass


def menu_render(game):
    game.display.fill(BLACK)
    
    # checking if the current level is bigger
    # than the old saved level, if it is, lvl_n
    # becomes the current level otherwise not
    lvl_n = game.lvls.old_unlocked_lvl + 1
    if game.lvls.current_lvl >= game.lvls.old_unlocked_lvl:
        lvl_n = game.lvls.current_lvl + 1

    text("Dungeon Crawler", WHITE, 60, game.display.get_size()[0] / 2,
         game.display.get_size()[1] / 2 - 50, FONT, game.display)

    pg.draw.rect(game.display, WHITE, game.play_button, border_radius=10)
    text("Play", BLACK, 30, game.display.get_size()[0] / 2, game.display.get_size()[1] / 2, FONT, game.display)

    pg.draw.rect(game.display, WHITE, game.help_button, border_radius=10)
    text("Help", BLACK, 30, game.display.get_size()[0] / 2, game.display.get_size()[1] / 2 + 50, FONT, game.display)

    pg.draw.rect(game.display, WHITE, game.exit_button, border_radius=10)
    text("Exit", BLACK, 30, game.display.get_size()[0] / 2, game.display.get_size()[1] / 2 + 150, FONT, game.display)
    
    # here we now properly use the lvl_n variable
    # to check if the player should be able to
    # select a level    
    if lvl_n + 1 > 1:
        pg.draw.rect(game.display, WHITE, game.lvls_button, border_radius=10)
        text("Lvls", BLACK, 30, game.display.get_size()[0] / 2, game.display.get_size()[1] / 2 + 100, FONT, game.display)

    # this is the help screen in the game with simple
    # instructions on how to play the game
    if game.helping:
        game.display.fill(BLACK)
        
        text("WASD to move", WHITE, 30, game.display.get_size()[0] / 2, game.display.get_size()[1] / 2 - 100, FONT, game.display)
        text("Space to jump or double it", WHITE, 30, game.display.get_size()[0] / 2, game.display.get_size()[1] / 2 - 80, FONT, game.display)
        text("R to respawn", WHITE, 30, game.display.get_size()[0] / 2, game.display.get_size()[1] / 2 - 60, FONT, game.display)
        text("E to attack, F for ability", WHITE, 30, game.display.get_size()[0] / 2, game.display.get_size()[1] / 2 - 40, FONT, game.display)
        text("Avoid the lava and the spikes", WHITE, 30, game.display.get_size()[0]/2, game.display.get_size()[1] / 2, FONT, game.display) 


    mouse_rect = pg.Rect(game.mouse_pos[0], game.mouse_pos[1], 16, 16)
    ### level select screen
    if game.selecting_lvls:
        game.display.fill(GRAY)
        posx = 20
        posy = game.display.get_size()[1] / 2
        lvls = []
        for i in range(0, lvl_n):
            size = text(str(i + 1), WHITE, 30, posx, posy, FONT, game.display)
            lvls.append(pg.Rect(posx - size[0] / 2, posy - size[1] / 2, size[0], size[1]))
            pg.draw.rect(game.display, BLACK, lvls[i])
            size = text(str(i + 1), WHITE, 30, posx, posy, FONT, game.display)
            posx += 30
        
        for i in range(0, len(lvls)):
            if game.lmbtn_down:
                if lvls[i].colliderect(mouse_rect):
                    game.lvls.current_lvl = i
                    game.lvls.lvls[game.lvls.current_lvl] = load_map(game.lvls.map_path + str(game.lvls.current_lvl))
                    pos = game.lvls.get_player_pos()
                    game.player.rect = pg.Rect(pos[0], pos[1], game.player.rect.w, game.player.rect.h)
                    game.lvls.get_rects()
                    game.selecting_lvls = 0

    ### checking collisions with buttons
    if game.lmbtn_down and not game.selecting_lvls and not game.helping:
        if mouse_rect.colliderect(game.play_button):
            game.running = 2
            game.lmbtn_down = 0
            game.player.state = "idle"

            if game.lvls.current_lvl >= game.lvls.lvl_num:
                game.running = 5

        if mouse_rect.colliderect(game.help_button):
            game.helping = 1
            game.lmbtn_down = 0
        if mouse_rect.colliderect(game.lvls_button) and lvl_n + 1 > 1:
            game.selecting_lvls = 1
            game.lmbtn_down = 0

        if mouse_rect.colliderect(game.exit_button):
            game.running = 0
            game.lmbtn_down = 0


    # drawing everything to the big surface or the window
    game.window.draw(main_surf = game.display, scale = 2)
    

def menu(game):
    menu_events(game)
    menu_update(game)
    menu_render(game)

