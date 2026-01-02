import tkinter as tk
import json
import os
from PIL import Image, ImageTk
import tkinter as tk   

import datalogger
revive_unlocked = False
money_unlocked = False



image_refs = {}
def death_display(root):
    root.geometry("800x800")
    

    should_revive = [False]  
    should_continue = [True]


    def on_closing():
        should_revive[0] = False
        should_continue[0] = False
        root.quit() 
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    def show_frame(frame):
        frame.tkraise()

    def clear_screen(screen_name):
        for widget in screen_name.winfo_children():
            widget.destroy()

    def make_button_grid(screen_name, button_text, command_text,x, y):
        button = (tk.Button(screen_name ,text = button_text,command = command_text, font = ("Arial", 12)))
        button.grid(column= x, row = y)
        return button
        
    def make_label_grid(screen_name, label_text,x, y): 
        label = (tk.Label(screen_name, text = label_text, font = ("Arial", 12)))
        label.grid(column= x, row = y)
        return label

    def find_line(name):
        with open("textfile.txt","r") as file:
            lines = file.readlines()
            counter = 0 
            for line in lines:
                counter += 1
                if name in line:
                    return line

    dead_screen = tk.Frame(root)
    for frame in (dead_screen,):
        frame.grid(row = 0, column = 0)

    def open_datalogger():
        clear_screen(dead_screen)

        def back_to_death():
            clear_screen(dead_screen)
            deadscreen_display()
            dead_screen.tkraise()
        datalogger.datalogger("death", root, callback=back_to_death)

    def unlock_revive():
        print("pressed")
        global revive_unlocked
        if datalogger.three_questions_answered:
            revive_unlocked = True
            clear_screen(dead_screen)
            deadscreen_display()
            return revive_unlocked

    def unlock_money():
        print("pressed")
        global money_unlocked
        if datalogger.three_questions_answered:
            money_unlocked = True
            clear_screen(dead_screen)
            deadscreen_display()
            return money_unlocked

    def show_money_button(unlocked):
        if not unlocked:
            money_locked = Image.open("images/money_locked.png")
            width, height = money_locked.size
            money_locked = money_locked.resize((width //4 , height //4))
            money_locked_picture= ImageTk.PhotoImage(money_locked)
            image_refs['money_locked'] = money_locked_picture
            money_locked_button = tk.Button(dead_screen, image=money_locked_picture, command= lambda:unlock_money(), borderwidth=0)
            money_locked_button.grid(column=3, row = 3)
        elif  unlocked:
            money_unlocked = Image.open("images/money_unlocked.png")
            width, height = money_unlocked.size
            money_unlocked = money_unlocked.resize((width //4 , height //4))
            money_unlocked_picture= ImageTk.PhotoImage(money_unlocked)
            image_refs['money_unlocked_picrture'] = money_unlocked_picture
            money_unlocked_button = tk.Button(dead_screen, image=money_unlocked_picture, command=lambda:double_money(), borderwidth=0)
            money_unlocked_button.grid(column=3, row = 3)

    def show_revive_button(unlocked):
        if not unlocked:
            revive_locked = Image.open("images/revive_locked.png")
            width, height = revive_locked.size
            revive_locked = revive_locked.resize((width //4 , height //4))
            revive_locked_picture= ImageTk.PhotoImage(revive_locked)
            image_refs['revive_locked'] = revive_locked_picture
            revive_locked_button = tk.Button(dead_screen, image=revive_locked_picture, command=lambda:unlock_revive(), borderwidth=0)
            revive_locked_button.grid(column=0, row = 3)
        elif  unlocked:
            revive_unlocked = Image.open("images/revive_unlocked.png")
            width, height = revive_unlocked.size
            revive_unlocked = revive_unlocked.resize((width //4 , height //4))
            revive_unlocked= ImageTk.PhotoImage(revive_unlocked)
            image_refs['revive_unlocked'] = revive_unlocked
            revive_unlocked_button = tk.Button(dead_screen, image=revive_unlocked, command=lambda:revive(), borderwidth=0)
            revive_unlocked_button.grid(column=0, row = 3)

    flaschards_completed = False
    def deadscreen_display():
        global revive_unlocked, money_unlocked
        global flaschards_completed
        with open("textfile.txt","r") as file:
            all_Lines = file.readlines()
            for line in all_Lines:
                if "questions_attempted" in line:
                    parts = line.split()
                    questions_attempted = parts[2]
                    if int(questions_attempted) == 3:
                        print("Flaschards completed")
                        flaschards_completed = True

        
        show_revive_button(revive_unlocked)
        show_money_button(money_unlocked)

        l1 = make_label_grid(dead_screen , "Attempt Flashcards to unlock",2,2)
        l1.grid(column = 2 , row = 1 )

        l2 = make_button_grid(dead_screen, "Go to Flaschards", lambda: open_datalogger(),2,3)
        l2.grid(column =2, row = 2)

        if datalogger.three_questions_answered: 
            l1 = make_label_grid(dead_screen , "Have key to unlock",2,2)
            l1.grid(column = 2 , row = 4)
        elif not datalogger.three_questions_answered:
            l1 = make_label_grid(dead_screen , "No key to unlock",2,2)
            l1.grid(column = 2 , row = 4 )

    def revive():
        print("revived")
        if datalogger.three_questions_answered:
            should_revive[0] = True
            should_continue[0] = False
            root.quit()  # Stop mainloop, don't destroy
    
    def double_money():
        print("doubled money")
        if datalogger.three_questions_answered:
            should_revive[0] = False
            should_continue[0] = False
            root.quit()  # Stop mainloop

    deadscreen_display()
    dead_screen.tkraise()
    show_frame(dead_screen)

    try:
        root.mainloop()
    except:
        pass

    return should_revive[0]