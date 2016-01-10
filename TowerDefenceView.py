# -*- coding: utf8 -*-
from tkinter import *
from tkinter import ttk
import MapModel as Mm
import TowerDefenceController as Tdc
import Statistic as St
import Info
import itertools


class Viewer:
    def __init__(self, size_of_element, map_name):
        # Настройка Style
        self.top = Tk()
        self.top.resizable(0, 0)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar",
                    troughcolor='gray',
                    background='red')
        s.configure("blue.Vertical.TProgressbar",
                    troughcolor='gray',
                    background='blue')

        # Настройка canvas
        self.model = Mm.MapModel(self.view_map_model,
                                 self.show_game_over_screen,
                                 map_name)
        self.size_of_element = size_of_element
        self.canvas = Canvas(self.top,
                             width=Mm.size * size_of_element + 200,
                             height=Mm.size * size_of_element)
        self.canvas.pack()

        # Информационное поле героя
        self.info = Text(self.top, height=10, width=20)
        self.info.insert(END, "Информация о герое")
        self.info.place(x=Mm.size * size_of_element + 30, y=40)
        self.info.config(state=DISABLED)

        # Информационное поле ячейки
        self.about = Text(self.top, height=10, width=20)
        self.about.insert(END, "Информация об ячейке")
        self.about.place(x=Mm.size * size_of_element + 30, y=210)
        self.about_obj = self.model.cells[0][0].obj
        self.about.config(state=DISABLED)

        # Инструкуция
        self.readme = Text(self.top, height=10, width=20)
        self.readme.insert(END, Info.get_readme())
        self.readme.place(x=Mm.size * size_of_element + 30, y=380)
        self.readme.config(state=DISABLED)

        # Рекорды
        self.records = Text(self.top, height=10, width=20)
        self.records.insert(END, Info.get_records())
        self.records.place(x=Mm.size * size_of_element + 30, y=550)
        self.records.config(state=DISABLED)

        # EnemyLvlProgressBar
        self.enemy_bar = ttk.Progressbar(orient=VERTICAL,
                                         length=Mm.size * size_of_element - 10,
                                         mode='determinate',
                                         style="blue.Vertical.TProgressbar")
        self.enemy_bar.place(x=Mm.size * size_of_element + 5, y=5)
        self.enemy_bar["maximum"] = 15

        # HealthProgressBar
        self.health_bar = ttk.Progressbar(orient=HORIZONTAL,
                                          length=160,
                                          mode='determinate',
                                          style="red.Horizontal.TProgressbar")
        self.health_bar.place(x=Mm.size * size_of_element + 35, y=5)
        self.health_bar["maximum"] = self.model.player.max_health

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

        # Создание поля для отображения
        self.view_model = []
        self.images = []
        for i in range(Mm.size):
            self.view_model.append([])
            self.images.append([])
            for j in range(Mm.size):
                self.view_model[i].append(None)
                self.images[i].append(None)

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

    def view_map_model(self, hard=False):
        """
        Производит перерисовку поля в связи с произошедшими изменениями
        """
        for (i, j) in itertools.product(range(32), range(32)):
            # noinspection PyNoneFunctionAssignment
            image = self.element_to_image(self.model.cells[i][j].obj)
            if hard or image != self.view_model[i][j]:
                canvas = self.canvas
                canvas.delete(self.images[i][j])
                i_x = i * 24 + 12
                j_y = j * 24 + 12
                self.images[i][j] = canvas.create_image(i_x, j_y, image=image)
                self.view_model[i][j] = image

        self.enemy_bar["value"] = St.total_dead_enemies
        self.health_bar["value"] = self.model.player.health
        self.update_text_box()
        self.update_info_box()
        self.top.update()

    def update_text_box(self):
        player = self.model.player
        self.info.config(state=NORMAL)
        self.info.delete(1.0, END)
        self.info.insert(END, "Информация о герое\n")
        self.info.insert(END, "Очков: {0}\n".format(St.total_dead_enemies))
        self.info.insert(END, "Здоровье: {0} hp\n".format(player.health))
        self.info.insert(END, "Золото: {0} hp\n".format(St.player_gold))
        self.info.config(state=DISABLED)

    def update_info_box(self):
        self.about.config(state=NORMAL)
        self.about.delete(1.0, END)
        self.about.insert(END, self.about_obj.get_info())
        self.about.config(state=DISABLED)

    def update_records_box(self):
        self.records.config(state=NORMAL)
        self.records.delete(1.0, END)
        self.records.insert(END, Info.get_records())
        self.records.config(state=DISABLED)

    def show_info_about_cell(self, x, y):
        self.about_obj = self.model.cells[x][y].obj
        self.update_info_box()

    def show_game_over_screen(self):
        self.canvas.create_image(16 * 24, 16 * 24, image=self.i_game_over)

    def before_restart(self):
        self.update_records_box()


def main():
    map_name = "first"
    if len(sys.argv) > 1:
        map_name = sys.argv[1]
    init(map_name)


def init(map_name):
    controller = Tdc.Controller(Viewer(24, map_name))
    controller.start()
    controller.viewer.top.mainloop()

if __name__ == "__main__":
    main()
