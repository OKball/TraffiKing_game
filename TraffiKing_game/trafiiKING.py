import pygame
from sys import exit
import random
import time



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
        self.color = (255,255,255)
        self.restart_text = self.font.render("press spacebar to Restart", True, self.color)
        self.menu_text = self.font.render("press ESC for Menu", True, self.color)
        self.timer = 255

    def retry_text_update(self):
        self.timer -= 1
        self.color = (255,self.timer,self.timer)
        if self.timer <= 0:
            self.timer = 255
        self.font = pygame.font.Font("resources/Extrude.ttf", self.font_size)
        self.restart_text = self.font.render("press spacebar to Restart", True, self.color)
        self.menu_text = self.font.render("press ESC for Menu", True, self.color)
        screen.blit(self.restart_text, (255,500))
        screen.blit(self.menu_text, (340,700))

class Intro_animation():
    def __init__(self) -> None:
        self.intro_alpha = 0
        self.intro_image = pygame.image.load("resources/main_menu_image1.png").convert_alpha()
        self.intro_image.set_alpha(self.intro_alpha)
        self.intro_image = pygame.transform.scale(self.intro_image, (800,400))
        self.background_alpha = 0
        self.background_image = pygame.image.load("resources/roads1.png").convert_alpha()
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
        self.background_image = pygame.image.load("resources/roads1.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (1200,800))
        self.font_size = 52
        self.font = pygame.font.Font("resources/Extrude.ttf", self.font_size)
        self.color = (255,255,255)
        self.start_button = self.font.render("Start", True, self.color)
        self.skin_button = self.font.render("Skin", True, self.color)
        self.exit_button = self.font.render("Exit", True, self.color)
        self.pos_start = 450
        self.pos_skin = 550
        self.pos_exit = 650
        self.index = 0
        self.pointer = pygame.image.load("resources/police11.png").convert_alpha()
        self.pointer = pygame.transform.scale(self.pointer, (60,60))
        self.pointer = pygame.transform.rotate(self.pointer, 90)
        self.pointer_x = 1000
        self.pointer_y = 0
        self.timer = 0
        self.timer_button = 0


    
    def update_menu(self):
        if 45 > self.timer_button > 0:
            self.timer_button += 1
        else:
            self.timer_button = 0

        if self.timer < 255:
            self.timer += 1
        screen.blit(self.background_image, (0,0))
        screen.blit(self.image, (200, 70))
        self.start_button.set_alpha(self.timer)
        self.skin_button.set_alpha(self.timer)
        self.exit_button.set_alpha(self.timer)
        screen.blit(self.start_button, (530, self.pos_start))
        screen.blit(self.skin_button, (550, self.pos_skin))
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
                    pygame.quit()
                    exit()

            if self.index > 3:
                self.index = 1
            elif self.index < 1:
                self.index = 3

            if self.index == 1:
                screen.blit(self.pointer, (700, self.pos_start))
            elif self.index == 2:
                screen.blit(self.pointer, (700, self.pos_skin))
            elif self.index == 3:
                screen.blit(self.pointer, (700, self.pos_exit))

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


def player_obstacle_coliision():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        return False
    else: 
        return True

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
    

pygame.init()
screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption('traffiKING')
clock = pygame.time.Clock()
keys = pygame.key.get_pressed()


jimmy = Player("Jimmy")                     #initialize player
player = pygame.sprite.GroupSingle() 
player.add(Player(jimmy))                   #adding player to sprite

spawner = Spawner()
menu = Main_menu()
score = Score_indicator()
stat_bar = Stat_bar()

obstacle_group = pygame.sprite.Group()
obstacle_checker_group = pygame.sprite.Group()

available_positions = Spawn_possibilities_checker()

background_image_position_y = 0
background_image_position_y_speed = 20
background_image = pygame.image.load("resources/roads1.png").convert()

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
game_state = "intro"

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

    #if player started the game
    if game_state == "playing":
        background_draw(background_image_position_y)
        background_image_position_y += spawner.background_image_position_y_speed * dt * TARGET_FPS
        
        
        spawner.spawner_update()
        

        if background_image_position_y >= 800:
            background_image_position_y = 0
        
        

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        stat_bar.draw_stat_bar()
        score.update()

        if player_obstacle_coliision() == False:
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
        player.draw(screen)
        obstacle_group.draw(screen)
        retry_text.retry_text_update()
        font = pygame.font.Font("resources/Extrude.ttf", 120)
        score_text = font.render(f"SCORE: {jimmy.score}", True, (100,0,255))
        screen.blit(score_text, (200,200))
    
    #intro
    elif game_state == "intro":
        # screen.fill((0,0,0))
        # main_menu_image.set_alpha(1000)
        # screen.blit(main_menu_image, (200,200))
        intro.intro_update()
        if intro.intro_update() == False:
            game_state = "menu"


    #main menu
    else:
        background_draw(background_image_position_y)
        menu.update_menu()
        if menu.update_menu() == 1:
            game_state = "playing"


    # print(clock.get_fps())
    
    pygame.display.update()
    clock.tick(FPS)
        
        
        
