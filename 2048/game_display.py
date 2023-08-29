import tkinter as tk
import cf as c
import game_ai
import game_functions

UP_KEY = "'w'"
DOWN_KEY = "'s'"
LEFT_KEY = "'a'"
RIGHT_KEY= "'d'"
AI_KEY = "'q'"
AI_PLAY_KEY = "'p'"

class Display(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        
        self.main_grid = tk.Frame(
            self, bg=c.GRID_COLOUR, bd=3, width=400, height=400)
        self.main_grid.grid(pady=(80, 0))

        self.master.bind("<Key>", self.key_press)

        self.commands = {UP_KEY: game_functions.move_up, 
                         DOWN_KEY: game_functions.move_down,
                         LEFT_KEY: game_functions.move_left, 
                         RIGHT_KEY: game_functions.move_right,
                         AI_KEY: game_ai.ai_move,
                         }
        
        self.grid_cells = []
        self.build_grid()
        self.init_matrix()
        self.update_grid()

        self.mainloop()

    def build_grid(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOUR,
                    width=100,
                    height=100)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOUR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        title_frame = tk.Frame(self)
        title_frame.place(relx=0.5, y=40, anchor="center")
        tk.Label(
            title_frame,
            text="2048",
            font=c.TITLE_LABEL_FONT).grid(
            row=0)

    def init_matrix(self):
        self.matrix = game_functions.initialize_game()

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOUR)
                    self.cells[i][j]["number"].configure(
                        bg=c.EMPTY_CELL_COLOUR, text="")
                else:
                    self.cells[i][j]["frame"].configure(
                        bg=c.CELL_COLOURS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLOURS[cell_value],
                        fg=c.CELL_NUMBER_COLOURS[cell_value],
                        font=c.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value))
        self.update_idletasks()
    
    def key_press(self, event):
        valid_game = True
        key = repr(event.char)
        if key == AI_PLAY_KEY:
            move_count = 0
            while valid_game:
                self.matrix, valid_game = game_ai.ai_move(self.matrix,40, 30)
                if valid_game:
                    self.matrix = game_functions.add_new_tile(self.matrix)
                    self.update_grid()
                move_count += 1
        if key == AI_KEY:
            self.matrix, move_made = game_ai.ai_move(self.matrix, 20, 30)
            if move_made:
                self.matrix = game_functions.add_new_tile(self.matrix)
                self.update_grid()
                move_made = False

        elif key in self.commands:
            self.matrix, move_made, _ = self.commands[repr(event.char)](self.matrix)
            if move_made:
                self.matrix = game_functions.add_new_tile(self.matrix)
                self.update_grid()
                move_made = False
gamegrid = Display()