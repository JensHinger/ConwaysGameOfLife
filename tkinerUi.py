import tkinter as tk
from tkinter import ttk
from game import Game
from timer_decorator import measure_time

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.game_size = 40
        self.line_dist = 20
        self.canvas_width = self.line_dist * self.game_size
        self.canvas_height = self.line_dist * self.game_size

        self.pause_active = True

        self.canvas_rects = []
        self.game = Game(self.game_size)

        self.template = tk.IntVar()
        
        # TODO load in from json
        self.available_templates = ["No Template","Glider", "Blinker", "Quad Blinker", "Loafer"]
        self.template_list_templates = [
            [[1]]
            ,
            [[0, 0, 1],
            [1, 0, 1],
            [0, 1, 1]]
            ,
            [[0, 1, 0],
            [0, 1, 0],
            [0, 1, 0]]
            ,
            [[1, 0, 0],
            [1, 1, 1],
            [1, 0, 0]]
            ,
            [[0, 1, 1, 0, 0, 1, 0, 1, 1],
            [1, 0, 0, 1, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1 ,0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1]]
        ]

        # Window Heading
        self.heading_label = ttk.Label(
            self,
            text="Conway's Game Of Life",
            padding=10,
            background="gray80"
        )
        self.heading_label.grid(
            column=0,
            columnspan=2,
            row=0,
            sticky=tk.EW
        )

        #
        # Start Option frame
        #
        self.option_frame = ttk.Frame(
            self,
            width=200
        )
        self.option_frame.grid(
            column=0,
            row=1,
            sticky=tk.NSEW
        )

        self.un_pause_button = ttk.Button(
            self.option_frame,
            text="Un-pause",
            command=self.handle_pause
        )
        self.un_pause_button.pack(fill="x")

        self.init_random_button = ttk.Button(
            self.option_frame,
            text="Init random",
            command=self.init_random
        )
        self.init_random_button.pack(fill="x")

        self.clear_button = ttk.Button(
            self.option_frame,
            text="Clear field",
            command=self.init_empty
        )
        self.clear_button.pack(fill="x")

        #
        # Start Template Frame
        #
        self.template_frame = ttk.Frame(
            self.option_frame
        )
        self.template_frame.pack()

        for index, temp in enumerate(self.available_templates):
            radiob = tk.Radiobutton(
                self.template_frame,
                text=temp,
                value=index,
                variable=self.template
            )
            radiob.pack()

        # 
        # Start Game frame
        # 
        self.game_frame = ttk.Frame(
            self,
            border=1,
        )
        self.game_frame.grid(
            column=1,
            row=1,
            sticky=tk.NSEW
        )

        self.game_canvas = tk.Canvas(
            self.game_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            background="gray90",
            borderwidth=0,
            highlightthickness=0
        )
        self.game_canvas.pack()
        self.create_grid()

        self.game_canvas.bind("<ButtonPress-1>", self.handle_click)

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=8)

        self.minsize(800, 800)
        self.mainloop()

    @measure_time
    def loop(self):
        # TODO make more beautiful / Performant not using self.after -> multithread?
        self.game.step()
        self.draw_game_field()
        if not self.pause_active:
            self.after(50, self.loop)

    def init_random(self):
        self.game.init_random_field()
        self.draw_game_field()

    def init_empty(self):
        self.game.clear_field()
        self.draw_game_field()

    def draw_game_field(self):
        for y in range(len(self.game.game_field)):
            for x in range(len(self.game.game_field)):
                fill_value = "black" if self.game.game_field[y][x] == 1 else "white"
                self.game_canvas.itemconfig(self.canvas_rects[y][x], fill=fill_value)

    def handle_click(self, event):
        x = int(event.x / self.line_dist)
        y = int(event.y / self.line_dist)
        
        if x > len(self.canvas_rects) - 1 or y > len(self.canvas_rects) - 1:
            return
        
        if self.template.get() == 0:
            self.no_template_click(x, y)
        else:
            self.template_click(x, y, self.template_list_templates[self.template.get()])

    def template_click(self, x, y, template):
        center_temp_y = int(1/2 * len(template))

        for temp_y in range(-center_temp_y, center_temp_y + 1):
            center_temp_x = int(1/2 * len(template[temp_y]))

            for temp_x in range(-center_temp_x, center_temp_x + 1):
                current_x = (temp_x + x)
                current_y = (temp_y + y)

                self.change_cell(
                    current_x % self.game_size,
                    current_y % self.game_size,
                    template[temp_y + center_temp_y][temp_x + center_temp_x]
                )

    def no_template_click(self, x, y):
        if self.game.game_field[y][x] == 0:
            self.change_cell(x, y, 1)
        else:
            self.change_cell(x, y, 0)

    def change_cell(self, x, y, new_state):
        self.game_canvas.itemconfig(self.canvas_rects[y][x], fill="black" if new_state else "white")
        self.game.game_field[y][x] = new_state

    def handle_pause(self):
        if self.pause_active:
            self.un_pause_button["text"] = "Pause"
            self.pause_active = False
            self.loop()
        else:
            self.un_pause_button["text"] = "Un-pause"
            self.pause_active = True

    @measure_time
    def create_grid(self):

        for y in range(int(self.canvas_width/self.line_dist)):
            self.canvas_rects.append([])
            for x in range(int(self.canvas_height/self.line_dist)):
                self.canvas_rects[y].append(self.game_canvas.create_rectangle(
                    x * self.line_dist, 
                    y * self.line_dist,
                    (x + 1) * self.line_dist - 1,
                    (y + 1) * self.line_dist - 1,
                    fill="white",
                    activestipple="gray50"
                )
            )

if __name__ == "__main__":
    window = MainWindow()