from tkinter import *
from prop import HEIGHT, WIDTH, MULT, bgColor
from Entities import *
from Enums import LiverStatus
from Analitics import *


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


class Render:
    window = None
    canvas = None

    def __init__(self, area_obj):
        self.area = area_obj

    def show_in_terminal(self):
        for i in self.area.space:
            for a in i:
                print(a.obj, end='')
            print()
        for i in self.area.space:
            for a in i:
                if isinstance(a.obj, Liver):
                    print(a.obj.get_info())
        print(Liver.counter)

    def init_tk(self):
        self.window = Tk()
        self.window.protocol('WM_DELETE_WINDOW', self.window_closer_handler)
        self.canvas = Canvas(self.window, height=HEIGHT*MULT, width=WIDTH*MULT, bg=bgColor)
        self.canvas.pack()

    def create_canvas(self):
        for i in self.area.space:
            for a in i:
                check_color(a)
                if a.obj.symbol == '♥':
                    self.canvas.create_rectangle(a.obj.x*MULT, a.obj.y*MULT, a.obj.x*MULT+MULT, a.obj.y*MULT+MULT,
                                                 fill='#' + str(a.obj.colors['red']) + str(a.obj.colors['green'])
                                                 + str(a.obj.colors['blue']))
                elif a.obj.symbol == '▼' or a.obj.symbol == 'Ⓟ' or a.obj.symbol == '◉':
                    self.canvas.create_oval(a.obj.x*MULT, a.obj.y*MULT, a.obj.x*MULT+MULT, a.obj.y*MULT+MULT,
                                                 fill='#' + str(a.obj.colors['red']) + str(a.obj.colors['green'])
                                                 + str(a.obj.colors['blue']))

        self.canvas.focus_set()
        self.canvas.bind("<Return>", lambda event: self.recreate_canvas(event))
        self.canvas.bind("<Button-1>", lambda event: print(self.area.space_manager.get_obj(event.x//10, event.y//10)))
        self.canvas.bind("<Button-2>", lambda event: self.area.clear(event.x//10, event.y//10, 5))
        self.canvas.bind("<Button-3>", lambda event:
        self.area.place_obj(event.x // 10, event.y // 10, Liver(event.x // 10, event.y // 10, self.area)))
        self.canvas.bind("<f>", lambda event : self.area.place_obj (event.x // 10, event.y // 10, Food(event.x // 10,
                                                                                                       event.y // 10)))
        self.canvas.bind ("<p>", lambda event : self.area.place_obj (event.x // 10, event.y // 10, Poison(event.x // 10,
                                                                                                          event.y//10)))

        self.canvas.bind("<a>", lambda event: print(self.show_in_terminal()))
        self.canvas.bind("<l>", lambda event: self.area.clear_line(event.y//10))
        self.canvas.bind("<space>", lambda event: print(event))

        self.canvas.pack()

    def recreate_canvas(self, event):
        self.canvas.pack_forget()
        self.canvas.destroy()
        self.canvas = Canvas(self.window, height=HEIGHT*MULT, width=WIDTH*MULT, bg=bgColor)
        self.create_canvas()

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



