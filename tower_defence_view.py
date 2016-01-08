# -*- coding: utf8 -*-
from tkinter import *
from tkinter import ttk
import map_model as mm
import tower_defence_controller as tdc
import Statistic as st
import Info


class Viewer:
    def __init__(self, size_of_element, width, height):
        # Настройка Style
        self.top = Tk()
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", troughcolor='gray', background='red')
        s.configure("blue.Vertical.TProgressbar", troughcolor='gray', background='blue')

        # Настройка canvas
        self.model = mm.MapModel(width, height, self.view_map_model, self.show_game_over_screen)
        self.size_of_element = size_of_element
        self.canvas = Canvas(self.top, width=self.model.width * size_of_element + 200,
                             height=self.model.height * size_of_element)
        self.canvas.pack()

        # Информационное поле героя
        self.info = Text(self.top, height=10, width=20)
        self.info.insert(END, "Информация о герое")
        self.info.place(x=self.model.width * size_of_element + 30, y=40)
        self.info.config(state=DISABLED)

        # Информационное поле ячейки
        self.about = Text(self.top, height=10, width=20)
        self.about.insert(END, "Информация об ячейке")
        self.about.place(x=self.model.width * size_of_element + 30, y=210)
        self.about_obj = self.model.cells[0][0].obj
        self.about.config(state=DISABLED)

        # Инструкуция
        self.readme = Text(self.top, height=10, width=20)
        self.readme.insert(END, Info.get_readme())
        self.readme.place(x=self.model.width * size_of_element + 30, y=380)
        self.readme.config(state=DISABLED)

        # Рекорды
        self.records = Text(self.top, height=10, width=20)
        self.records.insert(END, Info.get_records())
        self.records.place(x=self.model.width * size_of_element + 30, y=550)
        self.records.config(state=DISABLED)

        # EnemyLvlProgressBar
        self.enemy_lvl_progress_bar = ttk.Progressbar(orient=VERTICAL, length=self.model.height * size_of_element - 10, mode='determinate', style="blue.Vertical.TProgressbar")
        self.enemy_lvl_progress_bar.place(x=self.model.width * size_of_element + 5, y=5)
        self.enemy_lvl_progress_bar["maximum"] = 15

        # HealthProgressBar
        self.health_progress_bar = ttk.Progressbar(orient=HORIZONTAL, length=160, mode='determinate', style="red.Horizontal.TProgressbar")
        self.health_progress_bar.place(x=self.model.width * size_of_element + 35, y=5)
        self.health_progress_bar["maximum"] = self.model.player.max_health

        # Загрузка текстур
        imagesdir = "images/"
        self.ibigwall = PhotoImage(file=imagesdir + "wall2.png")
        self.ismallwall = PhotoImage(file=imagesdir + "Barrage.png")
        self.iground = PhotoImage(file=imagesdir + "ground3.png")
        self.ienemy1 = PhotoImage(file=imagesdir + "enemy3.png")
        self.iplayer = PhotoImage(file=imagesdir + "playerv3.png")
        self.ibigarrow = PhotoImage(file=imagesdir + "ballv3.png")
        self.ismallarrow = PhotoImage(file=imagesdir + "sball.png")
        self.iheartstone = PhotoImage(file=imagesdir + "heartv2.png")
        self.itrap = PhotoImage(file=imagesdir + "trap.png")
        self.igameover = PhotoImage(file=imagesdir + "game_over.png")
        self.ispiralgenerator = PhotoImage(file=imagesdir + "spiral_generator.png")

        # Создание поля для отображения
        self.view_model = []
        self.images_id = []
        for i in range(self.model.width):
            self.view_model.append([])
            self.images_id.append([])
            for j in range(self.model.height):
                self.view_model[i].append(None)
                self.images_id[i].append(None)

    '''
    Переводит координаты поля в координаты на экране
    '''

    def coor(self, x):
        return x * 24 + self.size_of_element / 2

    '''
    Сопоставляет каждому элементу на поле сохранённую текстуру
    '''

    def element_to_image(self, argument):
        switcher = {
            mm.Ground: lambda: self.iground,
            mm.Player: lambda: self.iplayer,
            mm.Arrow: lambda: self.arrow_image(argument),
            mm.HeartStone: lambda: self.iheartstone,
            mm.Enemy: lambda: self.ienemy1,
            mm.Trap: lambda: self.itrap,
            mm.SpiralTower: lambda: self.ispiralgenerator,
            mm.Wall: lambda: self.wall_image(argument),
        }
        return switcher.get(type(argument), lambda: None)()

    def wall_image(self, wall):
        return self.ibigwall if wall.max_health > 100 else self.ismallwall

    def arrow_image(self, arrow):
        return self.ibigarrow if arrow.damage > 5 else self.ismallarrow

    def view_map_model(self, hard=False):
        '''
        Производит перерисовку поля в связи с произошедшими изменениями
        '''
        for i in range(0, 32):
            for j in range(0, 32):
                image = self.element_to_image(self.model.cells[i][j].obj)
                if hard or image != self.view_model[i][j]:
                    self.canvas.delete(self.images_id[i][j])
                    self.images_id[i][j] = self.canvas.create_image(i * 24 + 12, j * 24 + 12, image=image)
                    self.view_model[i][j] = image

        self.enemy_lvl_progress_bar["value"] = st.total_dead_enemies
        self.health_progress_bar["value"] = self.model.player.health
        self.update_text_box()
        self.update_info_box()
        self.top.update()

    def update_text_box(self):
        self.info.config(state=NORMAL)
        self.info.delete(1.0, END)
        self.info.insert(END, "Информация о герое\n")
        self.info.insert(END, "Очков: {0}\n".format(st.total_dead_enemies))
        self.info.insert(END, "Здоровье: {0} hp\n".format(self.model.player.health))
        self.info.insert(END, "Золото: {0} hp\n".format(st.player_gold))
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
        self.canvas.create_image(16 * 24, 16 * 24, image=self.igameover)

    def before_restart(self):
        with open("records.txt", "a") as f:
            f.write("{0}\n".format(st.total_dead_enemies))
        self.update_records_box()


def main():
    init()


def init():
    controller = tdc.Controller(Viewer(24, 32, 32), init)
    controller.start()
    controller.viewer.top.mainloop()

if __name__ == "__main__":
    main()
