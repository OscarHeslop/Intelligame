#imports needed
import tkinter as tk
from PIL import Image, ImageTk
from player_gui import *
from datalogger import datalogger



save_created = False
datalogger_state= ""
save_created = False
def startofgame():

    
    root = tk.Tk()
    root.geometry("800x400")
    root.save_icon = None

    def make_button(screen_name, button_text, command_text,):
        button = (tk.Button(screen_name ,text = button_text,command = command_text, font = ("Arial", 12)))
        button.pack()
        return button
    def make_label(screen_name, label_text, ): 
        label = (tk.Label(screen_name, text = label_text, font = ("Arial", 12)))
        label.pack()
        return label

    def show_frame(frame):
        frame.tkraise()
        
    def image_clicked():
        print("image clicked")

    def new_save():
        clear_screen(step_1)
        step2_screen()
        show_frame(step_2)


        #go to new screen 
        #frame has create_account 
        #once account created go back to save 

    def clear_screen(screen_name):
        for widget in screen_name.winfo_children():
            widget.destroy()




    def run_game():
        clear_screen(step_2)
        lobby()
        show_frame(main_screen)

    def find_line(name):
        with open("textfile.txt","r") as file:
            lines = file.readlines()
            counter = 0 
            for line in lines:
                counter += 1
                if name in line:
                    return line


    def update(name, num):
        with open("textfile.txt", "r") as file:
                lines = file.readlines()
                line_num = find_line(name)
                lines[line_num] = f'{name} : {num}\n'
                with open("textfile.txt", "w") as file:
                    file.writelines(lines)

    def save_delete():
            global save_created
            with open("textfile.txt", "w") as file:
                file.writelines("")
            save_created = False

            reload_screen()




    def reload_screen():
        clear_screen(step_1)
        step1_screen()
        show_frame(step_1)
    #------------------------- stage screens 

    step_1= tk.Frame(root)
    step_2 = tk.Frame(root)
    main_screen = tk.Frame(root)
    settings_screen = tk.Frame(root)
    statsoverview_screen = tk.Frame(root)
    shop_screen = tk.Frame(root)
    flashcards_screen = tk.Frame(root)

    for frame in (step_1, step_2, main_screen, settings_screen, statsoverview_screen, shop_screen, flashcards_screen):
        frame.grid(row = 0, column = 0)
    #------------------------ step 1
    #create account text 


    
    def step1_screen():
        global save_created
        name = ""
        save_created = False  # reset

        # Safely read save name
        try:
            with open("textfile.txt", "r") as file:
                for line in file:
                    if "savename" in line:
                        user_line = line
                        name = user_line.split()[2]
                        nospace = name.replace(" ", "")
                        if len(nospace) > 0:
                            save_created = True
        except FileNotFoundError:
            # file doesn't exist yet
            pass

        # Clear old widgets first
        clear_screen(step_1)

        if save_created:
            make_label(step_1, name)
            make_button(step_1, "Enter Game", run_game)
            make_button(step_1, "Delete save", save_delete)
        else:
            make_label(step_1, "Create Account")
            # Load image once and store in root
            make_button(step_1, "Create New Save", new_save)



    #------------------------ stage 2

    def back_to_save():
        clear_screen(step_2)
        step1_screen()
        show_frame(step_1)
    def step2_screen():
        global name_entry


        s = make_label(step_2, "Type in save name" )
        s.pack()
        name_entry = tk.Entry(step_2)
        name_entry.pack()
        name_submit  = make_button(step_2, "Submit name",save_name)
        back_save = make_button(step_2, "Back to save", back_to_save)
        #back button
    #---------------------------- step_3 lobby 
    pressed_counter = 0
    sound_text = "off"

    def lobby():
        clear_screen(main_screen)
        show_frame(main_screen)

        #getting name 
        with open("textfile.txt","r") as file:
            for line in (file):
                if "savename" in line:
                    words = line.split()
                    username = words[2]
                    make_label(main_screen, "Welcome "+username)
                    break
        make_button(main_screen,"Start Game",startgame)
        make_button(main_screen, "Settings", settings)
        make_button(main_screen, "Oscar's Shop", shop)
        make_button(main_screen, "Flaschards", flashcards)

    def startgame():
        root.withdraw()  # Hide tkinter window
        player_gui(root)
        root.deiconify()  # Show tkinter window again when pygame closes

    def go_back_to_lobby():
        # This is in startofgame.py, so it CAN access these
        clear_screen(main_screen)
        lobby()
        show_frame(main_screen)



    def settings_display():
        clear_screen(main_screen)
        show_frame(settings_screen)
        make_label(settings_screen, "Audio")
        make_button(settings_screen, sound_text, off_on_pressed)

        backhome_button(settings_screen)

    def flashcards():
        clear_screen(main_screen)
        root.withdraw()  # Hide main window
        datalogger("revise", root, callback=go_back_to_lobby)


        

    def magazine_cost():
        with open("textfile.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if "bulletdamage" in line:
                    parts = line.split()
                    mag_num = parts[2]        
                    #0 > 1 , 1> 2, 2 > 3
                    if mag_num == 0:
                        return 50
                    elif mag_num == 1:
                        return  200
                    elif mag_num == 2:
                        return 400
    #!------------------------------------------------------------------------------------------
    #!                                   SAVE NAME
    #!------------------------------------------------------------------------------------------

    #money update
    money =0
    magnum = 0 
    bullnum = 0 
    enemies_killed = 0 
    questions_attempted = 0
    def save_name():
        global money, magnum, bullnum, enemies_killed, questions_attempted
        money = 0
        magnum = 0 
        bullnum = 0 
        enemies_killed = 0 
        questions_attempted = 0
        with open("textfile.txt","w") as file:
            name = name_entry.get()
            if not len(name.strip()) == 0:
                make_label(step_2, "save name " + str(name) + " has been created")
                file.writelines(f'savename : {name}\n')
                file.writelines(f'money : {money}\n')
                file.writelines(f'enemies_killed : {enemies_killed}\n')
                file.writelines(f'playerspeed : {magnum}\n')
                file.writelines(f'bulletdamage : {bullnum}\n')
                file.writelines(f'questionseasy : {0}\n')
                file.writelines(f'questionhard: {0}\n')
            if  len(name.strip()) == 0:
                make_label(step_2, "name length cannot be zero")






    def bullet_cost():
        with open("textfile.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if "bulletdamage" in line:
                    parts = line.split()
                    bullet_num= parts[2]      
                    if int(bullet_num) == 0:
                        return 50
                    elif int(bullet_num) == 1:
                        return  200
                    elif int(bullet_num) == 2:
                        return 400
                    elif int(bullet_num)  == 3:
                        return "max"
    def speed_cost():
        with open("textfile.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if "playerspeed" in line:
                    parts = line.split()
                    magazine_num = parts[2]      
                    if int(magazine_num)  == 0:
                        return 50
                    elif int(magazine_num) == 1:
                        return  200
                    elif int(magazine_num)  == 2:
                        return 400
                    elif int(magazine_num)  == 3:
                        return "max"

        

    def get_money():
        #getting money
        with open("textfile.txt", "r") as file:
            for line in file:
                if "money" in line:
                    bull_line = line
                    bull_num =  bull_line.split()[2]
                    return bull_num
    def shop_display():
        global money
        clear_screen(main_screen)
        show_frame(shop_screen)
        print("shop")

        money =get_money()
        make_label(shop_screen, "Total money: " + str(money))
        make_label(shop_screen, f'Upgrade type: player speed , Cost: {speed_cost()}')
        make_button(shop_screen, find_num("playerspeed"), lambda: level_up("playerspeed"))
        make_label(shop_screen, f'Upgrade type: player bullet damage , Cost: {bullet_cost()}')
        make_button(shop_screen,find_num("bulletdamage"),lambda: level_up("bulletdamage"))

        backhome_button(shop_screen)


    def find_num(word):
            with open("textfile.txt", "r") as file:
                for line in file:
                    if  str(word) in line: 
                        parts = line.split()
                        return str(parts[2])


    def backhome_button(screen_n):
        make_button(screen_n, "Back to Main Menu", lambda:backhome(screen_n))




    def level_up(var_name):
        with open("textfile.txt","r") as file:
            all_lines = file.readlines()
            money = get_money()
            for i, line in enumerate(all_lines):
                if var_name in line:
                    parts = line.split()
                    current_level = int(parts[2])  # ADD int() HERE
                    if var_name == "playerspeed":
                        actual_cost = speed_cost()
                    elif var_name == "bulletdamage":
                        actual_cost = bullet_cost()
                    
                    # Check if already maxed
                    if actual_cost == "max":  # ADD THIS CHECK
                        return
                    
                    if int(money) >= int(actual_cost):  # REMOVE: and current_level < 3
                        parts[2] = str(int(parts[2]) + 1)
                        all_lines[i] = " ".join(parts) + "\n"

                        for j, money_line in enumerate(all_lines):
                            if "money" in money_line:
                                money_parts = money_line.split()
                                new_money = int(money) - int(actual_cost)
                                money_parts[2] = str(new_money)
                                all_lines[j] = " ".join(money_parts) + "\n"

                        with open("textfile.txt","w") as file:
                            file.writelines(all_lines)
                            print("bought")
                            break
        
        clear_screen(shop_screen)
        shop_display()
        show_frame(shop_screen)
                    
  





                    

    def backhome(screen_n):
        clear_screen(screen_n)
        show_frame(main_screen)
        lobby()

    def settings():
        print("settings")
        clear_screen(main_screen)
        show_frame(settings_screen)
        settings_display()

    def shop():
        clear_screen(main_screen)
        show_frame(shop_screen)
        shop_display()
    def off_on_pressed():
        global pressed_counter, sound_text
        pressed_counter += 1
        sound_text = "off"
        if pressed_counter % 2: 
            sound_text = "on"
        elif not pressed_counter % 2:
            sound_text = "off"
        clear_screen(settings_screen)
        settings_display()
        
        print(pressed_counter)
        return pressed_counter, sound_text



    #a box at start in middle of screen 
    #if textfile has a save, write that in the box 
    #if not say create new save 
    step1_screen()


    show_frame(step_1)
    root.mainloop() 

    #no save 
    #create save 
    # moves you to username 
    #then in the box it will say your name 

    # if save is clicked takes to lobby
startofgame()
