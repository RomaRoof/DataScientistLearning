import os
import requests

url = 'https://img11.rl0.ru/afisha/e2086x1180p291x0f1050x594q65i/s1.afisha.ru/mediastorage/56/4c/7fe45647591c4a088af9c4bf4c56.jpg'
url_glasses ='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjt_P_VCXa1HLnO13Q6gyz7gWDwBPHgGl-kg&s'
#url_glasses = 'https://www.freeiconspng.com/thumbs/deal-with-it-glasses-png/deal-with-it-glasses-png-clip-art-3.png' резервные очки
# Имя файла, под которым нужно сохранить изображение
file_name = 'Keanu.jpg'
file_name2 = 'sunglasses.png'

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

if not os.path.exists(file_name2):
    # Если файл не существует, выполняется его загрузка
    response = requests.get(url_glasses)
    with open(file_name2, 'wb') as f:
        f.write(response.content)
    print(f"Файл '{file_name2}' загружен и сохранен.")
else:
    # Если файл существует, выводится сообщение
    print(f"Файл '{file_name2}' уже существует и не был загружен повторно.")
