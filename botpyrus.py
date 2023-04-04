from flask import Flask, request, redirect
import requests

app = Flask(__name__)

@app.route('/<task_id>/<count>', methods=['GET', 'POST'])
def index(task_id, count):
    username = 'bot@e6d54a56-0c25-4264-96f0-743734861368'
    secret = 'VPeAZs5-bCifonL23rWah~7hNC6nkc8nHQxzguF5NYrZB-02HZNxwjZjqGjbctPZJMFr8JdZF-E5nWuTaA2O4Mdo9sU7xHkw'
    auth_url = 'https://api.pyrus.com/v4/auth'
    response = requests.post(auth_url, json={'login': username, 'security_key': secret})
    if response.status_code == 200:
       access_token = response.json()['access_token']
       print(access_token)
    else:
       print('Ошибка авторизации')

    url = 'https://api.pyrus.com/v4/tasks/{}/comments'.format(task_id)
    print(url)
    data = {'text': "Клиент звонил повторно.",
            'field_updates': [
                {
                    'id': 13,
                    'type': 'number',
                    'name': 'Количество обращений по задаче:',
                    'value': str(int(count) + 1)
                }
            ]
        }
    headers = {
               'Authorization': 'Bearer {}'.format(access_token),
               'Content-Type': 'application/json'
             }
    headers_dict = dict(headers)
    response = requests.post(url, json=data, headers=headers_dict)
    return redirect(f'https://pyrus.com/t#id{task_id}')

if __name__ == '__main__':
    app.run("0.0.0.0", 5001)
