# -*- coding: utf8 -*-
from tkinter import *
from tkinter import ttk
import map_model as mm
import tower_defence_controller as tdc
import Statistic as st
class Viewer:
    def __init__ (self, sizeOfElement, map_model):
        #Настройка Stype
        self.top = Tk()
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", troughcolor ='gray', background='red')
        s.configure("blue.Vertical.TProgressbar", troughcolor ='gray', background='blue')
        #Настройка canvas
        self.model = map_model
        self.sizeOfElement = sizeOfElement
        self.canvas = Canvas(self.top, width = map_model.width * sizeOfElement + 200, height = map_model.height * sizeOfElement)
        self.canvas.pack()
        #EnemyLvlProgressBar
        self.enemyLvlProgressBar = ttk.Progressbar(orient=VERTICAL, length=map_model.height * sizeOfElement - 10, mode='determinate', style = "blue.Vertical.TProgressbar")
        self.enemyLvlProgressBar.place(x = map_model.width * sizeOfElement + 5, y = 5)
        self.enemyLvlProgressBar["maximum"] = 15
        #HealthProgressBar
        self.healthProgressBar = ttk.Progressbar(orient=HORIZONTAL, length=160, mode='determinate', style="red.Horizontal.TProgressbar")
        self.healthProgressBar.place(x = map_model.width * sizeOfElement + 35, y = 5)
        self.healthProgressBar["maximum"] = self.model.player.maxHealth
        #Загрузка текстур
        imagesdir = "images/"
        self.iwall = PhotoImage(file=imagesdir+"wall.png")
        self.iground = PhotoImage(file=imagesdir+"ground1.png")
        self.ienemy1 = PhotoImage(file=imagesdir+"enemy2v2.png")
        self.iplayer = PhotoImage(file=imagesdir+"playerv2.png")
        self.iarrow = PhotoImage(file=imagesdir+"ballv2.png")
        self.iheartstone = PhotoImage(file=imagesdir+"heart.png")

        #Создание поля для отображения
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
        return x * 24 + self.sizeOfElement / 2;

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

        self.enemyLvlProgressBar["value"] = st.TotalDeadEnem
        self.healthProgressBar["value"] = self.model.player.health
        self.top.update()


def main():
    controller = tdc.Controller(Viewer(24, mm.MapModel(32, 32)))
    controller.Start()
    controller.viewer.top.mainloop()

if __name__ == "__main__":
    main()
