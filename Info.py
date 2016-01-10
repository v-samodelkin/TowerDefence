# -*- coding: utf8 -*-
import TowerDefenceController as Tdc


def shell(number, target):
    if number == target:
        return "[{0}]".format(number)
    else:
        return " {0} ".format(number)


def get_editor_readme(target):
    readme = ["Управление\n",
              shell('1', target) + " - пустая клетка\n",
              shell('2', target) + " - игрок\n",
              shell('3', target) + " - камень жизни\n",
              shell('4', target) + " - шипы\n",
              shell('5', target) + " - спираль\n",
              shell('6', target) + " - стена\n",
              shell('7', target) + " - стена [40%]\n",
              " s  - сохранение\n"]
    return merge(readme)


def get_readme():
    readme = ["Управление\n",
              "wasd - перемещение\n",
              "e - ожидание\n",
              "space - выстрел\n",
              "shift - пауза\n",
              "r - Рестарт\n",
              "1 - Шипы [40]\n",
              "2 - Заграждение [10]\n",
              "3 - Спираль [30]\n"]
    return merge(readme)


def get_editor_description():
    return merge(["     /:\    (''') \n",
                  "     |:|     III  \n",
                  "     |:|     III  \n",
                  "     |:|     III  \n",
                  "     |:|   __III__\n",
                  "     |:| /:-.___,-:\\\n",
                  "     |:| \]  |:|  [/\n",
                  "     |:|     |:| \n",
                  "     |:|     |:| \n",
                  "     |:|     |:| \n",
                  " /]  |:|  [\ |:| \n",
                  " \:-''''`-:/ |:| \n",
                  "   ''III''   |:| \n",
                  "     III     |:| \n",
                  "     III     |:| \n",
                  "     III     |:| \n",
                  "    (___)    \:/"])


def merge(string_list):
    merged = ""
    for element in string_list:
        merged += element
    return merged


# noinspection PyBroadException
def get_records():
    try:
        with open(Tdc.records_file_name, "r") as f:
            records = list(map(int, f.read().split()))
            records.sort(reverse=True)
            if len(records) == 0:
                return "Рекордов нет"
            text = "Рекорды по очкам\n"
            counter = 1
            for record in records:
                text += "{0} место: {1}\n".format(counter, record)
                counter += 1
            return text
    except FileNotFoundError:
        return "Рекорды по очкам\nРекордов нет."
    except Exception:
        return "Рекорды по очкам\nОшибка загрузки"
