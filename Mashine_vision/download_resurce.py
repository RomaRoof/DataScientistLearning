import requests

url = 'https://www.film.ru/sites/default/files/people/1457583-2618007.jpg'
response = requests.get(url)

with open('friends.jpg', 'wb') as f:
    f.write(response.content)