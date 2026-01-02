import pygame
import math

pygame.init()

screen_width, screen_height = 500, 500
level_num = 1
total_xp_gained = 0
current_time = 0
enemy_delay = 0
shooting_cooldown = 200
new_enemies = []
enemy_bullets = []
player_bullets = []
enemy_killed = 0

player_vel = 5

#font 
Font = pygame.font.SysFont("timesnewroman", 30)

player_image = pygame.image.load("images/player.png")
actual_width, actual_height = player_image.get_width(), player_image.get_height()
transformed_width, transformed_height = actual_width//4 , actual_height // 4
#player proprties (size)
class Player():
    def __init__(self, x, y):
        global screen_width,screen_height, transformed_width, transformed_height
        self.health = 100
        self.height = 32
        self.width = 32
        self.x = x 
        self.y = y
        
        player_image = pygame.image.load("images/player.png")
        self.width = transformed_width
        self.height = transformed_height
        self.player_image = pygame.transform.scale(player_image, (transformed_width, transformed_height))

    def move(self, keys):
        global player_vel
        if keys[pygame.K_a] and self.x > 0:            
            self.x -= player_vel
        if keys[pygame.K_d] and self.x < screen_width - self.width:
            self.x += player_vel
        if keys[pygame.K_w] and self.y > 0:
            self.y -= player_vel
        if keys[pygame.K_s] and self.y < screen_height - self.height:
            self.y += player_vel

    def update(self, keys):
        self.move(keys)

    # def xp_bar( screen):
    #     global level_num, total_xp_gained, Font
    #     middle = screen_width / 2
    #     left_x = middle - 0.2 * (screen_width)
    #     xp_width = 0.4 * (screen_width)
    #     left_y = 0.95 * (screen_height)
    #     pygame.draw.rect(screen, "grey", pygame.Rect(left_x, left_y, xp_width, 10))
    #     total_level_xp  = 50 + (10 * (level_num-1))

    #     #display xp bar
    #     if total_level_xp > 0:
    #         progress = min(total_xp_gained / total_level_xp, 1.0)
    #         pygame.draw.rect(screen, "yellow", pygame.Rect(left_x, left_y, xp_width * progress, 10))
    #     xp_time = pygame.time.get_ticks()

    #     if total_xp_gained >= total_level_xp and pygame.time.get_ticks() > xp_time:
    #         print("next level")
    #         level_num += 1
    #         total_xp_gained = 0

    #     #level num display
    #     text = f'level{level_num}'
    #     word = Font.render(text, False, "black","white")
    #     screen.blit(word, (left_x, left_y))
    def stats_display(screen, money):
        money_display = Font.render("Money: "+str(money), True, (0, 0, 0))
        import player_gui
        screen_width = player_gui.screen_width
        screen_height = player_gui.screen_height
        screen.blit(money_display, (screen_width - (money_display.get_width() * 1.5) , screen_height * 0.05))

    def rotate(self, screen, player_health):
        player_x, player_y = self.x, self.y
        if player_health > 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dist_x, dist_y = mouse_x - player_x, mouse_y - player_y
            angle = math.atan2(dist_y, dist_x)
            angle_degrees = angle * (-180 / math.pi)
            rotated_image = pygame.transform.rotate(self.player_image, angle_degrees)
            rotated_rect = rotated_image.get_rect(center=(player_x, player_y))
            screen.blit(rotated_image, rotated_rect)

class enemy_shooting:
    def __init__(self, screen, color, speed, size, player_pos, enemy_pos):
        self.screen = screen
        self.color = color
        self.speed = speed
        self.size = size
        self.x, self.y = enemy_pos
        player_x, player_y = player_pos

        dist_x, dist_y = player_x - self.x, player_y - self.y
        angle = math.atan2(dist_y, dist_x)
        self.velocity_x = speed * math.cos(angle)
        self.velocity_y = speed * math.sin(angle)
    
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class collision:
    def __init__(self, object_pos, object_dimensions, bullet_pos):
        self.object_x, self.object_y = object_pos
        self.bullet_x, self.bullet_y = bullet_pos
        self.object_width, self.object_height = object_dimensions

    def hit_check(self):
        # Check if bullet is inside the rectangle
        half_width = self.object_width / 2
        half_height = self.object_height / 2
        
        return (self.object_x - half_width <= self.bullet_x <= self.object_x + half_width and 
                self.object_y - half_height <= self.bullet_y <= self.object_y + half_height)
class Bullet:
    def __init__(self, x, y, target_pos):
        self.x = x
        self.y = y
        self.speed = 8
        self.size = 4
        
        # Calculate direction
        target_x, target_y = target_pos
        dist_x, dist_y = target_x - x, target_y - y
        angle = math.atan2(dist_y, dist_x)
        self.velocity_x = self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)
    
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.size)