import pygame as pg
import math, random

# a load lvl function which returns each line in the lvl file as a list
# and returns the whole lvl as a 2d list
def load_lvl(path):
    return [list(row) for row in open(path + ".txt", "r").read().split("\n")]

class level:
    def __init__(self, lvl_num, lvl_path, tile_size, tile_num, tiles):
        self.map_path = lvl_path
        self.lvls = []
        for i in range(0, lvl_num):
            self.lvls.append(load_lvl(lvl_path + str(i)))

        self.lvl_num = lvl_num
        self.rects = []
        self.current_lvl = 0
        self.tile_size = tile_size
        self.level_completed = 0
        self.score = 0
        self.lvl_load = 0
        ### save file
        ### if it exists it will be loaded in
        ### otherwise the corresponding values
        ### are set to 0 
        try:
            lvl_str = open(lvl_path + "save.txt", "r").read().split("\n")
            self.current_lvl = int(lvl_str[0]) - 1
            self.old_unlocked_lvl = self.current_lvl
            self.game_timer = int(lvl_str[1]) 
            try:
                self.prev_score = int(lvl_str[2])
            except Exception as e:
                self.prev_score = 0
            try:
                self.player_ability = int(lvl_str[3])
            except Exception as e:
                if self.current_lvl > 0:
                    self.player_ability = 1
                else:
                    self.player_ability = 0

        except Exception as e:
            self.current_lvl = 0
            self.old_unlocked_lvl = 0
            self.prev_score = 0
            self.game_timer = 0
            self.player_ability = 0
        
        # the 3 enemy images list which we choose
        # the different enemies from
        self.enemy_imgs = [pg.image.load("res/enemy.png").convert(),
                           pg.image.load("res/enemy_two.png").convert(),
                           pg.image.load("res/enemy_three.png").convert() ]

        # the boss image and other stuff
        self.boss_image = pg.transform.scale(pg.image.load("res/boss.png").convert(), (64, 64))
        self.boss_image.set_colorkey((0, 0, 0))
        self.boss = None
        self.boss_size = (64, 64)
        self.boss_dead = 0
        self.boss_fight = 0
        self.boss_hp = 100
        # used to add a delay to the boss's movement
        # to make it fair for the player
        self.frames_passed = 0
        self.saved_player_pos = []

        # transforming the size of the enemy images to 32x32
        # and also setting colorkey
        for i in range(0, len(self.enemy_imgs) - 1):
            self.enemy_imgs[i] = pg.transform.scale(self.enemy_imgs[i], tile_size)
            self.enemy_imgs[i].set_colorkey((0, 0, 0))
                
        # this is the list where all the enemies on a map 
        # are stored as well as the image they are
        self.enemies = []
        self.enemy_num = []

        ### tile images
        self.tiles = {}
        for i in range (0, tile_num):
            self.tiles[str(i)] = pg.image.load(tiles[str(i)]).convert()
            self.tiles[str(i)] = pg.transform.scale(self.tiles[str(i)], tile_size)

    # function that makes rect for each tile on the lvl, 
    # in our case we only need rects for the tiles that are
    # not 0, 2, 3, 4, 5, 6, 7, 9 and b
    # remember to call the get_player_pos function before
    # this one
    def get_rects(self):
        self.rects = []
        y = 0
        for row in self.lvls[self.current_lvl]:
            x = 0
            for tile in row:
                if tile != "0" and tile != "2" and tile != "3" and tile != "4" and tile != "5" and tile != "6" and tile != "7" and tile != "9" and tile != "b":
                    self.rects.append(pg.Rect(
                        x * self.tile_size[0],
                        y * self.tile_size[1],
                        self.tile_size[0],
                        self.tile_size[1]
                    ))

                if tile == "9":
                    self.enemies.append(pg.Rect(
                        x * self.tile_size[0],
                        y * self.tile_size[1],
                        self.tile_size[0],
                        self.tile_size[1]
                    ))
                    self.enemy_num.append(random.randint(0, len(self.enemy_imgs) - 1))
                    self.lvls[self.current_lvl][y][x] = "0"


                if tile == "b":
                    self.boss = pg.Rect(
                        x * self.tile_size[0],
                        y * self.tile_size[1] - 32,
                        self.boss_size[0],
                        self.boss_size[1]
                    )
                    self.lvls[self.current_lvl][y][x] = "0"

                x += 1
            y += 1

    # gets the position of the player on the current map
    # and then removes it from the map to prevent parsing
    # errors or rendering errors
    def get_player_pos(self):
        y = 0
        lvl_n = self.current_lvl
        if self.current_lvl >= self.lvl_num: lvl_n -= 1 
        for row in self.lvls[lvl_n]:
            x = 0
            for tile in row:
                if tile == "p":
                    self.lvls[lvl_n][y][x] = "0"
                    return (x * self.tile_size[0], y * self.tile_size[1])

                x += 1
            y += 1

    # checking collisions 
    # through adding the velocity of the player 
    # to one axis 
    # to find out more search SAT or Separating Axis Theorem
    def check_collisions(self, player):
        # checking if we are on the final level or not
        # and if the boss has been killed or not
        try:
            if self.current_lvl == self.lvl_num - 1 and not self.boss_dead:
                boss_dist_from_player = player.rect.x - self.boss.x
                # if the boss is alive and the distance 
                # between him and the player is less than
                # 7 * self.tile_size[0] or 7 * 32 pixels,
                # we have entered the boss fight phase
                if boss_dist_from_player < 4 * self.tile_size[0]:
                    self.boss_fight = 1
        except Exception as e:
            pass

        # just parsing through the enemies on a map
        # and checking for collisions 
        for i in self.enemies:
            s_coll = 0
            if player.bullet is not None:
                if i.colliderect(player.bullet):
                    idx = self.enemies.index(i)
                    self.enemies.remove(i)
                    self.enemy_num.pop(idx)
                    player.bullet = None
                    s_coll = 1
            if not s_coll:
                xdist_from_player = player.rect.x - i.x
                if abs(xdist_from_player) < 6 * self.tile_size[0]:
                    if xdist_from_player < 0 and player.rect.y == i.y:
                        i.x -= 1
                    if xdist_from_player > 0 and player.rect.y == i.y:
                        i.x += 1
                        
                    a_coll = 0
                    if i.colliderect(player.rect) and player.state == "attack": 
                        idx = self.enemies.index(i)
                        self.enemies.remove(i)
                        self.enemy_num.pop(idx)
                        a_coll = 1

                    if not a_coll and player.rect.y == i.y:
                        coll = 0
                        p_rect = None
                        if xdist_from_player < 0:
                            p_rect = pg.Rect(player.rect.x + 6, player.rect.y, 10, 16) 
                        if xdist_from_player > 0:
                            p_rect = pg.Rect(player.rect.x, player.rect.y, 10, 16) 

                        if i.colliderect(p_rect): 
                            coll = 1
                            player.health -= 1
                            if player.flipped:
                                player.vel[0] -= i.w * 1.25
                            if not player.flipped:
                                player.vel[0] += i.w * 1.25

                        if coll:
                            if player.flipped:
                                i.x += i.w * 1.25
                            else:
                                i.x -= i.w * 1.25


        ### checking for collisions with special 
        ### tiles, like spikes, lava, end tile
        ### and more 
        y = 0
        for row in self.lvls[self.current_lvl]:
            x = 0
            for tile in row:
                if tile == "3":
                    g_rect = pg.Rect(
                        x * self.tile_size[0],
                        y * self.tile_size[1],
                        self.tile_size[0],
                        1
                    )
                    if player.rect.colliderect(g_rect):
                        player.health -= 1
                        if player.flipped:
                            player.vel[0] -= 30
                        if not player.flipped:
                            player.vel[0] += 30
                         
                
                if tile == "4":
                    g_rect = pg.Rect(
                        x * self.tile_size[0],
                        y * self.tile_size[1],
                        self.tile_size[0],
                        self.tile_size[1]
                    )
                    if player.rect.colliderect(g_rect):
                        player.state = "dead"
                        # player.rect = player.orig_rect

                if tile == "6":
                    g_rect = pg.Rect(
                        x * self.tile_size[0],
                        y * self.tile_size[1],
                        self.tile_size[0],
                        self.tile_size[1]
                    )
                    if player.rect.colliderect(g_rect):
                        player.coins_collected += 1
                        tile = 0
                        self.lvls[self.current_lvl][y][x] = "0"
                        # player.rect = player.orig_rect

                if tile == "2":
                    g_rect = pg.Rect(
                        x * self.tile_size[0],
                        y * self.tile_size[1],
                        self.tile_size[0],
                        self.tile_size[1]
                    )
                    if player.rect.colliderect(g_rect):
                        tile = 0
                        self.lvls[self.current_lvl][y][x] = "0"
                        player.health += 1
                        # player.rect = player.orig_rect


                if tile == "7":
                    g_rect = pg.Rect(
                        x * self.tile_size[0],
                        y * self.tile_size[1],
                        self.tile_size[0],
                        self.tile_size[1]
                    )
                    if self.current_lvl != self.lvl_num - 1:
                        if player.rect.colliderect(g_rect):
                            player.rect = player.orig_rect
                            self.level_completed = 1
                    else:
                        if self.boss_dead:
                            if player.rect.colliderect(g_rect):
                                player.rect = player.orig_rect
                                self.level_completed = 1
 
                if tile == "5":
                    g_rect = pg.Rect(
                        x * self.tile_size[0],
                        y * self.tile_size[1],
                        self.tile_size[0],
                        self.tile_size[1]
                    )
                    if player.rect.colliderect(g_rect):
                        player.ability_unlocked = 1
                        self.lvls[self.current_lvl][y][x] = "0"
                        tile = 0

                x += 1
            y += 1
            # self.enemies.rect

        # the boss fight phase        
        if self.boss_fight:
            self.frames_passed += 1
            if self.frames_passed % 120 == 0:
                self.saved_player_pos = [player.rect.x, player.rect.y]
                self.frames_passed = 0
            try:
                xdist_from_player = self.saved_player_pos[0] - self.boss.x
                if xdist_from_player > 0:
                    self.boss.x += 1 
                if xdist_from_player < 0:
                    self.boss.x -= 1
            except Exception as e:
                pass    
            
        # checking collisions with tiles and boss
        self.get_rects()
        player.rect.x += player.vel[0]
        hit_list = [tile for tile in self.rects if player.rect.colliderect(tile)]
        for i in hit_list:
            if player.vel[0] < 0:
                player.rect.left = i.right 
                player.collision["left"] = 1

            if player.vel[0] > 0:
                player.rect.right = i.left 
                player.collision["right"] = 1
        
        if self.boss_fight and self.boss.colliderect(player.rect) and player.state != "attack":
            if not player.flipped:
                player.rect.x += 60
                self.boss.x -= 20
            if player.flipped:
                player.rect.x -= 60 
                self.boss.x += 20
            player.health -= 1

        if self.boss_fight and self.boss.colliderect(player.rect) and player.state == "attack":
            if not player.flipped:
                self.boss.x -= 20
            if player.flipped:
                self.boss.x += 20
            self.boss_hp -= 1

        player.vel[1] += player.y_momentum
        player.rect.y += player.vel[1]
        hit_list = [tile for tile in self.rects if player.rect.colliderect(tile)]
        for i in hit_list:
            if player.vel[1] < 0:
                player.rect.top = i.bottom
                player.collision["up"] = 1

            if player.vel[1] > 0:
                player.rect.bottom = i.top
                player.collision["down"] = 1

        if self.boss_fight and self.boss.colliderect(player.rect):
            if player.vel[1] < 0:
                player.rect.y += 60

        try:
            if self.boss_fight and self.boss.colliderect(player.bullet):
                self.boss_hp -= 5
                if player.bullet_vel[0] < 0:
                    self.boss.x -= 5
                if player.bullet_vel[0] > 0:
                    self.boss.x += 5
                player.bullet = None
        except Exception as e:
            pass

        if self.boss_hp <= 0:
            self.boss_dead = 1
       
        if self.boss_dead:
            self.boss_fight = 0
        
        # this is important as if we need to save the game,
        # we need to know if the player has his ability 
        # or not, if the ability is in the player class,
        # then we save it in the level class as well and
        # save it at the end.
        # The next time we load in, if the player doesn't
        # have the ability and the level class says the
        # player has the ability, then the player's ability
        # value is set to 1 or true
        if self.player_ability:
            player.ability_unlocked = 1
        if player.ability_unlocked:
            self.player_ability = 1

    # rendering is done here by looping through lvl file
    # and then checking the number and then rendering the 
    # corresponding image  
    def render(self, surf, scroll):
        y = 0
        for row in self.lvls[self.current_lvl]:
            x = 0
            for tile in row:
                if tile != "0":
                    rect = pg.Rect(
                        x * self.tile_size[0] - scroll[0],
                        y * self.tile_size[1] - scroll[1],
                        self.tile_size[0],
                        self.tile_size[1]
                    )
                    t = int(tile) - 1
                    if tile == "7":
                        if self.current_lvl != self.lvl_num - 1:
                            surf.blit(self.tiles[str(t)], rect)
                        else:
                            if self.boss_dead:
                                surf.blit(self.tiles[str(t)], rect)
                    else:
                        surf.blit(self.tiles[str(t)], rect)


                x += 1
            y += 1

        n = 0
        for i in self.enemies:
            n_rect = pg.Rect(i.x - scroll[0], i.y - scroll[1], 16, 16)
            surf.blit(self.enemy_imgs[self.enemy_num[n]], n_rect)
            n += 1

        # rendering the boss
        if self.current_lvl == self.lvl_num - 1 and not self.boss_dead:
            n_rect = pg.Rect(self.boss.x - scroll[0], self.boss.y - scroll[1], 64, 64)
            surf.blit(self.boss_image, n_rect)

        # rendering boss health
        if self.boss_fight and self.boss_hp:
            pg.draw.rect(surf, (20, 20, 25), pg.Rect(0, 0, surf.get_size()[0], surf.get_size()[1] / 4))
            pg.draw.rect(surf, (20, 20, 25), pg.Rect(0, surf.get_size()[1] - surf.get_size()[1] / 4, surf.get_size()[0], surf.get_size()[1] / 4))
            health = pg.Rect(surf.get_size()[0] / 2, 
                                 surf.get_size()[1] / 4, self.boss_hp, 5)
            health.x -= health.w / 2
            pg.draw.rect(surf, (200, 30, 170), health)

    # save function, 
    # just saves:
        # current or biggest unlocked level, game time, 
        # high score, ability unlocked or not 
    def save(self, path_file):
        save_f = open(path_file, "w")
        final_str = []
        lvl_n = 0
        if self.current_lvl > self.old_unlocked_lvl:
            final_str.append(str(self.current_lvl + 1) + "\n")
            lvl_n = self.current_lvl
        else:
            final_str.append(str(self.old_unlocked_lvl + 1) + "\n")
            lvl_n = self.old_unlocked_lvl

        final_str.append(str(int(self.game_timer)))
        final_str.append("\n")

        if self.prev_score > 0:
            final_str.append(str(self.prev_score))
        else:
            final_str.append(str(0))

        final_str.append("\n")
        final_str.append(str(self.player_ability))
        final_str.append("\n")
        save_f.write("".join(final_str))                    
        save_f.close()
