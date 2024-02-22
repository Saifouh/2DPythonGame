import pygame as pg
import sys

def load_map(path):
    return [list(row) for row in open(path + ".txt", "r").read().split("\n")]

fonts = {}
def text(text, color, size, x, y, font, surface):
    if size not in fonts:
        fonts[size] = pg.font.Font(font, size)
    surf = fonts[size].render(text, False, color)  
    x = x - surf.get_rect().width / 2
    y = y - surf.get_rect().height / 2

    surface.blit(surf, (x, y))

WHITE = (255, 255, 255)
GRAY = (10, 10, 15)
BLACK = (0, 0, 0)
FONT = "res/m5x7.ttf"

def game_events(game):
    game.events = pg.event.get()
    for e in game.events:
        if e.type == pg.QUIT:
            game.running = 0

        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                game.running = 1

    game.player.handle_events(game.events)

def game_update(game):
    if game.lvls.level_completed:
        game.lvls.current_lvl += 1

    # prevents an error where the current level may 
    # be bigger than the actual number of levels,
    # if it is bigger, the player goes to the end screen
    if game.lvls.current_lvl >= game.lvls.lvl_num:
        game.running = 3
        game.lvls.current_lvl -= 1
    
    # if the player has completed the level,
    # the next level is loaded in
    if game.lvls.level_completed:
        game.lvls.lvls[game.lvls.current_lvl] = load_map(game.lvls.map_path + str(game.lvls.current_lvl))
        pos = game.lvls.get_player_pos()
        game.player.rect.x = pos[0]
        game.player.rect.y = pos[1]
        game.lvls.rects = []
        game.lvls.enemies = []
        game.lvls.enemy_num = []
        game.lvls.level_completed = 0



    game.player.calc_scroll()
    game.player.reset_val()

    if game.player.state != "dead":
        if game.player.moving["right"]:
            game.player.vel[0] += 2
        
        if game.player.moving["left"]:
            game.player.vel[0] -= 2

    # simple checking if the player is dead or not,
    # if the player is dead, the game resets the level
    if game.player.state == "dead":
        game.lvls.lvls[game.lvls.current_lvl] = load_map(game.lvls.map_path + str(game.lvls.current_lvl))
        pos = game.lvls.get_player_pos()
        game.player.rect.x = pos[0]
        game.player.rect.y = pos[1]
        game.lvls.rects = []
        game.lvls.enemies = []
        game.lvls.enemy_num = []
        game.player.coins_collected = 0

    game.lvls.check_collisions(game.player)
    game.player.update()

    if game.window.fps.get_fps() > 0:
        game.lvls.game_timer += 1/game.window.fps.get_fps()

def game_render(game):
    game.display.fill((0, 0, 0))

    game.lvls.render(game.display, game.player.scroll)
    game.player.render(game.display)

    text(f"{game.player.coins_collected} coins collected", WHITE, 
         30, 100, 20, FONT, game.display)

    if game.player.state == "dead":
        text("Press r to replay", WHITE, 30, game.display.get_size()[0] / 2, 30, FONT, game.display)

    game.window.draw(main_surf = game.display, scale = 2);


def gameplay(game):
    game_events(game)
    game_update(game)
    game_render(game)
 


