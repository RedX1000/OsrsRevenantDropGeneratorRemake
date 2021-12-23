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
from os import listdir
from os.path import isfile, join
import PIL
from tkinter import font
from tkinter import ttk
from PIL import Image, ImageTk
import math
import random
import time
import threading
import queue
from queue import Queue


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
        main_frame = tk.Frame(parent, background="gray62")
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

        # First value, level. Second value, hitpoints.
        self.revenant_data = {'Select a revenant': [0, 0],
                              'Revenant imp': [7, 10],
                              'Revenant goblin': [15, 14],
                              'Revenant pyrefiend': [52, 48],
                              'Revenant hobgoblin': [60, 72],
                              'Revenant cyclops': [82, 110],
                              'Revenant hellhound': [90, 80],
                              'Revenant demon': [98, 80],
                              'Revenant ork': [105, 105],
                              'Revenant dark beast': [120, 136],
                              'Revenant knight': [126, 143],
                              'Revenant dragon': [135, 155]}

        with open(resource_path('images/items/item_list.txt'), 'r') as f:
            self.item_list = [line.strip() for line in f]
        self.img_item_list = []
        for i in range(len(self.item_list)):
            if i == 0:
                temp = resource_path(self.item_list[0])
            else:
                temp = tk.PhotoImage(file=(resource_path("images/items/" + self.item_list[i])))
            self.img_item_list.append(temp)

        self.revenant_data_var = tk.StringVar(parent)
        self.revenant_data_var.set("Select a revenant")

        self.var_entry_kills = tk.StringVar(parent)
        self.var_entry_kills.set("0")

        self.var_skulled = tk.IntVar(parent)
        self.var_skulled.set(2)

        self.var_display = tk.IntVar(parent)
        self.var_display.set(1)

        self.total_drops = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        c_left = tk.Canvas(main_frame, background=self.left_canvas_color, highlightbackground=self.left_canvas_color, bd=0, highlightthickness=0, relief='ridge')

        c_left_top = tk.Canvas(c_left, background=self.left_canvas_top_color, highlightbackground=self.left_canvas_top_color, bd=0)
        self.lbl_title = tk.Label(c_left_top, text=" OSRS Revenant Drop Generator v1.0.1 ", font=self.title_font, background=self.left_canvas_top_color)
        self.lbl_title.pack(padx=20)
        self.lbl_desc = tk.Label(c_left_top, text="Enter the amount of kills, choose whether you're skulled or not, select the revenant, set data display speed, and run the code!", font=self.desc_font, wraplength=450, background=self.left_canvas_top_color)
        self.lbl_desc.pack()
        self.lbl_disclaimer = tk.Label(c_left_top, text="(If it freezes it's running. Screen won't be movable, and try not to minimize the window)", font=self.stand_font_small, wraplength=450, background=self.left_canvas_top_color)
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
        self.entry_kills.delete(0, tk.END)

        self.lbl_skulled = tk.Label(c_info, background=self.left_label_color, highlightbackground=self.left_label_color, text="Are you skulled?", font=self.stand_font_bold)
        self.lbl_skulled.grid(row=2, column=0, padx=20, pady=10)
        c_buttons = tk.Canvas(c_info, background=self.left_canvas_color, highlightbackground=self.left_canvas_color, bd=0)
        self.rb_skulled = tk.Radiobutton(c_buttons, font=self.stand_font_small_bold, variable=self.var_skulled, text="Skulled", bg=self.left_canvas_top_color, activebackground=self.left_canvas_top_color, value=1)
        self.rb_skulled.grid(row=0, column=0, pady=10)
        self.rb_not_skulled = tk.Radiobutton(c_buttons, font=self.stand_font_small_bold, variable=self.var_skulled, text="Not Skulled", bg=self.left_canvas_top_color, activebackground=self.left_canvas_top_color, value=2)
        self.rb_not_skulled.grid(row=0, column=1, pady=10)
        c_buttons.grid(row=2, column=1, padx=20, pady=5)

        self.lbl_mode = tk.Label(c_info, background=self.left_label_color, highlightbackground=self.left_label_color, text="Which speed mode?", font=self.stand_font_bold)
        self.lbl_mode.grid(row=3, column=0, padx=20, pady=10)
        c_buttons = tk.Canvas(c_info, background=self.left_canvas_color, highlightbackground=self.left_canvas_color, bd=0)
        self.rb_static = tk.Radiobutton(c_buttons, font=self.stand_font_small_bold, variable=self.var_display, text="Fast Mode", bg=self.left_canvas_top_color, activebackground=self.left_canvas_top_color, value=1)
        self.rb_static.grid(row=0, column=0, pady=10)
        self.rb_dynamic = tk.Radiobutton(c_buttons, font=self.stand_font_small_bold, variable=self.var_display, text="Fancy Mode", bg=self.left_canvas_top_color, activebackground=self.left_canvas_top_color, value=2)
        self.rb_dynamic.grid(row=0, column=1, pady=10)
        c_buttons.grid(row=3, column=1, padx=20, pady=5)

        self.lbl_status = tk.Label(c_info, background=self.left_label_color, highlightbackground=self.left_label_color, text="Standing by...", font=self.stand_font_bold)
        self.lbl_status.grid(row=4, column=0, padx=20, pady=10)
        self.btn_start = tk.Button(c_info, text="   Press to generate loot   ", command=lambda: self.display_choice(), activebackground="#1c8170", font=self.stand_font_small_bold, bg="#30d7bb")
        self.btn_start.grid(row=4, column=1, padx=20, pady=10)
        self.btn_start.bind("<Enter>", lambda e: self.btn_start.config(bg="#26ac95"))
        self.btn_start.bind("<Leave>", lambda e: self.btn_start.config(bg="#30d7bb"))
        c_info.pack(side="top", pady=20)

        # Old color for c_image and revenant_photo_lbl was #219581
        c_bottom = tk.Canvas(c_left, width=365, height=365, background="#13564a", highlightbackground="#13564a", bd=5, borderwidth=5)
        c_image = tk.Canvas(c_bottom, width=350, height=350, background="#1d8674", highlightbackground="#1d8674", bd=0, highlightthickness=0, relief='ridge')
        self.revenant_image = PIL.Image.open(resource_path("images/revenants/Select a revenant.png"))
        self.revenant_photo_image = PIL.ImageTk.PhotoImage(self.revenant_image)
        self.revenant_photo_lbl = tk.Label(c_image, image=self.revenant_photo_image, width=350, height=350, bg="#1d8674", highlightbackground="#219581", bd=0, highlightthickness=1, relief='ridge')
        self.revenant_photo_lbl.pack(padx=10, pady=10)
        c_image.pack(side="top", padx=5, pady=5)
        c_bottom.pack(side="top", pady=(5, 35))

        self.lbl_signature = self.lbl_mode = tk.Label(c_left, background=self.left_label_color, text="© RedX1000/CrownMauler", font=self.stand_font_small_bold)
        self.lbl_signature.pack(side="top", anchor="w", padx=1, pady=1)
        c_left.pack(side="left")


        c_right = tk.Canvas(main_frame, background="gray62", highlightbackground="light gray", bd=0, highlightthickness=0, relief='ridge')

        self.title_x_spacing = (5, 5)
        self.title_y_spacing = (6, 6)
        self.grid_x_spacing = (10, 5)
        self.grid_y_spacing = (2, 2)

        self.lbl_loot_title = tk.Label(c_right, text="                  Here is your loot!                  ", font=self.title_font, background="gray50")
        self.lbl_loot_title.pack(side="top")

        self.lbl_currency_title = tk.Label(c_right, text="  Ether & Coins  ", font=self.desc_font, background="gray50")
        self.lbl_currency_title.pack(side="top", padx=self.title_x_spacing, pady=self.title_y_spacing, anchor="w")
        c_currency = tk.Canvas(c_right, background="gray62", highlightbackground="gray", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_ether_img = tk.Label(c_currency, image=self.img_item_list[42], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_ether_value = tk.Label(c_currency, text="0", font=self.stand_font_small, background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_ether_value.grid(row=1, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_coins_img = tk.Label(c_currency, image=self.img_item_list[25], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_coins_value = tk.Label(c_currency, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_coins_value.grid(row=1, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        c_currency.pack(side="top", anchor="w")
        for i in range(4):
            if i % 2 == 0:
                c_currency.grid_columnconfigure(i, minsize=35)
            else:
                c_currency.grid_columnconfigure(i, minsize=80)

        self.lbl_weapons_title = tk.Label(c_right, text="  Weapons & Statuettes  ", font=self.desc_font, background="gray50")
        self.lbl_weapons_title.pack(side="top", padx=self.title_x_spacing, pady=self.title_y_spacing, anchor="w")
        c_weapons_statuettes = tk.Canvas(c_right, background="gray62", highlightbackground="gray", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_avarice_img = tk.Label(c_weapons_statuettes, image=self.img_item_list[2], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_avarice_value = tk.Label(c_weapons_statuettes, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_avarice_value.grid(row=1, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_bow_img = tk.Label(c_weapons_statuettes, image=self.img_item_list[26], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_bow_value = tk.Label(c_weapons_statuettes, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_bow_value.grid(row=1, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_sceptre_img = tk.Label(c_weapons_statuettes, image=self.img_item_list[51], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=4, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_sceptre_value = tk.Label(c_weapons_statuettes, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_sceptre_value.grid(row=1, column=5, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_chainmace_img = tk.Label(c_weapons_statuettes, image=self.img_item_list[53], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=6, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_chainmace_value = tk.Label(c_weapons_statuettes, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_chainmace_value.grid(row=1, column=7, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_emblem_img = tk.Label(c_weapons_statuettes, image=self.img_item_list[5], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_emblem_value = tk.Label(c_weapons_statuettes, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_emblem_value.grid(row=2, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_totem_img = tk.Label(c_weapons_statuettes, image=self.img_item_list[9], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_totem_value = tk.Label(c_weapons_statuettes, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_totem_value.grid(row=2, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_crystal_img = tk.Label(c_weapons_statuettes, image=self.img_item_list[3], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=4, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_crystal_value = tk.Label(c_weapons_statuettes, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_crystal_value.grid(row=2, column=5, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_statuette_img = tk.Label(c_weapons_statuettes, image=self.img_item_list[8], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=6, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_statuette_value = tk.Label(c_weapons_statuettes, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_statuette_value.grid(row=2, column=7, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_medallion_img = tk.Label(c_weapons_statuettes, image=self.img_item_list[6], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=3, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_medallion_value = tk.Label(c_weapons_statuettes, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_medallion_value.grid(row=3, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_effigy_img = tk.Label(c_weapons_statuettes, image=self.img_item_list[4], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=3, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_effigy_value = tk.Label(c_weapons_statuettes, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_effigy_value.grid(row=3, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_relic_img = tk.Label(c_weapons_statuettes, image=self.img_item_list[7], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=3, column=4, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_relic_value = tk.Label(c_weapons_statuettes, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_relic_value.grid(row=3, column=5, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        c_weapons_statuettes.pack(side="top", anchor="w")
        for i in range(8):
            if i % 2 == 0:
                c_weapons_statuettes.grid_columnconfigure(i, minsize=35)
            else:
                c_weapons_statuettes.grid_columnconfigure(i, minsize=80)

        self.lbl_equipment_title = tk.Label(c_right, text="  Equipment  ", font=self.desc_font, background="gray50")
        self.lbl_equipment_title.pack(side="top", padx=self.title_x_spacing, pady=self.title_y_spacing, anchor="w")
        c_equipment = tk.Canvas(c_right, background="gray62", highlightbackground="gray", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_brace_img = tk.Label(c_equipment, image=self.img_item_list[23], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_brace_value = tk.Label(c_equipment, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_brace_value.grid(row=1, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_staff_img = tk.Label(c_equipment, image=self.img_item_list[10], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_staff_value = tk.Label(c_equipment, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_staff_value.grid(row=1, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_rhelm_img = tk.Label(c_equipment, image=self.img_item_list[43], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=4, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_rhelm_value = tk.Label(c_equipment, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_rhelm_value.grid(row=1, column=5, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_rplate_img = tk.Label(c_equipment, image=self.img_item_list[45], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=6, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_rplate_value = tk.Label(c_equipment, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_rplate_value.grid(row=1, column=7, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_rlegs_img = tk.Label(c_equipment, image=self.img_item_list[46], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_rlegs_value = tk.Label(c_equipment, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_rlegs_value.grid(row=2, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_rkite_img = tk.Label(c_equipment, image=self.img_item_list[44], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_rkite_value = tk.Label(c_equipment, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_rkite_value.grid(row=2, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_rhammer_img = tk.Label(c_equipment, image=self.img_item_list[47], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=4, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_rhammer_value = tk.Label(c_equipment, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_rhammer_value.grid(row=2, column=5, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dds_img = tk.Label(c_equipment, image=self.img_item_list[29], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=6, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dds_value = tk.Label(c_equipment, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_dds_value.grid(row=2, column=7, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dlong_img = tk.Label(c_equipment, image=self.img_item_list[30], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=3, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dlong_value = tk.Label(c_equipment, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_dlong_value.grid(row=3, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dlegs_img = tk.Label(c_equipment, image=self.img_item_list[32], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=3, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dlegs_value = tk.Label(c_equipment, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_dlegs_value.grid(row=3, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dskirt_img = tk.Label(c_equipment, image=self.img_item_list[33], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=3, column=4, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dskirt_value = tk.Label(c_equipment, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_dskirt_value.grid(row=3, column=5, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dhelm_img = tk.Label(c_equipment, image=self.img_item_list[31], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=3, column=6, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dhelm_value = tk.Label(c_equipment, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_dhelm_value.grid(row=3, column=7, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        c_equipment.pack(side="top", anchor="w")
        for i in range(8):
            if i % 2 == 0:
                c_equipment.grid_columnconfigure(i, minsize=35)
            else:
                c_equipment.grid_columnconfigure(i, minsize=80)

        self.lbl_resources_title = tk.Label(c_right, text="  Resources  ", font=self.desc_font, background="gray50")
        self.lbl_resources_title.pack(side="top", padx=self.title_x_spacing, pady=self.title_y_spacing, anchor="w")
        c_resources = tk.Canvas(c_right, background="gray62", highlightbackground="gray", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_coal_img = tk.Label(c_resources, image=self.img_item_list[24], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_coal_value = tk.Label(c_resources, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_coal_img.grid(row=1, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_coal_value.grid(row=1, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_runite_img = tk.Label(c_resources, image=self.img_item_list[49], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_runite_value = tk.Label(c_resources, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_runite_img.grid(row=1, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_runite_value.grid(row=1, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_abar_img = tk.Label(c_resources, image=self.img_item_list[1], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_abar_value = tk.Label(c_resources, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_abar_img.grid(row=1, column=4, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_abar_value.grid(row=1, column=5, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_rbar_img = tk.Label(c_resources, image=self.img_item_list[48], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_rbar_value = tk.Label(c_resources, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_rbar_img.grid(row=1, column=6, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_rbar_value.grid(row=1, column=7, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dhide_img = tk.Label(c_resources, image=self.img_item_list[11], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_dhide_value = tk.Label(c_resources, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_dhide_img.grid(row=2, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dhide_value.grid(row=2, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dstone_img = tk.Label(c_resources, image=self.img_item_list[52], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_dstone_value = tk.Label(c_resources, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_dstone_img.grid(row=2, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dstone_value.grid(row=2, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_ylog_img = tk.Label(c_resources, image=self.img_item_list[54], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_ylog_value = tk.Label(c_resources, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_ylog_img.grid(row=2, column=4, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_ylog_value.grid(row=2, column=5, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_mlog_img = tk.Label(c_resources, image=self.img_item_list[37], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_mlog_value = tk.Label(c_resources, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_mlog_img.grid(row=2, column=6, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_mlog_value.grid(row=2, column=7, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_mplank_img = tk.Label(c_resources, image=self.img_item_list[39], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_mplank_value = tk.Label(c_resources, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_mplank_img.grid(row=3, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_mplank_value.grid(row=3, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_yseed_img = tk.Label(c_resources, image=self.img_item_list[55], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_yseed_value = tk.Label(c_resources, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_yseed_img.grid(row=3, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_yseed_value.grid(row=3, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_mseed_img = tk.Label(c_resources, image=self.img_item_list[38], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_mseed_value = tk.Label(c_resources, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_mseed_img.grid(row=3, column=4, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_mseed_value.grid(row=3, column=5, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        c_resources.pack(side="top", anchor="w")
        for i in range(8):
            if i % 2 == 0:
                c_resources.grid_columnconfigure(i, minsize=35)
            else:
                c_resources.grid_columnconfigure(i, minsize=80)

        self.lbl_resources_title = tk.Label(c_right, text="  Other & Tertiary  ", font=self.desc_font, background="gray50")
        self.lbl_resources_title.pack(side="top", padx=self.title_x_spacing, pady=self.title_y_spacing, anchor="w")
        c_other_tertiary = tk.Canvas(c_right, background="gray62", highlightbackground="gray", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_teleport_img = tk.Label(c_other_tertiary, image=self.img_item_list[41], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_teleport_value = tk.Label(c_other_tertiary, text="Disabled", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_teleport_value.grid(row=1, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_law_img = tk.Label(c_other_tertiary, image=self.img_item_list[35], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_law_value = tk.Label(c_other_tertiary, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_law_value.grid(row=1, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_death_img = tk.Label(c_other_tertiary, image=self.img_item_list[27], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=4, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_death_value = tk.Label(c_other_tertiary, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_death_value.grid(row=1, column=5, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_blood_img = tk.Label(c_other_tertiary, image=self.img_item_list[22], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=6, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_blood_value = tk.Label(c_other_tertiary, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_blood_value.grid(row=1, column=7, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dstonetip_img = tk.Label(c_other_tertiary, image=self.img_item_list[28], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_dstonetip_value = tk.Label(c_other_tertiary, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_dstonetip_value.grid(row=2, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_onyxtip_img = tk.Label(c_other_tertiary, image=self.img_item_list[40], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_onyxtip_value = tk.Label(c_other_tertiary, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_onyxtip_value.grid(row=2, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_lootbag_img = tk.Label(c_other_tertiary, image=self.img_item_list[36], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=4, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_lootbag_value = tk.Label(c_other_tertiary, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_lootbag_value.grid(row=2, column=5, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_enchant_img = tk.Label(c_other_tertiary, image=self.img_item_list[50], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=6, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_enchant_value = tk.Label(c_other_tertiary, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_enchant_value.grid(row=2, column=7, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_key_img = tk.Label(c_other_tertiary, image=self.img_item_list[34], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=3, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_key_value = tk.Label(c_other_tertiary, text="0", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_key_value.grid(row=3, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        c_other_tertiary.pack(side="top", anchor="w")
        for i in range(8):
            if i % 2 == 0:
                c_other_tertiary.grid_columnconfigure(i, minsize=35)
            else:
                c_other_tertiary.grid_columnconfigure(i, minsize=80)

        self.lbl_blighted_title = tk.Label(c_right, text="  Blighted  ", font=self.desc_font, background="gray50")
        self.lbl_blighted_title.pack(side="top", padx=self.title_x_spacing, pady=self.title_y_spacing, anchor="w")
        c_blighted = tk.Canvas(c_right, background="gray62", highlightbackground="gray", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_bind_img = tk.Label(c_blighted, image=self.img_item_list[14], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_bind_value = tk.Label(c_blighted, text="Disabled", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_bind_value.grid(row=1, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_snare_img = tk.Label(c_blighted, image=self.img_item_list[18], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_snare_value = tk.Label(c_blighted, text="Disabled", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_snare_value.grid(row=1, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_entangle_img = tk.Label(c_blighted, image=self.img_item_list[15], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=4, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_entangle_value = tk.Label(c_blighted, text="Disabled", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_entangle_value.grid(row=1, column=5, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_teleblock_img = tk.Label(c_blighted, image=self.img_item_list[20], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=1, column=6, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_teleblock_value = tk.Label(c_blighted, text="Disabled", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_teleblock_value.grid(row=1, column=7, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_vengeance_img = tk.Label(c_blighted, image=self.img_item_list[21], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_vengeance_value = tk.Label(c_blighted, text="Disabled", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_vengeance_value.grid(row=2, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_ice_img = tk.Label(c_blighted, image=self.img_item_list[12], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_ice_value = tk.Label(c_blighted, text="Disabled", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_ice_value.grid(row=2, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_karam_img = tk.Label(c_blighted, image=self.img_item_list[16], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=4, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_karam_value = tk.Label(c_blighted, text="Disabled", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_karam_value.grid(row=2, column=5, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_manta_img = tk.Label(c_blighted, image=self.img_item_list[17], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=2, column=6, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_manta_value = tk.Label(c_blighted, text="Disabled", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_manta_value.grid(row=2, column=7, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_angler_img = tk.Label(c_blighted, image=self.img_item_list[13], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=3, column=0, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_angler_value = tk.Label(c_blighted, text="Disabled", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_angler_value.grid(row=3, column=1, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_restore_img = tk.Label(c_blighted, image=self.img_item_list[19], background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge').grid(row=3, column=2, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        self.lbl_restore_value = tk.Label(c_blighted, text="Disabled", font=self.stand_font_small,  background="gray62", highlightbackground="gray62", bd=0, highlightthickness=0, relief='ridge')
        self.lbl_restore_value.grid(row=3, column=3, padx=self.grid_x_spacing, pady=self.grid_y_spacing)
        c_blighted.pack(side="top", anchor="w")
        for i in range(8):
            if i % 2 == 0:
                c_blighted.grid_columnconfigure(i, minsize=35)
            else:
                c_blighted.grid_columnconfigure(i, minsize=80)

        c_right.pack(side="right", anchor="n")

        self.label_list = [self.lbl_ether_value, self.lbl_coins_value, self.lbl_chainmace_value, self.lbl_bow_value,
                           self.lbl_sceptre_value, self.lbl_avarice_value, self.lbl_relic_value,
                           self.lbl_medallion_value,
                           self.lbl_statuette_value, self.lbl_effigy_value, self.lbl_mseed_value, self.lbl_yseed_value,
                           self.lbl_crystal_value, self.lbl_totem_value, self.lbl_emblem_value, self.lbl_dhelm_value,
                           self.lbl_brace_value, self.lbl_staff_value, self.lbl_rhelm_value, self.lbl_rplate_value,
                           self.lbl_rlegs_value, self.lbl_rkite_value, self.lbl_rhammer_value, self.lbl_dds_value,
                           self.lbl_dlong_value, self.lbl_dlegs_value, self.lbl_dskirt_value, self.lbl_coal_value,
                           self.lbl_runite_value, self.lbl_abar_value, self.lbl_rbar_value, self.lbl_dhide_value,
                           self.lbl_dstone_value, self.lbl_ylog_value, self.lbl_mlog_value, self.lbl_mplank_value,
                           self.lbl_teleport_value, self.lbl_law_value, self.lbl_death_value, self.lbl_blood_value,
                           self.lbl_dstonetip_value, self.lbl_onyxtip_value, self.lbl_lootbag_value, self.lbl_key_value,
                           self.lbl_enchant_value, self.lbl_bind_value, self.lbl_snare_value, self.lbl_entangle_value,
                           self.lbl_teleblock_value, self.lbl_vengeance_value, self.lbl_ice_value, self.lbl_karam_value,
                           self.lbl_manta_value, self.lbl_angler_value, self.lbl_restore_value]

    def display_choice(self):
        if self.var_display.get() == 2:
            self.start_menu_thread()
        else:
            self.menu()


    def change_picture(self):
        # https://stackoverflow.com/questions/3482081
        img = PIL.ImageTk.PhotoImage(Image.open(resource_path("images/revenants/"+self.revenant_data_var.get()+".png")))
        self.revenant_photo_lbl.configure(image=img)
        self.revenant_photo_lbl.image = img


    def start_menu_thread(event):
        # TO-DONE AND COMPLETE: Actually TRY to learn multithreading for once.
        #                       Success! It's a bit janky but it'll do.
        #                       https://stackoverflow.com/questions/41371815
        global menu_thread
        menu_thread = threading.Thread(target=event.menu)
        menu_thread.daemon = True
        menu_thread.start()

    def label_refresh(self):
        for i in range(len(self.label_list)):
            if i == 36 or i >= 45:
                pass
            else:
                self.label_list[i]["text"] = 0

    def label_update(self):
        for i in range(len(self.label_list)):
            if i == 36 or i >= 45:
                pass
            else:
                self.label_list[i]["text"] = str(self.total_drops[i])

    def menu(self):
        passed_try = True
        try:
            int(self.var_entry_kills.get())
        except:
            passed_try = False
            self.lbl_status['bg'] = "Orange"
            self.lbl_status['text'] = "Enter numbers only"

        print(self.var_entry_kills.get())
        if self.revenant_data_var.get() == "Select a revenant" and passed_try == True:
            self.lbl_status['bg'] = "Orange"
            self.lbl_status['text'] = "Choose a revenant"
        elif int(self.var_entry_kills.get()) < 0 and passed_try == True:
            self.lbl_status['bg'] = "Orange"
            self.lbl_status['text'] = "No negative/zero kills"
        elif self.var_entry_kills.get().find("0") == 0 and passed_try == True:
            self.lbl_status['bg'] = "Orange"
            self.lbl_status['text'] = "No leading zeroes"
        elif passed_try == True:
            try:
                self.lbl_status['bg'] = "yellow"
                self.lbl_status['text'] = "Running..."
                self.lbl_status.update_idletasks()

                skull = self.var_skulled.get()
                print(self.var_entry_kills.get())
                kills = str(self.var_entry_kills.get())
                kills = int(kills)
                data = self.revenant_data[self.revenant_data_var.get()]
                level = data[0]
                hp = data[1]
                display = self.var_display.get()

                self.total_drops = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                self.label_refresh()

                if level < 10:
                    bag_level = 10
                elif level > 50:
                    bag_level = 50
                else:
                    bag_level = level

                for i in range(0, kills):
                    if level > 144:
                        clamped_level = 144
                    elif level < 1:
                        clamped_level = 1
                    else:
                        clamped_level = level

                    # Formula for chance_a
                    chance_a = int(2200 / int(math.sqrt(clamped_level)))

                    # Formula for chance_b
                    chance_b = int(15 + (math.pow((level + 60), 2) / 200))

                    # This will randomize a number,
                    # A is set between 0 and (chance_a - 1) inclusive
                    a = int(random.randint(0, (chance_a - 1)))

                    if a == 0:
                        self.good_drops(skull, display)
                    elif a >= 1 and a <= chance_b:
                        self.mediocre_drops(display)

                    # Ether
                    if display == 2:
                        self.lbl_ether_value["text"] = int(self.lbl_ether_value["text"]) + (random.randint(1, math.ceil(1 + math.sqrt(level) + math.floor(math.sqrt(level))) / 2) * 2)
                    else:
                        self.total_drops[0] += random.randint(1, math.ceil(1 + math.sqrt(level) + math.floor(math.sqrt(level))) / 2) * 2

                    # Coins
                    if self.revenant_data_var.get() == "Revenant dragon":
                        pass
                    else:
                        if display == 2:
                            self.lbl_coins_value["text"] = int(self.lbl_coins_value["text"]) + random.randint(1, math.ceil(1 + 25 * math.floor(math.sqrt(level))))
                        else:
                            self.total_drops[1] += random.randint(1, math.ceil(1 + 25 * math.floor(math.sqrt(level))))

                    # Looting Bag
                    if int(random.randint(1, math.floor(150 / bag_level))) == 1:
                        if display == 2:
                            self.lbl_lootbag_value["text"] = int(self.lbl_lootbag_value["text"]) + 1
                        else:
                            self.total_drops[42] += 1

                    # Slayer's Enchantment
                    if int(random.randint(1, 320 - math.floor(float(hp) * 8/10))) == 1:
                        if display == 2:
                            self.lbl_enchant_value["text"] = int(self.lbl_enchant_value["text"]) + 1
                        else:
                            self.total_drops[43] += 1

                    # Larran's Key
                    if level <= 80:
                        if random.randint(1, math.floor((3/10) * math.pow((80 - level), 2)) + 100) == 1:
                            if display == 2:
                                self.lbl_key_value["text"] = int(self.lbl_key_value["text"]) + 1
                            else:
                                self.total_drops[44] += 1
                    # Formula is supposed to be + 115, but the result is +1 higher than expected
                    # So I randint at 2 instead :(
                    # Was told I should int truncate, but the formula shows a floor.
                    elif level >= 81:
                        if random.randint(2, math.floor((5/-27) * level) + 115) == 2:
                            if display == 2:
                                self.lbl_key_value["text"] = int(self.lbl_key_value["text"]) + 1
                            else:
                                self.total_drops[44] += 1

                        # print(self.revenant_data_var.get() +", "+ str(level))
                        # print("math.floor((5/-27) * "+str(level)+") + 114 = " + str(math.floor((5/-27) * level) + 115))

                    # Todo: Add Blighted items when they give drop rates

                    if display == 2:
                        self.lbl_status.update_idletasks()

                if display == 1:
                    self.label_update()

                self.lbl_status['bg'] = "lime green"
                self.lbl_status['text'] = "   Finished!   "

            except Exception as e:
                print(e)
                self.lbl_status['bg'] = "OrangeRed2"
                self.lbl_status['text'] = "Some Crash Occurred"
                self.lbl_status.update_idletasks()


    def good_drops(self, skull, display):
        if skull == 1:
            val = random.randint(0, 21)
        else:
            val = random.randint(0, 39)
        if display == 2:
            if val == 0:
                wep_val = random.randint(0, 4)
                if wep_val == 0:  # Viggora's Chainmace
                    self.lbl_chainmace_value["text"] = int(self.lbl_chainmace_value["text"]) + 1
                elif wep_val == 1:  # Craw's Bow
                    self.lbl_bow_value["text"] = int(self.lbl_bow_value["text"]) + 1
                elif wep_val == 2:  # Thammaron's Sceptre
                    self.lbl_sceptre_value["text"] = int(self.lbl_sceptre_value["text"]) + 1
                else:  # Amulet of Avarice
                    self.lbl_avarice_value["text"] = int(self.lbl_avarice_value["text"]) + 1
            elif val == 1:  # Ancient Relic
                self.lbl_relic_value["text"] = int(self.lbl_relic_value["text"]) + 1
            elif val == 2:  # Ancient Effigy
                self.lbl_effigy_value["text"] = int(self.lbl_effigy_value["text"]) + 1
            elif val == 3:  # Ancient Medallion
                self.lbl_medallion_value["text"] = int(self.lbl_medallion_value["text"]) + 1
            elif val == 4 or val == 5:  # Ancient Statuette
                self.lbl_statuette_value["text"] = int(self.lbl_statuette_value["text"]) + 1
            elif val in [6, 7, 8, 9]:  # Magic tree seed
                self.lbl_mseed_value["text"] = int(self.lbl_mseed_value["text"]) + random.randint(2, 6)
            elif val in [10, 11, 12, 13]:  # Yew tree seed
                self.lbl_yseed_value["text"] = int(self.lbl_yseed_value["text"]) + random.randint(2, 6)
            elif val in [14, 15, 16]:  # Ancient Crystal
                self.lbl_crystal_value["text"] = int(self.lbl_crystal_value["text"]) + 1
            elif val in [17, 18, 19, 20]:  # Ancient Totem
                self.lbl_totem_value["text"] = int(self.lbl_totem_value["text"]) + 1
            elif val in [21, 22, 23, 24, 25, 26]:  # Ancient Emblem
                self.lbl_emblem_value["text"] = int(self.lbl_emblem_value["text"]) + 1
            elif val >= 27 or val <= 39:  # Dragon med helm
                self.lbl_dhelm_value["text"] = int(self.lbl_dhelm_value["text"]) + 1

        else:
            if val == 0:
                wep_val = random.randint(0, 4) #todo: fix order?
                if wep_val == 0:  # Viggora's Chainmace
                    self.total_drops[2] += 1
                elif wep_val == 1:  # Craw's Bow
                    self.total_drops[3] += 1
                elif wep_val == 2:  # Thammaron's Sceptre
                    self.total_drops[4] += 1
                else:  # Amulet of Avarice
                    self.total_drops[5] += 1
            elif val == 1:  # Ancient Relic
                self.total_drops[6] += 1
            elif val == 2:  # Ancient Effigy
                self.total_drops[7] += 1
            elif val == 3:  # Ancient Medallion
                self.total_drops[8] += 1
            elif val == 4 or val == 5:  # Ancient Statuette
                self.total_drops[9] += 1
            elif val in [6, 7, 8, 9]:  # Magic tree seed
                self.total_drops[10] += random.randint(2, 6)
            elif val in [10, 11, 12, 13]:  # Yew tree seed
                self.total_drops[11] += random.randint(2, 6)
            elif val in [14, 15, 16]:  # Ancient Crystal
                self.total_drops[12] += 1
            elif val in [17, 18, 19, 20]:  # Ancient Totem
                self.total_drops[13] += 1
            elif val in [21, 22, 23, 24, 25, 26]:  # Ancient Emblem
                self.total_drops[14] += 1
            elif val >= 27 or val <= 39:  # Dragon med helm
                self.total_drops[15] += 1


    def mediocre_drops(self, display):
        val = random.randint(1, 106)
        if display == 2:
            if val in [1, 2, 3, 4, 5]:  # Battlestaves
                self.lbl_staff_value["text"] = int(self.lbl_staff_value["text"]) + 4
            elif val in [6, 7]:  # Rune Full Helm
                self.lbl_rhelm_value["text"] = int(self.lbl_rhelm_value["text"]) + 2
            elif val in [8, 9]:  # Rune Platebody
                self.lbl_rplate_value["text"] = int(self.lbl_rplate_value["text"]) + 2
            elif val in [10, 11]:  # Rune Platelegs
                self.lbl_rlegs_value["text"] = int(self.lbl_rlegs_value["text"]) + 2
            elif val in [12, 13]:  # Rune Kiteshield
                self.lbl_rkite_value["text"] = int(self.lbl_rkite_value["text"]) + 2
            elif val in [14, 15]:  # Rune Warhammer
                self.lbl_rhammer_value["text"] = int(self.lbl_rhammer_value["text"]) + 2
            elif val == 16:  # Dragon Dagger
                self.lbl_dds_value["text"] = int(self.lbl_dds_value["text"]) + 2
            elif val == 17:  # Dragon Longsword
                self.lbl_dlong_value["text"] = int(self.lbl_dlong_value["text"]) + 2
            elif val == 18:  # Dragon Platelegs
                self.lbl_dlegs_value["text"] = int(self.lbl_dlegs_value["text"]) + random.randint(1, 2)
            elif val == 19:  # Dragon Plateskirt
                self.lbl_dskirt_value["text"] = int(self.lbl_dskirt_value["text"]) + random.randint(1, 2)
            elif val in [20, 21, 22, 23, 24, 25]:  # Coal
                self.lbl_coal_value["text"] = int(self.lbl_coal_value["text"]) + random.randint(30, 60)
            elif val in [26, 27, 28, 29, 30, 31]:  # Runite Ore
                self.lbl_runite_value["text"] = int(self.lbl_runite_value["text"]) + random.randint(2, 4)
            elif val in [31, 32, 33, 34, 35, 36]:  # Adamant Bar
                self.lbl_abar_value["text"] = int(self.lbl_abar_value["text"]) + random.randint(4, 6)
            elif val in [37, 38, 39, 40, 41, 42]:  # Runite Bar
                self.lbl_rbar_value["text"] = int(self.lbl_rbar_value["text"]) + random.randint(2, 3)
            elif val in [43, 44, 45, 46, 47, 48]:  # Black Dragonhide
                self.lbl_dhide_value["text"] = int(self.lbl_dhide_value["text"]) + 4
            elif val == 49:  # Uncut Dragonstone
                self.lbl_dstone_value["text"] = int(self.lbl_dstone_value["text"]) + random.randint(2, 5)
            elif val in [50, 51, 52]:  # Yew Logs
                self.lbl_ylog_value["text"] = int(self.lbl_ylog_value["text"]) + random.randint(20, 40)
            elif val in [53, 54]:  # Magic Logs
                self.lbl_mlog_value["text"] = int(self.lbl_mlog_value["text"]) + random.randint(8, 16)
            elif val in [55, 56, 57, 58, 59]:  # Mahogany Plank
                self.lbl_mplank_value["text"] = int(self.lbl_mplank_value["text"]) + random.randint(8, 16)
            elif val in [60, 61, 62]:  # Law Runes
                self.lbl_law_value["text"] = int(self.lbl_law_value["text"]) + random.randint(20, 45)
            elif val in [63, 64, 65]:  # Death Runes
                self.lbl_death_value["text"] = int(self.lbl_death_value["text"]) + random.randint(30, 60)
            elif val in [66, 67, 68]:  # Blood Runes
                self.lbl_blood_value["text"] = int(self.lbl_blood_value["text"]) + random.randint(50, 100)
            elif val in [69, 70, 71, 72]:  # Dragonstone Bolt Tips
                self.lbl_dstonetip_value["text"] = int(self.lbl_dstonetip_value["text"]) + random.randint(20, 40)
            elif val in [73, 74, 75, 76]:  # Onyx Bolt Tips
                self.lbl_onyxtip_value["text"] = int(self.lbl_onyxtip_value["text"]) + random.randint(3, 6)
        #   elif val in [Some range]:
        #       Give teleport
            else:
                self.lbl_brace_value["text"] = int(self.lbl_brace_value["text"]) + 1

        else:
            if val in [1, 2, 3, 4, 5]:  # Battlestaves
                self.total_drops[17] += 4
            elif val in [6, 7]:  # Rune Full Helm
                self.total_drops[18] += 2
            elif val in [8, 9]:  # Rune Platebody
                self.total_drops[19] += 2
            elif val in [10, 11]:  # Rune Platelegs
                self.total_drops[20] += 2
            elif val in [12, 13]:  # Rune Kiteshield
                self.total_drops[21] += 2
            elif val in [14, 15]:  # Rune Warhammer
                self.total_drops[22] += 2
            elif val == 16:  # Dragon Dagger
                self.total_drops[23] += 2
            elif val == 17:  # Dragon Longsword
                self.total_drops[24] += 2
            elif val == 18:  # Dragon Platelegs
                self.total_drops[25] += random.randint(1, 2)
            elif val == 19:  # Dragon Plateskirt
                self.total_drops[26] += random.randint(1, 2)
            elif val in [20, 21, 22, 23, 24, 25]:  # Coal
                self.total_drops[27] += random.randint(30, 60)
            elif val in [26, 27, 28, 29, 30, 31]:  # Runite Ore
                self.total_drops[28] += random.randint(2, 4)
            elif val in [31, 32, 33, 34, 35, 36]:  # Adamant Bar
                self.total_drops[29] += random.randint(4, 6)
            elif val in [37, 38, 39, 40, 41, 42]:  # Runite Bar
                self.total_drops[30] += random.randint(2, 3)
            elif val in [43, 44, 45, 46, 47, 48]:  # Black Dragonhide
                self.total_drops[31] += 4
            elif val == 49:  # Uncut Dragonstone
                self.total_drops[32] += random.randint(2, 5)
            elif val in [50, 51, 52]:  # Yew Logs
                self.total_drops[33] += random.randint(20, 40)
            elif val in [53, 54]:  # Magic Logs
                self.total_drops[34] += random.randint(8, 16)
            elif val in [55, 56, 57, 58, 59]:  # Mahogany Plank
                self.total_drops[35] += random.randint(8, 16)
            elif val in [60, 61, 62]:  # Law Runes
                self.total_drops[37] += random.randint(20, 45)
            elif val in [63, 64, 65]:  # Death Runes
                self.total_drops[38] += random.randint(30, 60)
            elif val in [66, 67, 68]:  # Blood Runes
                self.total_drops[39] += random.randint(50, 100)
            elif val in [69, 70, 71, 72]:  # Dragonstone Bolt Tips
                self.total_drops[40] += random.randint(20, 40)
            elif val in [73, 74, 75, 76]:  # Onyx Bolt Tips
                self.total_drops[41] += random.randint(3, 6)
        #   elif val in [Some range]:
        #       self.total_drops[36] give teleports
            else:
                self.total_drops[16] += 1



if __name__ == '__main__':
    root = tk.Tk()
    root.iconbitmap(resource_path("images/revenants/revenant_imp.ico"))
    root.title("Osrs Revenant Drop Generator: Remake")
    a = Application(root)
    root.configure(bg="gray62")
    root.mainloop()
