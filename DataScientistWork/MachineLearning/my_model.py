import matplotlib
import tensorflow as tf
import tensorflow_datasets as tfds
from matplotlib import pyplot as plt

train_data, val_data, test_data = tfds.load("cifar10",
                                            split=['train[10000:]', 'train[0:10000]', 'test'],
                                            batch_size=128, as_supervised=True)

x_viz, y_viz = tfds.load("cifar10", split=['train[:5000]'], batch_size=-1, as_supervised=True)[
    0]  # Взять все одним батчем и выбрать его для визуализации
print('Размерность исходных данных:', x_viz.shape)

