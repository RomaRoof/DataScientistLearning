import warnings

warnings.filterwarnings('ignore')
import pandas as pd
import matplotlib.pyplot as plt
import ast

#Датафрейм из метадаты фильмов
df = pd.read_csv('DF/movies_metadata.csv')
#Датафрейм из credits
credits_df = pd.read_csv('DF/credits.csv')
# Функция для безопасного парсинга строк в структуры данных Python
def parse_cast_crew(text):
    try:
        # Проверяем, является ли текст строкой, если нет, возвращаем пустой список
        if isinstance(text, str):
            return ast.literal_eval(text)
        return []
    except (ValueError, SyntaxError):
        return []
# Применение функции к столбцам cast и crew
credits_df['cast'] = credits_df['cast'].apply(parse_cast_crew)
credits_df['crew'] = credits_df['crew'].apply(parse_cast_crew)
#Врезультате запуска обнаружил ошибку в мета дате по столцу id, не получалось привести к int.
# Выявление некорректных значений в столбце 'id' в movies_df
def is_valid_id(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

# Фильтрация строк с некорректными значениями
df = df[df['id'].apply(is_valid_id)]

#так как в мета даных фильмов id имеет тип "object" а в credits - "int64", приводим их к общему типу
credits_df['id'] = credits_df['id'].astype(int)
df['id'] = df['id'].astype(int)

# Объединяю два файла по ключевым признакам
merged_df = pd.merge(credits_df, df, on='id')

# Замена NaN значений в столбце 'cast' на пустые списки
merged_df['cast'] = merged_df['cast'].apply(lambda x: x if isinstance(x, list) else [])
# Функция для извлечения всех актеров из столбца 'cast'
def extract_actors(cast_list):
    # Проверяем, является ли cast_list списком
    if isinstance(cast_list, list):
        return [actor['name'] for actor in cast_list if isinstance(actor, dict) and 'name' in actor]
    return []

# Добавление нового столбца с актерами
merged_df['actors'] = merged_df['cast'].apply(extract_actors)
merged_df.head()

# Создание датафрейма с актерами и их фильмами
actors_df = merged_df[['actors', 'revenue', 'budget']].explode('actors').groupby('actors').sum()
actors_df.head(15)

#Проверка на тип даных значенией в budget
actors_df['budget'] = pd.to_numeric(actors_df['budget'], errors='coerce')

#Проверка на колличество пропущенных значений
actors_df = actors_df.dropna(subset=['budget'])

#Сортировка даных
sorted_budget = actors_df.sort_values('budget', ascending=False)['budget'].head(10)

#Построение графика
sorted_budget.plot(kind='bar')
pd.set_option('display.float_format', '{:.2f}'.format)
plt.show()
