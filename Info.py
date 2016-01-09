# -*- coding: utf8 -*-
def get_readme():
    return '''Управление
wasd - перемещение
e - ожидание
space - выстрел
shift - пауза
1 - Шипы [40]
2 - Заграждение [10]
3 - Спираль [30]

r - Рестарт
'''


def get_records():
    try:
        with open("records.txt", "r") as f:
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
    except:
        return "Рекорды по очкам\nОшибка загрузки"
