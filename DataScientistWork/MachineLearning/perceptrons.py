""" Perceptrons """
import numpy as np


# Объявим функцию расчета весов
def perceptron_train(X, y, learning_rate=0.01, max_iter=1000):
    # X - Вектор входной последовательности (признаков)
    # y - Вектор выходной последовательности (классов)
    # learning_rate - коэффициент скорости обучения
    # max_iter - число итерации (попыток)
    m, n = X.shape  # Получаем форму входной последовательности m x n
    W = np.random.rand(n, 1)  # Генерируем случайные веса

    for _ in range(max_iter):  # Обучаем на max_iter итерациях (эпохах)
        y_pred = np.heaviside(np.dot(X, W), 0)  # Предсказываем класс по взвешенным входным признакам
        error = y - y_pred  # Отклонение предсказанного класса от ожидаемого
        delta_W = learning_rate * np.dot(X.T, error)  # Поправка к весу по Розенблатту
        W += delta_W

    return W


# Параметры медицинских карт
X = np.array([[1, 2], [3, 7], [3, 4], [4, 5], [5, 6]])
y = np.array([[0], [2], [0], [1], [1]])
W = perceptron_train(X, y)
print('Веса персептрона для входных признаков медицинских карт:', W)
