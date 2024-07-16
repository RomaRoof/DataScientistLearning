import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

FILE_PATH = './dataset'
df_news = pd.read_csv(f'{FILE_PATH}/fake_news.csv')

df_news.drop_duplicates(inplace=True)
df_news.dropna(subset=['text', 'label'], inplace=True)

X = df_news['text']
y = df_news['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)

tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)

tfidf_train = tfidf_vectorizer.fit_transform(X_train)
tfidf_test = tfidf_vectorizer.transform(X_test)

pac = PassiveAggressiveClassifier(max_iter=50)
pac.fit(tfidf_train, y_train)

y_pred = pac.predict(tfidf_test)

score = accuracy_score(y_test, y_pred)
print(f'Accuracy: {score * 100:.2f}%')

score = accuracy_score(y_test, y_pred)
print(f'Accuracy: {score * 100:.2f}%')

conf_matrix = confusion_matrix(y_test, y_pred)
print(conf_matrix)

# Визуализация матрицы ошибок
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['FAKE', 'REAL'], yticklabels=['FAKE', 'REAL'])
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

class_report = classification_report(y_test, y_pred, target_names=['FAKE', 'REAL'])
print("Отчет классификаций:")
print(class_report)

# Визуализация распределения меток
plt.figure(figsize=(10, 5))
ax = sns.countplot(x=y_pred, palette='viridis')
ax.set_xticklabels(['FAKE', 'REAL'])
plt.xlabel('Прогноз меток')
plt.ylabel('Колличество')
plt.title('Распространение предсказанных меток')
plt.show()
