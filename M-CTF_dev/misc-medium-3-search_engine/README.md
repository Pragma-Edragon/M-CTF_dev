# Secure Search Engine

## Суть
Многие негодовали, почему выкидывает после перехода к первому уровню.
Можно было понять, что сервер убивает сессию спустя определенное время.

К данному заданию приложен файл с простейшей "криптой":

```python
from app.scripts import random_hex, get_hex
from base64 import encodebytes
from random import randint


def encode_data(data_to_encode: bytes):
    res = ''
    key = randint(1, 3)
    while True:
        if key == 0:
            break
        res += ' '.join(str(''.join(list(map(get_hex, map(ord, str(encodebytes(data_to_encode))))))))
        if key % 2 == 0:
            res += "="
        key -= 1
    return res
```

Логика проста: Картинка переводится в байты, поступает на вход данной функции, после чего накладывается функция ord на b64 байты картинок. После - Хекс.

Мой вариант декодирования:
```python
from base64 import decodebytes

with open('sometxt.txt', 'r') as file:
    data = file.read().replace(' ', '').split('=')
    res = []
    iter = 0
    while True:
        if iter >= len(data[0]):
            break
        res.append(data[0][iter:iter+6])
        iter += 6

with open('solve.txt', 'w') as file:
    file.write(str(res))
    file.close()

with open('solve.txt', 'r') as f:
    new = f.read().replace('][', ']=[').split('=')
    new = eval(new[0])
    var = map(lambda x: chr(int(x, 16)), res)
    var = ''.join(var)
    var = eval(var)
    var = decodebytes(var)
    open('a.png', 'wb').write(var)
print(var)
```

(Алсо, решение можно уместить в пару строк, написано, чтоб было понятно)

Далее - есть 2 вектора.
-  Сохранять картинки локально и далее искать их в Яндексе/Гугле. Записывать статически результаты поиска в словарь с хешами картинок и далее сравнивать. Не самый оптимальный вариант. 
- Пользоваться api яндекса по поиску картинок, под названием cbir.
Приведу пример кода, который может найти картинку:

```python
import requests, json, re
from bs4 import BeautifulSoup as bs4

searchUrl = 'https://yandex.ru/images/search'
files = {'upfile': ('', open('anime.jpg', 'rb'), 'image/jpeg')}
params = {'rpt': 'imageview', 'format': 'json', 'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
url = r'https://yandex.ru/images/search?&rpt=imageview&format=json&request=[{"block":"cbir-uploader__get-cbir-id"}]'
response = requests.post(searchUrl, params=params, files=files)
query_string = json.loads(response.content)['blocks'][0]['params']['url']
img_search_url= searchUrl + '?' + query_string
soup = bs4(requests.get(img_search_url).text, 'lxml')
parsed = soup.find('div', class_=re.compile('Tags Tags_*'))
for items in parsed.findAll('span', class_=re.compile(r'Button\d-Text')):
    print (items.text)
```