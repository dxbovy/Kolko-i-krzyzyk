import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

root = ctk.CTk()
root.title("Kółko i krzyżyk")

root.resizable(True, True)
root.update()

try:
    root.state('zoomed')
except tk.TclError:
    root.attributes('-zoomed', True)

ctk.set_appearance_mode("dark")
field_size = 3
win_condition = 3

field = []
virtual_field = [["" for _ in range(field_size)] for _ in range(field_size)]

menu_frame = None
game_frame = None
nav_frame = None
botStarts = None

fieldSizeEntry = None
winConditionEntry = None
error_label = None

game_over = False

def playersMove(row, col):
    global game_over

    if game_over:
        return

    button = field[row][col]
    if button.cget("text") == "":
        button.configure(text="O")
        virtual_field[row][col] = "O"

        if check_win_at(row, col, "O"):
            print("Wygrałeś!")
            game_over = True
            return
            
        if isMovesLeft() == False:
            print("Remis")
            game_over = True
            return
            
        root.update()

        aisMove()


def aisMove():
    global game_over
    
    i, j = findBestMove()
    print("Tura przeciwnika")

    field[i][j].configure(text="X")
    virtual_field[i][j] = "X"
    
    if check_win_at(i, j, "X"):
        print("Bot wygrał")
        game_over = True
        return
        
    if isMovesLeft() == False:
        print("Remis!")
        game_over = True
        return
    

def check_win_at(row, col, sign):
    # Sprawdzanie w poziomie [_]
    counter = 1
    for i in range(1, win_condition):
        if col+i < field_size and sign == virtual_field[row][col+i]: counter += 1
        else: break
    for i in range(1, win_condition):
        if col-i >= 0 and sign == virtual_field[row][col-i]: counter += 1
        else: break
    if counter >= win_condition:
        field[row][col].configure(bg="red")
        for i in range(1, win_condition):
            if col-i >= 0 and sign == field[row][col-i]["text"]: field[row][col-i].configure(bg="red")
            if col+i < field_size and sign == field[row][col+i]["text"]: field[row][col+i].configure(bg="red")
        return True

    # Sprawdzanie w pionie [|]
    counter = 1
    for i in range(1, win_condition):
        if row+i < field_size and sign == virtual_field[row+i][col]: counter += 1
        else: break
    for i in range(1, win_condition):
        if row-i >= 0 and sign == virtual_field[row-i][col]: counter += 1
        else: break
    if counter >= win_condition:
        field[row][col].configure(bg="red")
        for i in range(1, win_condition):
            if row+i < field_size and sign == field[row+i][col]["text"]: field[row+i][col].configure(bg="red")
            if row-i >= 0 and sign == field[row-i][col]["text"]: field[row-i][col].configure(bg="red")
        return True

    # Sprawdzanie w skosie [\]
    counter = 1
    for i in range(1, win_condition):
        if row+i < field_size and col+i < field_size and sign == virtual_field[row+i][col+i]: counter += 1
        else: break
    for i in range(1, win_condition):
        if row-i >= 0 and col-i >= 0 and sign == virtual_field[row-i][col-i]: counter += 1
        else: break
    if counter >= win_condition:
        field[row][col].configure(bg="red")
        for i in range(1, win_condition):
            if row-i >= 0 and col-i >= 0 and sign == field[row-i][col-i]["text"]: field[row-i][col-i].configure(bg="red")
            if row+i < field_size and col+i < field_size and sign == field[row+i][col+i]["text"]: field[row+i][col+i].configure(bg="red")
        return True

    # Sprawdzanie w skosie [/]
    counter = 1
    for i in range(1, win_condition):
        if row+i < field_size and col-i >= 0 and sign == virtual_field[row+i][col-i]: counter += 1
        else: break
    for i in range(1, win_condition):
        if row-i >= 0 and col+i < field_size and sign == virtual_field[row-i][col+i]: counter += 1
        else: break
    if counter >= win_condition:
        field[row][col].configure(bg="red")
        for i in range(1, win_condition):
            if row+i < field_size and col-i >= 0 and sign == field[row+i][col-i]["text"]: field[row+i][col-i].configure(bg="red")
            if row-i >= 0 and col+i < field_size and sign == field[row-i][col+i]["text"]: field[row-i][col+i].configure(bg="red")
        return True

    return False

def evaluate():
    total_score = 0

    # Sprawdzanie w poziomie [_]
    for i in range(field_size):
        for j in range(field_size - win_condition + 1):
            x_count = 0
            o_count = 0
            for k in range(win_condition):
                cell = virtual_field[i][j+k]
                if cell == "X": x_count += 1
                elif cell == "O": o_count += 1
                
                # Wczesne wyjście: jeśli są oba znaki, linia jest zablokowana - szkoda czasu na resztę
                if x_count > 0 and o_count > 0:
                    break 
            
            # Punktacja tylko, jeśli pętla nie została przerwana jako zablokowana
            if x_count > 0 and o_count == 0:
                if x_count == win_condition: return 100000
                total_score += x_count ** 4
            elif o_count > 0 and x_count == 0:
                if o_count == win_condition: return -100000
                total_score -= (o_count ** 5)

    # Sprawdzanie w pionie [|]
    for j in range(field_size):
        for i in range(field_size - win_condition + 1):
            x_count = 0
            o_count = 0
            for k in range(win_condition):
                cell = virtual_field[i+k][j]
                if cell == "X": x_count += 1
                elif cell == "O": o_count += 1
                
                if x_count > 0 and o_count > 0:
                    break
            
            if x_count > 0 and o_count == 0:
                if x_count == win_condition: return 100000
                total_score += x_count ** 4
            elif o_count > 0 and x_count == 0:
                if o_count == win_condition: return -100000
                total_score -= (o_count ** 5)

    # Sprawdzanie w skosie [\]
    for i in range(field_size - win_condition + 1):
        for j in range(field_size - win_condition + 1):
            x_count = 0
            o_count = 0
            for k in range(win_condition):
                cell = virtual_field[i+k][j+k]
                if cell == "X": x_count += 1
                elif cell == "O": o_count += 1
                
                if x_count > 0 and o_count > 0:
                    break
            
            if x_count > 0 and o_count == 0:
                if x_count == win_condition: return 100000
                total_score += x_count ** 4
            elif o_count > 0 and x_count == 0:
                if o_count == win_condition: return -100000
                total_score -= (o_count ** 5)

    # Sprawdzanie w skosie [/]
    for i in range(win_condition - 1, field_size):
        for j in range(field_size - win_condition + 1):
            x_count = 0
            o_count = 0
            for k in range(win_condition):
                cell = virtual_field[i-k][j+k]
                if cell == "X": x_count += 1
                elif cell == "O": o_count += 1
                
                if x_count > 0 and o_count > 0:
                    break
            
            if x_count > 0 and o_count == 0:
                if x_count == win_condition: return 100000
                total_score += x_count ** 4
            elif o_count > 0 and x_count == 0:
                if o_count == win_condition: return -100000
                total_score -= (o_count ** 5)

    return total_score

def isMovesLeft():
    for i in range(field_size) :
        for j in range(field_size) :
            if (virtual_field[i][j] == "") :
                return True 
    return False

def minimax(depth, isMax, alpha, beta, max_depth):
    score = evaluate()
    
    if score >= 90000:
        return score - depth
    if score <= -90000:
        return score + depth
        
    if isMovesLeft() == False:
        return 0
    
    if depth == max_depth:
        return score
    
    if isMax:
        best = -100000

        for i in range(field_size):
            for j in range(field_size):
                if virtual_field[i][j] == "":
                    virtual_field[i][j] = "X"

                    best = max(best, minimax(depth+1, not isMax, alpha, beta, max_depth))
                    
                    virtual_field[i][j] = ""

                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return best
    else:
        best = 100000
        for i in range(field_size):
            for j in range(field_size):
                if virtual_field[i][j] == "":
                    virtual_field[i][j] = "O"

                    best = min(best, minimax(depth+1, not isMax, alpha, beta, max_depth))
                    
                    virtual_field[i][j] = ""
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return best
        
                        

def findBestMove():
    global field_size
    bestVal = -100000
    bestMove = (-1, -1)
    alpha = -100000
    beta = 100000

    if field_size == 3: max_depth = 9
    elif field_size == 4: max_depth = 5
    elif field_size >= 5: max_depth = 4


    for i in range(field_size):
        for j in range(field_size):
            if(virtual_field[i][j] == ""):
                virtual_field[i][j] = 'X'
                moveVal = minimax(0, False, alpha, beta, max_depth)
                virtual_field[i][j] = ''
                if (moveVal > bestVal) :                
                    bestMove = (i, j)
                    bestVal = moveVal
                alpha = max(alpha, bestVal)
    return bestMove

def createMenu():
    global menu_frame, game_frame, nav_frame
    global fieldSizeEntry, winConditionEntry
    global botStarts
    global error_label

    botStarts = tk.BooleanVar(value=False)

    if game_frame:
        game_frame.destroy()
    if nav_frame:
        nav_frame.destroy()

    menu_frame = ctk.CTkFrame(root, 
                              fg_color="#242424", 
                              border_width=3, 
                              border_color="#444444", 
                              corner_radius=15)
    menu_frame.pack(padx=20, pady=20)

    lbl = ctk.CTkLabel(menu_frame, text="Podaj ile na ile ma być pole:", fg_color="#444444", corner_radius=15, text_color="white")
    lbl.pack(padx=20, pady=20)
    fieldSizeEntry = ctk.CTkEntry(menu_frame,
                                  fg_color="#1A1A1A",
                                  text_color="white",
                                  border_color="#444444",
                                  border_width=2,
                                  corner_radius=8,
                                  justify="center",
                                  font=("Arial", 14))
    fieldSizeEntry.pack(pady=5)
    fieldSizeEntry.insert(0, field_size)

    lbl = ctk.CTkLabel(menu_frame, text="Podaj warunek zwycięstwa (ile pod rząd):", fg_color="#444444", corner_radius=15, text_color="white")
    lbl.pack(padx=20, pady=20)
    winConditionEntry = ctk.CTkEntry(menu_frame,
                                     fg_color="#1A1A1A",
                                     text_color="white",
                                     border_color="#444444",
                                     border_width=2,
                                     corner_radius=8,
                                     justify="center",
                                     font=("Arial", 14))
    winConditionEntry.pack(pady=5)
    winConditionEntry.insert(0, win_condition)

    whoStarts = ctk.CTkCheckBox(menu_frame,
                                text="Zaczyna bot",
                                variable=botStarts,
                                onvalue=True,
                                offvalue=False,
                                font=("Arial", 16),
                                text_color="white") 
    whoStarts.pack(padx=20, pady=20)

    error_label = ctk.CTkLabel(menu_frame, 
                               text="", 
                               text_color="#FF4C4C",
                               font=("Arial", 14, "bold"))
    error_label.pack(pady=(0, 10))

    playButton = ctk.CTkButton(menu_frame, 
                               text="Graj", 
                               command=createField,
                               font=("Arial", 24, "bold"),
                               fg_color="#2FA572",
                               hover_color="#106A43",
                               text_color="white",
                               corner_radius=15,
                               border_width=3,
                               border_color="#106A43",
                               width=150, 
                               height=50,
                               cursor="hand2")
    playButton.pack(pady=20)



def createField():
    global menu_frame, game_frame, nav_frame
    global field_size, win_condition, field, virtual_field
    global game_over
    global botStarts
    global error_label
    

    try:
        temp_field = int(fieldSizeEntry.get())
        temp_win = int(winConditionEntry.get())
    except ValueError:
        error_label.configure(text="Wprowadź poprawne liczby całkowite!")
        return

    if temp_field < 3 or temp_field > 10:
        error_label.configure(text="Rozmiar planszy musi wynosić od 3 do 10!")
        return

    if temp_win < 2:
        error_label.configure(text="Warunek wygranej musi wynosić minimum 2!")
        return

    if temp_win > temp_field:
        error_label.configure(text=f"Warunek wygranej ({temp_win}) nie może być większy niż plansza ({temp_field})!")
        return

    field_size = temp_field
    win_condition = temp_win

    game_over = False
    field = []
    virtual_field = [["" for _ in range(field_size)] for _ in range(field_size)]

    if menu_frame:
        menu_frame.destroy()

    game_frame = ctk.CTkFrame(root, 
                            fg_color="#444444",
                            border_width=0, 
                            corner_radius=3)
    game_frame.pack(padx=20, pady=20)


    if field_size <= 6:
        b_font = ("Arial Black", 24)
    elif field_size <= 6:
        b_font = ("Arial Black", 18)
    elif field_size <= 8:
        b_font = ("Arial Black", 16)
    else:
        b_font = ("Arial Black", 12)

    for i in range(0, field_size):
        row = []
        for j in range(0, field_size):
            button = tk.Button(game_frame, 
                                text="", 
                                bg="#1C1C1C",
                                fg="#FFFFFF",
                                activebackground="#2D2D2D",  
                                activeforeground="#FFFFFF",
                                relief=tk.FLAT,
                                bd=0,
                                anchor="center",
                                cursor="hand2",
                                disabledforeground="gray",
                                font=b_font,
                                height=2,
                                width=5,
                                justify="center")
            row.append(button)
            button.configure(command=lambda row=i, col=j: playersMove(row, col))
            button.grid(row=i,column=j,padx=2, pady=2)
        field.append(row)

    nav_frame = ctk.CTkFrame(root, 
                              fg_color="#242424",
                              border_width=3,
                              border_color="#444444",
                              corner_radius=15)
    nav_frame.pack(padx=20, pady=20)

    backButton = ctk.CTkButton(nav_frame, 
                               text="Powrót ", 
                               command=createMenu,
                               font=("Arial", 20, "bold"),
                               fg_color="#D32F2F",
                               hover_color="#9A0007",
                               text_color="white",
                               corner_radius=15,
                               border_width=3,
                               border_color="#9A0007",
                               width=150, 
                               height=50,
                               cursor="hand2")
    backButton.pack()
    if botStarts.get() == True:
        aisMove()

createMenu()

root.mainloop()

