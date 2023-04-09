from flask import Flask, request, redirect
import requests

app = Flask(__name__)

@app.route('/<task_id>/<count>', methods=['GET', 'POST'])
def index(task_id, count):
    username = 'bot@e6d54a56-0c25-4264-96'  # Логин бота 
    secret = 'VPeAZs5-bCifonL23rWah~7hNC6nkc8nHQx'  # Пароль бота
    auth_url = 'https://api.pyrus.com/v4/auth'
    response = requests.post(auth_url, json={'login': username, 'security_key': secret})
    if response.status_code == 200:
       access_token = response.json()['access_token']
       print(access_token)
    else:
       print('Ошибка авторизации')

    url = 'https://api.pyrus.com/v4/tasks/{}/comments'.format(task_id)
    print(url)
    data = {'text': "Клиент звонил повторно.",   # Текст комментария 
            'field_updates': [  #  Изменяемые поля
                {
                    'id': 13,  # id поля с счётчиком обращений (его нужно создать)
                    'type': 'number',  # тип поля
                    'name': 'Количество обращений по задаче:',  # название поля
                    'value': str(int(count) + 1)  # значение поля
                }
            ]
        }
    headers = {
               'Authorization': 'Bearer {}'.format(access_token),
               'Content-Type': 'application/json'
             }
    headers_dict = dict(headers)
    response = requests.post(url, json=data, headers=headers_dict)
    return redirect(f'https://pyrus.com/t#id{task_id}')  # после редиректимся на страницу с задачей

if __name__ == '__main__':
    app.run("0.0.0.0", 5001)
