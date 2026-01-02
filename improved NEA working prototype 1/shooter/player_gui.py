#https://www.youtube.com/watch?v=-ZP2Xm-mY4E
#uses enumerate  - vid 5: 30 

import random
import pygame 
import math
from enum import Enum
from enemy import *
from player import *
import tkinter as tk
from PIL import Image, ImageTk
import json
import os


#for djstra algorithm
import heapq
import sys



counter = 0
player_is_alive = False


screen_width = 1280
screen_height = 720
block_x = int(1/2 * screen_width)
block_y =  0
patrol_nodes = []
enemy_targets = {}
block_vel = 5   
cooldown = 2
binary_obstacles_grid = []
switch_cooldown_counter = 0 
enemy_see_player = False
button_pressed = 0



#kill target
start_safezone_countdown = False
time_entered_safezone = 0
survive_start_time = None
total_enemies_spawned = 0 
enemies_killed_this_wave = 0
transformed_width = 0
transformed_height = 0






#start of wave
current_wave = 1
wave_active = False
current_objective = None
survive_start_time = None
def player_gui(root):
    global transformed_width, transformed_height 
    global wave_active,num_enemies_needed_kill, current_wave, total_enemies_spawned, enemies_killed_this_wave, current_objective, player_speed
    Font = pygame.font.SysFont("timesnewroman", 30)

    enemies_killed_this_wave = 0
    total_enemies_spawned = 0
    wave_active = False
    current_objective = None
    

    #shop addintions

    #playerspeed
    player_speed = 5
    player_bullet_damage = 10

    # Shop additions - Player speed
    with open("textfile.txt", "r") as file:
        for line in file:
            if "playerspeed" in line:
                parts = line.split(":")
                speed_level = int(parts[1].strip())  # Convert to int and remove whitespace
                
                if speed_level == 0:
                    player_speed = 5

                elif speed_level == 1:
                    player_speed = 10
                elif speed_level == 2:
                    player_speed = 15

                elif speed_level == 3:
                    player_speed = 30
            
            # Bullet damage
            if "bulletdamage" in line:
                parts = line.split(":")
                bulletdamage_level = int(parts[1].strip())  # Convert to int and remove whitespace
                
                if bulletdamage_level == 0:
                    player_bullet_damage = 10

                elif bulletdamage_level == 1:
                    player_bullet_damage = 20

                elif bulletdamage_level == 2:
                    player_bullet_damage = 50

                elif bulletdamage_level == 3:
                    player_bullet_damage = 100

    
                
  

   


    def time_remaining_display(screen, time_remaining):
            global screen_width, screen_height

            time_to_survive = 10 # 10 seconds
            timeleft_display = Font.render((str(time_remaining) + "s"), True, (255, 0, 0))  # RED color
            screen.blit(timeleft_display, (screen_width//2 - timeleft_display.get_width()//2, screen_height * 0.05))
            
            return time_remaining <= 0
    
    def num_enemies_killed_display(screen, enemies_killed_this_wave):
        enemies_killed_num_display = Font.render((str(enemies_killed_this_wave) + "/ " + str(num_enemies_needed_kill)), True, (255, 0, 0))  # RED color
        screen.blit(enemies_killed_num_display, (screen_width//2 - enemies_killed_num_display.get_width()//2, screen_height * 0.05))


    def survive_complete_screen(screen, wave_num):
        exit_button_rect = pygame.Rect(screen_width//2 - 100, screen_height//2, 200, 60)
        
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 3000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        root.deiconify()
                        return
            
            pygame.time.Clock().tick(60)
            screen.fill((0, 0, 0))
            
            text = Font.render("Wave " + str(wave_num) + " completed!", True, (255, 255, 255))
            screen.blit(text, (screen_width//2 - text.get_width()//2, screen_height * 0.3))
            
            pygame.draw.rect(screen, (255, 255, 255), exit_button_rect)
            button_text = Font.render("Exit to Lobby", True, (0, 0, 0))
            screen.blit(button_text, (exit_button_rect.centerx - button_text.get_width()//2, 
                                    exit_button_rect.centery - button_text.get_height()//2))
            
            pygame.display.flip()





    def start_of_wave(screen, wave_number, screen_width, screen_height):
        global font
        import random
        import pygame
    
        # Define fonts
        title_font = pygame.font.Font(None, 64)
        objective_font = pygame.font.Font(None, 48)
        countdown_font = pygame.font.Font(None, 120)
        
        # Choose objective
        objective_type = random.choice(["survive", "kill_count"])
        
        if objective_type == "survive":
            # Phase 1: Show wave number and objective (3 seconds)
            wavenum_text = title_font.render("Wave " + str(wave_number), True, (255,255,255))
            objective_text = objective_font.render("Survive for 10s", True, (255,255,255))
            
            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start_time < 3000:
                # Handle events to prevent freezing
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                
                screen.fill((0, 0, 0))  # Clear screen
                
                # Center the text
                wavenum_rect = wavenum_text.get_rect(center=(screen_width//2, screen_height * 0.3))
                objective_rect = objective_text.get_rect(center=(screen_width//2, screen_height * 0.5))
                
                screen.blit(wavenum_text, wavenum_rect)
                screen.blit(objective_text, objective_rect)
                pygame.display.flip()

            
        
            # Phase 2: Countdown 3, 2, 1
            for count in [3, 2, 1]:
                countdown_start = pygame.time.get_ticks()
                while pygame.time.get_ticks() - countdown_start < 1000:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                    
                    screen.fill((0, 0, 0))
                    
                    countdown_text = countdown_font.render(str(count), True, (255,255,255))
                    countdown_rect = countdown_text.get_rect(center=(screen_width//2, screen_height//2))
                    screen.blit(countdown_text, countdown_rect)
                    
                    pygame.display.flip()
            
            # Phase 3: Show "GO!"
            go_start = pygame.time.get_ticks()
            while pygame.time.get_ticks() - go_start < 1000:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                
                screen.fill((0, 0, 0))
                
                go_text = countdown_font.render("GO!", True, (255,255,255))
                go_rect = go_text.get_rect(center=(screen_width//2, screen_height//2))
                screen.blit(go_text, go_rect)
                pygame.display.flip()
                
            
            # Start the survive challenge
            # survive()  # Uncomment when you have this function
        
        elif objective_type == "kill_count":
    # Phase 1: Show wave number and objective (3 seconds)
            wavenum_text = title_font.render("Wave " + str(wave_number), True, (255, 255, 255))
            objective_text = objective_font.render("Kill " + str(num_enemies_needed_kill) + " enemies", True, (255, 255, 255))

            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start_time < 3000:
                # Handle events to prevent freezing
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                
                screen.fill((0, 0, 0))  # Clear screen
                
                # Center the text
                wavenum_rect = wavenum_text.get_rect(center=(screen_width//2, screen_height * 0.3))
                objective_rect = objective_text.get_rect(center=(screen_width//2, screen_height * 0.5))
                
                screen.blit(wavenum_text, wavenum_rect)
                screen.blit(objective_text, objective_rect)
                
                pygame.display.flip()
            
            # Phase 2: Countdown 3, 2, 1
            for count in [3, 2, 1]:
                countdown_start = pygame.time.get_ticks()
                while pygame.time.get_ticks() - countdown_start < 1000:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                    
                    screen.fill((0, 0, 0))
                    
                    countdown_text = countdown_font.render(str(count), True, (255, 255, 255))
                    countdown_rect = countdown_text.get_rect(center=(screen_width//2, screen_height//2))
                    screen.blit(countdown_text, countdown_rect)
                    
                    pygame.display.flip()
            
            # Phase 3: Show "GO!"
            go_start = pygame.time.get_ticks()
            while pygame.time.get_ticks() - go_start < 1000:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                
                screen.fill((0, 0, 0))
                
                go_text = countdown_font.render("GO!", True, (255,255,255))
                go_rect = go_text.get_rect(center=(screen_width//2, screen_height//2))
                screen.blit(go_text, go_rect)
                
                
        return objective_type


    def kill_enemies_target(new_enemies, screen, binary_obstacles_grid, grid_block_width, grid_block_height, player):
        global enemies_killed_this_wave, total_enemies_spawned, current_wave
        
        # Difficulty scaling
         # Wave 1: 10, Wave 2: 13, Wave 3: 16
        max_enemies_at_once = min(3 + (current_wave // 2), 8)  # Wave 1-2: 3, Wave 3-4: 4, caps at 8
        
        # Count alive enemies
        current_alive = len([e for e in new_enemies if e.active])
        
        # Check if we should spawn more
        if total_enemies_spawned >= num_enemies_needed_kill:
            spawn_count = 0  # Stop spawning once we've hit the target
        else:
            # Spawn to maintain max enemies at once
            spawn_count = max_enemies_at_once - current_alive
            # Don't spawn more than needed to reach target
            spawn_count = min(spawn_count, num_enemies_needed_kill - total_enemies_spawned)
        
        # Get valid spawn positions (walkable cells)
        valid_nodes = []
        for row in range(len(binary_obstacles_grid)):
            for col in range(len(binary_obstacles_grid[0])):
                if binary_obstacles_grid[row][col] == 0 or binary_obstacles_grid[row][col] == 2:
                    x = col * grid_block_width + grid_block_width // 2
                    y = row * grid_block_height + grid_block_height // 2
                    valid_nodes.append((x, y))
        
        # Spawn enemies
        spawned = 0
        for i in range(spawn_count):
            if not valid_nodes:
                break
            
            # Try to spawn away from player (don't spawn on top of them)
            for attempt in range(20):
                spawn_x, spawn_y = random.choice(valid_nodes)
                distance_to_player = math.sqrt((spawn_x - player.x)**2 + (spawn_y - player.y)**2)
                
                if distance_to_player >= 150:  # At least 150 pixels away
                    enemy = Enemy(screen, spawn_x, spawn_y, wave=current_wave)  # Pass wave for scaling
                    new_enemies.append(enemy)
                    total_enemies_spawned += 1
                    spawned += 1
                    break
        
        # Check if wave complete
        wave_complete = enemies_killed_this_wave >= num_enemies_needed_kill
        
        return wave_complete






#!---------------------------------------------------------------------------------------------------------------------  
#!   A* ALGORITHM
#!---------------------------------------------------------------------------------------------------------------------  
    
    # Define the Cell class
    class Cell:
        def __init__(self):
            self.parent_i = 0  # Parent cell's row index
            self.parent_j = 0  # Parent cell's column index
            self.f = float('inf')  # Total cost of the cell (g + h)
            self.g = float('inf')  # Cost from start to this cell
            self.h = 0  # Heuristic cost from this cell to destination

    # Define the size of the grid


    # Check if a cell is valid (within the grid)
    def is_valid(row, col):
        return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

    # Check if a cell is unblocked
    def is_unblocked(grid, row, col):
        return grid[row][col] == 0 or grid[row][col] == 2
    # Check if a cell is the destination
    def is_destination(row, col, dest):
        return row == dest[0] and col == dest[1]

    # Calculate the heuristic value of a cell (Euclidean distance to destination)
    def calculate_h_value(row, col, dest):
        return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

    # Trace the path from source to destination
    def trace_path(cell_details, dest):
        path = []
        row = dest[0]
        col = dest[1]

        # Trace the path from destination to source using parent cells
        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col

        # Add the source cell to the path
        path.append((row, col))
        # Reverse the path to get the path from source to destination
        path.reverse()
        

        return path

    # Implement the A* search algorithm
    def a_star_search(grid, src, dest):
        # Check if the source and destination are valid
        if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
            #print("Source or destination is invalid")
            return None

        # Check if the source and destination are unblocked
        if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
            #print("Source or the destination is blocked")
            return None

        # Check if we are already at the destination
        if is_destination(src[0], src[1], dest):
            #print("We are already at the destination")
            return None

        # Initialize the closed list (visited cells)
        closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
        # Initialize the details of each cell
        cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

        # Initialize the start cell details
        i = src[0]
        j = src[1]
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j

        # Initialize the open list (cells to be visited) with the start cell
        open_list = []
        heapq.heappush(open_list, (0.0, i, j))

        # Initialize the flag for whether destination is found
        found_dest = False

        # Main loop of A* search algorithm
        while len(open_list) > 0:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)

            # Mark the cell as visited
            i = p[1]
            j = p[2]
            closed_list[i][j] = True

            # For each direction, check the successors
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dir in directions:
                new_i = i + dir[0]
                new_j = j + dir[1]

                # If the successor is valid, unblocked, and not visited
                if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                    # If the successor is the destination
                    if is_destination(new_i, new_j, dest):
                        # Set the parent of the destination cell
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        #print("The destination cell is found")
                        # Trace and print the path from source to destination
                        path = trace_path(cell_details, dest)
                        found_dest = True
                        return path
                    else:
                        # Calculate the new f, g, and h values
                        g_new = cell_details[i][j].g + 1.0
                        h_new = calculate_h_value(new_i, new_j, dest)
                        f_new = g_new + h_new

                        # If the cell is not in the open list or the new f value is smaller
                        if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            # Update the cell details
                            cell_details[new_i][new_j].f = f_new
                            cell_details[new_i][new_j].g = g_new
                            cell_details[new_i][new_j].h = h_new
                            cell_details[new_i][new_j].parent_i = i
                            cell_details[new_i][new_j].parent_j = j

        # If the destination is not found after visiting all cells
        if not found_dest:
            return None

#use node
#calculate distance between nodes 
#only have squares turn into nodes # each square will be node 
#create arrawy with 0 and 1

#!---------------------------------------------------------------------------------------------------------------------  
#!   Chase function
#!---------------------------------------------------------------------------------------------------------------------
    def chase_player(player_x, player_y, enemy_x, enemy_y): 
        player_node_x = int(player_x // grid_block_width)
        player_node_y = int(player_y // grid_block_height) 
        player_node = (player_node_y, player_node_x)

        enemy_node_x = int(enemy_x // grid_block_width)
        enemy_node_y = int(enemy_y // grid_block_height)
        enemy_node = (enemy_node_y, enemy_node_x) 

        if not (0 <= player_node[0] < ROW and 0 <= player_node[1] < COL):
            return None
        if not (0 <= enemy_node[0] < ROW and 0 <= enemy_node[1] < COL):
            return None
        
        
        # Check if standing ON a blocked cell (1 = blocked blue cell)
        player_blocked = binary_obstacles_grid[player_node[0]][player_node[1]] == 1
        enemy_blocked = binary_obstacles_grid[enemy_node[0]][enemy_node[1]] == 1
        
        # Temporarily make them walkable for pathfinding
        if player_blocked:
            binary_obstacles_grid[player_node[0]][player_node[1]] = 0
        if enemy_blocked:
            binary_obstacles_grid[enemy_node[0]][enemy_node[1]] = 0

        path = a_star_search(binary_obstacles_grid, enemy_node, player_node)

        if path and len(path) > 1:
            for i in range(len(path) - 1):
                # Convert grid coordinates to pixel coordinates
                start_x = path[i][1] * grid_block_width + grid_block_width // 2
                start_y = path[i][0] * grid_block_height + grid_block_height // 2
                end_x = path[i+1][1] * grid_block_width + grid_block_width // 2
                end_y = path[i+1][0] * grid_block_height + grid_block_height // 2
                #if display_grid:
                    #pygame.draw.line(screen, "green", (start_x, start_y), (end_x, end_y), 3)
                
                # Put them back to blocked
        if player_blocked:
            binary_obstacles_grid[player_node[0]][player_node[1]] = 1
        if enemy_blocked:
            binary_obstacles_grid[enemy_node[0]][enemy_node[1]] = 1
        
        if not path:
            dist_x = player_x - enemy_x
            dist_y = player_y - enemy_y
            magnitude = math.sqrt(dist_x**2 + dist_y**2)
            if magnitude != 0:
                return dist_x / magnitude, dist_y / magnitude
            return None
        
        if len(path) > 1:
            current_node = path[0]
            next_node = path[1]
            
            current_x = current_node[1] * grid_block_width + (grid_block_width // 2)
            current_y = current_node[0] * grid_block_height + (grid_block_height // 2)
            next_x = next_node[1] * grid_block_width + (grid_block_width // 2)
            next_y = next_node[0] * grid_block_height + (grid_block_height // 2)

            dist_x = next_x - current_x
            dist_y = next_y - current_y
            magnitude = math.sqrt((dist_x ** 2) + (dist_y ** 2))
            
            if magnitude != 0:
                return dist_x / magnitude, dist_y / magnitude
    
        return None
#!----------------------------------------------------------------------------------------
#!   Patrol
#!---------------------------------------------------------------------------------------------------------------------
#pick node to go to
#go to that node
#once reached go to another node

    def patrol(enemy, enemy_x, enemy_y):
        global patrol_nodes, enemy_targets, binary_obstacles_grid, c
        
        # Build patrol nodes once
        if not patrol_nodes:
            with open("map.json", "r") as file:
                grid = json.load(file)
                for y in range(len(grid)):
                    for x in range(len(grid[y])):
                        if grid[y][x] == 2:
                            patrol_nodes.append((y, x))
        
        if not patrol_nodes:
            return None
        
        # Give this enemy a target
        if enemy not in enemy_targets:
            enemy_targets[enemy] = random.choice(patrol_nodes)
        
        target_node = enemy_targets[enemy]
        
        # Check if reached target - pick new one
        target_x = target_node[1] * grid_block_width + grid_block_width // 2
        target_y = target_node[0] * grid_block_height + grid_block_height // 2
        distance = math.sqrt((enemy_x - target_x)**2 + (enemy_y - target_y)**2)


        #if display_grid:
            #pygame.draw.line(screen, "red", (enemy_x, enemy_y), (target_x, target_y),3)
        
        if distance < 30:
            enemy_targets[enemy] = random.choice(patrol_nodes)
        
        # Use chase_player (which already has A* pathfinding)
        return chase_player(target_x, target_y, enemy_x, enemy_y)



        

#source for patrol nodes
#https://www.geeksforgeeks.org/python/randomly-select-n-elements-from-list-in-python/







#source https://www.geeksforgeeks.org/maths/euclidean-distance/








#!---------------------------------------------------------------------------------------------------------------------  
#!   GRID FOR DJSTRA
#!---------------------------------------------------------------------------------------------------------------------
#  
    #want beack block 50px
    
    #grid creation 

        #saving block obstacle in json file
    def toggle_store(binary_obstacles_grid):
        """Save the obstacle grid to a JSON file."""
        with open("map.json", "w") as file:
            json.dump(binary_obstacles_grid, file)

    def toggle_retrieve(cols, rows):
        if os.path.exists("map.json"):
            try:
                with open("map.json", "r") as file:
                    if os.path.getsize("map.json") > 0:
                        toggle_background = json.load(file)
                        if isinstance(toggle_background, list):
                            return toggle_background
            except:
                pass
            return None


    

 

    grid_block_width, grid_block_height = 20,20
    cols, rows = screen_width // grid_block_width, screen_height // grid_block_height
    binary_obstacles_grid = toggle_retrieve(cols, rows)
    if binary_obstacles_grid is None or len(binary_obstacles_grid) == 0:
        binary_obstacles_grid = [[0] * cols for _ in range(rows)]
        toggle_store(binary_obstacles_grid)


    def grid_create(screen, binary_obstacles_grid):
        # draw toggled cells
        for row in range(rows):
            for col in range(cols):
                if binary_obstacles_grid[row][col] == 1:
                    rect = pygame.Rect(col*grid_block_width, row*grid_block_height, grid_block_width, grid_block_height)
                    pygame.draw.rect(screen, "blue", rect)
                if binary_obstacles_grid[row][col] == 2:
                    rect = pygame.Rect(col*grid_block_width, row*grid_block_height, grid_block_width, grid_block_height)
                    pygame.draw.rect(screen, "green", rect)
        for a in range(cols):
            pygame.draw.line(screen, "red", (a * grid_block_width,0), (a * grid_block_width, screen_height)) # screen, colour, start cord(x, y ),  endcord(x, y)
        for g in range(rows):
            pygame.draw.line(screen, "red", (0, g * grid_block_height), (screen_width, g * grid_block_height))
        


    ROW = len(binary_obstacles_grid)
    COL = len(binary_obstacles_grid[0])
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    


#source https://gamedevacademy.org/pygame-draw-line-tutorial-complete-guide/

#!---------------------------------------------------------------------------------------------------------------------  
#! THE MAP
#!---------------------------------------------------------------------------------------------------------------------
# 
    def rect(fraction_x, fraction_y, width, height):
        # width and height in pixels
        rectangle = pygame.Rect(fraction_x * screen_width - width//2,
                                fraction_y * screen_height - height//2,
                                width, height)
        return rectangle


    # Make a symmetrical cross in the middle
    cross_thickness = 50  # thickness of bars
    cross_length = 200    # length of bars

    obstacles = [
        #cross in middle
        rect(0.5, 0.5, cross_thickness, cross_length),   
        rect(0.5, 0.5, cross_length, cross_thickness),  

        #rectangle objects at side
        rect(0.75, 0.25, 400, 50),

        rect(0.2, 0.5, 50, 300),

        rect(0.1, 0.25, 100, 20),

        rect(0.8, 0.8, 100, 20),

        rect(0.4, 0.8, 40, 100)




    ]
    def background():
        global counter, block_vel, block_x, block_y, switch_cooldown_counter



        #interative objects
        switch = pygame.Rect((0), (1/2), (1/6), (1/6))#switch
        block_height = (1/6)
        moveable_block = rect((block_x ),(block_y), 1/6, 1/6)

        for obstacle in obstacles:
            pygame.draw.rect(screen, "grey", obstacle)
        #for objects in switch, moveable_block:
            #pygame.draw.rect(screen, "red", objects, 2)





        for bullet in player_bullets[:]:
            bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.size, bullet.size)
            if bullet_rect.colliderect(switch) and switch_cooldown_counter == 0:
                print("collided")
                counter += 1
                switch_cooldown_counter = cooldown  # start cooldown

        if counter % 2 == 0 and block_y > 0:  # move up
            block_y -= block_vel
        if counter % 2 != 0 and block_y < screen_height - block_height:  # move down
            block_y += block_vel

        # reduce cooldown per frame
        if switch_cooldown_counter > 0:
            switch_cooldown_counter -= 1

                #interactive switch
        return  moveable_block, obstacles
            
    def background_collision(player, obstacles, moveable_block):
        global transformed_width, transformed_height
        
        # Set the actual dimensions
        if transformed_width == 0 or transformed_height == 0:
            player_image = pygame.image.load("images/player.png")
            actual_width, actual_height = player_image.get_width(), player_image.get_height()
            transformed_width = actual_width // 4
            transformed_height = actual_height // 4
        
        player_rect = pygame.Rect(player.x - transformed_width//2, player.y - transformed_height//2, transformed_width, transformed_height)
        
        if player_rect.colliderect(moveable_block):
            return True
        
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                return True
        
        return False
    
    

    def bullet_background_collision_check(bullets, obstacles):
        for bullet in bullets[:]:
            if hasattr(bullet, 'bullet_x'):
                # Enemy bullet
                bullet_x = bullet.bullet_x
                bullet_y = bullet.bullet_y


            bullet_rect = pygame.Rect(bullet_x - bullet.size//2, bullet_y - bullet.size//2, bullet.size, bullet.size)

            for obstacle in obstacles:
                if bullet_rect.colliderect(obstacle):
                    try:
                        bullets.remove(bullet)
                        break
                    except ValueError:
                        pass



            

#!--------------------------------------------------------------------------------------------------------------------- 
#!   DONE DJSTRA ALGORITHM
#!--------------------------------------------------------------------------------------------------------------------- 





    enemy_chase_cooldown= 30  # run every 30 frames (~0.5s at 60 FPS)
    enemy_chase_counter = 0




#!_-------------------------------------------------------------------------------------------
    gameover = False
    new_enemies = []
    enemy_bullets = []
    teleport_range = 40
    max_teleport_cooldown = 200
    player_active = True
    
    
    

    level_num = 1
    total_xp_gained = 0

    #player stats
    player_image = pygame.image.load("images/player.png")
    vel = 5
    display_grid = False
    
    actual_width, actual_height = player_image.get_width(), player_image.get_height()
    transformed_width = actual_width // 4
    transformed_height = actual_height // 4
    player = Player(screen_width - transformed_width, screen_height - transformed_height)
    

    #game start stuff
    money = 0  # Initialize money with default value
    try:
        with open("textfile.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if "money" in line:
                    parts = line.split()
                    money = int(parts[2])
    except:
        pass
        

    level_num = 1 
    total_xp_gained = 0
    player_bullets = []
    weapon_drops = []

    #pygame stuff
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game")
    clock = pygame.time.Clock()
    #font stuff
    font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 18)

    
    #----------------------------------------------num enemies spawning 
    new_enemies = []
    for i in range(2):
        x = random.randint(50, screen_width - 50)
        y = random.randint(50, screen_height - 50)
        enemy = Enemy(screen, x, y)
        new_enemies.append(enemy)

    #------------------------------------------------
    class collision:
        def __init__(self, object_pos, object_dimensions, bullet_pos):
            self.object_x, self.object_y = object_pos
            self.bullet_x, self.bullet_y = bullet_pos
            self.object_width, self.object_height = object_dimensions
            self.total_damage = 0

        def hit_check(self):
            if (self.object_x - self.object_width) <= self.bullet_x and self.bullet_x <= (self.object_x + self.object_width) and (self.object_y - self.object_height) <= self.bullet_y and self.bullet_y <= (self.object_y + self.object_height):
                return True
            return False

    class Bullet():
        def __init__(self, x, y, colour, size, speed):
            self.x = x
            self.y = y
            self.colour = colour
            self.size = size
            self.speed = speed

            mouse_x, mouse_y = pygame.mouse.get_pos()
            dist_x, dist_y = mouse_x - x, mouse_y - y
            distance = math.sqrt(dist_x**2 + dist_y**2)
            if distance > 0:
                self.velocity_x = (dist_x / distance) * self.speed
                self.velocity_y = (dist_y / distance) * self.speed
            else:
                self.velocity_x = 0
                self.velocity_y = 0
        
        def update(self):
            self.y += self.velocity_y
            self.x += self.velocity_x
        
        def draw(self, screen):
            pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size // 2)

    
    
    class items():
        def __init__(self, screen, screen_width, screen_height):
            self.screen = screen
            self.radius = 10
            self.x = random.randint(self.radius, screen_width - 2*self.radius)
            self.y = random.randint(self.radius, screen_height - 2*self.radius)
            self.collected = False
        
        def draw_health(self):
            if not self.collected:
                pygame.draw.circle(self.screen, "green", (self.x, self.y), self.radius)
        
        def xp_used(self, player_pos):
            player_x, player_y = player_pos
            distance = math.sqrt((self.x - player_x)**2 + (self.y - player_y)**2)   
            xp_pickup_rad = self.radius + 15
            if distance <= xp_pickup_rad:
                self.collected = True

#!---------------------------------------------------------------------------------------------------------------------  
#!    MONEY ORBS 
#!---------------------------------------------------------------------------------------------------------------------                  
    money_orbs = []
    class money_orb():
        def __init__(self, x, y):
            self.x = x 
            self.y = y
            self.radius = 8 
            self.colour = "blue"
            self.collected = False
        
        def draw(self, screen):
            if not self.collected:
                pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)
        
        def pick_up_check(self, player_x, player_y):
            distance = math.sqrt((self.x - player_x)**2 + (self.y - player_y)**2)
            pickup_rad = 14
            if distance <= pickup_rad:
                self.collected = True
                return True
            return False

    def draw_healthbar(pos, tank_width, tank_height, current_health, max_health):
        x, y = pos
        health_x = x - 0.5*(tank_width)
        health_y = y - 1.25*(tank_height)
        current_health = max(0, min(current_health, max_health))  # Fixed: use parameter instead of player.health
        health_damage_ratio = current_health / max_health
        damage_bar_left = tank_width * health_damage_ratio
        damage_bar_width = tank_width - damage_bar_left
        damage_x = (x - 0.5*(tank_width)) + damage_bar_left
        damage_y = y - 1.25*(tank_height)

        pygame.draw.rect(screen, "green", pygame.Rect(health_x, health_y, tank_width, 0.25*(tank_height)))
        pygame.draw.rect(screen, "red", pygame.Rect(damage_x, damage_y, damage_bar_width, 0.25*(tank_height)))

    #---------------------------
    weapon_pick_up_rad = 50
    def weapon_pick_up_check(player):
        for drop in weapon_drops[:]:
            distance = math.sqrt((drop.x - player.x)**2 + (drop.y - player.y)**2)
            if distance <= weapon_pick_up_rad:
                weapon_drops.remove(drop)
                print(f"Picked up weapon: {drop.weapon_type}")
                small_multiplier = 7
                
                try:
                    if "rocket" == drop.weapon_type:
                        player_image = pygame.image.load("images/player_rocket.png")
                        actual_width, actual_height = player_image.get_width(), player_image.get_height()
                        transformed_width, transformed_height = actual_width//small_multiplier, actual_height//small_multiplier
                        player.player_image = pygame.transform.scale(player_image, (transformed_width, transformed_height))
                        
                    elif "shotgun" == drop.weapon_type:
                        player_image = pygame.image.load("images/player_shotgun.png")
                        actual_width, actual_height = player_image.get_width(), player_image.get_height()
                        transformed_width, transformed_height = actual_width//small_multiplier, actual_height//small_multiplier
                        player.player_image = pygame.transform.scale(player_image, (transformed_width, transformed_height))
                        
                    elif "dualak" == drop.weapon_type:
                        player_image = pygame.image.load("images/player_dualak.png")
                        actual_width, actual_height = player_image.get_width(), player_image.get_height()
                        transformed_width, transformed_height = actual_width//small_multiplier, actual_height//small_multiplier
                        player.player_image = pygame.transform.scale(player_image, (transformed_width, transformed_height))
                except pygame.error:
                    print(f"Could not load weapon image for {drop.weapon_type}")

    #-------------------------- items 
    xp_orbs = items(screen, screen_width, screen_height)
    player_max_health = 100
    enemy_max_health = 50
    actual_width, actual_height = player_image.get_width(), player_image.get_height()
    
    safezone_x = random.randint(0, screen_width)
    safezone_y = random.randint(0, screen_height)

#!---------------------------------------------------------------------------------------------------------------------  
#!     SAFEZONE 
#!---------------------------------------------------------------------------------------------------------------------    
    
   

    


    run = True
    while run:

        clock.tick(60)
        #background_image = pygame.image.load("images/moon_background.webp")
        #background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        #screen.blit(background_image, (0, 0))
        screen.fill("white")

        wave_complete = False

        if current_objective == "kill_count":
            wave_complete = kill_enemies_target(new_enemies, screen, binary_obstacles_grid, 
                                        grid_block_width, grid_block_height, player)
            num_enemies_killed_display(screen, enemies_killed_this_wave)
        elif current_objective == "survive":
            # Display timer
            time_elapsed = (pygame.time.get_ticks() - survive_start_time) / 1000
            time_remaining = max(0, 10 - time_elapsed)
            time_remaining_display(screen, int(time_remaining))
            
            # Check if survived 10 seconds
            if time_remaining <= 0:
                wave_complete = True

        if wave_complete:
            survive_complete_screen(screen, current_wave)
            wave_active = False
            current_wave += 1
            total_enemies_spawned = 0
            enemies_killed_this_wave = 0
            current_objective = None
            survive_start_time = None



        #start of new ave 
        #start of new ave 
        if not wave_active:
            # Start new wave#
            num_enemies_needed_kill = 1 + (current_wave * 3) 
            current_objective = start_of_wave(screen, current_wave, screen_width, screen_height)
            wave_active = True
            if current_objective == "survive":
                survive_start_time = pygame.time.get_ticks()
            # Reset wave stats
            total_enemies_spawned = 0
            enemies_killed_this_wave = 0
        
        moveable_block, obstacles = background()
        background_collision(player, obstacles, moveable_block)

       

        # Draw UI elements
        xp_orbs.draw_health()
        if hasattr(Player, 'stats_display'):
            Player.stats_display(screen, money)
        if hasattr(Player, 'xp_bar'):
            Player.xp_bar(screen)
                                  
        for enemy in new_enemies:
            draw_healthbar((enemy.x, enemy.y), enemy.width, enemy.height, enemy.health, enemy_max_health)




#!---------------------------------------------------------------------------------------------------------------------  
#!     executed A* algorithm
#!--------------------------------------------------------------------------------------------------------------------- 
        enemy_movements = {}
        for enemy in new_enemies:
            enemy_movements[enemy] = None

        # Then in the game loop:
        enemy_chase_counter += 1

        # Only recalculate paths every 15 frames
        #if enemy_chase_counter >= 15:
            #enemy_chase_counter = 0
        chase_radius = 250
        for enemy in new_enemies:
            distance = math.sqrt((enemy.x - player.x)**2 + (enemy.y - player.y) **2)
            print(distance)



            if display_grid:
                pygame.draw.circle(screen, "red", (enemy.x, enemy.y), chase_radius, 2) 
            #pygame.draw.circle(surface, color, center_coordinates, radius, width=0)

            #https://www.geeksforgeeks.org/python/pygame-drawing-objects-and-shapes/
            
            if distance < chase_radius:
                enemy_see_player = True
                enemy_movements[enemy] = chase_player(player.x, player.y, enemy.x, enemy.y)

            elif distance > chase_radius:
                enemy_see_player = False
                enemy_movements[enemy] = patrol(enemy, enemy.x, enemy.y)

#!---------------------------------------------------------------------------------------------------------------------  
#!     enemy speed
#!--------------------------------------------------------------------------------------------------------------------- 

        # Apply stored movements every frame
        for enemy in new_enemies:
            if enemy_movements[enemy]:
                unit_x, unit_y = enemy_movements[enemy]
                enemy.x += unit_x * 3
                enemy.y += unit_y * 3


    
#!---------------------------------------------------------------------------------------------------------------------  
#!     PlAYER DEAD
#!---------------------------------------------------------------------------------------------------------------------  

        if player.health <= 0:
            player_active = False
            run = False
            player_is_alive = False
        
            # Clear the root window completely before passing it
            for widget in root.winfo_children():
                widget.destroy()
            
            # Make sure the window is visible
            root.deiconify()
            root.update()  # Force update
            
            import death_screen
            death_screen.death_display(root)




 
#!---------------------------------------------------------------------------------------------------------------------  
#!    MAIN GAME LOOP
#!---------------------------------------------------------------------------------------------------------------------  
        
        


        weapon_pick_up_check(player)

       
        if player_active:
            draw_healthbar((player.x, player.y), player.width, player.height, player.health, player_max_health)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                keys = pygame.key.get_pressed()
                if player_active:
                    #shotting
                    if event.button == 1 and not keys[pygame.K_e]:  # Left click
                        bullet1 = Bullet(player.x, player.y, (0, 0, 0), 5, 100)
                        player_bullets.append(bullet1)
                    if event.button == 3 and not keys[pygame.K_e]:  # Right click
                        bullet2 = Bullet(player.x, player.y, (0, 0, 0), 20, 100)
                        player_bullets.append(bullet2)



                    #adding nodes and obstacle grid
                    if event.button == 3 and not keys[pygame.K_a]:
                        #green
                        clicked_x, clicked_y = pygame.mouse.get_pos()
                        col = clicked_x // grid_block_width
                        row = clicked_y // grid_block_height
                        

                    mouse_pos = pygame.mouse.get_pos()
                    x, y = mouse_pos
                    col = x // grid_block_width
                    row = y // grid_block_height

                    if event.button == 1 and keys[pygame.K_e]: 
                        #e for edit
                        if 0 <= row < rows and 0 <= col < cols:
                            #blue is left click
                            binary_obstacles_grid[row][col] = 1 if binary_obstacles_grid[row][col] == 0 else 0
                            with open("map.json", "w") as file:
                                json.dump(binary_obstacles_grid, file)
                    elif event.button == 3 and keys[pygame.K_e]: 
                        #geren is right click
                        if 0 <= row < rows and 0 <= col < cols:
                            binary_obstacles_grid[row][col] = 2 if binary_obstacles_grid[row][col] == 0 else 0
                            with open("map.json", "w") as file:
                                json.dump(binary_obstacles_grid, file)


                        
                    

        
                
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and player.x > transformed_width//2:
            player.x -= player_speed
            if background_collision(player, obstacles, moveable_block):
                player.x += player_speed

        if keys[pygame.K_d] and player.x < screen_width - transformed_width//2:
            player.x += player_speed
            if background_collision(player, obstacles, moveable_block):
                player.x -= player_speed

        if keys[pygame.K_w] and player.y > transformed_height//2:
            player.y -= player_speed
            if background_collision(player, obstacles, moveable_block):
                player.y += player_speed

        if keys[pygame.K_s] and player.y < screen_height - transformed_height//2:
            player.y += player_speed
            if background_collision(player, obstacles, moveable_block):
                player.y -= player_speed

        if keys[pygame.K_g]:
            display_grid = not display_grid






        
#!-------------------------------------------------------------------
#!           ENEMY BULLETS
#!-------------------------------------------------------------------
        enemy_can_see = {}
        for enemy in new_enemies:
            distance = math.sqrt((enemy.x - player.x)**2 + (enemy.y - player.y)**2)
            enemy_can_see[enemy] = distance < chase_radius

        # Step 2: Update and draw ALL enemy bullets
        for bullet in enemy_bullets[:]:
            bullet.update()
            bullet.draw(screen)
            
            # Remove bullets that go off screen
            if bullet.x < 0 or bullet.x > screen_width or bullet.y < 0 or bullet.y > screen_height:
                try:
                    enemy_bullets.remove(bullet)
                except ValueError:
                    pass

        # Step 3: Check bullet collisions with walls
        #bullet_background_collision_check(enemy_bullets, obstacles)

        # Step 4: Check bullet collisions with player
        for bullet in enemy_bullets[:]:
            player_col = collision((player.x, player.y), (player.width, player.height), (bullet.x, bullet.y))
            if player_col.hit_check():
                try:
                    enemy_bullets.remove(bullet)
                    player.health -= 10  # Changed from 0 to actual damage
                    print(f"Player hit! Health: {player.health}")
                except ValueError:
                    pass

        # Step 5: Handle each enemy (shooting, rotation, drawing)
        current_time = pygame.time.get_ticks()

        for enemy in new_enemies[:]:
            # Remove inactive enemies
            if not enemy.active:
                new_enemies.remove(enemy)
                continue
            
            # If THIS specific enemy can see the player - draw rotated
            if enemy_can_see.get(enemy, False):
                # Rotate THIS enemy toward player
                enemy.rotate(screen, enemy.health, enemy.x, enemy.y, player.x, player.y)
                
                # Check if THIS enemy can shoot
                if current_time - enemy.last_shot_time > enemy.shooting_cooldown:
                    bullet = enemy.shoot((player.x, player.y))
                    if bullet:
                        enemy_bullets.append(bullet)
            else:
        # Enemy can't see player - just draw normally without rotation
                enemy.draw(screen)

        # Step 6: Draw weapon drops and money orbs
        for drop in weapon_drops[:]:
            drop.draw(screen)

        for orb in money_orbs[:]:
            orb.draw(screen)
            if orb.pick_up_check(player.x, player.y):
                money_orbs.remove(orb)
                money += 5
#!-------------------------------------------------------------------
#!   END ENEMY BULLETS
#!-------------------------------------------------------------------    
#!-------------------------------------------------------------------
#!   PLAYER BULLETS
#!-------------------------------------------------------------------      

        # Check collision with enemies
        for bullet in player_bullets[:]:
            bullet.update()
            bullet.draw(screen)
            
            # Check wall collision
            bullet_rect = pygame.Rect(bullet.x - bullet.size* 2, bullet.y - bullet.size//2, bullet.size, bullet.size)
            for obstacle in obstacles:
                if bullet_rect.colliderect(obstacle):
                    try:
                        player_bullets.remove(bullet)
                        break
                    except ValueError:
                        pass

                
            
            # Remove bullets that go off screen
            if bullet.x < 0 or bullet.x > screen_width or bullet.y < 0 or bullet.y > screen_height:
                try:
                    player_bullets.remove(bullet)
                except ValueError:
                    pass
                        
            for enemy in new_enemies[:]:
                if enemy.active:
                    
                    enemy_col = collision((enemy.x, enemy.y), (enemy.width * 5, enemy.height * 5), (bullet.x, bullet.y))
                    if enemy_col.hit_check():
                        try:
                            player_bullets.remove(bullet)
                            
                            # Check if enemy was alive before damage
                            was_alive = enemy.active
                            
                            weapon_drop = enemy.take_damage(5)
                            if weapon_drop:
                                weapon_drops.append(weapon_drop)
                            
                            # Only drop orbs if the enemy JUST died from this hit
                            if was_alive and not enemy.active:
                                enemies_killed_this_wave += 1 
                                money += 50
                                total_xp_gained += 50
                                
                                # Create money orbs at enemy position
                                for i in range(5):
                                    orb_x = enemy.x + random.randint(-20, 20)
                                    orb_y = enemy.y + random.randint(-20, 20)
                                    orb = money_orb(orb_x, orb_y)
                                    money_orbs.append(orb)
                                
                                
                                # Update file
                                with open("textfile.txt", "r") as file:
                                    lines = file.readlines()
                                
                                for i, line in enumerate(lines):
                                    if "money :" in line:
                                        lines[i] = f"money : {money}\n"
                                
                                with open("textfile.txt", "w") as file:
                                    file.writelines(lines)
                            
                            break
                        except:
                            pass

#!-------------------------------------------------------------------
#!   END PLAYER BULLETS
#!-------------------------------------------------------------------     

#!---------------------------------------------------------------------------------------------------
#!    BACKGROUND PHYSICS
#!---------------------------------------------------------------------------------------------------



        if display_grid == True:
            grid_create(screen, binary_obstacles_grid)


        # Draw player
        if player_active:
            player.rotate(screen, player.health)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    pygame.init()  # Initialize pygame ONCE here
    root = tk.Tk()
    root.withdraw()
    player_gui(root)

