import os
import unittest
from PIL import Image
import anfis
import numpy as np
import matlab
from random import shuffle
import sqlite3

from ANFIS import нормализацияКаналов
from ANFIS import АнфисаРаспознать
from DB import сохранить
from DB import загрузитьСписокНаборов
from DB import загрузитьНабор

class TestНормализацияКаналов(unittest.TestCase):
    def test_нормализация_существующего_файла(self):
        результат = нормализацияКаналов('test_image.png')
        self.assertIsNotNone(результат, "Функция должна возвращать не None для существующего файла")
        self.assertTrue((результат >= 0).all() and (результат <= 1).all(), "Все значения должны быть в диапазоне от 0 до 1")

    def test_нормализация_несуществующего_файла(self):
        результат = нормализацияКаналов('несуществующий_файл.jpg')
        self.assertIsNone(результат, "Функция должна возвращать None для несуществующего файла")

class TestАнфисаРаспознать(unittest.TestCase):
    def setUp(self):
        self.путь = 'test_image.png'
        self.имяМодели = 'test_model_name'

    def test_распознавание_изображения(self):
        результат = АнфисаРаспознать(self.путь, self.имяМодели)
        self.assertIsInstance(результат, Image.Image, "Функция должна возвращать объект изображения")

    def test_сохранение_изображения(self):
        результат = АнфисаРаспознать(self.путь, self.имяМодели)
        self.assertTrue(os.path.isfile('output_image.png'), "Файл изображения должен быть сохранён")

class TestАнфисаТренировать(unittest.TestCase):
    def setUp(self):
        self.Набор = [[0.1, 0.2, 0.3, 0.3], [0.4, 0.5, 0.6, 0.3], [0.7, 0.8, 0.9, 0.3]]
        self.Размер = (3, 4)
        self.ИмяМодели = 'test_model'

    def test_инициализация_анфисы(self):
        try:
            Анфиса = anfis.initialize()
            Анфиса.terminate()
        except Exception as e:
            self.fail('Ошибка инициализации Анфисы: {}'.format(e))

    def test_перемешивание_набора(self):
        Набор_до = list(self.Набор)
        shuffle(self.Набор)
        self.assertNotEqual(Набор_до, self.Набор, "Набор данных должен быть перемешан")

    def test_обучение_анфисы(self):
        try:
            Анфиса = anfis.initialize()
            Анфиса.Anfis(matlab.double(np.array(self.Набор, np.double).flatten().tolist(), size=self.Размер), self.ИмяМодели)
            Анфиса.terminate()
        except Exception as e:
            self.fail('Ошибка во время обучения: {}'.format(e))

class TestСохранить(unittest.TestCase):
    def setUp(self):
        self.ИмяМодели = 'test_model'
        self.Набор = [(1, 2, 3, 4), (5, 6, 7, 8)]
        self.Подключение = sqlite3.connect(':memory:')
        self.Курсор = self.Подключение.cursor()
        self.Курсор.execute('''CREATE TABLE Готовые_данные (Адрес_файла TEXT)''')
        self.Курсор.execute('''CREATE TABLE Тренировочный_набор (Красный_канал INTEGER, Синий_канал INTEGER, Зелёный_канал INTEGER, Выходные_данные INTEGER)''')
        self.Курсор.execute('''CREATE TABLE Модель (Имя_модели TEXT, ИД_Тренировочного_набора INTEGER, ИД_Готовых_данных INTEGER)''')

    def test_подключение_к_базе(self):
        self.assertIsNotNone(self.Подключение, "Должно быть установлено подключение к базе данных")

    def test_добавление_в_готовые_данные(self):
        сохранить(self.ИмяМодели, self.Набор)
        self.Курсор.execute("SELECT * FROM Готовые_данные WHERE Адрес_файла = ?", (self.ИмяМодели,))
        результат = self.Курсор.fetchone()
        self.assertIsNotNone(результат, "Модель должна быть добавлена в таблицу Готовые_данные")

    def test_добавление_в_тренировочный_набор(self):
        сохранить(self.ИмяМодели, self.Набор)
        for данные in self.Набор:
            self.Курсор.execute("SELECT * FROM Тренировочный_набор WHERE Красный_канал = ? AND Синий_канал = ? AND Зелёный_канал = ? AND Выходные_данные= ?", данные)
            результат = self.Курсор.fetchone()
            self.assertIsNotNone(результат, "Данные должны быть добавлены в таблицу Тренировочный_набор")

    def test_закрытие_подключения(self):
        self.Подключение.close()
        self.assertRaises(sqlite3.ProgrammingError, self.Курсор.execute, "SELECT * FROM Готовые_данные")

    def tearDown(self):
        self.Подключение.close()

class TestЗагрузитьСписокНаборов(unittest.TestCase):
    def setUp(self):
        self.Подключение = sqlite3.connect(':memory:')
        self.Курсор = self.Подключение.cursor()
        self.Курсор.execute('''CREATE TABLE Готовые_данные (Адрес_файла TEXT)''')
        self.Курсор.executemany("INSERT INTO Готовые_данные (Адрес_файла) VALUES (?)", [('file1',), ('file2',), ('file3',)])

    def test_загрузка_списка(self):
        ожидаемый_список = ['file1', 'file2', 'file3']
        результат = загрузитьСписокНаборов()
        self.assertEqual(результат, ожидаемый_список, "Список наборов должен соответствовать ожидаемому")

    def test_закрытие_подключения(self):
        загрузитьСписокНаборов()
        self.assertRaises(sqlite3.ProgrammingError, self.Курсор.execute, "SELECT * FROM Готовые_данные")

    def tearDown(self):
        self.Подключение.close()

class TestЗагрузитьНабор(unittest.TestCase):
    def setUp(self):
        Название = 'test_model'
        self.Подключение = sqlite3.connect(':memory:')
        self.Курсор = self.Подключение.cursor()
        self.Курсор.execute('''CREATE TABLE Модель (Имя_модели TEXT, ИД_Тренировочного_набора INTEGER)''')
        self.Курсор.execute('''CREATE TABLE Тренировочный_набор (ИД_тренировочного_набора INTEGER, Красный_канал INTEGER, Синий_канал INTEGER, Зелёный_канал INTEGER, Выходные_данные INTEGER)''')
        self.Курсор.execute("INSERT INTO Модель (Имя_модели, ИД_Тренировочного_набора) VALUES (?, ?)", (Название, 1))
        self.Курсор.execute("INSERT INTO Тренировочный_набор (ИД_тренировочного_набора, Красный_канал, Синий_канал, Зелёный_канал, Выходные_данные) VALUES (1, 255, 0, 0, 1)")

    def test_загрузка_набора(self):
        ожидаемый_выход = [(255, 0, 0, 1)]
        результат = загрузитьНабор('test_model')
        self.assertEqual(результат[0], ожидаемый_выход, "Загруженный набор должен соответствовать ожидаемому")

    def test_формат_выходных_данных(self):
        результат = загрузитьНабор('test_model')
        self.assertEqual(результат[1], (1, 4), "Формат выходных данных должен быть кортежем с размерностью набора")

    def test_закрытие_подключения(self):
        загрузитьНабор('test_model')
        self.assertRaises(sqlite3.ProgrammingError, self.Курсор.execute, "SELECT * FROM Модель")

    def tearDown(self):
        self.Подключение.close()

if __name__ == '__main__':
    unittest.main()
