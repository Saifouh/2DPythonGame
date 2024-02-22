from copy import copy
import pygame as pg
import sys

### add double jump
class player:
    def __init__(self, pos, img_folder, state_num, states_list, size):
        ## physics
        self.moving = {
            "right" : 0,
            "left"  : 0,
            "up"    : 0,
            "down"  : 0
        }
        self.collision = {
            "right" : 0,
            "left"  : 0,
            "up"    : 0,
            "down"  : 0
        }
        self.vel = [0, 0]
        self.air_timer = 0
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.orig_rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.y_momentum = 0

        ## camera
        self.scroll = [0, 0]
        self.true_scroll = [0.0, 0.0]

        ## animation
        ## we use a dictionary to store the images for each
        ## state
        self.animated_imgs = {}
        for i in range(0, state_num):
            self.animated_imgs[states_list[i][0]] = [] 
            for n in range(0, states_list[i][1]):
                img = pg.image.load(img_folder + states_list[i][0] + "/" + str(n) + ".png").convert_alpha()
                img = pg.transform.scale(img, size)
                self.animated_imgs[states_list[i][0]].append(img)


        self.current_img = None
        self.state = "idle"
        self.health_img = pg.image.load(img_folder + "heart.png").convert_alpha()
        self.health_img.set_colorkey((0, 0, 0))
        self.health_img = pg.transform.scale(self.health_img, (20, 20))
        self.health_img.set_colorkey((0, 0, 0))
        self.coins_collected = 0
        self.health = 4
        self.frames_passed = 0
        self.current_frame = 0
        self.flipped = 0
        self.ability_unlocked = 0
        self.bullet = None
        self.bullet_vel = []
        self.bullet_cooldown = 0.0
             
    def calc_scroll(self):
        # how this works is that we take half of the display surface size
        # which is 320 since the actual width is 640 and the height 180 
        # since actual height is 360. Then we add half the width and height of the
        # player which is 16 pixels and we have the camera centering the player
        # in the screen
        self.true_scroll[0] += (self.rect.x - self.true_scroll[0] - 320 + 8*2) / 10
        self.true_scroll[1] += (self.rect.y - self.true_scroll[1] - 180 + 8*2) / 10
        self.scroll = [int(self.true_scroll[0]), int(self.true_scroll[1])]


    # resetting the velocity of the player every frame
    def reset_val(self):
        self.vel = [0, 0]
        self.collision = {
            "right" : 0,
            "left"  : 0,
            "up"    : 0,
            "down"  : 0
        }

    def handle_events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_d:
                    self.moving["right"] = 1

                if e.key == pg.K_a:
                    self.moving["left"] = 1

                if e.key == pg.K_SPACE and self.air_timer < 5 and self.state != "dead":
                    self.y_momentum = -6

                if e.key == pg.K_r and self.state == "dead":
                    self.health = 4
                    self.state = "idle"
                    self.rect.x = self.orig_rect.x 
                    self.rect.y = self.orig_rect.y 

                if e.key == pg.K_e and self.state != "dead":
                    self.state = "attack"
                    self.frames_passed = 0
                    self.current_frame = 0

                if e.key == pg.K_f and self.ability_unlocked and self.bullet_cooldown <= 0:
                    if self.flipped:
                        self.bullet_vel = [5, 0]
                    else:
                        self.bullet_vel = [-5, 0]
                    self.bullet = pg.Rect(self.rect.x, self.rect.y + self.rect.h / 2, 10, 5)
                    self.bullet_cooldown = 4.0

            if e.type == pg.KEYUP:
                if e.key == pg.K_d:
                    self.moving["right"] = 0

                if e.key == pg.K_a:
                    self.moving["left"] = 0

    def update(self):
        # physics and game logic handling
        if self.health <= 0:
            self.state = "dead"
        
        self.y_momentum += 0.25
        if self.y_momentum >= 3:
            self.y_momentum = 3

        if self.collision["down"]:
            self.y_momentum = 0
            self.air_timer = 0
        
        if not self.collision["down"] and self.vel[1] != 0:
            self.air_timer += 0.25

        if self.collision["up"]:
            self.y_momentum += 1

        if self.state != "dead" and self.state != "attack":
            # if velocity is less than 0, it means walking left
            if self.vel[0] < 0:
                self.state = "walk"
                self.flipped = 0

            # if velocity is more than 0, it means walking right
            if self.vel[0] > 0:
                self.state = "walk"
                self.flipped = 1

            # if air timer is more than 0.75 and y vel is not 0 then state is jump
            if self.air_timer > 0.75 and self.vel[1] != 0:
                self.state = "jump"

            # if all velocity val are 0, then idle
            if self.vel[0] == 0 and self.vel[1] == 0:
                self.state = "idle"

        if self.state != "attack":
            self.frames_passed += 1

        if self.state == "attack":
            self.frames_passed += 5

        # the animation runs at 1 frame every 15 frames
        if self.frames_passed % 15 == 0:
            self.frames_passed = 0
            if self.current_frame < len(self.animated_imgs[self.state]) - 1:
                self.current_frame += 1
            else:
                if self.state != "dead":
                    self.current_frame = 0
                if self.state == "attack":
                    self.state = "idle"
                    self.current_frame = 0


        if self.bullet != None:
            self.bullet.x += self.bullet_vel[0]
            self.bullet.y += self.bullet_vel[1]

        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 0.05
        if self.bullet_cooldown < 0:
            self.bullet_cooldown = 0
        
  
    def render(self, surf):
        self.current_img = (self.animated_imgs[self.state][self.current_frame])
        self.current_img = pg.transform.flip(self.current_img, self.flipped, 0)
        r = pg.Rect(self.rect.x - self.scroll[0], self.rect.y - self.scroll[1], self.rect.w, self.rect.h)
        surf.blit(self.current_img, r)

        # updating the bullet
        # just a note that whenever you are drawing 
        # something that needs to be moving with
        # the player camera, you need to subtract
        # the scroll
        if self.bullet is not None:
            n = copy(self.bullet)
            n.x -= self.scroll[0]
            n.y -= self.scroll[1]
            pg.draw.rect(surf, (128, 150, 170), n)

        x = 20
        y = 35
        for i in range(0, self.health):
            surf.blit(self.health_img, (x, y))
            x += 35

