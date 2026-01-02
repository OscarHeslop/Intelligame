import pygame
import math 
from enum import Enum
import random 

level_num = 1
enemy_delay = 0
shooting_cooldown = 200

enemy_bullets = []
enemy_active = True

class EnemyState(Enum):
    #weapons have limited ammo 
    patrol = "idle"
    chase_player = "direct persuit"
    teleport_to_player = "teleport"

class WeaponDrop:
    def __init__(self, x, y, weapon_type):
        self.x = x 
        self.y = y 
        self.weapon_type = weapon_type
        self.width = 20
        self.height = 20 
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            if self.weapon_type == "rocket":
                image = pygame.image.load("images/rocket.png")
            elif self.weapon_type == "dual_ak":
                image = pygame.image.load("images/dualak.png")
            elif self.weapon_type == "shotgun":
                image = pygame.image.load("images/shotgun.png")

            actual_width, actual_height = image.get_width(), image.get_height()
            transformed_width, tranformed_height = actual_width // 8, actual_height //8
            transformed_image = pygame.transform.scale(image, (transformed_width, tranformed_height))
            screen.blit(transformed_image, (self.x - 10, self.y - 10))

class EnemyShooting():
    def __init__(self,screen,  color, speed, size, player_pos, enemy_pos):
        self.screen = screen
        self.color = color
        self.speed = speed
        self.size = size
        self.x, self.y = enemy_pos
        player_x, player_y = player_pos

        dist_x, dist_y = player_x - self.x, player_y - self.y # for all functions in class to access variable must be in init
        angle = math.atan2(dist_y, dist_x)
        self.velocity_x = speed * math.cos(angle)
        self.velocity_y = speed  * math.sin(angle)
        self.bullet_x = self.x
        self.bullet_y = self.y 

    def update(self):
        self.bullet_x += self.velocity_x
        self.bullet_y += self.velocity_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color ,(int(self.bullet_x), int(self.bullet_y)) ,self.size)# circle parameters: (surface, colour, center, radius)

class Enemy:
    def __init__(self, screen, x, y, image_path= "images/enemy_img.png", wave=1):
        self.screen = screen 
        self.x = x 
        self.y = y 
        self.image = pygame.image.load(image_path)
        self.width = 30
        self.height = 30
        self.health = 100
        self.active = True

        #enemy attack stuff 
        self.state = EnemyState.patrol
        self.speed = 5
        self.chase_player_range = 40 #seeing player distance
        #tp stuff
        self.teleport_range = self.chase_player_range * 2
        self.max_teleport_cooldown = 100
#!-----------------------------------------------------------------------------------------------------------------------
#!                                                  ENEMY SHOOTING AND COOLDOWN
#!-----------------------------------------------------------------------------------------------------------------------
        self.last_shot_time = 0 
        self.shooting_cooldown = 500


        #weapon drops 
        self.weapon_types = ["dual_ak", "shotgun","rocket"]
        #chance of dropping weapoen when killing enemy 
        self.weapon_drop = random.random() < 1 # chance weapon droppped in first place
        self.teleport_cooldown = 0

    def shoot(self, player_pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shooting_cooldown:
            self.last_shot_time = current_time
            return EnemyShooting(self.screen, (255, 0, 0), 3, 4, player_pos, (self.x, self.y))
        return None
    
    def rotate(self, screen, enemy_health, enemy_x, enemy_y, player_x, player_y):
        if enemy_health > 0:
            # Use the already-scaled image from draw() method
            actual_width, actual_height = self.image.get_width(), self.image.get_height()
            transformed_width, transformed_height = actual_width // 8, actual_height // 8
            
            # Scale the ORIGINAL image only once per frame
            base_image = pygame.transform.scale(self.image, (transformed_width, transformed_height))
            
            # Calculate angle
            dist_x = player_x - enemy_x  # Fixed direction (was backwards)
            dist_y = player_y - enemy_y
            angle = math.atan2(dist_y, dist_x)
            angle_degrees = angle * (-180 / math.pi)
            
            # Rotate and draw
            rotated_image = pygame.transform.rotate(base_image, angle_degrees)
            rotated_rect = rotated_image.get_rect(center=(enemy_x, enemy_y))
            screen.blit(rotated_image, rotated_rect)
#!-----------------------------------------------------------------------------------------------------------------------

    def teleport_to_player(self, player_pos):
        player_x, player_y = player_pos
        #random dist
        #rand angle
        too_close = 20
        #random_angle from x axis 
        angle = random.randint(0, 360)
        radians = math.radians(angle)  #https://pythonguides.com/python-degrees-to-radians/
        random_dist = random.randint(too_close, self.teleport_range)
        self.x = player_x + math.cos(radians) * random_dist
        self.y = player_y + math.sin(radians) * random_dist

        self.teleport_cooldown = self.max_teleport_cooldown
        
#------------------------------------------------------------------

    def get_distance_player(self, player_pos):
        player_x, player_y  = player_pos
        return math.sqrt((self.x - player_x)**2 + (self.y - player_y)**2)
    
    def update_state(self, player_pos):
        distance = self.get_distance_player(player_pos)

        if distance <= self.chase_player_range:
            self.state = EnemyState.chase_player
        elif distance <= self.teleport_range:
            self.state = EnemyState.teleport_to_player
        else:
            self.state = EnemyState.patrol

    def execute_action(self, player_pos):
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= 1 
        #exectuing diff actions 
        elif self.state == EnemyState.teleport_to_player and self.teleport_cooldown <= 0:
            self.teleport_to_player(player_pos)
        elif self.state == EnemyState.patrol:
            self.patrol()

    def update(self, player_pos):
        if self.active:
            self.update_state(player_pos)
            self.execute_action(player_pos)

    def take_damage(self, damage):
        self.health -= damage
        
        # If damaged, mark that we should chase player
        if damage > 0:
            self.has_damaged_player = True  # Reusing this variable name
        
        if self.health <= 0:
            self.active = False
            return self.enemy_drop_weapon()
        return None

    def enemy_drop_weapon(self):
        if self.weapon_drop:
            weapon_type = random.choice(self.weapon_types)
            return WeaponDrop(self.x, self.y, weapon_type)
        return None
        
    def draw(self, screen):
        global enemy_width, enemy_height
        if self.active:
            actual_width , actual_height = self.image.get_width(), self.image.get_height()
            transformed_width, transformed_height = actual_width //8, actual_height //8
            enemy_width, enemy_height = transformed_width, transformed_height
            self.transformed_enemy = pygame.transform.scale(self.image, (transformed_width, transformed_height))
            screen.blit(self.transformed_enemy, (int(self.x - transformed_width//2), int(self.y - transformed_height//2)))