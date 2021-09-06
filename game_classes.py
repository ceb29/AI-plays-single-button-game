import pygame
import random
from pygame.constants import K_SPACE
import sprite_classes
from constants import *

class Game_Text():
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.text_list = []
        self.font = pygame.font.Font('freesansbold.ttf', 32) #font used for all text
        self.win = win
        self.score = 0
        self.high_score = 0
        self.game_over_width = (self.width/2) - 100
        self.game_over_height = (self.height/2) - 32
        self.score_padding = 125 
        self.high_score_padding = 200
        self.score_pad_num = 10
        self.high_score_pad_num = 10

    def get_score(self):
        return self.score

    def get_high_score(self):
        return self.high_score

    def set_score(self, score):
        self.score = score

    def set_high_score(self, high_score):
        self.high_score = high_score

    #add spacing to keep numbers from overflowing onto text 
    def padding(self):
        if self.score / self.score_pad_num == 1:
            self.score_padding += 10
            self.score_pad_num *= 10

        if self.high_score / self.high_score_pad_num == 1:
            self.high_score_padding += 10
            self.high_score_pad_num *= 10

    #update score text and check if there is a new high score
    def update_score(self):
        self.padding()
        if self.score > self.high_score:
            self.high_score = self.score
        self.text_list[3] = self.font.render(str(self.score), False, COLOR_WHITE)
        self.text_list[4] = self.font.render(str(self.high_score), False, COLOR_WHITE)

    #create the text for pygame and make a list to hold them   
    def create_text(self):
        text_score = self.font.render('Score:', False, COLOR_WHITE)
        text_game_over = self.font.render('Game Over', False, COLOR_WHITE)
        text_high_score = self.font.render('High Score:', False, COLOR_WHITE)
        score = self.font.render(str(self.score), False, COLOR_WHITE)
        high_score = self.font.render(str(self.high_score), False, COLOR_WHITE)
        self.text_list = [text_score, text_game_over, text_high_score, score, high_score]  

    #functions for displaying text
    def display_score(self):
        self.win.blit(self.text_list[0], (5, 10)) #text_score
        self.win.blit(self.text_list[2], (5, HEIGHT - 40))  #text_high_score
        self.win.blit(self.text_list[3], (self.score_padding, 10))  #score
        self.win.blit(self.text_list[4], (self.high_score_padding, HEIGHT - 40))  #high_score

    def display_game_over(self):
        self.win.blit(self.text_list[1], (self.game_over_width, self.game_over_height)) #text_game_over

    #always display score and high score, if game status is 1 display game over and stop updating score
    def update_text(self, game_status):
        if game_status == 0:
            self.update_score()   
        elif game_status == 1:
            self.display_game_over()
        self.display_score()

class Game():
    def __init__(self, clock_speed, rgb_tuple, win, width, height):
        self.width = width
        self.height = height
        self.win = win
        self.text = Game_Text(win, width, height)
        self.game_status = 0
        self.player_start = [width/4, height/2 + 300]
        self.background = sprite_classes.Background(width, height, [width/2, height/2], "images/background.png", COLOR_WHITE)
        self.walls = pygame.sprite.Group()
        self.top_walls = pygame.sprite.Group()
        self.bottom_walls = pygame.sprite.Group()
        self.smoke = pygame.sprite.Group()
        self.surfaces = pygame.sprite.Group()
        self.closest_wall_top = [0, 0]
        self.closest_wall_bottom = [0, 0]
        self.clock = pygame.time.Clock()
        self.clock_speed = clock_speed
        self.win_rgb = rgb_tuple
        self.last_top = 0
        self.last_bottom = 0
        self.players = []
        self.genomes = []
        self.nets = []
        self.wall_top_list = []
        self.wall_bottom_list = []
        self.start_points_flag = 0

    def get_status(self):
        return self.game_status

    def get_max_point(self):
        return self.max_point

    #function for genome input/output 
    def update_genome(self):
        for i in range(len(self.players)):
            collision_top = 0
            collision_bottom = 0
            player_top = self.players[i].get_center_y() - 30
            player_bottom = self.players[i].get_center_y() + 30
            if player_top < self.closest_wall_top[1]:
                collision_top = 1
            if player_bottom > self.closest_wall_bottom[1]:
                collision_bottom = 1
            output = self.nets[i].activate((self.players[i].get_center_y(),
                                            self.players[i].get_speed_y(),
                                            collision_top,
                                            collision_bottom,
                                            self.closest_wall_top[1],
                                            self.closest_wall_bottom[1]))      
            if output[0] > 0.5:
                self.players[i].set_n(1)
            else:
                self.players[i].set_n(0)

    #functions for game progression
    def start(self):
        self.add_sprites()
        self.create_walls()
        self.read_high_score()
        self.text.create_text()
 
    #draw all surfaces on screen
    def draw_surfaces(self):
        for s in self.surfaces:
            self.win.blit(s.surf1, s.rect)
    
    #update all sprite positions
    def update_sprite_pos(self):
        for i in range(len(self.players)):
            self.players[i].update()
        for smoke in self.smoke:
            smoke.update()
        self.walls.update()
    
    def update_closest_wall(self):
        self.closest_wall_top = (self.closest_wall_top[0] - 1, self.closest_wall_top[1])
        self.closest_wall_bottom = (self.closest_wall_bottom[0] - 1, self.closest_wall_bottom[1])
        for i in range (len(self.wall_top_list)):
            self.wall_top_list[i] = [self.wall_top_list[i][0] - 1, self.wall_top_list[i][1]]
            self.wall_bottom_list[i] = [self.wall_bottom_list[i][0] - 1, self.wall_bottom_list[i][1]]

    #main game function
    def update(self):
        self.win.fill(self.win_rgb)
        self.draw_surfaces()
        self.text.update_text(self.game_status)
        self.update_genome()
        self.update_sprite_pos()
        self.wall_out_bounds()
        self.add_point()
        self.check_for_collisions()
        self.update_closest_wall()
        pygame.display.flip()
        self.clock.tick_busy_loop(self.clock_speed) 

    #functions for adding sprites
    def add_player(self):
        for player in self.players:
            self.surfaces.add(player)

    def add_sprites(self):
        self.surfaces.add(self.background)
        self.add_player()

    def add_new_wall(self, centerx, centery):
        wall = sprite_classes.Wall(self.width, self.height, [centerx, centery], "images\wall.png")
        self.walls.add(wall)
        self.surfaces.add(wall)
        return wall

    def add_top_wall(self, centerx, top_rand_int):
        centery = self.height / 2 - top_rand_int
        if centery + 100 > self.last_bottom:
            centery = self.last_bottom - 200
        wall = self.add_new_wall(centerx, centery)
        self.top_walls.add(wall)
        self.wall_top_list.append([wall.get_center_x(), wall.get_center_y() + 470])
        return centery

    def add_bottom_wall(self, centerx, centery, top_rand_int):
        a = centery + 970 + 50
        b = 800 - (970 - top_rand_int)
        centery = random.randint(a, a + b)
        if centery - 100 < self.last_top:
            centery = self.last_top + 200
        wall = self.add_new_wall(centerx, centery)
        self.bottom_walls.add(wall)
        self.wall_bottom_list.append([wall.get_center_x(), wall.get_center_y() - 470])
        return centery
        
    def add_walls(self, centerx):
        top_rand_int = random.randint(250, 850)
        top_centery = self.add_top_wall(centerx, top_rand_int)
        bottom_centery = self.add_bottom_wall(centerx, top_centery, top_rand_int)
        self.last_top = top_centery + WALL_HEIGHT
        self.last_bottom = bottom_centery - WALL_HEIGHT

    def add_smoke(self, center):
        rand_x = random.randint(-5, 5)
        rand_y = random.randint(-5, 5)
        smoke = sprite_classes.Smoke(self.width, self.height, [center[0] + rand_x, center[1] + 25 + rand_y], "images/smoke.png")
        self.smoke.add(smoke)
        self.surfaces.add(smoke)

    #create initial walls at the start of each game 
    def create_walls(self):
        centerx =  WALL_WIDTH/2 + WALL_WIDTH * 4 #wall offset
        number_of_walls = 13
        flag = 0
        for i in range(number_of_walls):
            self.add_walls(centerx)
            centerx += WALL_WIDTH
        for wall in self.top_walls:
            if flag == 0:
                self.closest_wall_top = (wall.get_center_x(), wall.get_center_y() - 470)
                flag = 1
        flag = 0
        for wall in self.bottom_walls:
            if flag == 0:
                self.closest_wall_bottom = (wall.get_center_x(), wall.get_center_y() + 470)
    
    #add point when player passes a wall
    def add_point(self):
        for wall in self.top_walls:
            if wall.get_center_x() + WALL_WIDTH/2 <= self.player_start[0] and wall.get_score_flag() == 0:
                self.text.set_score(self.text.get_score() + 1)
                self.text.update_score()
                wall.set_score_flag(1)
                self.start_points_flag == 1
                for i in  range(len(self.players)):
                    if self.players[i].collision_flag == 0:
                        self.genomes[i].fitness += 1

    #draw a line at the center of the next top and bottom walls
    def draw_center_line(self):
        wall_distance = self.closest_wall_bottom - self.closest_wall_top
        self.background.clear()
        pygame.draw.line(self.background.surf1, COLOR_WHITE, (self.player_start[0] + 48, self.closest_wall_top[1] + wall_distance/2), (self.player_start[0], self.closest_wall_top[1] + wall_distance/2), 3)
        
    #if wall passes left side of screen delete it and add a new wall to the right side of the screen
    def wall_out_bounds(self):
        for wall in self.top_walls:
            if wall.get_center_x() - 48 <= 0 and wall.get_flag() == 0:
                self.wall_top_list.pop(0)
                self.wall_bottom_list.pop(0)
                self.add_walls(self.width + WALL_WIDTH  - 1)
                wall.set_flag(1)
            if wall.get_center_x() + WALL_WIDTH/2 <= 0:
                wall.kill()
            if wall.get_center_x() < self.player_start[0] + WALL_WIDTH + WALL_WIDTH/2 and wall.get_flag_player() == 0:
                wall.set_flag_player(1)
                self.closest_wall_top = (wall.get_center_x(), wall.get_center_y() + 470)  
        for wall in self.bottom_walls:
            if wall.get_center_x() < self.player_start[0] + WALL_WIDTH + WALL_WIDTH/2 and wall.get_flag_player() == 0:
                wall.set_flag_player(1)
                self.closest_wall_bottom = (wall.get_center_x(), wall.get_center_y() - 470)

    #functions for collisions
    def wall_collisions(self, player):
        collision = pygame.sprite.spritecollideany(player, self.walls, collided=pygame.sprite.collide_mask)
        if collision != None:
            return 1

    def player_out_of_bounds(self, player):
        if player.get_center_y() > self.height + 30 or player.get_center_y() < - 30:
            return 1

    def smoke_on_collision(self, center):
        for i in range(5):
            self.add_smoke(center)

    def check_for_collisions(self):
        list1 = []
        for i in  range(len(self.players)):
            self.players[i].collision_flag = 0
            if self.player_out_of_bounds(self.players[i]) == 1 or self.wall_collisions(self.players[i]) == 1:
                self.smoke_on_collision(self.players[i].get_center())
                self.players[i].kill()
                self.players[i].collision_flag = 1
                list1.append(i)
                self.genomes[i].fitness -= 1     
        if len(list1) > 0:
            for i in range(len(list1)):
                n = list1[len(list1) - i - 1]
                self.players.pop(n)
                self.genomes.pop(n)
                self.nets.pop(n)

#functions for high score
    def read_high_score(self):
        high_score_file = open('./high_score.txt', "r")
        self.text.set_high_score(int(high_score_file.read()))
        high_score_file.close()

    def write_high_score(self):
        high_score_file = open('./high_score.txt', "w")
        high_score_file.write(str(self.text.get_high_score()))
        high_score_file.close()