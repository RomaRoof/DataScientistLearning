import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from xgboost import XGBClassifier

# Считываем имена столбцов из .data файл
def read_names(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        column_names = []
        for line in lines:
            if line.strip() and not line.startswith('|'):
                column_names.append(line.split(':')[0].strip())
    return column_names

# Путь к файлам
data_file = 'D:\Рома Учеба\Founder\DSHomeWork\DataScientistWork\dataset\parkinsons\parkinsons.data'
# Adaptive path to /data for git
# FILE_PATH = '/data'
# data_file = pd.read_csv(f'{FILE_PATH}/parkinsons.data')

# Читаем имена столбцов
column_names = read_names(data_file)

# Загружаем данные в DataFrame
data = pd.read_csv(data_file)
#print(data.head())
#print(data.columns)

# Подготовка данных
X = data.drop(columns=['name', 'status'])
y = data['status']

# Нормализация признаков
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=43)

# Обучение модели XGBoost
model = XGBClassifier().fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)


# Оценка точности модели
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print(f'Confusion Matrix:\n{conf_matrix}')
print(f'Classification Report:\n{class_report}')