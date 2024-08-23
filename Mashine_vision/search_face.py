import cv2
import numpy as np
from matplotlib import pyplot as plt

from download_resurce import file_name

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt_tree.xml")
eye_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

def blur_face(face_region, eyes):
    """Размазывает лицо, исключая глаза."""
    mask = np.ones(face_region.shape[:2], dtype=np.uint8) * 255
    for (ex, ey, ew, eh) in eyes:
        mask[ey:ey + eh, ex:ex + ew] = 0  # Глаза не будут размываться
    blurred_face = cv2.blur(face_region, (25, 25))
    face_region[:] = cv2.bitwise_and(blurred_face, blurred_face, mask=mask) + cv2.bitwise_and(face_region, face_region,
                                                                                              mask=~mask)
    return face_region


def overlay_sunglasses(image, eyes, scale_factor=1.24):
    # Загрузка изображения очков с альфа-каналом
    sunglasses_img = cv2.imread('sunglasses.png', cv2.IMREAD_UNCHANGED)

    if len(eyes) >= 2:  # Проверка, что обнаружено хотя бы два глаза
        # Определение крайних координат для объединения области обоих глаз
        ex1, ey1, ew1, eh1 = eyes[0]
        ex2, ey2, ew2, eh2 = eyes[1]

        # Определение общей области, охватывающей оба глаза
        x1 = min(ex1, ex2)
        y1 = min(ey1, ey2)
        x2 = max(ex1 + ew1, ex2 + ew2)
        y2 = max(ey1 + eh1, ey2 + eh2)

        # Вычисление ширины и высоты очков с учетом коэффициента масштабирования
        sunglass_width = int((x2 - x1) * scale_factor)
        sunglass_height = int(sunglass_width * sunglasses_img.shape[0] / sunglasses_img.shape[1])

        # Изменение размера изображения очков
        sunglasses_resized = cv2.resize(sunglasses_img, (sunglass_width, sunglass_height))

        # Корректировка координат размещения очков на лице
        y1 = y1 - int(sunglass_height / 4)
        x1 = x1 - int((sunglass_width - (x2 - x1)) / 2)
        y2 = y1 + sunglass_height

        # Наложение очков на изображение
        for c in range(0, 3):
            image[y1:y2, x1:x1 + sunglass_width, c] = (
                    sunglasses_resized[:, :, c] * (sunglasses_resized[:, :, 3] / 255.0) +
                    image[y1:y2, x1:x1 + sunglass_width, c] * (1.0 - sunglasses_resized[:, :, 3] / 255.0)
            )

    return image


# Снова загрузим изображения
img = cv2.imread(file_name)
img_copy = img.copy()

# Обнаружение лиц на изображении
bboxes = face_classifier.detectMultiScale(img)

x_shift = 60
y_shift = -50

# Обработка лиц на изображении
for box in bboxes:
    x, y, width, height = box

    # Корректировка размера области лица
    height = int(height * 1.2)
    width = int(width * 0.8)

    # Определение области лица
    face_region = img[y:y + height, x:x + width]
    face_copy = img_copy[y:y + height, x:x + width]

    # Добавление эллипса вокруг лица
    center = (x + width // 2 + x_shift, y + height // 2 + y_shift)
    axes = (width // 2, height // 2)
    img_copy = cv2.ellipse(img_copy, center, axes, angle=0, startAngle=0, endAngle=360, color=(255, 0, 0), thickness=2)

    # Обнаружение глаз в области лица
    eyes = eye_classifier.detectMultiScale(face_region, scaleFactor=1.3, minNeighbors=3, minSize=(50, 50))

    # Размытие лица, исключая глаза
    face_region = blur_face(face_copy, eyes)

    # Наложение очков
    img_copy[y:y + height, x:x + width] = overlay_sunglasses(face_copy, eyes, scale_factor=1.24)

# Отображение изображений
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
ax1.xaxis.set_ticks([])
ax1.yaxis.set_ticks([])
ax1.set_title('Исходное изображение')

ax2.imshow(cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB))
ax2.xaxis.set_ticks([])
ax2.yaxis.set_ticks([])
ax2.set_title('С лицом и очками')

plt.show()
