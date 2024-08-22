import cv2
from matplotlib import pyplot

from download_resurce import file_name

img = cv2.imread(file_name)
img_copy = img.copy()

classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt_tree.xml")

bboxes = classifier.detectMultiScale(img)

x_shift = 60
y_shift = -50
# формирование прямоугольника вокруг каждого обнаруженного лица
for box in bboxes:
    x, y, width, height = box

    # Ручная корректировка высоты (например, увеличить на 20%)
    height = int(height * 1.2)
    width = int(width * 0.8)

    # Вычисление новых координат
    #x2, y2 = x + width, y + height

    # Рисование эллипса
    center = (x + width // 2 + x_shift, y + height // 2 + y_shift)
    axes = (width // 2, height // 2)
    cv2.ellipse(img_copy, center, axes, 0, 0, 360, (0, 0, 255), 2)

fig, (ax1, ax2) = pyplot.subplots(1, 2, figsize=(15, 8))
ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
ax1.xaxis.set_ticks([])
ax1.yaxis.set_ticks([])
ax1.set_title('Исходное изображение')

ax2.imshow(cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB))
ax2.xaxis.set_ticks([])
ax2.yaxis.set_ticks([])
ax2.set_title('Распознанные лица')

pyplot.show()
