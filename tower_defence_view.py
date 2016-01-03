# -*- coding: utf8 -*-
from tkinter import *
from tkinter import ttk
import map_model as mm
import tower_defence_controller as tdc
import Statistic as st


class Viewer:
    def __init__(self, size_of_element, map_model):
        # Настройка Style
        self.top = Tk()
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", troughcolor='gray', background='red')
        s.configure("blue.Vertical.TProgressbar", troughcolor='gray', background='blue')

        # Настройка canvas
        self.model = map_model
        self.size_of_element = size_of_element
        self.canvas = Canvas(self.top, width=map_model.width * size_of_element + 200,
                             height=map_model.height * size_of_element)
        self.canvas.pack()

        # Текстовое поле
        self.info = Text(self.top, height=10, width=20)
        self.info.insert(END, "Информация о герое:")

        self.info.place(x=map_model.width * size_of_element + 30, y=40)

        # EnemyLvlProgressBar
        self.enemy_lvl_progress_bar = ttk.Progressbar(orient=VERTICAL, length=map_model.height * size_of_element - 10,
                                                   mode='determinate', style="blue.Vertical.TProgressbar")
        self.enemy_lvl_progress_bar.place(x=map_model.width * size_of_element + 5, y=5)
        self.enemy_lvl_progress_bar["maximum"] = 15

        # HealthProgressBar
        self.health_progress_bar = ttk.Progressbar(orient=HORIZONTAL, length=160, mode='determinate',
                                                 style="red.Horizontal.TProgressbar")
        self.health_progress_bar.place(x=map_model.width * size_of_element + 35, y=5)
        self.health_progress_bar["maximum"] = self.model.player.max_health

        # Загрузка текстур
        imagesdir = "images/"
        self.iwall = PhotoImage(file=imagesdir + "wall2.png")
        self.iground = PhotoImage(file=imagesdir + "ground3.png")
        self.ienemy1 = PhotoImage(file=imagesdir + "enemy3.png")
        self.iplayer = PhotoImage(file=imagesdir + "playerv3.png")
        self.iarrow = PhotoImage(file=imagesdir + "ballv3.png")
        self.iheartstone = PhotoImage(file=imagesdir + "heartv2.png")

        # Создание поля для отображения
        self.view_model = []
        self.images_id = []
        for i in range(map_model.width):
            self.view_model.append([])
            self.images_id.append([])
            for j in range(map_model.height):
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
            mm.Wall: self.iwall,
            mm.Ground: self.iground,
            mm.Player: self.iplayer,
            mm.Arrow: self.iarrow,
            mm.HeartStone: self.iheartstone,
            mm.Enemy: self.ienemy1,
        }
        return switcher.get(type(argument), None)

    '''
    Производит перерисовку поля в связи с произошедшими изменениями
    '''

    def view_map_model(self):
        for i in range(0, 32):
            for j in range(0, 32):
                image = self.element_to_image(self.model.cells[i][j].obj)
                if (image != self.view_model[i][j]):
                    self.canvas.delete(self.images_id[i][j])
                    self.images_id[i][j] = self.canvas.create_image(i * 24 + 12, j * 24 + 12, image=image)
                    self.view_model[i][j] = image

        self.enemy_lvl_progress_bar["value"] = st.total_dead_enemies
        self.health_progress_bar["value"] = self.model.player.health
        self.update_text_box()
        self.top.update()

    def update_text_box(self):
        self.info.delete(1.0, END)
        self.info.insert(END, "Информация о герое\n")
        self.info.insert(END, "Очков: {0}\n".format(st.total_dead_enemies))
        self.info.insert(END, "Здоровье: {0} hp\n".format(self.model.player.health))

def main():
    controller = tdc.Controller(Viewer(24, mm.MapModel(32, 32)))
    controller.start()
    controller.viewer.top.mainloop()


if __name__ == "__main__":
    main()
