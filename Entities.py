from random import randint, choice
from Enums import LiverStatus, ObjTypes
from prop import *
from time import sleep


class Entities:
    x = 0
    y = 0
    ids = 0
    symbol = '-'
    colors = {'red': 10, 'green': 10, 'blue': 10}
    counter = 0

    def __str__(self):
        return self.symbol


class Liver(Entities):
    ids = 0
    counter = 0
    sun_light = 0
    minerals = 0
    armor = 0
    area = None

    def get_info(self):
        return self.symbol + " generation = " + str(self.generation) + ", minerals = " + str(self.minerals) +\
               ', armor = '\
               + str(self.armor) + ', coords: (' + str(self.x)+","+str(self.y)+")" + str(self.colors) + " " \
               + str(self.health) + " " + str(self.status) + ', id = %d' % self.my_id + ' pht_c %s' % self.pht_counter

    def get_pinfo(self):
        return "#############################\n" +\
               "#  %s     %d      %s           #\n" % (self.pht_counter, self.mnrlprc_counter, self.hunt_counter) +\
               "# pht  mnrl  hunt  ##########\n" +\
               "#############################\n" +\
               "#############################\n" +\
               "#############################\n" +\
               "#############################\n" +\
               "#############################\n" +\
               "#############################\n" +\
               "#############################\n" +\
               "#############################"

    def get_brain(self):
        return str(self.brain)

    @staticmethod
    def gen_brain():
        return [randint(0, 13) for i in range(255)]

    def __init__(self, x, y, area, brain=None, generation=0, command=0):
        if command == 0:
            self.command = randint(0, 1000)
        else:
            self.command = command
        self.my_id = Liver.ids
        Liver.ids += 1
        Liver.counter += 1
        self.pht_counter = 0
        self.mnrlprc_counter = 0
        self.hunt_counter = 0
        self.health = 100
        if brain is None:
            self.brain = Liver.gen_brain()
        else:
            self.brain = brain

        self.generation = generation
        self.energy = 2
        self.acid = 0
        self.x = x
        self.y = y
        self.symbol = '♥'
        self.step = 0
        self.status = LiverStatus.Child
        self.area = area
        self.function_list = [self.move_up, self.move_down, self.move_right, self.move_left, self.pht_sintes,
                              self.mineral_processing, self.energy_transform, self.doNot, self.doNot,
                              self.doNot, self.doNot, self.doNot, self.doNot, self.doNot, self.doNot,
                              self.doNot, self.doNot, self.doNot, self.doNot, self.doNot, self.doNot,
                              self.doNot]
        self.behavior_dict = {i: self.doNot for i in range(20)}
        self.colors = {'red' : 10, 'green' : 10, 'blue' : 10}
        self.behavior_dict.update({0: self.move_up,
                                   1: self.move_down,
                                   2: self.move_right,
                                   3: self.move_left,
                                   4: self.pht_sintes,
                                   5: self.mineral_processing,
                                   6: self.energy_transform,
                                   7: self.replication,
                                   8: self.hunt,
                                   9: self.up_raise,
                                   10: self.search_food,
                                   11: self.search_poison,
                                   12: self.friend_cerry
                                   })

    def __del__(self):
        Liver.counter -= 1

    def mover(self, from_c, to):
        if to[0] == -1:
            to = (WIDTH-1, to[1])
        elif to[0] == WIDTH-1:
            to = (0, to[1])
        result = self.area.space_manager.check_place(*to)

        if result == ObjTypes.Empty:
            self.area.space_manager.replace(*from_c, *to)
            self.x, self.y = to
            self.health -= step_damage
            return 1
        elif result == ObjTypes.Corpse:
            self.eat_food(*to)
            self.health -= step_damage
            Food.counter += 1
            self.step += 2
            return 2
        elif result == ObjTypes.Border:
            self.step += 3
            return 3
        elif result == ObjTypes.Food:
            self.eat_food(*to)
            self.health -= step_damage
            self.step += 4
            return 4
        elif result == ObjTypes.Poison:
            self.eat_poison(*to)
            self.health -= step_damage
            self.step += 5
            return 5
        elif result == ObjTypes.Liver:
            res = self.eat_liver(*to)
            self.health -= step_damage
            if res:
                self.area.space_manager.replace(*from_c, *to)
            else:
                self.step += 1
                return 6

    def move_up(self):
        from_c, to = (self.x, self.y), (self.x, self.y-1)
        self.mover(from_c, to)

    def move_down(self):
        from_c, to = (self.x, self.y), (self.x, self.y + 1)
        self.mover(from_c, to)

    def move_right(self):
        from_c, to = (self.x, self.y), (self.x-1, self.y)
        self.mover(from_c, to)

    def move_left(self):
        from_c, to = (self.x, self.y), (self.x+1, self.y)
        self.mover(from_c, to)

    def energy_transform(self):
        self.health -= step_damage
        if self.health <= 100:
            if self.energy >= 50:
                self.energy -= 50
                self.health += 10

    def pht_sintes(self):
        self.health -= step_damage
        if self.sun_light >= pht_sunlight_limit and self.minerals >= pht_minerals_limit:
            self.pht_counter += 1
            tmp = (self.sun_light / light_for_photo_sintes * self.minerals / minerals_for_photo_sintes) * pht_efficiency
            self.energy += tmp
            self.acid += tmp
            self.sun_light /= light_for_photo_sintes
            self.minerals /= minerals_for_photo_sintes
            self.color_processing('green', 'red', 'blue')
            return 1
        else:
            return 0

    def mineral_processing(self):
        self.health -= step_damage
        if self.minerals >= minerals_limit:
            self.mnrlprc_counter += 1
            tmp = self.minerals / mnrl_proc_efficiency
            self.minerals = 0
            self.armor += tmp * mnrl_armor_efficiency
            self.energy += tmp * mnrl_energy_efficiency
            self.color_processing('blue', 'red', 'green')
            return tmp
        else:
            return 0

    def behavior(self):
        if self.step > len(self.brain)-1:
            self.step = 0

        if self.health <= 0:
            self.area.destroy(self.x, self.y)
            self.area.place_obj(self.x, self.y, Corpse(self.x, self.y))
        else:
            self.behavior_dict.get(self.brain[self.step])()
            self.step += 1
            if self.energy >= 100:
                self.replication()

    def doNot(self):
        pass

    def up_raise(self):
        self.health -= step_damage
        if self.status == LiverStatus.Child and self.energy > 100:
            self.status = ObjTypes.Liver
            self.energy -= 80

    def replication(self):
        self.health -= step_damage
        if self.energy <= 100:
            return
        if self.status == LiverStatus.Child:
            return
        tmp_env = self.area.space_manager.look_around(self.x, self.y)
        new_brain = self.brain.copy()
        for i in range(8):
            new_brain[randint(0, 254)] = randint(0, 19)

        for i in tmp_env:
            if isinstance(i[0], Empty) and randint(0, 8) < 4 and self.energy >= 0:
                self.area.place_obj(i[1], i[2], Liver(i[1], i[2], self.area, new_brain,self.generation+1, self.command))
                self.energy -= 100
            if isinstance(i[0], Corpse) and randint(0, 8) < 4 and self.energy >= 0:
                self.area.place_obj(i[1], i[2], Liver(i[1], i[2], self.area, new_brain,self.generation+1, self.command))
                self.energy -= 50

    def eat_liver(self, x, y):
        target = self.area.space_manager.get_obj(x, y)
        if self.compare_generation(target.get_generation()):
            return False
        if target.armor <= 0:
            self.hunt_counter += 1
            self.energy += target.energy / 2
            self.health += target.health / 2
            self.armor += 5
            self.area.destroy(x, y)
            self.area.space_manager.replace(self.x, self.y, x, y)
            self.energy /= 1.5

            if self.status == LiverStatus.Child:
                self.status = ObjTypes.Liver

            self.color_processing('red', 'green', 'blue')
            return True
        else:
            target.armor -= self.energy/2
            target.armor -= self.acid * 10
            self.acid = 0
            self.energy -= 10
            return False

    def hunt(self):
        if self.energy <= 20:
            return
        tmp_env = self.area.space_manager.look_around(self.x, self.y)
        targets = [(i[1], i[2]) for i in tmp_env if isinstance(i[0], Liver) and not
                   i[0].compare_generation(self.get_generation())]
        if (self.x, self.y) in targets:
            targets.remove((self.x, self.y))

        if len(targets) > 0:
            self.eat_liver(*choice(targets))

    def get_generation(self):
        return self.command

    def compare_generation(self, gen_code):
        if self.command == gen_code:
            return True
        else:
            return False

    def color_processing(self, main_color, other, another):
        if self.colors[main_color] < 99:
            self.colors[main_color] += 3
            self.colors[other] -= 1
            self.colors[another] -= 1
            if self.colors[other] <= 10:
                self.colors[other] = 10
            if self.colors[other] > 99:
                self.colors[other] = 99
            if self.colors[another] <= 10:
                self.colors[another] = 10
            if self.colors[another] > 99:
                self.colors[another] = 99
        elif self.colors[main_color] > 99:
            self.colors[main_color] = 99

    def eat_food(self, x, y):
        self.area.destroy(x, y)
        self.health += 20
        self.energy += 20
        self.area.replace_obj(self.x, self.y, x, y)
        Food.counter -= 1

    def search_food(self):
        self.health -= step_damage
        tmp_env = self.area.space_manager.look_around(self.x, self.y)
        targets = [(i[1], i[2]) for i in tmp_env if isinstance(i[0], Food) or isinstance(i[0], Corpse)]
        for i in targets:
            self.eat_food(*i)
        # if len(targets) > 0:
        #     self.eat_food(*choice(targets))

    def eat_poison(self, x, y):
        self.area.destroy(x, y)
        self.health -= self.health // 2
        self.energy += 10
        self.area.replace_obj(self.x, self.y, x, y)
        Poison.counter -= 1

    def search_poison(self):
        self.health -= step_damage
        tmp_env = self.area.space_manager.look_around(self.x, self.y)
        targets = [(i[1], i[2]) for i in tmp_env if isinstance(i[0], Poison)]
        if len(targets) > 0:
            self.process_poison(*choice(targets))

    def process_poison(self, x, y):
        self.health -= step_damage
        if self.energy >= 10:
            self.energy -= 10
            self.health += 30
            self.energy += 20
            self.armor += 5
            self.area.destroy(x, y)
        else:
            return

    def friend_cerry(self):
        if self.energy <= 40:
            return
        tmp_env = self.area.space_manager.look_around(self.x, self.y)
        targets = [(i[1], i[2]) for i in tmp_env if isinstance(i[0], Liver) and
                   i[0].compare_generation(self.get_generation())]
        if (self.x, self.y) in targets:
            targets.remove((self.x, self.y))

        for i in targets:
            self.cerry_to(*i)

    def cerry_to(self, x, y):
        if self.energy < 30:
            return
        self.health -= step_damage
        if self.energy > self.area.space[y][x].obj.energy:
            tmp = (self.energy + self.area.space[y][x].obj.energy)/2
            self.energy = tmp
            self.area.space[y][x].obj.energy = tmp
        if self.minerals > self.area.space[y][x].obj.minerals :
            tmp = (self.minerals + self.area.space[y][x].obj.minerals) / 2
            self.minerals = tmp
            self.area.space[y][x].obj.minerals = tmp
        if self.acid > self.area.space[y][x].obj.acid:
            tmp = (self.acid + self.area.space[y][x].obj.acid)/2
            self.acid = tmp
            self.area.space[y][x].obj.acid = tmp


class Food(Entities):
    counter = 0

    def __init__(self, x, y):
        Food.counter += 1
        self.x = x
        self.y = y
        self.symbol = '▼'
        self.colors['red'] = 50
        self.colors['green'] = 50
        self.colors = {'red': 99, 'green': 99, 'blue': 10}


class Corpse(Entities):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.symbol = '◉'
        self.colors = {'red': 99, 'green': 99, 'blue': 99}


class Poison(Entities):
    counter = 0

    def __init__(self, x, y):
        Poison.counter += 1
        self.x = x
        self.y = y
        self.symbol = 'Ⓟ'
        self.colors = {'red': 99, 'green': 10, 'blue': 10}


class Empty(Entities):
    symbol = '.'
