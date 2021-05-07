from tkinter import *
from functools import partial
import math
import operator
import time


class GUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # Initialize variables
        self.dimension = 20
        self.pack()
        self.origin = None
        self.destination = None

        # Contains all the cells that make up the grid
        self.cells = []

        # Contains all the cells that need to be checked for a path
        self.open = []

        # Contains all the cells for which a potential path was already evaluated
        self.closed = []

        # Contains the positions of the obstacles
        self.obstacles = []

        # This parameter can be changed through the drop down menu, and change the type of algorithm
        # A-Star is more efficient as it will race to the destination, however it might not always find the best path
        # Dijkstra is more reliable, but as to check a much larger number of cell before finding the destination
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

                # Add buttons to list of buttons
                self.cells.append(Cell(button, i, j))

        # Create solve and reset button
        self.bottom_frame = Frame(self, borderwidth=10)
        self.bottom_frame.grid(row=3)
        solve = Button(self.bottom_frame, text="Solve", justify='center', bd=2, relief='raised')
        solve.config(command=self.solve)
        solve.grid(ipady=5, ipadx=10, padx=20, row=1, column=1)

        reset = Button(self.bottom_frame, text="Reset", justify='center', bd=2, relief='raised')
        reset.config(command=self.reset)
        reset.grid(ipady=5, ipadx=10, row=1, column=2)

    def button_click(self, button, i, j):
        # If origin is not set, create it
        if self.origin is None:
            button.config(bg='DodgerBlue2', text='A')
            self.top_label.config(text='Place the destination')
            self.origin = Cell(button, i, j)

        # If destination is not set, create it
        elif self.destination is None:
            button.config(bg='DodgerBlue2', text='B')
            self.top_label.config(text='Place some obstacles')
            self.destination = Cell(button, i, j)

        # If both destination and origin are set, the next clicks create obstacles
        else:
            self.top_label.config(text='Place some obstacles')

            # If button was an obstacle, remove it from obstacles and put in white
            if (i, j) in self.obstacles:
                button.config(bg='white', text=' ')
                self.obstacles.remove((i, j))

            # Otherwise create the button as an obstacle (in black)
            else:
                button.config(bg='black', text=' ')
                self.obstacles.append((i, j))

    def reset(self):
        # When reset button is clicked, reset the grid to its initial state
        self.origin = None
        self.destination = None

        self.open = []
        self.closed = []
        self.obstacles = []

        for cell in self.cells:
            cell.name.config(bg='white', text='')
            cell.reset_cell()

        self.top_label.config(text="Place the origin")

    def change_settings(self, settings):
        # Change algorithm according to the value from the drop down menu
        # 0 is Dijkstra, 1 is A-Star
        self.parameters = settings

    def solve(self):
        # When solve button is pressed, check if the origin and destination were set
        if self.origin is None or self.destination is None:
            self.top_label.config(text='Please put at least the origin and the destination')
        else:
            self.top_label.config(text='Solving...')

            # Set origin as the current cell and add it to the open list
            current = self.origin
            self.open.append(current)

            # Loop while we still have cells to check in the open list
            while len(self.open) > 0:

                # If the current position is the same as the destination, call the function to retrace the path
                # and exit the loop
                if current.pos == self.destination.pos:
                    self.retrace_path(current)
                    break

                # Sort the open list by ascending order of f values
                self.open = sorted(self.open, key=operator.attrgetter('f'))

                # Set current cell as the cell in the open list with the smallest f value
                current = self.open[0]

                # Color it in red if it is not the destination or the origin
                if current.name != self.origin.name and current.name != self.destination.name:
                    current.name.config(text=f"{current.f}", bg='red3')
                    self.update()

                # Append the current cell to the closed list and remove it from the open list
                self.closed.append(current)
                self.open.remove(current)

                # Return list of neighbours that are walkable and not in the closed list
                children = self.check_neighbours(current)

                for child in children:
                    # If cell was not already checked:
                    if child not in self.open:
                        # Set current cell as parent (from were it comes from. We will use it to retrace the path)
                        child.parent = current
                        # update g, h and f values
                        child.g = current.g + distance(child.pos, current.pos)
                        child.h = distance(child.pos, self.destination.pos) * self.parameters
                        child.f = child.g + child.h
                        # Append it to the open list = cells potentially on the path
                        self.open.append(child)

                        # Change its color to orange if it is not the origin or destination and display its f value
                        if child.name != self.origin.name and child.name != self.destination.name:
                            child.name.config(bg='orange', text=f"{child.f}")
                            self.update()
                        continue

                    # If cell was already in open list, check if the new path is better than the one previously
                    # calculated for this cell
                    elif child in self.open:
                        new_g = current.g + distance(child.pos, current.pos)
                        if new_g < child.g:
                            # In this case, recalculate its g and f value and set the current cell as its parent
                            child.g = new_g
                            child.f = child.g + child.h
                            child.parent = current

                    else:
                        continue

            # If we exited the loop without finding a solution, the path was not solvable
            if len(self.open) == 0:
                self.top_label.config(text='No path has been found. Click reset and create another problem.')

    def check_neighbours(self, current):
        children = []
        # Check all cells around current cell as well as itself
        for i in range(-1, 2):
            for j in range(-1, 2):
                pos = (current.pos[0] + i, current.pos[1] + j)
                for cell in self.cells:
                    if pos == cell.pos:
                        child = cell
                # if cell checked is current cell, ignore it
                if pos == current.pos:
                    continue
                else:
                    # Check if checked cell is part of the grid
                    if 0 <= pos[0] < self.dimension and 0 <= pos[1] < self.dimension:
                        # Check that cell is not in obstacles or already checked cells, if yes, ignore it
                        if pos in self.obstacles or child in self.closed:
                            continue

                        children.append(child)

        return children

    def retrace_path(self, current):
        parent = current.parent

        # Retrace path in green and calculate numbers of steps
        steps = 0
        while parent is not None:
            if parent.name != self.origin.name:
                parent.name.config(bg='green4')
                time.sleep(0.05)
                self.update()
                steps += 1
            parent = parent.parent

        # Calculate nodes expanded
        nodes = 0
        for cell in self.cells:
            if cell.name.cget('bg') == 'orange' or cell.name.cget('bg') == 'green4' or cell.name.cget('bg') == 'red3':
                nodes += 1

        self.top_label.config(text=f'A path has been found ! Nodes expanded: {nodes}, steps: {steps}')


class Cell:
    def __init__(self, name, row, col):
        # super().__init__(self, master=None)

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


def distance(a, b):
    # Calculate the distance between two cells using the Pythagoras' theorem
    dist = int(math.sqrt(abs(a[0]-b[0])**2+abs(a[1]-b[1])**2)*10)
    return dist


if __name__ == '__main__':
    # Create the Tkinter app -> GUI
    root = Tk()
    app = GUI(master=root)
    app.mainloop()
    root.quit()
