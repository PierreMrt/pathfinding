import math
import operator
import time

def distance(a, b):
    dist = int(math.sqrt(abs(a[0]-b[0])**2+abs(a[1]-b[1])**2)*10)
    return dist

class Solver:
    def __init__(self, gui, dimension):
        self.gui = gui

        self.dimension = dimension
        self.origin = None
        self.destination = None
        self.cells = []

        self.open = []
        self.closed = []
        self.obstacles = []

    def solve(self):
        # When solve button is pressed, check if the origin and destination were set
        if self.origin is None or self.destination is None:
            self.gui.top_label.config(text='Please put at least the origin and the destination')
        else:
            self.gui.top_label.config(text='Solving...')

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
                    self.gui.update()

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
                        child.h = distance(child.pos, self.destination.pos) * self.gui.parameters
                        child.f = child.g + child.h
                        # Append it to the open list = cells potentially on the path
                        self.open.append(child)

                        # Change its color to orange if it is not the origin or destination and display its f value
                        if child.name != self.origin.name and child.name != self.destination.name:
                            child.name.config(bg='orange', text=f"{child.f}")
                            self.gui.update()
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

            if len(self.open) == 0:
                self.gui.top_label.config(text='No path has been found. Click reset and create another problem.')

    def check_neighbours(self, current):
        children = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                pos = (current.pos[0] + i, current.pos[1] + j)
                for cell in self.cells:
                    if pos == cell.pos:
                        child = cell
                if pos == current.pos:
                    continue
                else:
                    if 0 <= pos[0] < self.dimension and 0 <= pos[1] < self.dimension:
                        if pos in self.obstacles or child in self.closed:
                            continue

                        children.append(child)

        return children

    def retrace_path(self, current):
        parent = current.parent

        steps = 0
        while parent is not None:
            if parent.name != self.origin.name:
                parent.name.config(bg='green4')
                time.sleep(0.05)
                self.gui.update()
                steps += 1
            parent = parent.parent

        nodes = 0
        for cell in self.cells:
            if cell.name.cget('bg') == 'orange' or cell.name.cget('bg') == 'green4' or cell.name.cget('bg') == 'red3':
                nodes += 1

        self.gui.top_label.config(text=f'A path has been found ! Nodes expanded: {nodes}, steps: {steps}')