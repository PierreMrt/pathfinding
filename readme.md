# Path finding visualization
A GUI application made with tkinter to showcase two different path finding algorithms and visualize how they behave.

The goal for these algorithms is to find the shortest path between A and B, while avoiding obstacles.

### Algorithms
* [A-Star (or A*)](https://en.wikipedia.org/wiki/A*_search_algorithm): Use an heuristic to make path finding more 
efficient, calculated as the estimation of the euclidean distance with the destination. This allows the algorithm to
'race' to the destination.

* [Dijkstra](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm): Does not use the heuristic value and instead will 
search equally in every directions. This allows to make sure we always find the shortest path, at the detriment of 
efficiency.

### Utilisation
> python \PATH_TO_FILE\Pathfinding.py

Place an origin and a destination wherever you want by clicking on the grid. First click places the origin (A), second 
places the destination (B).

Then click again wherever you want to place some obstacles. You can also remove them by clicking on them again.

When you are satisfied with the layout, click 'Solve' to start the resolution and its visualization. By default, the 
program will use the A-Star algorithm. Click on the 'change algorithm' button at the top to switch algorithm.

The numbers on each cells represent the value assigned to them in order to determine the shortest path.

You can also reset the grid when you want to start another simulation by clicking 'Reset' at the bottom of the screen.

### Main libraries
Every libraries used in this application is part of python' standard libraries.
* Tkinter for the GUI
* Operator to sort the custom class objects by their f values
* Math to calculate distances using Pythagoras theorem

### Screenshots
* A-Star:

![astar](https://user-images.githubusercontent.com/69766734/105030431-11f5b480-5a54-11eb-9895-ec131199d09e.png)

* Dijkstra:

![dijkstra](https://user-images.githubusercontent.com/69766734/105030436-128e4b00-5a54-11eb-87fd-84eae062dab7.png)
