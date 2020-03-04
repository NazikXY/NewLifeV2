from prop import WIDTH, HEIGHT
from Enums import ObjTypes
from Entities import *
from random import choice


class SpaceManager:
    def __init__(self, area_obj):
        self.area = area_obj

    def get_obj(self, x, y):
        if (0 <= x < WIDTH) & (0 <= y < HEIGHT):
            return self.area.space[y][x].obj

    def get_info(self, x, y):
        if isinstance(self.area.space[y][x].obj,  Liver):
            return self.area.space[y][x].obj.get_pinfo()

    def set_obj(self, x, y, obj):
        if (0 <= x < WIDTH) & (0 <= y < HEIGHT) :
            self.area.space[y][x].obj = obj

    def check_place(self, x, y):
        if (0 <= x < WIDTH) & (0 <= y < HEIGHT):
            if isinstance(self.get_obj(x, y), Empty):
                return ObjTypes.Empty
            elif isinstance(self.get_obj(x, y), Liver):
                return ObjTypes.Liver
            elif isinstance(self.get_obj(x, y), Food):
                return ObjTypes.Food
            elif isinstance(self.get_obj(x, y), Poison):
                return ObjTypes.Poison
            elif isinstance(self.get_obj(x, y), Corpse):
                return ObjTypes.Corpse
        else:
            return ObjTypes.Border

    def replace(self, x, y, tx, ty):
        if self.check_place(tx, ty) is ObjTypes.Border:
            return False, 'Out of Range'
        else:
            self.set_obj(tx, ty, self.get_obj(x, y))
            self.set_obj(x, y, Empty())

    def delete(self, x, y):
        if self.check_place(x, y) is not ObjTypes.Border:
            self.set_obj(x, y, Empty())

    def random_empty_coords(self, depth=0):
        if depth >= 10:
            return
        value = choice(choice(self.area.space))
        if isinstance(value.obj, Empty):
            return value
        else:
            return self.random_empty_coords()

    def look_around(self, x, y):
        coord_list = []
        res_list = []
        for i in range(-1, 2):
            for a in range(-1, 2):
                coord_list.append((a + x, i + y))

        for i in coord_list:
            res_list.append((self.get_obj(*i), *i))
        return res_list

