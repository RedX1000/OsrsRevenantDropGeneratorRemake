import os
import sys
import tkinter as tk
from tkinter import font
import math


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
        self.left_canvas_color = "#17bca1"
        self.left_canvas_top_color = "#129680"
        self.left_label_color = "#17bca1"

        c_left = tk.Canvas(main_frame, background=self.left_canvas_color, highlightbackground=self.left_canvas_color, bd=0)

        c_left_top = tk.Canvas(c_left, background=self.left_canvas_top_color,
                               highlightbackground=self.left_canvas_top_color, bd=0)
        self.lbl_title = tk.Label(c_left_top, text=" OSRS Revenent Drop Generator ", font=self.title_font,
                                  background=self.left_canvas_top_color).pack(padx=20)
        self.lbl_desc = tk.Label(c_left_top, text="Enter the amount of kills, choose whether you're skulled or not, select the "
                                     "revenant, and run the code!", font=self.desc_font, wraplength=450, background=self.left_canvas_top_color).pack()
        c_left_top.pack(side="top")

        c_info = tk.Canvas(c_left, width=500, background=self.left_canvas_color, highlightbackground=self.left_canvas_color, bd=0)

        self.lbl_rev = tk.Label(c_info, background=self.left_label_color, highlightbackground=self.left_label_color, text="Revenant being killed", font=self.stand_font_bold).grid(row=0, column=0, padx=20, pady=10)


        self.lbl_kills = tk.Label(c_info, background=self.left_label_color, highlightbackground=self.left_label_color, text="Number being killed", font=self.stand_font_bold).grid(row=1, column=0, padx=20, pady=10)
        self.var_entry_kills = tk.IntVar(value=0)
        self.entry_kills = tk.Entry(c_info, bg="light gray", fg="black", textvariable=self.var_entry_kills, font=self.stand_font,
                                    highlightbackground=self.left_label_color, exportselection=0, width="15").grid(row=1, column=1, padx=20, pady=10)

        self.lbl_skulled = tk.Label(c_info, background=self.left_label_color, highlightbackground=self.left_label_color, text="Are you skulled?", font=self.stand_font_bold).grid(row=2, column=0, padx=20, pady=10)


        self.lbl_status = tk.Label(c_info, background=self.left_label_color, highlightbackground=self.left_label_color, text="Standing by...", font=self.stand_font_bold).grid(row=3, column=0, padx=20, pady=10)

        c_info.pack(side="top", pady=20)

        #cRev = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0)
        #cRevLeft = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0)
        #cRevRight = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0)
        #cRev.pack(side="top")
        #
        #cKills = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0)
        #cKillsLeft = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0)
        #cKillsRight = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0
        #cKills.pack(side="top")
        #
        #cSkulled = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0)
        #cSkulledLeft = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0)
        #cSkulledRight = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0
        #cSkulled.pack(side="top")
        #
        #cRun = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0)
        #cRevLeft = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0)
        #cRevRight = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0
        #cRun.pack(side="top")
        #
        #cPicture = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0)
        #cRevLeft = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0)
        #cRevRight = tk.Canvas(cLeft, background="#17bca1", highlightbackground="#17bca1", bd=0
        #cPicture.pack(side="top")

        c_left.pack(side="left")


        c_right = tk.Canvas(main_frame, background="gray65", highlightbackground="light gray", bd=0)

        c_right.pack(side="right")

    def menu(self, skullS, killsS, levelS):
        skull = int(skullS)
        kills = int(killsS)
        level = int(levelS)
        totalKills = 0

        totalDrops = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        totalCalculatedDrops = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for i in range(0, kills):
            totalDrops[0] += 1
            totalDrops[1] += 1

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

            # if (a == 1):
            #     goodDrops(skull, totalDrops)
            # elif a == 0 or a >= 2 and a <= 86:
            #     mediocreDrops(totalDrops)

            totalKills += 1
            # print(totalKills)


if __name__ == '__main__':
    root = tk.Tk()
    root.iconbitmap(resource_path(""))
    root.title("Osrs Revenant Drop Generator: Remake")
    a = Application(root)
    root.mainloop()
