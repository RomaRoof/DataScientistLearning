"""Гадание на мед.картах. Алгоритм случайный лес (Random Forest)"""
# Преимущество алгоритма, что он позволяет обрабатывать большие массивы данных.
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# Создаем набор данных

# Параметры медицинских карт
X = np.array([[1, 2], [3, 7], [3, 4], [4, 5], [5, 6]])
y = np.array([0, 2, 0, 1, 1])

h=0.01 # Шаг сетки
classifier = RandomForestClassifier() # Создаем классификатор
classifier.fit(X, y) # Обучаем модель на наших картах

# создаём сетку для построения графика
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

plt.subplot(1, 1, 1)
Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()]) # делаем предсказание для каждой точки сетки
Z = Z.reshape(xx.shape)
plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8) # На контурном графике цветами рисуем предсказанные области по всей сетке

result = plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired) # Проставляем точки Х и отображаем их цветом из y

plt.legend(result.legend_elements()[0], ['0', '1', '2']) # У нас несколько графиков, поэтому нужно явно указать откуда берем легенду и какие метки используем для точек

plt.xlabel('Основной симптом')
plt.ylabel('Сопутствующий симптом')
plt.xlim(xx.min(), xx.max())
plt.title('Алгоритм случайный лес')
plt.show()
import numpy as np
