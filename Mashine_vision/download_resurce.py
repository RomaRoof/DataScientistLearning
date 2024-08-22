import os
import requests

url = 'https://www.film.ru/sites/default/files/people/1457583-2618007.jpg'
# Имя файла, под которым нужно сохранить изображение
file_name = 'Ryan Reynolds.jpg'

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