import numpy as np
from PIL import Image

class ANFIS:
    def __init__(self, num_input, num_membership_functions):
        self.num_input = num_input
        self.num_membership_functions = num_membership_functions
        self.weights = np.random.rand(num_input, num_membership_functions)
        self.biases = np.random.rand(num_membership_functions)
        self.input_values = None

    def forward_pass(self, input_values):
        self.input_values = input_values
        aggregated_values = np.dot(self.input_values, self.weights.T) + self.biases
        return aggregated_values

def read_image(file_path):
    image = Image.open(file_path)
    return np.array(image)

def preprocess_image(image):
    # Преобразование изображения в формат, подходящий для подачи на вход ANFIS
    # Здесь можно реализовать любую необходимую предварительную обработку изображения
    # Например, нормализацию значений цветовых каналов

    # Масштабирование значений пикселей в диапазон от 0 до 1
    normalized_image = image / 255.0

    # Размерность входных данных ANFIS должна быть (1, num_input)
    # Поэтому добавляем измерение для каждого цветового канала
    reshaped_image = normalized_image.reshape(-1, 1)

    return reshaped_image

def find_objects_in_image(anfis_model, image_path):
    image = read_image(image_path)
    preprocessed_image = preprocess_image(image)
    output_values = anfis_model.forward_pass(preprocessed_image)
    # Здесь можно реализовать дополнительную обработку вывода ANFIS,
    # чтобы определить объекты на изображении на основе полученных значений
    return output_values

# Пример использования:
num_input = 3
num_membership_functions = 3
anfis_model = ANFIS(num_input, num_membership_functions)
# Пример использования функции для чтения изображения и передачи его в ANFIS
image_path = r"C:\Users\bvvzx\YandexDisk\d&d\Иконки\czy to freddy fazbear.png"
output_values = find_objects_in_image(anfis_model, image_path)
print("Output values for image:", output_values)
