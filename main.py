"""
#     |==============================================================|
#     |Formula made by Mod Ash                                       |
#     |Code written by CrownMauler/Red X 500/RedX1000                |
#     |Contact me at Discord: RedX1000#3655                          |
#     |Check my Github: https://www.github.com/RedX1000              |
#     |Program is based on this                                      |
#     |https://pbs.twimg.com/media/DpbCbE_WkAYCD6L.jpg:large         |
#     |This is a complete rewrite of the original program            |
#     |Updated drop rates pulled from the OSRS Wiki:                 |
#     |https://oldschool.runescape.wiki/w/Template:Revenants/Drops   |
#     |==============================================================|
"""

import os
import sys
import tkinter as tk
import PIL
from tkinter import font
from tkinter import ttk
from PIL import Image, ImageTk
import math
import random
import time


def resource_path(relative_path):
    # Link used for this: https://stackoverflow.com/questions/51060894
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Application:
    def __init__(self, parent):
        main_frame = tk.Frame(parent, background="gray65")
        main_frame.pack()

        self.title_font = font.Font(family="Arial", size=20, weight=font.BOLD)
        self.desc_font = font.Font(family="Arial", size=16)
        self.stand_font_bold = font.Font(family="Arial", size=14, weight=font.BOLD)
        self.stand_font = font.Font(family="Arial", size=14)
        self.stand_font_small_bold = font.Font(family="Arial", size=11, weight=font.BOLD)
        self.stand_font_small = font.Font(family="Arial", size=11)
        self.left_canvas_color = "#17bca1"
        self.left_canvas_top_color = "#129680"
        self.left_label_color = "#17bca1"

        self.revenant_data = {'Select a revenant': 0,
                              'Revenant imp': 7,
                              'Revenant goblin': 15,
                              'Revenant pyrefiend': 52,
                              'Revenant hobgoblin': 60,
                              'Revenant cyclops': 82,
                              'Revenant hellhound': 90,
                              'Revenant demon': 98,
                              'Revenant ork': 105,
                              'Revenant dark beast': 120,
                              'Revenant knight': 126,
                              'Revenant dragon': 135}

        self.revenant_data_var = tk.StringVar(parent)
        self.revenant_data_var.set("Select a revenant")

        self.var_entry_kills = tk.IntVar(parent)
        self.var_entry_kills.set(0)

        self.var_skulled = tk.IntVar(parent)
        self.var_skulled.set(2)

        c_left = tk.Canvas(main_frame, background=self.left_canvas_color, highlightbackground=self.left_canvas_color, bd=0, highlightthickness=0, relief='ridge')

        c_left_top = tk.Canvas(c_left, background=self.left_canvas_top_color, highlightbackground=self.left_canvas_top_color, bd=0)
        self.lbl_title = tk.Label(c_left_top, text=" OSRS Revenant Drop Generator ", font=self.title_font, background=self.left_canvas_top_color)
        self.lbl_title.pack(padx=20)
        self.lbl_desc = tk.Label(c_left_top, text="Enter the amount of kills, choose whether you're skulled or not, select the revenant, and run the code!", font=self.desc_font, wraplength=450, background=self.left_canvas_top_color)
        self.lbl_desc.pack()
        self.lbl_disclaimer = tk.Label(c_left_top, text="(If it freezes it's running)", font=self.stand_font_small, wraplength=450, background=self.left_canvas_top_color)
        self.lbl_disclaimer.pack()
        c_left_top.pack(side="top")

        c_info = tk.Canvas(c_left, width=500, background=self.left_canvas_color, highlightbackground=self.left_canvas_color, bd=0, highlightthickness=0, relief='ridge')
        self.lbl_rev = tk.Label(c_info, background=self.left_label_color, highlightbackground=self.left_label_color, text="Revenant being killed", font=self.stand_font_bold)
        self.lbl_rev.grid(row=0, column=0, padx=20, pady=10)
        self.revenant_options = tk.OptionMenu(c_info, self.revenant_data_var, *self.revenant_data, command=lambda e: self.change_picture())
        self.revenant_options.config(bg="#30d7bb", fg="black", highlightbackground=self.left_label_color, activebackground="#17bda2", font=self.stand_font_small_bold, width=19)
        self.revenant_menu = c_info.nametowidget(self.revenant_options.menuname)
        self.revenant_menu.config(font=self.stand_font_small)
        # Todo: Change the dropdown menu arrow.
        self.revenant_options.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_kills = tk.Label(c_info, background=self.left_label_color, highlightbackground=self.left_label_color, text="Number being killed", font=self.stand_font_bold)
        self.lbl_kills.grid(row=1, column=0, padx=20, pady=10)
        self.entry_kills = tk.Entry(c_info, bg="light gray", fg="black", textvariable=self.var_entry_kills, font=self.stand_font, highlightbackground=self.left_label_color, exportselection=0, width="17")
        self.entry_kills.grid(row=1, column=1, padx=20, pady=10)

        self.lbl_skulled = tk.Label(c_info, background=self.left_label_color, highlightbackground=self.left_label_color, text="Are you skulled?", font=self.stand_font_bold)
        self.lbl_skulled.grid(row=2, column=0, padx=20, pady=10)
        c_buttons = tk.Canvas(c_info, background=self.left_canvas_color, highlightbackground=self.left_canvas_color, bd=0)
        self.rb_skulled = tk.Radiobutton(c_buttons, font=self.stand_font_small_bold, variable=self.var_skulled, text="Skulled", bg=self.left_canvas_top_color, activebackground=self.left_canvas_top_color, value=1)
        self.rb_skulled.grid(row=0, column=0, pady=10)
        self.rb_not_skulled = tk.Radiobutton(c_buttons, font=self.stand_font_small_bold, variable=self.var_skulled, text="Not Skulled", bg=self.left_canvas_top_color, activebackground=self.left_canvas_top_color, value=2)
        self.rb_not_skulled.grid(row=0, column=1, pady=10)
        c_buttons.grid(row=2, column=1, padx=20, pady=10)

        self.lbl_status = tk.Label(c_info, background=self.left_label_color, highlightbackground=self.left_label_color, text="Standing by...", font=self.stand_font_bold)
        self.lbl_status.grid(row=3, column=0, padx=20, pady=10)
        self.btn_start = tk.Button(c_info, text="   Press to generate loot   ", command=lambda: self.menu(), activebackground="#1c8170", font=self.stand_font_small_bold, bg="#30d7bb")
        self.btn_start.grid(row=3, column=1, padx=20, pady=10)
        self.btn_start.bind("<Enter>", lambda e: self.btn_start.config(bg="#26ac95"))
        self.btn_start.bind("<Leave>", lambda e: self.btn_start.config(bg="#30d7bb"))
        c_info.pack(side="top", pady=20)

        # Old color for c_image and revenant_photo_lbl was #219581
        c_bottom = tk.Canvas(c_left, width=365, height=365, background="#13564a", highlightbackground="#13564a", bd=5, borderwidth=5)
        c_image = tk.Canvas(c_bottom, width=350, height=350, background="#1d8674", highlightbackground="#1d8674", bd=0, highlightthickness=0, relief='ridge')
        self.revenant_image = PIL.Image.open("images/revenants/Select a revenant.png")
        self.revenant_photo_image = PIL.ImageTk.PhotoImage(self.revenant_image)
        self.revenant_photo_lbl = tk.Label(c_image, image=self.revenant_photo_image, width=350, height=350, bg="#1d8674", highlightbackground="#219581", bd=0, highlightthickness=1, relief='ridge')
        self.revenant_photo_lbl.pack(padx=10, pady=10)
        c_image.pack(side="top", padx=5, pady=5)
        c_bottom.pack(side="top", pady=(5, 35))


        c_left.pack(side="left")


        c_right = tk.Canvas(main_frame, background="gray65", highlightbackground="light gray", bd=0)

        c_right.pack(side="right")

    def on_enter(self):
        self.btn_start['bg'] = "#17bda2"
        print("in")

    def on_leave(self):
        self.btn_start['bg'] = "#30d7bb"
        print("out")

    def change_picture(self):
        # https://stackoverflow.com/questions/3482081
        img = PIL.ImageTk.PhotoImage(Image.open("images/revenants/"+self.revenant_data_var.get()+".png"))
        self.revenant_photo_lbl.configure(image=img)
        self.revenant_photo_lbl.image = img

    def menu(self):
        if self.revenant_data_var.get() == "Select a revenant":
            self.lbl_status['bg'] = "Orange"
            self.lbl_status['text'] = "Choose a revenant"

        else:
            try:
                self.lbl_status['bg'] = "yellow"
                self.lbl_status['text'] = "Running..."
                self.lbl_status.update_idletasks()
                time.sleep(2)
                print("menu")

                skull = self.var_skulled.get()  # todo: make getters for these
                kills = self.var_entry_kills.get()  # todo: make getters for these
                level = self.revenant_data[self.revenant_data_var.get()]  # todo: make getters for these

                totalDrops = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                totalCalculatedDrops = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                for i in range(0, kills):
                    totalDrops[0] += 1
                    totalDrops[1] += 1
                    print(i)
                    chanceA = 0.0
                    chanceB = 0.0

                    clampedLevel = level

                    # Formula for chanceA
                    chanceA = 2200 / int(math.sqrt(clampedLevel))
                    chanceA = int(chanceA)

                    # Formula for chanceB
                    chanceB = 15 + (math.pow((level + 60), 2) / 200)
                    chanceB = int(chanceB)

                    # This will randomize a number,
                    # A is set between 0 and (chanceA - 1) inclusive
                    a = int(random.randint(0, (chanceA - 1)))

                    print(chanceA)
                    print(a)
                    print(chanceB)

                    if (a == 0):
                        self.good_drops(skull, totalDrops)
                    elif a >= 1 and a <= chanceB:
                        self.mediocre_drops(totalDrops)


                self.lbl_status['bg'] = "lime green"
                self.lbl_status['text'] = "   Finished!   "

            except Exception as e:
                print(e)
                self.lbl_status['bg'] = "OrangeRed2"
                self.lbl_status['text'] = "Some Crash Occurred"
                self.lbl_status.update_idletasks()


    def good_drops(self, skull, total_drops):
        pass

    def mediocre_drops(self, total_drops):
        pass

if __name__ == '__main__':
    root = tk.Tk()
    root.iconbitmap(resource_path(""))
    root.title("Osrs Revenant Drop Generator: Remake")
    a = Application(root)
    root.mainloop()
