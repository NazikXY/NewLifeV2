from Render import Render
from SpaceManager import SpaceManager as SM
from Entities import *
from threading import Thread
from time import sleep
from Enums import *


class Point:
    obj = None
    effect = None

    def __init__(self, sl, mn, y, x):
        self.x = x
        self.y = y
        self.obj = Empty()
        self.effect = [AirEffect(sl/10), MineralEffect(mn/10)]


    def get_effects(self):
        return "sun = " + str(self.effect[0].sun_light) + " mineral = "\
               + str(self.effect[1].minerals)

    def app_eff(self):
        for i in self.effect:
            if not isinstance(self.obj, Liver):
                return
            i.apply_effect(self.obj)


class Area:
    def __init__(self, point_list):
        self.space = point_list
        self.renderer = Render(self)
        self.space_manager = SM(self)
        self.live_thread = None

    @classmethod
    def gen_area(cls, height, width):
        return [[Point(abs(y-height+1)/2, y/2, y, x)for x in range(width)] for y in range(height)]

    def text_render(self):
        self.renderer.show_in_terminal()

    def place_obj(self, x, y, obj):
        self.space_manager.set_obj(x, y, obj)

    def replace_obj(self, x, y, tx, ty):
        self.space_manager.replace(x, y, tx, ty)

    def destroy(self, x, y):
        self.space_manager.delete(x, y)

    def graph_render(self):
        self.renderer.show_g()

    def populate(self, count):
        for i in range(count):
            point = self.space_manager.random_empty_coords()
            point.obj = Liver(point.x, point.y, self)

    def run_live(self):
        self.live_thread = Thread(target=self.live, daemon=True)
        self.live_thread.start()

    def live(self):
        flag = 0
        while True:
            for row in self.space:
                for point in row:
                    if isinstance(point.obj, Liver):
                        if point.obj.generation >= 160:
                            flag = 0
                        point.obj.behavior()
                        point.app_eff()

            if Food.counter <= 10 and Poison.counter <= 10:
                self.place_food_and_poison(count=5)
            if flag:
                break
            sleep(0.01)

    def clear(self, x, y, radius):
        for i in range(-radius, radius + 1):
            for a in range(-radius, radius + 1):
                if self.space_manager.check_place(x, y) is not ObjTypes.Border:
                    if isinstance(self.space[y+a][x+i].obj, Liver):
                        self.space[y + a][x + i].obj.health = -1
                        # self.destroy(x+i, y+a)

    def place_food_and_poison(self, count):
        for i in range(count):
            result = self.space_manager.random_empty_coords()
            result = result.x, result.y
            self.place_obj(*result, Food(*result))
        for i in range(count):
            result = self.space_manager.random_empty_coords()
            result = result.x, result.y
            self.place_obj(*result, Poison(*result))

    def clear_line(self, y):
        for i in range(WIDTH):
            self.destroy(i, y)



# EFFECTS PART ####################################################################################################
class Effects:
    e_type = None

    def apply_effect(self, obj):
        pass


class AirEffect(Effects):
    def __init__(self, sun_light):
        self.e_type = "Light"
        self.sun_light = sun_light

    def apply_effect(self, obj):
        if self.sun_light >= 1:
            obj.sun_light += self.sun_light
        else:
            if obj.sun_light > 0:
                obj.sun_light -= 0.1


class MineralEffect(Effects):
    def __init__(self, mnrl):
        self.e_type = "Mineral"
        self.minerals = mnrl

    def apply_effect(self, obj):
        obj.minerals += self.minerals
