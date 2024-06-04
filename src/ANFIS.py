import numpy as НП
from PIL import Image
import anfis
import anfisReady
import matlab

def нормализацияКаналов(ПутьФайла):
    try:
        Изображение = Image.open(ПутьФайла)
        Изображение = Изображение.resize((720, 720), Image.LANCZOS)
    except IOError:
        print("Ошибка при чтении файла изображения.")
        return None
    МассивИзображения = НП.array(Изображение)
    КрасныйКанал = МассивИзображения[:, :, 0].flatten() / 255.0
    ЗелёныйКанал = МассивИзображения[:, :, 1].flatten() / 255.0
    СинийКанал = МассивИзображения[:, :, 2].flatten() / 255.0
    return
def АнфисаРаспознать(Путь, ИмяМодели):
    Анфиса = anfisReady.initialize()
    Изображение = Image.open(Путь)
    Изображение = Изображение.resize((720, 720), Image.LANCZOS)
    МассивИзображения = НП.array(Изображение)
    КрасныйКанал = МассивИзображения[:, :, 0].flatten() / 255.0
    ЗелёныйКанал = МассивИзображения[:, :, 1].flatten() / 255.0
    СинийКанал = МассивИзображения[:, :, 2].flatten() / 255.0
    ОбучающийНабор = matlab.double(КрасныйКанал.tolist() + ЗелёныйКанал.tolist() + СинийКанал.tolist(),
                                   size=(518400, 3))
    Результат = Анфиса.AnfisReady(ОбучающийНабор, ИмяМодели)
    Маска = НП.empty((720, 720, 4), dtype=НП.uint8)
    for i in range(720):
        for j in range(720):
            if Результат[i * 720 + j][0] > 0:
                Маска[i][j][0] = НП.uint8(Результат[i * 720 + j][0] * 255)
                Маска[i][j][1] = НП.uint8(Результат[i * 720 + j][0] * 255)
                Маска[i][j][2] = НП.uint8(Результат[i * 720 + j][0] * 255)
            else:
                Маска[i][j][0] = 0
                Маска[i][j][1] = 0
                Маска[i][j][2] = 0
            Маска[i][j][3] = 255
    Файл = Image.fromarray(Маска, mode='RGBA')
    Файл.save('output_image.png')
    Файл.close()
    return Image.fromarray(Маска)

def АнфисаТренировать(Набор, Размер, ИмяМодели):
    try:
        Анфиса = anfis.initialize()
    except Exception as e:
        print('Ошибка инициализации пакета Анфисы:\n{}'.format(e))
        exit(1)
    try:
        Анфиса.Anfis(matlab.double(НП.array(Набор, НП.double).flatten().tolist(), size=(Размер[0], Размер[1])), ИмяМодели)
    except Exception as e:
        print('Ошибка во время обучения:\n{}'.format(e))
    Анфиса.terminate()
    return