from tkinter import *
from prop import HEIGHT, WIDTH, MULT, bgColor
from Entities import *
from Enums import LiverStatus
from Analitics import *


def energy_view(value):
    if value.energy < 10:
        return '101099'
    elif 10 < value.energy < 500:
        res = value.energy/10
        if res > 99:
            res = 99
        if res < 10:
            res = 10
        if res is None :
            res = 10

        return '10'+str(int(res))+'10'
    elif 500 < value.energy:
        res = value.energy / 100
        if res > 99:
            res = 99
        if res < 10:
            res = 10
        if res is None :
            res = 10
        return str(int(res))+'1010'


def check_color(a):
    if a.obj.colors['red'] > 99:
        a.obj.colors['red'] = 99
    elif a.obj.colors['red'] < 10:
        a.obj.colors['red'] = 10

    if a.obj.colors['green'] > 99:
        a.obj.colors['green'] = 99
    elif a.obj.colors['green'] < 10:
        a.obj.colors['green'] = 10

    if a.obj.colors['blue'] > 99:
        a.obj.colors['blue'] = 99
    elif a.obj.colors['blue'] < 10:
        a.obj.colors['blue'] = 10


def command_view(obj) :
    return str(obj.command) * 3


class Render:
    window = None
    canvas = None
    check_flag = 0

    def __init__(self, area_obj):
        self.area = area_obj

    def show_in_terminal(self):
        for i in self.area.space:
            for a in i:
                print(a.obj, end='')
            print()
        for i in self.area.space:
            for a in i:
                print(a.effect[0].sun_light, a.effect[1].minerals, end='')
                break
            print()
        # for i in self.area.space:
        #     for a in i:
        #         if isinstance(a.obj, Liver):
        #             print(a.obj.get_info())
        print(Liver.counter)

    def init_tk(self):
        self.window = Tk()
        self.window.protocol('WM_DELETE_WINDOW', self.window_closer_handler)
        self.canvas = Canvas(self.window, height=HEIGHT*MULT, width=WIDTH*MULT, bg=bgColor)
        self.canvas.pack()

    def create_canvas(self):
        self.create_figures()
        self.canvas.focus_set()
        self.canvas.bind("<Return>", lambda event: self.recreate_canvas(event))
        self.canvas.bind("<Button-1>", lambda event: print(self.area.space_manager.get_obj(event.x//10, event.y//10)))
        self.canvas.bind("<Button-2>", lambda event: self.area.clear(event.x//10, event.y//10, 5))
        self.canvas.bind("<Button-3>", lambda event:
        self.area.place_obj(event.x // 10, event.y // 10, Liver(event.x // 10, event.y // 10, self.area)))
        self.canvas.bind("<f>", lambda event: self.area.place_obj (event.x // 10, event.y // 10, Food(event.x // 10,
                                                                                                      event.y // 10)))
        self.canvas.bind ("<p>", lambda event: self.area.place_obj (event.x // 10, event.y // 10, Poison(event.x // 10,
                                                                                                         event.y//10)))
        self.canvas.bind("<a>", lambda event: print(self.show_in_terminal()))
        self.canvas.bind("<l>", lambda event: self.area.clear_line(event.y//10))
        self.canvas.bind("<space>", lambda event: print(event))
        self.canvas.bind("<c>", lambda event: self.change_indicator())
        self.canvas.bind("<q>", lambda event: self.clear_all())


        self.canvas.pack()

    def recreate_canvas(self, event):
        # self.canvas.pack_forget()
        self.canvas.delete(ALL)
        # self.canvas = Canvas(self.window, height=HEIGHT*MULT, width=WIDTH*MULT, bg=bgColor)
        self.create_figures()

    def create_figures(self):
        for i in self.area.space:
            if self.check_flag == 1:
                for a in i :
                    mltx = a.x * MULT
                    mlty = a.y * MULT
                    check_color (a)
                    if a.obj.symbol == '♥' :
                        self.canvas.create_rectangle (mltx, mlty, mltx + MULT, mlty + MULT,
                                                      fill='#' + energy_view(a.obj))
                    elif a.obj.symbol == '▼' or a.obj.symbol == 'Ⓟ' or a.obj.symbol == '◉' :
                        self.canvas.create_oval (mltx, mlty, mltx + MULT, mlty + MULT,
                                                 fill='#' + str (a.obj.colors['red']) + str (a.obj.colors['green'])
                                                      + str (a.obj.colors['blue']))
                continue

            elif self.check_flag == 2:
                for a in i :
                    mltx = a.x * MULT
                    mlty = a.y * MULT
                    check_color (a)
                    if a.obj.symbol == '♥' :
                        self.canvas.create_rectangle (mltx, mlty, mltx + MULT, mlty + MULT,
                                                          fill='#' + command_view (a.obj))
                    elif a.obj.symbol == '▼' or a.obj.symbol == 'Ⓟ' or a.obj.symbol == '◉' :
                        self.canvas.create_oval (mltx, mlty, mltx + MULT, mlty + MULT,
                                                 fill='#' + str (a.obj.colors['red']) + str (a.obj.colors['green'])
                                                 + str (a.obj.colors['blue']))
                continue

            for a in i:
                mltx = a.x*MULT
                mlty = a.y*MULT
                check_color(a)
                if a.obj.symbol == '♥':
                    self.canvas.create_rectangle(mltx, mlty, mltx+MULT, mlty+MULT,
                                                 fill='#' + str(a.obj.colors['red']) + str(a.obj.colors['green'])
                                                      + str(a.obj.colors['blue']))
                elif a.obj.symbol == '▼' or a.obj.symbol == 'Ⓟ' or a.obj.symbol == '◉':
                    self.canvas.create_oval(mltx, mlty, mltx+MULT, mlty+MULT,
                                            fill='#' + str(a.obj.colors['red']) + str(a.obj.colors['green'])
                                                 + str(a.obj.colors['blue']))

    def show_g(self):
        self.init_tk()
        self.create_canvas()
        self.window.mainloop()

    def window_closer_handler(self):
        to_anal = []
        for i in self.area.space:
            for a in i:
                if isinstance(a.obj, Liver):
                    to_anal.append(a.obj)
        self.window.quit()
        # analise(to_anal)

    def change_indicator(self) :
        if self.check_flag == 0:
            self.check_flag = 1
        elif self.check_flag == 1:
            self.check_flag = 2
        elif self.check_flag == 2:
            self.check_flag = 0

    def clear_all(self) :
        for a in self.area.space:
            for i in a:
                if isinstance(i.obj, Liver):
                    self.area.destroy(i.x, i.y)



