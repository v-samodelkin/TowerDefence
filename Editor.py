# -*- coding: utf8 -*-
from tkinter import *
from tkinter import ttk
import MapModel as Mm
import MapParser
import Info
from itertools import product

char_by_object_switcher = {
    Mm.Wall: 'W',
    Mm.Player: 'P',
    Mm.HeartStone: 'H',
    Mm.Ground: '.',
    Mm.Arrow: '?',
    Mm.SpiralTower: 'S',
    Mm.Trap: 'T',
}

class Editor:
    def __init__(self, size_of_element, map_name):
        self.map_name = map_name
        self.prev_key = '1'

        # Настройка Style
        self.top = Tk()
        self.top.resizable(0, 0)
        s = ttk.Style()
        s.theme_use('clam')
        self.size_of_element = size_of_element
        self.canvas = Canvas(self.top,
                             width=Mm.size * size_of_element + 200,
                             height=Mm.size * size_of_element)
        self.canvas.pack()

        # Инициализация объектов для размещения
        self.cells = MapParser.read_from_file(map_name)
        self.player = Mm.Player()
        self.heartstone = Mm.HeartStone(self.player)

        # Информационное поле ячейки
        self.about = Text(self.top, height=10, width=20)
        self.about.insert(END, Info.get_editor_description())
        self.about.place(x=Mm.size * size_of_element + 20, y=10)
        self.about_obj = Mm.ground
        self.about.config(state=DISABLED)

        # Лог
        self.log = Text(self.top, height=10, width=20)
        self.log.insert(END, "Лог изменений")
        self.log.place(x=Mm.size * size_of_element + 20, y=180)
        self.log.config(state=DISABLED)

        # Инструкуция
        self.readme = Text(self.top, height=20, width=20)
        self.readme.insert(END, Info.get_editor_readme(self.prev_key))
        self.readme.place(x=Mm.size * size_of_element + 20, y=350)
        self.readme.config(state=DISABLED)



        # Сохранение
        self.save_messages = ["Сохранено!", "Сохранение успешно", "Карта сохранена"]
        self.save_message_id = 0

        # Загрузка текстур
        images_dir = "images/"
        self.i_big_wall = PhotoImage(file=images_dir + "wall2.png")
        self.i_small_wall = PhotoImage(file=images_dir + "Barrage.png")
        self.i_ground = PhotoImage(file=images_dir + "ground3.png")
        self.i_enemy_1 = PhotoImage(file=images_dir + "enemy3.png")
        self.i_player = PhotoImage(file=images_dir + "playerv3.png")
        self.i_big_arrow = PhotoImage(file=images_dir + "ballv3.png")
        self.i_small_arrow = PhotoImage(file=images_dir + "sball.png")
        self.i_heartstone = PhotoImage(file=images_dir + "heartv2.png")
        self.i_trap = PhotoImage(file=images_dir + "trap.png")
        self.i_game_over = PhotoImage(file=images_dir + "game_over.png")
        self.i_spiral = PhotoImage(file=images_dir + "spiral_generator.png")

        # Настройка управления
        self.top.bind("<Key>", self.key)
        self.top.bind("<Button-1>", self.callback)
        self.tower = Mm.Ground
        self.unrepeatable = {Mm.HeartStone, Mm.Player}
        self.tower_switcher = {
            '1': lambda: Mm.ground,
            '2': lambda: self.player,
            '3': lambda: self.heartstone,
            '4': lambda: Mm.Trap(10, 15),
            '5': lambda: Mm.SpiralTower(),
            '6': lambda: Mm.Wall(200),
            '7': lambda: Mm.Arrow(1, 0, 0)
        }
        self.action_switcher = {
            's': lambda: self.save()
        }
        self.try_change_tower_by_key(self.prev_key)

        # Создание поля для отображения
        self.view_model = []
        self.images = []
        for i in range(Mm.size):
            self.view_model.append([])
            self.images.append([])
            for j in range(Mm.size):
                self.view_model[i].append(None)
                self.images[i].append(None)
        self.view_map()
        self.top.mainloop()


    def coordinate(self, x):
        """
        Переводит координаты поля в координаты на экране
        """
        return x * 24 + self.size_of_element / 2

    def element_to_image(self, argument):
        """
        Сопоставляет каждому элементу на поле сохранённую текстуру
        """
        switcher = {
            Mm.Ground: lambda: self.i_ground,
            Mm.Player: lambda: self.i_player,
            Mm.Arrow: lambda: self.arrow_image(argument),
            Mm.HeartStone: lambda: self.i_heartstone,
            Mm.Enemy: lambda: self.i_enemy_1,
            Mm.Trap: lambda: self.i_trap,
            Mm.SpiralTower: lambda: self.i_spiral,
            Mm.Wall: lambda: self.wall_image(argument),
        }
        return switcher.get(type(argument), lambda: None)()

    def wall_image(self, wall):
        return self.i_big_wall if wall.max_health > 100 else self.i_small_wall

    def arrow_image(self, arrow):
        return self.i_big_arrow if arrow.damage > 5 else self.i_small_arrow

    def update_info_box(self):
        self.about.config(state=NORMAL)
        self.about.delete(1.0, END)
        self.about.insert(END, self.about_obj.get_info())
        self.about.config(state=DISABLED)


    def view_map(self, hard=False):
        """
        Производит перерисовку поля в связи с произошедшими изменениями
        """
        for (i, j) in product(range(Mm.size), range(Mm.size)):
            # noinspection PyNoneFunctionAssignment
            image = self.element_to_image(self.cells[i][j])
            if hard or image != self.view_model[i][j]:
                canvas = self.canvas
                canvas.delete(self.images[i][j])
                i_x = i * 24 + 12
                j_y = j * 24 + 12
                self.images[i][j] = canvas.create_image(i_x, j_y, image=image)
                self.view_model[i][j] = image
        self.top.update()

    def callback(self, event):
        x = event.x // self.size_of_element
        y = event.y // self.size_of_element
        if not type(self.cells[x][y]) in self.unrepeatable:
            self.cells[x][y] = self.place()
            self.view_map()

    def key(self, event):
        self.prev_key = event.char
        self.try_change_tower_by_key(event.char)
        self.do_action_by_key(event.char)
        self.view_map()

    def clear(self, type):
        for (x, y) in product(range(Mm.size), range(Mm.size)):
            if isinstance(self.cells[x][y], type):
                self.cells[x][y] = Mm.ground

    def place(self):
        if type(self.tower) in self.unrepeatable:
            self.clear(type(self.tower))
        obj = self.tower
        self.try_change_tower_by_key(self.prev_key)
        return obj

    def do_action_by_key(self, argument):
        self.action_switcher.get(argument, lambda: None)()

    def try_change_tower_by_key(self, argument):
        self.tower = self.tower_switcher.get(argument, lambda: Mm.ground)()
        self.readme.config(state=NORMAL)
        self.readme.delete(1.0, END)
        self.readme.insert(END, Info.get_editor_readme(self.prev_key))
        self.readme.config(state=DISABLED)

    def get_char_by_object(self, x, y):
        obj = self.cells[x][y]
        return char_by_object_switcher.get(type(obj), '.')

    def save(self):
        try:
            with open(self.map_name, "w") as f:
                for y in range(Mm.size):
                    for x in range(Mm.size):
                        f.write(self.get_char_by_object(x, y))
                    f.write("\n")
            self.log.config(state=NORMAL)
            self.log.delete(1.0, END)
            self.log.insert(END, self.save_messages[self.save_message_id])
            self.log.config(state=DISABLED)
            self.save_message_id = (self.save_message_id + 1) % 3
        except Exception:
            self.log.config(state=NORMAL)
            self.log.delete(1.0, END)
            self.log.insert(END, "Ошибка сохранения")
            self.log.config(state=DISABLED)
def main():
    map_name = "no_name"
    if len(sys.argv) > 1:
        map_name = sys.argv[1]
    Editor(24, map_name)

if __name__ == "__main__":
    main()
