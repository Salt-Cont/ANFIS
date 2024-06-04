import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('Based_data.db')
cursor = conn.cursor()
conn.commit()
conn.close()

def сохранить(ИмяМодели, Набор):
    return

def загрузитьСписокНаборов():
    return

def загрузитьНабор(Название):
    return