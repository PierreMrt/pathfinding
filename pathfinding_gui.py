from tkinter import *
from functools import partial

from algo import distance, Solver

class GUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.dimension = 20
        self.pack()

        self.solver = Solver(self, self.dimension)

        # This parameter can be changed through the drop down menu, and change the type of algorithm
        self.parameters = 1 

        # Create drop down menu for parameters
        self.top_frame = Frame(self, borderwidth=10)
        self.top_frame.grid(row=1)

        self.settings = Menubutton(self.top_frame, text="≡ Change algorithm", relief='raised')
        self.settings.grid(row=1, column=1)

        drop_down = Menu(self.settings, tearoff=False)
        drop_down.add_command(label='Dijkstra', command=partial(self.change_settings, 0))
        drop_down.add_command(label='A* [default]', command=partial(self.change_settings, 1))

        self.settings.configure(menu=drop_down)

        # Create top label
        self.top_label = Label(self.top_frame, text="Place the origin", width=70, justify='center', bd=0)
        self.top_label.grid(row=1, column=2)

        self.main_frame = Frame(self, borderwidth=2, relief=SUNKEN, bg='black', padx=10, pady=10)
        self.main_frame.grid(row=2)

        # Create the grid
        for i in range(self.dimension):
            for j in range(self.dimension):

                button = Button(self.main_frame, text=" ", justify='center', width=2, bd=0, bg='white')
                button.config(command=partial(self.button_click, button, i, j))
                button.grid(row=i, column=j, padx=1, pady=1, ipady=2, ipadx=4)

                self.solver.cells.append(Cell(button, i, j))

        # Create solve and reset button
        self.bottom_frame = Frame(self, borderwidth=10)
        self.bottom_frame.grid(row=3)
        solve = Button(self.bottom_frame, text="Solve", justify='center', bd=2, relief='raised')
        solve.config(command=self.solver.solve)
        solve.grid(ipady=5, ipadx=10, padx=20, row=1, column=1)

        reset = Button(self.bottom_frame, text="Reset", justify='center', bd=2, relief='raised')
        reset.config(command=self.reset)
        reset.grid(ipady=5, ipadx=10, row=1, column=2)

    def button_click(self, button, i, j):
        if self.solver.origin is None:
            button.config(bg='DodgerBlue2', text='A')
            self.top_label.config(text='Place the destination')
            self.solver.origin = Cell(button, i, j)

        elif self.solver.destination is None:
            button.config(bg='DodgerBlue2', text='B')
            self.top_label.config(text='Place some obstacles')
            self.solver.destination = Cell(button, i, j)

        else:
            self.top_label.config(text='Place some obstacles')

            if (i, j) in self.solver.obstacles:
                button.config(bg='white', text=' ')
                self.solver.obstacles.remove((i, j))

            else:
                button.config(bg='black', text=' ')
                self.solver.obstacles.append((i, j))

    def reset(self):
        self.solver.origin = None
        self.solver.destination = None

        self.solver.open = []
        self.solver.closed = []
        self.solver.obstacles = []

        for cell in self.solver.cells:
            cell.name.config(bg='white', text='')
            cell.reset_cell()

        self.top_label.config(text="Place the origin")

    def change_settings(self, settings):
        # Change algorithm according to the value from the drop down menu
        # 0 is Dijkstra, 1 is A-Star
        self.parameters = settings


class Cell:
    def __init__(self, name, row, col):
        self.name = name
        self.pos = (row, col)
        self.parent = None

        self.g = 0
        self.h = 0
        self.f = 0

    def reset_cell(self):
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = ()