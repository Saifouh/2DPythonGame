from copy import copy
import pygame as pg 

fonts = {}
def text(text, color, size, x, y, font, surface):
    if size not in fonts:
        fonts[size] = pg.font.Font(font, size)
    surf = fonts[size].render(text, False, color)  
    x = x - surf.get_rect().width / 2
    y = y - surf.get_rect().height / 2

    surface.blit(surf, (x, y))

def load_map(path):
    return [list(row) for row in open(path + ".txt", "r").read().split("\n")]

WHITE = (255, 255, 255)
GRAY = (10, 10, 15)
BLACK = (0, 0, 0)
FONT = "res/m5x7.ttf"

def endgame_events(game):
    # handling events
    # mainly related to checking if the player is going 
    # to replay or go back to the menu and pre-loading
    # the levels
    game.lvls.lvl_load = 0
    game.events = pg.event.get()
    for e in game.events:
        if e.type == pg.QUIT:
            game.running = 0
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_m:
                game.running = 1 
                game.player.state = "idle"
                game.lvls.current_lvl = 0
                game.lvls.lvls[game.lvls.current_lvl] = load_map(game.lvls.map_path + str(game.lvls.current_lvl))
                game.lvls.lvl_load = 1

            if e.key == pg.K_r:
                game.running = 2
                game.player.state = "idle"
                game.lvls.lvls[game.lvls.current_lvl] = load_map(game.lvls.map_path + str(game.lvls.current_lvl))
                game.lvls.lvl_load = 1
                game.lvls.boss_dead = 0
                game.lvls.boss_hp = 100


### add special score for points
def endgame_update(game):
    # making sure the current level number is correct
    # and not more than the number of levels
    if game.lvls.current_lvl >= game.lvls.lvl_num:
        game.state_changed = 1
        game.lvls.current_lvl -= 1
    
    # setting up the player pos if the player
    # has selected a level
    if game.lvls.lvl_load:
        pos = game.lvls.get_player_pos()
        game.player.rect.x = pos[0]
        game.player.rect.y = pos[1]
        game.player.reset_val()


def endgame_render(game):
    game.display.fill(GRAY)

    text("You finished the game!", 
         WHITE, 30, game.display.get_size()[0] / 2, 30, FONT, game.display)

    text("Press r to replay", WHITE, 41, game.display.get_size()[0] / 2, 100, FONT, game.display)
    text("or m to go the menu", WHITE, 41, game.display.get_size()[0] / 2, 140, FONT, game.display)

    time_str = f"{str(int(game.lvls.game_timer))} sec"
    coins = f"{game.player.coins_collected} coins collected"

    text(f"Time took to complete the game: {time_str}", WHITE, 40,  game.display.get_size()[0] / 2, 180, FONT, game.display)
    text(f"Coins collected: {coins}", WHITE, 40, game.display.get_size()[0] / 2, 210, FONT, game.display)
    if not game.running == 2:
        score_int = int(((240 - game.lvls.game_timer) + game.player.coins_collected) * 2)
        game.lvls.score = score_int
    #text("New score: " + str(score_int), WHITE, 40, game.display.get_size()[0] / 2, 280, FONT, game.display)
    if game.lvls.score > game.lvls.prev_score:
        game.lvls.prev_score = game.lvls.score 
    text(f"High score: {game.lvls.prev_score}", WHITE, 40, game.display.get_size()[0] / 2, 240, FONT, game.display)
    text("New score: " + str(game.lvls.score), WHITE, 40, game.display.get_size()[0] / 2, 280, FONT, game.display)
    # final render
    game.window.draw(main_surf = game.display, scale = 2);


def endgame(game):
    endgame_events(game)
    endgame_update(game)
    endgame_render(game)
