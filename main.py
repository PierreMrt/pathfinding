from tkinter import Tk

from pathfinding_gui import GUI

if __name__ == '__main__':
    root = Tk()
    app = GUI(master=root)
    app.mainloop()
    root.quit()