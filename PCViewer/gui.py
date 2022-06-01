"""
Project - PC Viewer
GUI
CSSE4011 - Advanced Embedded Systems
Semester 1, 2022
"""

__author__ = "L. van Teijlingen"

from PIL import ImageTk, Image
import os
import tkinter as tk
from tkinter import messagebox
import time
from global_ import *
import math
from threading import Thread
from queue import *

# GUI Defines =================================================================

BACKGROUND = "#18191A"
CARD = "#242526"
HOVER = "#3A3B3C"
PRIMARY_TEXT = "#E4E6EB"
SECONDARY_TEXT = "#B0B3B8"
TERTIARY_TEXT = "#808387"

WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920
GRID_LENGTH_PX = 900
GRID_VERT_LENGTH_PX = 900
GRID_HORI_LENGTH_PX = 600
HALF_HORI_GRID_PX = GRID_HORI_LENGTH_PX / 2
THIRD_VERT_GRID_PX = GRID_VERT_LENGTH_PX / 3
PX_OFFSET = 30
TOTAL_GRID_LINES = 6
MAJOR_AXES = int(600/2)
MINOR_AXES = int(600/10)

TITLE = "Project - Room Occupancy Monitor"

# GUI =========================================================================


class MainApplication(tk.Frame):
    """
    Main application class.
    """

    def __init__(self, inq_q, master=None):
        super().__init__(master)
        self._master = master
        self.in_q = inq_q
        self._stop = False
        self._master.title(TITLE)
        self._master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self._master.configure(bg=BACKGROUND)
        self.pack()

        title_active = False
        if title_active:
            title = tk.Label(
                self._master,
                text=TITLE,
                borderwidth=0,
                font="Montserrat, 25",
                bg=BACKGROUND,
                fg=PRIMARY_TEXT,
            )
            title.pack(side=tk.TOP, padx=10, pady=10)

        # Create the grid
        self._grid = Grid(self._master)
        self._grid.place(relx=0.4, rely=0.5, anchor=tk.W)

        self._data_container = DataDisplayContainer(self._master)
        self._data_container.place(relx=0.35, rely=0.5, anchor=tk.E)
        self._data = DataDisplay(self._data_container)

        self._node = Person(self._grid, "slow", 20, 50)

        self._master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.refresh_application()

    def on_closing(self):
        """Handle the closing of the window."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self._stop = True
            self._master.destroy()

    def refresh_application(self):
        """
        Update the position of the mobile node and the values.
        """

        while True:
            time.sleep(SHORT_SLEEP)

            if self._stop:
                break
            # Update the GUI

            self._master.update()

class Grid(tk.Canvas):
    """
    Class for the grid.
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(
            master,
            bg=CARD,
            height=GRID_VERT_LENGTH_PX,
            width=GRID_HORI_LENGTH_PX,
            highlightthickness=0,
        )
        self._master = master

        # create a grid
        for i in range(0, GRID_HORI_LENGTH_PX, MINOR_AXES): # vertical major lines
            self.create_line(i, 0, i, GRID_VERT_LENGTH_PX, fill=TERTIARY_TEXT, width=0.25)
        for i in range(0, GRID_VERT_LENGTH_PX, MINOR_AXES): # horizontal major lines
            self.create_line(0, i, GRID_HORI_LENGTH_PX, i, fill=TERTIARY_TEXT, width=0.25)
        for i in range(0, GRID_HORI_LENGTH_PX, MAJOR_AXES): # vertical major lines
            self.create_line(i, 0, i, GRID_VERT_LENGTH_PX, fill=SECONDARY_TEXT, width=3)
        for i in range(0, GRID_VERT_LENGTH_PX, MAJOR_AXES): # horizontal major lines
            self.create_line(0, i, GRID_HORI_LENGTH_PX, i, fill=SECONDARY_TEXT, width=3)
        # outline the grid
        self.create_line(0, 0, GRID_HORI_LENGTH_PX, 0, fill=SECONDARY_TEXT, width=6)
        self.create_line(
            GRID_HORI_LENGTH_PX,
            0,
            GRID_HORI_LENGTH_PX,
            GRID_VERT_LENGTH_PX,
            fill=SECONDARY_TEXT,
            width=6,
        )
        self.create_line(
            GRID_HORI_LENGTH_PX,
            GRID_VERT_LENGTH_PX,
            0,
            GRID_VERT_LENGTH_PX,
            fill=SECONDARY_TEXT,
            width=6,
        )
        self.create_line(0, GRID_VERT_LENGTH_PX, 0, 0, fill=SECONDARY_TEXT, width=6)

        self.create_static_graphic(GRID_HORI_LENGTH_PX / 2, GRID_VERT_LENGTH_PX - 10, 10)

    def create_static_graphic(self, pos_x, pos_y, size):
        """
        Create the graphic for the static node.
        """
        self.create_rectangle(
            pos_x - size*2,
            pos_y - size/2,
            pos_x + size*2,
            pos_y + size/2, 
            fill="#E2703A",
        )



class DataDisplayContainer(tk.Canvas):
    def __init__(self, master):
        super().__init__(
            master,
            bg=CARD,
            height=GRID_VERT_LENGTH_PX,
            width=GRID_HORI_LENGTH_PX / 2,
            highlightthickness=0,
        )
        self._master = master


class DataDisplay(object):
    def __init__(self, canvas, master=None):
        self.canvas = canvas
        # Create Labels
        data_label_offset = 220
        self.canvas.create_text(
            data_label_offset,
            PX_OFFSET,
            text="Current Occupants: 3",
            font="Montserrat, 12",
            fill="#E2703A",
            anchor="e",
        )
        self.canvas.create_text(
            data_label_offset,
            50,
            text="Total Occupants Today: 7",
            font="Montserrat, 12",
            fill="#3E7CB1",
            anchor="e",
        )
        

    def update_data(self, data):
        """
        Redraw the position of the mobile node.
        """
        try:
            self.canvas.itemconfig(
                self.multilat_pos,
                text=f"({math.ceil(data.multilat_pos[0])/100.0}, {math.ceil(data.multilat_pos[1])/100.0})",
            )
        except:
            return

        self.canvas.itemconfig(
            self.data_fusion_pos,
            text=f"({math.ceil(data.k_multilat_pos[0])/100.0}, {math.ceil(data.k_multilat_pos[1])/100.0})",
        )
        self.canvas.itemconfig(
            self.ml_pos,
            text=f"({math.ceil(data.k_ml_pos[0])/100.0}, {math.ceil(data.k_ml_pos[1])/100.0})",
        )
        for idx in range(0, 12):
            self.canvas.itemconfig(self.rssi[idx], text=f"{data.node_rssi[idx]}")
        for idx in range(0, 12):
            self.canvas.itemconfig(
                self.distance[idx], text=f"{math.ceil(data.node_distance[idx])}"
            )
        for idx in range(0, 4):
            self.canvas.itemconfig(self.ultra[idx], text=f"{data.node_ultra[idx]}")
        self.canvas.itemconfig(
            self.accel, text=f"({data.accel[0]}, {data.accel[1]}, {data.accel[2]})"
        )
        self.canvas.itemconfig(
            self.gyro, text=f"({data.gyro[0]}, {data.gyro[1]}, {data.gyro[2]})"
        )
        self.canvas.itemconfig(
            self.mag, text=f"({data.mag[0]}, {data.mag[1]}, {data.mag[2]})"
        )
        self.canvas.itemconfig(self.time, text=f"{data.timestamp}")
        self.canvas.itemconfig(self.delay, text=f"{data.rssi_delay}")


class Person(object):
    """
    Class for the mobile node
    """

    def __init__(self, canvas, type, xpos, ypos, master=None):
        self.pos_x = xpos
        self.pos_y = ypos

        slowbig = Image.open(os.getcwd()+"/PCViewer/Still.png")
        slowsmall = slowbig.resize((80,47), Image.ANTIALIAS)
        fastbig = Image.open(os.getcwd()+"/PCViewer/Speed.png")
        fastsmall = fastbig.resize((80,80), Image.ANTIALIAS)

        self.canvas = canvas
        if type == "fast":
            self.image = ImageTk.PhotoImage(fastsmall)
        elif type == "slow":
            self.image = ImageTk.PhotoImage(slowsmall)

        self.canvas.create_image(xpos, ypos, image=self.image, anchor="nw")


# GUI Interface ===============================================================


def gui_thread(in_q):
    """
    GUI interface for the application.
    """
    root = tk.Tk()
    app = MainApplication(in_q, master=root)
    app.mainloop()
