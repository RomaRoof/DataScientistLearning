import os

import requests


url = 'https://img11.rl0.ru/afisha/e2086x1180p291x0f1050x594q65i/s1.afisha.ru/mediastorage/56/4c/7fe45647591c4a088af9c4bf4c56.jpg'
# Имя файла, под которым нужно сохранить изображение
file_name = 'Keanu.jpg'

# Проверка, существует ли файл
if not os.path.exists(file_name):
    # Если файл не существует, выполняется его загрузка
    response = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(response.content)
    print(f"Файл '{file_name}' загружен и сохранен.")
else:
    # Если файл существует, выводится сообщение
    print(f"Файл '{file_name}' уже существует и не был загружен повторно.")
