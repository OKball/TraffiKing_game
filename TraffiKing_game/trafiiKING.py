import pygame
from sys import exit
import random
import time
import json



class Player(pygame.sprite.Sprite):

    def __init__(self, name):
        """initializes playes"""
        super().__init__()
        self.name = name
        self.image = pygame.image.load('resources/car.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (90,90))
        self.rect = self.image.get_bounding_rect()
        self.image = self.image.subsurface(self.rect)
        self.topspeed = 600
        self.speedadd = 200
        self.speed_x = 0
        self.speed_y = 0
        self.drag_applier = 2
        self.drag_x = 0
        self.drag_y = 0
        self.grass_drag = 4
        self.pos_x = 600 - (self.rect.width / 2)
        self.pos_y = 600
        self.rect.y = self.pos_y
        self.rect.x = self.pos_x
        self.score = 0


    def scoring(self, point):
        """scoring mechanics"""
        self.point = point
        self.score += self.point
        self.point = 0


    def player_input(self):
        """checks user input, and changes values of moving speed"""

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0 and self.speed_y > -600 * dt:
            self.speed_y -= self.speedadd * dt
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < 700 and self.speed_y > -600 * dt:
            self.speed_y += self.speedadd * dt
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.x > 0 and self.speed_x > -550 * dt:
            self.speed_x -= self.speedadd * dt
        if (keys[pygame.K_d]  or keys[pygame.K_RIGHT]) and self.rect.x < 1155 and self.speed_x < 550 * dt:
            self.speed_x += self.speedadd * dt



    def movement(self):
        """Calculates movement and direction"""
        
        #speed boundries
        if self.speed_y > self.topspeed * dt:
            self.speed_y = self.topspeed * dt
        elif self.speed_y < -self.topspeed * dt:
            self.speed_y = -self.topspeed * dt
        if self.speed_x > self.topspeed * dt:
            self.speed_x = self.topspeed * dt
        elif self.speed_x < -self.topspeed * dt:
            self.speed_x = -self.topspeed * dt

        #screen boundry
        if self.rect.y <= -1:
            self.rect.y = 0
            self.pos_y = self.rect.y
            self.speed_y = 0
        if self.rect.y >= 701 - self.rect.height:
            self.rect.y = 700 - self.rect.height
            self.pos_y = self.rect.y
            self.speed_y = 0

        if self.rect.x <= -1:
            self.rect.x = 0 
            self.pos_x = self.rect.x
            self.speed_x = 0
        if self.rect.x >= 1156:
            self.rect.x = 1155
            self.pos_x = self.rect.x
            self.speed_x = 0

        #applying drag
        #X
        if self.speed_x > self.drag_applier * dt * TARGET_FPS:
                self.drag_x = -self.drag_applier * dt * TARGET_FPS
        elif 0 < self.speed_x < (self.drag_applier / 2) * dt * TARGET_FPS:
            self.drag_x = 0
            self.speed_x = 0
        if self.speed_x <  -self.drag_applier * dt * TARGET_FPS:
                self.drag_x = self.drag_applier * dt * TARGET_FPS
        elif 0 > self.speed_x > (-self.drag_applier / 2) * dt * TARGET_FPS:
            self.drag_x = 0
            self.speed_x = 0

        #Y        
        if self.speed_y > self.drag_applier * dt * TARGET_FPS:
                self.drag_y = -self.drag_applier * dt * TARGET_FPS
        elif 0 < self.speed_y < (self.drag_applier / 2) * dt * TARGET_FPS:
            self.drag_y = 0
            self.speed_y = 0
        if self.speed_y <  -self.drag_applier * dt * TARGET_FPS:
                self.drag_y = self.drag_applier * dt * TARGET_FPS
        elif 0 > self.speed_y > (-self.drag_applier / 2) * dt * TARGET_FPS:
            self.drag_y = 0
            self.speed_y = 0

       
 
        #checking road boundries and aplying drag
        if (1100 - (self.rect.width/2) < self.rect.x or self.rect.x < 100 - (self.rect.width/2)) and (self.rect.y < 701 - self.rect.height):
            self.speed_y += self.grass_drag * dt * TARGET_FPS
        


        self.speed_x += self.drag_x 
        self.speed_y += self.drag_y

        self.pos_x += self.speed_x 
        self.pos_y += self.speed_y 

        #passes actual values to drawing board
        self.rect.y = self.pos_y
        self.rect.x = self.pos_x


    def skin_update(self):
        if skins.skin_picked == 0:
            pass
        else:
            self.image = skins.skin_picked
            if skins.chosen == 3:
                self.image = pygame.transform.scale(self.image, (200,200))
            else:
                self.image = pygame.transform.scale(self.image, (90,90))
            self.rect = self.image.get_bounding_rect()
            self.image = self.image.subsurface(self.rect)

    
    def update(self):
        """calls all class methods"""
        self.player_input()
        self.movement()



    
    def clean(self):
        self.speed_x = 0
        self.speed_y = 0
        self.drag_applier = 2
        self.drag_x = 0
        self.drag_y = 0
        self.grass_drag = 4
        self.pos_x = 600 - (self.rect.width / 2)
        self.pos_y = 600
        self.rect.y = self.pos_y
        self.rect.x = self.pos_x
        self.score = 0
        
class Obstacle(pygame.sprite.Sprite):
    
    def __init__(self, type, direction, multiplier):
        super().__init__()
        self.direction = direction
        self.type = type
        self.pos_y = 0
        
        self.speed = 0
        self.multiplier = multiplier                      # speed point how fast object is falling, so the bigger the speed, the slower object seems to move
        self.spawn_possibilites = available_positions.current_possibilities
        self.random_centerline_offset = random.randint(-20, 20)
        

        if self.type == "truck":
            if self.direction == "up":
                self.speed = 10
            else:
                self.speed = 15
        elif self.type == "police":
            if self.direction == "up":
                self.speed = 1
            else:
                self.speed = 30
        elif self.type == "randomcar1":
            if self.direction == "up":
                self.speed = 4
            else:
                self.speed = 25
        elif self.type == "randomcar2":
            if self.direction == "up":
                self.speed = 5
            else:
                self.speed = 20
        else:
            if self.direction == "up":
                self.speed = 9
            else: 
                self.speed = 16

        if self.type == "truck":
            self.image = pygame.image.load("resources/truck1.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (200,200))
            self.speed *= self.multiplier
            
        elif self.type == "police":
            self.image = pygame.image.load("resources/police11.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (90,90))
            self.speed *= self.multiplier
        
        elif self.type == "randomcar1":
            self.image = pygame.image.load("resources/car21.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (90,90))
            self.speed *= self.multiplier

        elif self.type == "randomcar2":
            self.image = pygame.image.load("resources/car31.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (90,90))
            self.speed *= self.multiplier
        else: 
            self.image = pygame.image.load("resources/car41.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (90,90))
            self.speed *= self.multiplier

        self.rect = self.image.get_bounding_rect()
        self.image = self.image.subsurface(self.rect)

        
        if self.direction == "up":
            self.random_number = random.randint(0,len(self.spawn_possibilites[1]) - 1)
            self.rect.x = self.spawn_possibilites[1][self.random_number] + self.random_centerline_offset
            available_positions.update(1, self.random_number)
            self.rect.y = -500
            self.pos_y = self.rect.y
            self.obst_checker = Obstacle_checker(self.rect.x, self.rect.bottom, self.rect.width, self.speed)
            self.obst_checker.add(obstacle_checker_group)


        else:

            self.image = pygame.transform.rotate(self.image, 180)
            self.rect.x = self.spawn_possibilites[0][random.randint(0,4)] + self.random_centerline_offset
            self.rect.y = -500
            self.pos_y = self.rect.y
            self.obst_checker = Obstacle_checker(self.rect.x, self.rect.top, self.rect.width, self.speed)
            self.obst_checker.add(obstacle_checker_group)



   
    def movement(self):
       
        #right side
        if self.direction == "up":
            self.pos_y += self.speed * dt * 60
        #left side
        else:
            self.pos_y +=  self.speed  * dt * 60
            pass

        self.rect.y = self.pos_y

    def update(self):
        self.movement()
        self.destroy()
        self.obst_checker.update(self.rect.x, self.pos_y + self.rect.height, self.speed)

    def destroy(self):
        if self.rect.top >= 800: 
            self.kill()
            self.obst_checker.kill()
            Player.scoring(jimmy, 1)
    
    def clean(self):
        self.kill()
        self.obst_checker.kill()

class Obstacle_checker(pygame.sprite.Sprite):
    """Checks if obstacles collide with eachother, by creating rect behind them looking if something is in this rectangle"""
    def __init__(self, pos_x, pos_y, width, speed) -> None:
        super().__init__()
        self.speed = speed
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = pygame.rect.Rect(self.pos_x, self.pos_y, width, 20)
        
    
    def update(self, new_x, new_y, new_speed):
        self.speed = new_speed
        self.pos_x = new_x
        self.pos_y = new_y
        self.rect.topleft = (new_x, new_y + 1)

class Spawner():
    """handles type and desity of spawning cars, also speed of traffic"""
    def __init__(self) -> None:
        self.timer = 0
        self.timer2 = 0
        self.traffic_density = 0.05
        self.traffic_speed = 1
        self.available_types = ["truck", "randomcar1", "randomcar2", "randomcar3"] 
        self.background_image_position_y_speed = 20
        self.speedometer_timer = 0
        

    def spawner_update(self):
        self.timer += 1 * dt * TARGET_FPS + self.traffic_density
        if self.speedometer_timer < 4100:
            self.speedometer_timer += 1 * dt * TARGET_FPS
        self.random_pick = self.available_types[random.randint(0, len(self.available_types)-1)]
        self.background_image_position_y_speed = 20 * self.traffic_speed
        if (self.timer / 60) > 1:
            self.timer = 0
            self.timer2 += 1
            obstacle_group.add(Obstacle(self.random_pick, "up", self.traffic_speed))
            if (self.timer2/4) > 1:
                self.timer2 = 0
                if self.traffic_density < 6:
                    self.traffic_density += 0.05
                    self.traffic_density = round(self.traffic_density, 3)
                if self.traffic_speed < 3:
                    self.traffic_speed += 0.05
                    self.traffic_speed = round(self.traffic_speed, 3)
                obstacle_group.add(Obstacle(self.random_pick, "down", self.traffic_speed))

    def clean(self):
        self.timer = 0
        self.timer2 = 0
        self.traffic_density = 0.05
        self.traffic_speed = 1
        self.background_image_position_y_speed = 20
        self.speedometer_timer = 0

class Retry_screen_text():
    def __init__(self) -> None:
        self.font_size = 52
        self.font = pygame.font.Font("resources/Extrude.ttf", self.font_size)
        self.big_font = pygame.font.Font("resources/Extrude.ttf", 120)
        self.color = (255,255,255)
        self.press_text = self.font.render("press", True, self.color)
        self.restart_text = self.font.render("to restart", True, self.color)
        self.spacebar_text = self.font.render("SPACEBAR", True, (255,255,255))
        self.esc_text = self.font.render("ESC", True, (255,255,255))
        self.menu_text = self.font.render("for Menu", True, self.color)
        self.save_result_text = self.font.render("TYPE IN YOUR USERNAME", True, (255,250,100))
        self.high_score_text = self.font.render("New Highscore!", True, (255,250,100))
        self.user_text = ''
        self.timer = 255
        self.retry_text_start_x = 255
        self.esc_text_start_x = 360
        self.menu_text_y = 650
        self.esc_text_y = 750

    def retry_text_update(self):
        self.timer -= 1
        self.color = (255,self.timer,self.timer)
        if self.timer <= 0:
            self.timer = 255
        self.font = pygame.font.Font("resources/Extrude.ttf", self.font_size)
        self.press_text = self.font.render("press", True, self.color)
        self.restart_text = self.font.render("to Restart", True, self.color)
        self.menu_text = self.font.render("for Menu", True, self.color)
        score_text = self.big_font.render(f"SCORE: {jimmy.score}", True, (100,0,255))

        screen.blit(self.press_text, (self.retry_text_start_x ,self.menu_text_y))
        screen.blit(self.spacebar_text, (self.retry_text_start_x + self.press_text.get_width() + 5 ,self.menu_text_y))
        screen.blit(self.restart_text, (self.retry_text_start_x + self.press_text.get_width() + self.spacebar_text.get_width() + 10 ,self.menu_text_y))

        screen.blit(self.press_text, (self.esc_text_start_x ,self.esc_text_y))
        screen.blit(self.esc_text, (self.esc_text_start_x + self.press_text.get_width() + 5 ,self.esc_text_y))
        screen.blit(self.menu_text, (self.esc_text_start_x + self.press_text.get_width() + self.esc_text.get_width() + 10 ,self.esc_text_y))

        screen.blit(score_text, (200,100))

        if leaderboard.check_score(jimmy.score):              
            text_surface = self.big_font.render(self.user_text, True, (255,255,255))
            screen.blit(text_surface, (400, 400))
            screen.blit(self.high_score_text, (230, 200))
            screen.blit(self.save_result_text, (255, 300))

class Intro_animation():
    """hanldes intro animation"""
    def __init__(self) -> None:
        self.intro_alpha = 0
        self.intro_image = pygame.image.load("resources/main_menu_image1.png").convert_alpha()
        self.intro_image.set_alpha(self.intro_alpha)
        self.intro_image = pygame.transform.scale(self.intro_image, (800,400))
        self.background_alpha = 0
        self.background_image = pygame.image.load("resources/roads_blur_2.png").convert_alpha()
        self.background_image.set_alpha(self.background_alpha)
        self.background_image = pygame.transform.scale(background_image, (1200,800))
        self.intro_position_y = 200
        self.finished = 0

    def intro_update(self):
        if self.intro_alpha < 1000:
            screen.fill((0,0,0))
            self.intro_alpha += 1
            self.intro_image.set_alpha(self.intro_alpha)
            screen.blit(self.intro_image, (200,200))

        if self.intro_alpha >= 900 and self.background_alpha < 100:
            if self.background_alpha < 30:
                self.background_alpha += 0.06
            else:
                self.background_alpha += 1
            self.background_image.set_alpha(self.background_alpha)
            screen.blit(self.background_image, (0,0))
            screen.blit(self.intro_image, (200,200))


        if self.background_alpha >= 100 and self.intro_position_y > 70:
            self.intro_position_y -= 1
            screen.blit(self.background_image, (0,0))
            screen.blit(self.intro_image, (200, self.intro_position_y))
            if self.intro_position_y == 70:
                self.finished = 1

        if self.finished == 1:
            return False

class Main_menu():
    def __init__(self) -> None:
        self.image = pygame.image.load("resources/main_menu_image1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (800,400))
        self.background_image = pygame.image.load("resources/roads_blur_2.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (1200,800))
        self.font_size = 52
        self.font = pygame.font.Font("resources/Extrude.ttf", self.font_size)
        self.color = (255,250,100)
        self.start_button = self.font.render("Start", True, self.color)
        self.skin_button = self.font.render("Skin", True, self.color)
        self.leader_button = self.font.render("Leaderboard", True, self.color)
        self.exit_button = self.font.render("Exit", True, self.color)
        self.pos_start = 430
        self.pos_skin = 530
        self.pos_leaderboard = 630
        self.pos_exit = 730
        self.index = 0
        self.pointer = pygame.image.load("resources/police11.png").convert_alpha()
        self.pointer = pygame.transform.scale(self.pointer, (60,60))
        self.pointer = pygame.transform.rotate(self.pointer, 90)
        self.pointer_x = 1000
        self.pointer_y = 0
        self.timer = 0
        self.timer_button = 0
    
    def update_menu(self):
        if 80 > self.timer_button > 0:
            self.timer_button += 1
        else:
            self.timer_button = 0

        if self.timer < 255:
            self.timer += 1
        screen.blit(self.background_image, (0,0))
        screen.blit(self.image, (200, 70))
        self.start_button.set_alpha(self.timer)
        self.skin_button.set_alpha(self.timer)
        self.leader_button.set_alpha(self.timer)
        self.exit_button.set_alpha(self.timer)
        screen.blit(self.start_button, (530, self.pos_start))
        screen.blit(self.skin_button, (550, self.pos_skin))
        screen.blit(self.leader_button, (430, self.pos_leaderboard))
        screen.blit(self.exit_button, (550, self.pos_exit))
        if self.timer > 254:
            if self.timer_button == 0:
                if pygame.key.get_pressed()[pygame.K_UP] == True:
                    self.index -= 1
                    self.timer_button += 1
                    
                elif pygame.key.get_pressed()[pygame.K_DOWN] == True:
                    self.index += 1
                    self.timer_button += 1


                elif (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_RETURN]) == True and self.index == 1:
                    return 1
                elif (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_RETURN]) == True and self.index == 2:
                    return 2
                elif (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_RETURN]) == True and self.index == 3:
                    return 3
                elif (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_RETURN]) == True and self.index == 4:
                    with open("resources/leaderboard.json", 'r', encoding="utf-8") as score_list:
                        backup = json.load(score_list)

                    with open("resources/leaderboard_backup.json", 'w', encoding="utf-8") as score_list:
                        json.dump(backup, score_list)

                    pygame.quit()
                    exit()
                    

            if self.index > 4:
                self.index = 1
            elif self.index < 1:
                self.index = 4

            if self.index == 1:
                screen.blit(self.pointer, (720, self.pos_start))
            elif self.index == 2:
                screen.blit(self.pointer, (700, self.pos_skin))
            elif self.index == 3:
                screen.blit(self.pointer, (800, self.pos_leaderboard))
            elif self.index == 4:
                screen.blit(self.pointer, (700, self.pos_exit))

class Skin_pick():
    def __init__(self):
        self.background_image = pygame.image.load("resources/roads_blur_2.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (1200,800))
        self.image_size = 200
        self.skin1_image = pygame.image.load("resources/car.png").convert_alpha()
        self.skin1_image = pygame.transform.scale(self.skin1_image, (self.image_size,self.image_size))
        self.skin2_image = pygame.image.load("resources/police11.png").convert_alpha()
        self.skin2_image = pygame.transform.scale(self.skin2_image, (self.image_size,self.image_size))
        self.skin3_image = pygame.image.load("resources/truck2.png").convert_alpha()
        self.skin3_image = pygame.transform.scale(self.skin3_image, (self.image_size * 2,self.image_size * 2))
        self.image_position_x = (screen_width - self.image_size) / 2
        self.image_position_y = (screen_height - self.image_size) / 2
        self.rotation = 1 
        self.font_size = 45
        self.font = pygame.font.Font("resources/Extrude.ttf", self.font_size)
        self.color = (255,250,100)
        self.skin_text = self.font.render("Chosen", True, self.color)
        self.instruction_text = self.font.render("Press LEFT or RIGHT to choose between skins", True, self.color)
        self.esc_text = self.font.render("Press ESC to Main Menu", True, self.color)
        self.timer = 0
        self.timer_button = 0
        self.index = 1
        self.skins_number = 3
        self.skin_picked = 0  #class players takes information from here
        self.chosen = 1
        
    def skin_pick_update(self):
        if 45 > self.timer_button > 0:
            self.timer_button += 1
        else:
            self.timer_button = 0
      
        screen.blit(self.background_image, (0,0))
        if self.timer_button == 0:
            if pygame.key.get_pressed()[pygame.K_LEFT] == True:
                self.index -= 1
                self.timer_button += 1
                
            elif pygame.key.get_pressed()[pygame.K_RIGHT] == True:
                self.index += 1
                self.timer_button += 1


        if (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_RETURN]) == True and self.index == 1:
            self.skin_picked = self.skin1_image
            self.chosen = 1
            for sprite in player:
                sprite.skin_update()

        elif (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_RETURN]) == True and self.index == 2:
            self.skin_picked = self.skin2_image
            self.chosen = 2
            for sprite in player:
                sprite.skin_update()
        
        elif (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_RETURN]) == True and self.index == 3:
            self.skin_picked = self.skin3_image
            self.chosen = 3
            for sprite in player:
                sprite.skin_update()

                    
        if self.index > self.skins_number:
                self.index = 1
        elif self.index < 1:
                self.index = self.skins_number
        
        if self.index == 1:
            image = pygame.transform.rotate(self.skin1_image, self.rotation)

        elif self.index == 2:
            image = pygame.transform.rotate(self.skin2_image, self.rotation)
        
        elif self.index == 3:
            image = pygame.transform.rotate(self.skin3_image, self.rotation)
            
        self.image_position_x = (screen_width - image.get_width()) / 2
        self.image_position_y = (screen_height - image.get_height()) / 2
        screen.blit(image, (self.image_position_x, self.image_position_y))
        screen.blit(self.instruction_text, (70,600))
        screen.blit(self.esc_text, (330,700))
        if self.index == self.chosen:
            screen.blit(self.skin_text, (500, 500))
        self.rotation += 1
        if self.rotation > 360:
            self.rotation = 1

class Score_indicator():
    def __init__(self) -> None:
        self.font_size = 90
        self.color = (100,0,255)
        self.font = pygame.font.Font("resources/Extrude.ttf", self.font_size)
        self.score_text = self.font.render("0", False, self.color)
        self.score_pos_x = 30
        self.score_pos_y = 710
        self.score = 0


    def update(self):
        self.score = jimmy.score
        self.score_text = self.font.render(str(self.score), True, self.color)
        if stat_bar.bar_scroll_position == 700:
            screen.blit(self.score_text, (self.score_pos_x, self.score_pos_y))

class Stat_bar():
    """handles speedometer, score display, and animation"""
    def __init__(self) -> None:
        self.bar = pygame.rect.Rect(0,800,1200,100)
        self.bar_scroll_position = 800
        self.color = (100,0,255)
        self.font = pygame.font.Font("resources/Extrude.ttf", 40)
        self.speedometer_alpha = 0
        self.speedometer_image = pygame.image.load("resources/speedometer.png").convert_alpha()
        self.speedometer_image.set_alpha(self.speedometer_alpha)
        self.speedometer_image2 = pygame.image.load("resources/speedometer_pointer.png").convert_alpha()
        self.speedometer_image2.set_alpha(self.speedometer_alpha)
        self.speed_revealer_x = 350
        self.speed_revealer = pygame.rect.Rect(self.speed_revealer_x,750,500,50)
        self.result = 0
        

    
    def draw_stat_bar(self):
        if self.bar_scroll_position > 700:
            self.bar_scroll_position -= 1
            self.bar = pygame.rect.Rect(0,self.bar_scroll_position,1200,100)
        
        pygame.draw.rect(screen, (0,0,0), self.bar)
        if self.bar_scroll_position == 700:
            if self.speedometer_alpha < 255:
                self.speedometer_alpha += 1
                self.speedometer_image.set_alpha(self.speedometer_alpha)
                self.speedometer_image2.set_alpha(self.speedometer_alpha)


            self.result = self.speed_revealer_x + (spawner.speedometer_timer * 0.12)
            self.revealer_pixels_moved = round(self.result)
            self.speed_revealer = pygame.rect.Rect(self.revealer_pixels_moved,750,500,50)
            screen.blit(self.speedometer_image,(350, 700))
            screen.blit(self.speedometer_image2,(350, 750))
            pygame.draw.rect(screen, (0,0,0), self.speed_revealer)

    def clean(self):
        self.bar_scroll_position = 800
        self.color = (100,0,255)
        self.speedometer_alpha = 0
        self.speed_revealer_x = 350
        self.result = 0
        self.revealer_pixels_moved = 0
        spawner.speedometer_timer = 0

class Spawn_possibilities_checker():
    """helps obstacles to not spawn in eachother"""
    def __init__(self) -> None:
        self.current_possibilities = [
            [135,235,335,435,535],
            [635,735,835]
            ]
        self.list_of_deleted = [935, 1035]
        
    def update(self, li, index):
        self.list_of_deleted.insert(0, self.current_possibilities[li][index])
        del self.current_possibilities[li][index]
        self.current_possibilities[li].append(self.list_of_deleted[-1])
        del self.list_of_deleted[-1]

class Leaderboard():
    def __init__(self) -> None:
        self.background_image = pygame.image.load("resources/roads_blur_2.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (1200,800))
        self.path = "resources/leaderboard.json"
        self.score_list = []
        self.font_size = 45
        self.font = pygame.font.Font("resources/Extrude.ttf", self.font_size)
        self.color = (255,250,100)
        self.position_x = 400
        self.position_y = 100
        self.lines_distance = 60
        self.name_score_distance = 400
        self.title = self.font.render("Leaderboard", True, self.color)
        self.exit = self.font.render("Presc ESC to exit", True, self.color)
        try:
            with open(self.path, "r", encoding="utf-8") as saves:
                self.score_list = json.load(saves)
        except:
            self.score_list = [["AAAAA", 0], ["AAAAA", 0], ["AAAAA", 0], ["AAAAA", 0], ["AAAAA", 0], ["AAAAA", 0], ["AAAAA", 0], ["AAAAA", 0], ["AAAAA", 0], ["AAAAA", 0]]

        def replacer(element):
            return element[1]
        
        self.score_list = sorted(self.score_list, key=replacer, reverse=True)

        

    def draw_leaderboard(self):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.title, (450, 50))
        for line in self.score_list:
            name = self.font.render(line[0], True, self.color)
            screen.blit(name, (self.position_x, self.position_y))
            score = self.font.render(str(line[1]), True, self.color)
            screen.blit(score, (self.position_x + self.name_score_distance, self.position_y))
 
            self.position_y += self.lines_distance

        self.position_y = 100
        screen.blit(self.exit, (420, 700))


    def check_score(self, player_score):
        """checks if the score of a player fits in leaderboard
        """
        if player_score >= self.score_list[-1][1]:
            return True
    
    def ckeck_leaderboard(self, player_score, player_name) -> int:
        """check precisely where to put score of a player in leaderboard"""
        for i in range(10):
            if player_score > self.score_list[i][1]:
                self.score_list.insert(i, [player_name, player_score])
                del self.score_list[-1]
                break
        
        with open(self.path, "w", encoding="utf-8") as saves:
            json.dump(self.score_list, saves)

class Prop_spawner(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.position_left_x = -40
        self.position_right_x = 920
        self.position_y = -1400
        self.counter = 0
        self.lamp_size = 350
        self.index = 1
        #light from lamps
        self.light_rect = pygame.Rect((700,self.position_y), (400, 400))
        self.shape_surf = pygame.Surface(self.light_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(self.shape_surf, (255,255,0,10), (200, 200), 200)

   
        self.image_left =  pygame.image.load("resources/lamp_left.png").convert_alpha()
        self.image_left =  pygame.transform.scale(self.image_left, (self.lamp_size ,self.lamp_size))

        self.rect_left = pygame.rect.Rect(self.position_left_x, self.position_y, 100, 100)
        self.hitbox_left = pygame.rect.Rect(54, -1140, 10, 90)


        self.image_right =  pygame.image.load("resources/lamp.png").convert_alpha()
        self.image_right =  pygame.transform.scale(self.image_right, (self.lamp_size ,self.lamp_size))

        self.rect_right = pygame.rect.Rect(self.position_right_x, self.position_y, 100, 100)
        self.hitbox_right = pygame.rect.Rect(1129, -1140, 10, 90)
 
    def update(self):
        self.light_rect = pygame.Rect((100,self.rect_left.y), (400, 400))
        self.right_light_rect = pygame.Rect((700,self.rect_left.y), (400, 400))
        screen.blit(self.shape_surf, self.light_rect)
        screen.blit(self.shape_surf, self.right_light_rect)


        new_value = spawner.background_image_position_y_speed * dt * TARGET_FPS
        self.rect_left.y += new_value
        self.rect_right.y += new_value
        self.hitbox_left.y += new_value
        self.hitbox_right.y += new_value

        if self.rect_left.y >= 2000 or self.rect_right.y >= 2000:
            self.rect_left.y = -400
            self.rect_right.y = -400
            self.hitbox_left.y = -140
            self.hitbox_right.y = -140
            

        screen.blit(self.image_left, self.rect_left)
        screen.blit(self.image_right, self.rect_right)

        pygame.draw.rect(screen, (255,0,0), self.hitbox_left)
        pygame.draw.rect(screen, (255,0,0), self.hitbox_right)

    def draw(self):
        screen.blit(self.shape_surf, self.light_rect)
        screen.blit(self.shape_surf, self.right_light_rect)
        screen.blit(self.image_left, self.rect_left)
        screen.blit(self.image_right, self.rect_right)

    def clean(self):
        self.position_y = -1400
        self.counter = 0

        self.rect_left.y = -1400
        self.rect_right.y = -1400
        self.hitbox_left.y = -1140
        self.hitbox_right.y = -1140


def player_obstacle_collision():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        return False
    else: 
        return True

def player_prop_collision():
    if pygame.Rect.colliderect(player.sprite.rect, props.hitbox_left) or pygame.Rect.colliderect(player.sprite.rect, props.hitbox_right):
        return True
    else:
        return False

    
def background_draw(new_y):
    screen.blit(background_image, (0, new_y))
    screen.blit(background_image, (0, new_y - 800))
    screen.blit(background_image, (0, new_y + 800))
    
def main_menu_draw():

    screen.blit(main_menu_image, (200,70))
    #something goes here

def obstacle_obstacle_collision():
    obstacle_collision_dict = pygame.sprite.groupcollide(obstacle_group, obstacle_checker_group,False,False, collided=None)
    if obstacle_collision_dict:
        for obstacle_object, obstacle_checker_object in obstacle_collision_dict.items():
            obstacle_checker_object = obstacle_checker_object[0]
            obstacle_object.speed = obstacle_checker_object.speed
            obstacle_object.pos_y += 3

def clean_progress():
    for sprite in obstacle_group:
        sprite.clean()
    spawner.clean()
    for sprite in player:
        sprite.clean()
    jimmy.clean()
    stat_bar.clean()
    jimmy.score = 0
    retry_text.user_text = ''
    props.clean()


pygame.init()
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('traffiKING')
clock = pygame.time.Clock()
keys = pygame.key.get_pressed()



jimmy = Player("Jimmy")                   #initialize player
player = pygame.sprite.GroupSingle() 
player.add(Player(jimmy))                   #adding player to sprite


props = Prop_spawner()
skins = Skin_pick()
spawner = Spawner()
menu = Main_menu()
score = Score_indicator()
stat_bar = Stat_bar()

obstacle_group = pygame.sprite.Group()
obstacle_checker_group = pygame.sprite.Group()

available_positions = Spawn_possibilities_checker()
leaderboard = Leaderboard()

background_image_position_y = 0
background_image_position_y_speed = 20
background_image = pygame.image.load("resources/roads_blur_2.png").convert()

background_image = pygame.transform.scale(background_image, (1200,800))

main_menu_image = pygame.image.load("resources/main_menu_image1.png").convert_alpha()
main_menu_image = pygame.transform.scale(main_menu_image, (800,400))

intro = Intro_animation()
#frames
FPS = 144
TARGET_FPS = 60
current_frames = int(clock.get_fps())
prev_time = time.time()
dt = 0
game_state = "playing"

#font
retry_text = Retry_screen_text()


while True:
    now = time.time()
    dt = now - prev_time
    prev_time = now
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #retry screen player name getter
        if leaderboard.check_score(jimmy.score) and event.type == pygame.KEYDOWN and game_state == "retry_screen":
                if event.key == pygame.K_BACKSPACE:
                    retry_text.user_text = retry_text.user_text[:-1]
                elif event.key == pygame.K_RETURN and len(retry_text.user_text) > 0:
                        #saving score
                        leaderboard.ckeck_leaderboard(jimmy.score, retry_text.user_text)
                        clean_progress()
                        game_state = "leaderboard"
                else:
                    if len(retry_text.user_text) < 7 and event.key != pygame.K_RETURN:
                        retry_text.user_text += event.unicode


    #if player started the game
    if game_state == "playing":
        background_draw(background_image_position_y)
        background_image_position_y += spawner.background_image_position_y_speed * dt * TARGET_FPS
        spawner.spawner_update()
        
        if background_image_position_y >= 800:
            background_image_position_y = 0


        player.update()
        player.draw(screen)

        props.update()

        obstacle_group.draw(screen)
        obstacle_group.update()


        stat_bar.draw_stat_bar()
        score.update()

        if player_obstacle_collision() == False or player_prop_collision():
            game_state = "retry_screen"
        
        # checking if each obstacle in group colides with another
        obstacle_obstacle_collision()

            
    #retry menu screen
    elif game_state == "retry_screen":
        if pygame.key.get_pressed()[pygame.K_SPACE] == True:
            clean_progress()
            game_state = "playing"

        if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
            clean_progress()
            game_state = "menu"
        
        background_draw(background_image_position_y)
        props.draw()
        player.draw(screen)
        obstacle_group.draw(screen)
        retry_text.retry_text_update()
    
    #intro
    elif game_state == "intro":
        intro.intro_update()
        if intro.intro_update() == False:
            game_state = "menu"

    #skins
    elif game_state == "skins":
        skins.skin_pick_update()
        if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
            game_state = "menu"
    
    #leaderboard
    elif game_state == "leaderboard":
        leaderboard.draw_leaderboard()
        if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
            game_state = "menu"


    #main menu
    else:
        menu.update_menu()
        if menu.update_menu() == 1:
            game_state = "playing"
        elif menu.update_menu() == 2:
            game_state = "skins"
        elif menu.update_menu() == 3:
            game_state = "leaderboard"


    # print(clock.get_fps())
    
    pygame.display.update()
    clock.tick(FPS)
        
        
        
