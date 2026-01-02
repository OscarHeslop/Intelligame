import tkinter as tk
import json
import os
from PIL import Image, ImageTk
from tkinter import PhotoImage

from datetime import datetime, timedelta

def save_data(data):
        with open("flashcards.json", "w") as file:
            json.dump(data, file, indent=4)
            

def load_or_create_data():
    if os.path.exists("flashcards.json"):
        # File exists - load it
        try:
            with open("flashcards.json", "r") as file:
                return json.load(file)  # Returns your existing data
        except:
            # File is corrupted - create new
            return {"decks": {}}
    else:
        # File doesn't exist - create new structure
        return {"decks": {}}
#code added for spaced repetition algorithm




def calculate_EF(card_id, deck_name):
    data = load_or_create_data()
    for card in data["decks"][deck_name]["cards"]:
        if card["id"] == card_id:
            if card["performance"] == "easy":
                performance = 5
            elif card["performance"] == "medium":
                performance = 4
            elif card["performance"] == "hard":
                performance = 2
            elif card["performance"] == "again":
                performance = 1
            else:
                performance = 3

            # Handle "again" - reset progress
            if card["performance"] == "again":
                card["repetition"] = 0 
                card["interval"] = 1
                # Still update EF even on "again"
                new_EF = card["EF"] + (0.1 - (5 - performance) * (0.08 + (5 - performance) * 0.02))
                card["EF"] = max(min(new_EF, 3.0), 1.5)
            else:
                card["repetition"] += 1
                
                # ✨ ALWAYS calculate new EF, regardless of repetition
                new_EF = card["EF"] + (0.1 - (5 - performance) * (0.08 + (5 - performance) * 0.02))
                card["EF"] = max(min(new_EF, 3.0), 1.5)
                
                # Set interval based on repetition count
                if card["repetition"] == 1:
                    card["interval"] = 1
                elif card["repetition"] == 2:
                    card["interval"] = 6
                else:
                    # Use EF for interval calculation
                    card["interval"] = round(card["interval"] * card["EF"])
            
            # Calculate next review date
            next_review = datetime.now() + timedelta(days=int(card["interval"]))
            card["next_revise"] = next_review.isoformat()
            break
    
    save_data(data)

                         

def is_due(self):
    return datetime.now() >= self.next_review

#repetition = 0 
#interval = 1 
#else
#repetition += 1 








import os
three_questions_answered = False
def datalogger(state, root, callback=None):
    root.geometry("800x400")
    questions_attempted =  [] 

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    datalogger_screen = tk.Frame(canvas)

    datalogger_screen.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=datalogger_screen, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    #-------------------------------------------------------------Temporary code 
    def clear_screen(screen_name):
        for widget in screen_name.winfo_children():
            widget.destroy()

    def make_button(screen_name, button_text, command_text,):
        button = (tk.Button(screen_name ,text = button_text,command = command_text, font = ("Arial", 12)))
        button.pack()
        return button
    def make_label(screen_name, label_text, ): 
        label = (tk.Label(screen_name, text = label_text, font = ("Arial", 12)))
        label.pack()
        return label

    #-------------------------------------------
    def create_pie_chart(deck_name, parent_frame):
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import matplotlib.pyplot as plt
        
        # Load data from JSON
        data = load_or_create_data()
        cards = data["decks"][deck_name]["cards"]
        
        if len(cards) < 0:
            return  
        
        # Count difficulties
        difficulty_counts = {
            "not_answered": 0,
            "green": 0,
            "yellow": 0,
            "orange": 0,
            "red": 0
        }
        
        for card in cards:
            difficulty = card.get("difficulty", "green")
            attempted = card.get("attempted", False)

            if not attempted:
                difficulty_counts["not_answered"] += 1
            else:
                if difficulty == "green":
                    difficulty_counts["green"] += 1
                elif difficulty == "yellow":
                    difficulty_counts["yellow"] += 1
                elif difficulty == "orange":
                    difficulty_counts["orange"] += 1
                elif difficulty == "red":
                    difficulty_counts["red"] += 1
        

        labels = []
        sizes = []
        colors_list = []
        
        color_map = {
            "not_answered": ("#808080", "Not Answered"),   
            "green": ("#4CAF50", "Green"),
            "yellow": ("#FFEB3B", "Yellow"),
            "orange": ("#FF9800", "Orange"),
            "red": ("#F44336", "Red")
        }
        

        for diff_name, count in difficulty_counts.items():
            if count >= 1:  # Only show if at least 1 card
                color_hex, label_name = color_map[diff_name]
                sizes.append(count)
                colors_list.append(color_hex)
        
        fig, ax = plt.subplots(figsize=(1.5, 1.5))
        if sizes:
            ax.pie(sizes, colors=colors_list, startangle=90)
            ax.set_title(f'{len(cards)} flashcards', fontsize=10)
        
        # Embed in tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=5)


    def flashcards_display():
        clear_screen(datalogger_screen)
        #ask for name of deck 
        root.deiconify() 
        #new screen
        make_button(datalogger_screen, "CREATE DECK", create_deck)

        make_label(datalogger_screen, "All Decks")
        data = load_or_create_data()
        for deck_names in data["decks"]:
            make_button(datalogger_screen, deck_names, lambda name=deck_names: take_to_deck(name))
            create_pie_chart(deck_names, datalogger_screen)
        make_button(datalogger_screen, "GO BACK LOBBY", go_back_lobby)

    def go_back_lobby():
        clear_screen(datalogger_screen)
        root.destroy()  # Properly close the window
        if callback:
            callback()










  

    file = "flashcards.json"
    current_deck = None
    def show_frame(frame):
        frame.tkraise()

    def back_datalogger():
        make_button(datalogger_screen, "Back to datalogger", lambda:s())
    def s():
        clear_screen(datalogger_screen)
        flashcards_display()


 



    def datalogger_dislay():
        print("hello")
    #---------------------------------------


    
    def create_deck():
        global deck_name, difficulty_images
        clear_screen(datalogger_screen)
        make_label(datalogger_screen, "deck name")
        deck_name = tk.Entry(datalogger_screen)
        deck_name.pack()
        make_button(datalogger_screen, "Save Deck", deckname_save)

        back_datalogger()

        
    def deckname_save():
        val = deck_name.get()
        #check if deckname in there
        data = load_or_create_data()
        if len(val) == 0:
            make_label(datalogger_screen, "Deckname cannot be empty")
            print("Deckname cannot be empty")
        elif val in data["decks"]: #checks that specific category of json file
            print("Deck name already exists")
            make_label(datalogger_screen, "Deck name already exists")
        elif val not in data["decks"]:
            make_label(datalogger_screen, "Successfully created deck "+val)
            data["decks"][val] = {
                "cards": []
            }

        #update json file
        save_data(data)



        

    #-----------------------------------------
    #add section under which dislpays all flaschards in text file
    #use json better at storing data 
    #id = 
    #quesion = ""
    #anwser = ""
    #incorrect_count
    #difficulty - "easy" - hard 
    selected_difficulty = None
    attempted_save_flashcard = None
    def add(): # creates new flashcard 
        global selected_difficulty, attempted_save_flashcard, img1, img2, img3,img4
        selected_difficulty = None

        


        global question_entry, answer_entry
        clear_screen(datalogger_screen)
        make_label(datalogger_screen, "Quesion")
        question_entry = tk.Entry(datalogger_screen)
        question_entry.pack()
        
        difficulty_images = []
        make_label(datalogger_screen, "Answer")
        answer_entry = tk.Entry(datalogger_screen)
        answer_entry.pack()

        #from tkinter import PhotoImage
        button_frame = tk.Frame(datalogger_screen)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Load and store images
        img1 = Image.open("images/1d.png")
        img1 = img1.resize((100, 100))
        green = ImageTk.PhotoImage(img1)
        difficulty_images.append(green)

        img2 = Image.open("images/2d.png")
        img2 = img2.resize((100, 100))
        yellow = ImageTk.PhotoImage(img2)
        difficulty_images.append(yellow)

        img3 = Image.open("images/3d.png")
        img3 = img3.resize((100, 100))
        orange = ImageTk.PhotoImage(img3)
        difficulty_images.append(orange)
        
        img4 = Image.open("images/4d.png")
        img4 = img4.resize((100, 100))
        red = ImageTk.PhotoImage(img4)
        difficulty_images.append(red)
        button_frame = tk.Frame(datalogger_screen)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        # Create buttons with pack in button_frame
        button1 = tk.Button(button_frame, image=green, command=lambda: green_d())
        button1.image = green
        button1.pack(side=tk.LEFT, padx=10)

        button2 = tk.Button(button_frame, image=yellow, command=lambda: yellow_d())
        button2.image = yellow
        button2.pack(side=tk.LEFT, padx=10)

        button3 = tk.Button(button_frame, image=orange, command=lambda: orange_d())
        button3.image = orange
        button3.pack(side=tk.LEFT, padx=10)

        button4 = tk.Button(button_frame, image=red, command=lambda: red_d())
        button4.image = red
        button4.pack(side=tk.LEFT, padx=10)





        def green_d():
            global selected_difficulty, img1
            selected_difficulty = "green"
            make_label(datalogger_screen, "green picked")
        def yellow_d():
            global selected_difficulty, img2
            selected_difficulty = "yellow"
            make_label(datalogger_screen, "yellow picked")

        def orange_d():
            global selected_difficulty,img3
            selected_difficulty = "orange"
            make_label(datalogger_screen, "orange picked")
        def red_d():
            global selected_difficulty,img4
            selected_difficulty = "red"
            make_label(datalogger_screen, "red picked")

            
        
        
        #https://www.geeksforgeeks.org/python/python-add-image-on-a-tkinter-button/

        #submit button
        submit = make_button(datalogger_screen, "Save flaschcard", save_flashcard)
        
        #back to data logger button
        back_datalogger()
        return selected_difficulty





    def save_flashcard():
        global current_deck, selected_difficulty

        save_question = question_entry.get() 
        save_answer = answer_entry.get()
        data = load_or_create_data()
        
        
        if len(save_question) == 0: 
            make_label(datalogger_screen, "Question must not be empty")
            return
        if len(save_answer) == 0:
            make_label(datalogger_screen, "Answer must not be empty")
            return

        if selected_difficulty is None:
            make_label(datalogger_screen, "To create flashcard, must first select a difficulty :)")
            return
        


        #create new id
        if len(save_question) == 0 or len(save_answer) == 0:
            make_label(datalogger_screen, "quesion or answer cannot be empty")
        
        if current_deck in data["decks"]:
            all_cards = data["decks"][current_deck]["cards"]
            next_id = len(all_cards) + 1

            #new card structure
            new_card = {
                    "id": next_id,
                    "question": save_question,
                    "answer": save_answer,
                    "attempted": False, 
                    "difficulty": selected_difficulty,
                    "performance": None,
                    "interval":1,
                    "EF": 2.5,  # starts at 2.5 for SM2 
                    "repetition": 0, #num times answered
                    "next_revise":datetime.now().isoformat(),#want revise same day made
                    
            }
            data["decks"][current_deck]["cards"].append(new_card)
                
            # Save data
            save_data(data)
            make_label(datalogger_screen, "added flaschard to deck")

            #clears the entry
            # Clear entries
            question_entry.delete(0, tk.END)
            answer_entry.delete(0, tk.END)
            selected_difficulty = None # to reset the difficulty each time
        else:
            make_label(datalogger_screen, "No deck selected")

        
#!----------------------------------------------------------------------------
#!                   Correct / Incorrect 
#!--------------------------------------------------------------------------------
    easy_question = []
    hard_question  = []
    questions_attempted = []

    def go_back():
        clear_screen(datalogger_screen)
        if callback:
            callback()

        make_button(datalogger_screen, "Go back to game", go_back)
    def question_type(difficulty, name_of_deck, current_card):
        global three_questions_answered 
        
        data = load_or_create_data()
        for card in data["decks"][name_of_deck]["cards"]:
            if card["id"] == current_card["id"]:
                card["attempted"] = True
                card["performance"] = difficulty
                break
        save_data(data)

        calculate_EF(current_card["id"], name_of_deck)
        
        # Update difficulty color AFTER calculate_EF
        data = load_or_create_data()
        for card in data["decks"][name_of_deck]["cards"]:
            if card["id"] == current_card["id"]:
                if difficulty == "easy":
                    card["difficulty"] = "green"
                elif difficulty == "hard":
                    card["difficulty"] = "orange"
                elif difficulty == "again":
                    card["difficulty"] = "red"
                break
        save_data(data)

        if difficulty == "easy":
            easy_question.append(current_card)
        elif difficulty == "hard":
            hard_question.append(current_card)
        
        if current_card["id"] not in questions_attempted:
            questions_attempted.append(current_card["id"])
            if len(questions_attempted) >= 3:
                clear_screen(datalogger_screen)
                import death_screen
                make_label(datalogger_screen, "Congratulations, You have completed 3 flashcards")
                make_label(datalogger_screen, "Your choice:")
                make_button(datalogger_screen, "Go back to game", lambda:go_back())
                make_button(datalogger_screen, "Continue revising", lambda: start_revise(name_of_deck))
                back_datalogger()
                three_questions_answered = True
            else:
                start_revise(name_of_deck)

                        
                        
        
 

#!-------------------------------------------------------------------------------- correct / Incorrect END
    def show_answer(name_of_deck, current_card):
        clear_screen(datalogger_screen)


        current_anwser = "Not Found"
        #show question and ansqwer
        current_question = current_card["question"]
        current_answer = current_card["answer"]


        data = load_or_create_data()
        for card in data["decks"][name_of_deck]["cards"]:
            if card["question"] == current_question:
                current_answer = card["answer"]
                break

        make_label(datalogger_screen, current_question)
        make_label(datalogger_screen, "------------------------------")
        make_label(datalogger_screen, current_answer)
        
        #once show answer has been pressed
        #ask if easy or hard
        make_button(datalogger_screen, "Easy", lambda:question_type("easy", name_of_deck, current_card))
        make_button(datalogger_screen, "Hard", lambda:question_type("hard", name_of_deck, current_card))
        make_button(datalogger_screen, "Again", lambda:question_type("again", name_of_deck, current_card))


        #get the deckame 
        #get the card
        #display cards answer

    def start_revise(name_of_deck):
        #show a random quesion at start
        clear_screen(datalogger_screen)
        data = load_or_create_data()
        due_cards = []
        from datetime import datetime
        #from all decks have - randomly pick from ones due
        for cards in data["decks"][name_of_deck]["cards"]:
            if datetime.now() >= datetime.fromisoformat(cards["next_revise"]):
                due_cards.append(cards)
                
        if len(due_cards) != 0:
            import random
            card = random.choice(due_cards)  # Pick random from remaining cards
            make_label(datalogger_screen, f'{card["question"]}')
            make_button(datalogger_screen, "Show answer", lambda: show_answer(name_of_deck, card))
        else:
            make_label(datalogger_screen, "No Flashcards to do now")
            back_datalogger()



    def revise_revive():
        #display datalogger scren
        clear_screen(datalogger_screen)
        make_label(datalogger_screen, "Decks below have been filtered to have 3 or more flaschards")
        make_label(datalogger_screen, "Pick a deck")
        filtered_decks = []
        data = load_or_create_data()
        for deck in data["decks"]:
            num_cards = len(data["decks"][deck]["cards"])
            if num_cards >=  3:
                filtered_decks.append(deck)

        for deck in filtered_decks:
            make_button(datalogger_screen, deck, lambda name=deck: start_revise(name))
        if len(filtered_decks) == 0:
            print("no decks have 3 or more flaschards")
        back_datalogger()    

    #new code 
    import matplotlib

#!-------------------------------------------------------------------------------------------------------------------
#!-------------------------------------------------------------------------------------------------------------------
#!-------------------------------------------------------------------------------------------------------------------
#!-------------------------------------------------------------------------------------------------------------------
#!-------------------------------------------------------------------------------------------------------------------
#!-------------------------------------------------------------------------------------------------------------------
#!-------------------------------------------------------------------------------------------------------------------
#!-------------------------------------------------------------------------------------------------------------------
#!-------------------------------------------------------------------------------------------------------------------
#!-------------------------------------------------------------------------------------------------------------------

    def take_to_deck(name_of_deck):
        global current_deck
        current_deck = name_of_deck
        data = load_or_create_data()
        clear_screen(datalogger_screen)

        make_label(datalogger_screen, name_of_deck)
        make_button(datalogger_screen, "Start revising", lambda:start_revise(name_of_deck))

        make_button(datalogger_screen, f'ADD TO DECK', add)
        if data["decks"][name_of_deck]["cards"]:
            for card in data["decks"][name_of_deck]["cards"]:
                make_label(datalogger_screen, f'{card["question"]},{card["answer"]}')
        else:
            make_label(datalogger_screen, "No cards in Deck")

        back_datalogger()
        current_deck = name_of_deck
        return current_deck
    
    # Initialize the screen
    show_frame(datalogger_screen)



    # Check where we're being called from
    if state == "death":
        revise_revive()  # Death screen: show revive interface  # Main menu or direct: show full interface
        
    else:
        flashcards_display()
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Flashcards Datalogger")
    # You can choose a default state, e.g., "main" or "death"
    datalogger("main", root)
    root.mainloop()
