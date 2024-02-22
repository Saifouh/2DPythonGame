
TITLE = "Game"
WINDOW_SIZE = (1280, 720)
DISPLAY_SIZE = (640, 360)
DISPLAY_CENTER = (320, 180)


PLAYER_IMG_FOLDER = "res/player/"
PLAYER_STATES = 5
# The different player states and the number of 
# frames for each state animation
PLAYER_STATE_LIST = [("idle", 4), ("walk", 4), ("jump", 4), ("attack", 8), ("dead", 4)]
PLAYER_SIZE = (32, 32)

LVLS = 3
LVL_FOLDER = "res/lvls/"

TILE_SIZE = (32, 32)
TILE_NUMS = 7
TILES = {
        "0" : "res/tile.png",    ## normal tile
        "1" : "res/heart.png",    ## heart
        "2" : "res/spike.png",  ## spike
        "3" : "res/lava.png",   ## lava
        "4" : "res/mag.png",    ## ability unlock
        "5" : "res/coin.png",   ## coins 
        "6" : "res/end.png",   ## end tile 
}

