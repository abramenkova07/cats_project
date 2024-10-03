from http import HTTPStatus


def create_breeds(user_superuser_client):
    data1 = {
        'name': 'Порода',
        'slug': 'breed'
    }
    response = user_superuser_client.post('/api/breeds/', data=data1)
    assert response.status_code == HTTPStatus.CREATED, (
        'Если POST-запрос суперюзера к `/api/breeds/` '
        'содержит корректные данные - должен вернуться ответ со статусом 201.'
    )
    data2 = {
        'name': 'Новая порода',
        'slug': 'new_breed'
    }
    user_superuser_client.post('/api/breeds/', data=data2)
    return [data1, data2]


def check_permissions(client, url, data, user_role, objects,
                      expected_status):
    sufix = 'slug' if 'slug' in objects[0] else 'id'

    response = client.post(url, data=data)
    assert response.status_code == expected_status, (
        f'Проверьте, что POST-запрос {user_role} к `{url}` возвращает ответ '
        f'со статусом {expected_status}.'
    )
    response = client.patch(f'{url}{objects[0][sufix]}/', data=data)
    assert response.status_code == expected_status, (
        f'Проверьте, что PATCH-запрос {user_role} к `{url}<{sufix}>/` '
        f'возвращает ответ со статусом {expected_status}.'
    )
    response = client.delete(f'{url}{objects[0][sufix]}/')
    assert response.status_code == expected_status, (
        f'Проверьте, что DELETE-запрос {user_role} к `{url}<{sufix}>/` '
        f'возвращает ответ со статусом {expected_status}'
    )


def create_cats(user_client, user_superuser_client):
    breeds = create_breeds(user_superuser_client)
    result = []
    data = {
        'name': 'Котенок',
        'color': 'Белый',
        'age': 19,
        'breed': breeds[0]['name'],
        'description': 'Милый котик'
    }
    response = user_client.post('/api/cats/', data=data)
    assert response.status_code == HTTPStatus.CREATED, (
        'Если POST-запрос авторизованного пользователя к `/api/cats/`'
        ' содержит корректные данные - должен вернуться '
        'ответ со статусом 201.'
    )
    data['id'] = response.json()['id']
    result.append(data)
    data = {
        'name': 'Милаш',
        'color': 'Черный',
        'age': 10,
        'breed': breeds[1]['name'],
        'description': 'Лучший'
    }
    response = user_client.post('/api/cats/', data=data)
    data['id'] = response.json()['id']
    result.append(data)
    return result, breeds


def create_scores(user_client, user_superuser_client):
    cats, breeds = create_cats(user_client, user_superuser_client)
    result = []
    data = {
        'cat': cats[0]['id'],
        'score': 5
    }
    response = user_superuser_client.post('/api/scores/', data=data)
    assert response.status_code == HTTPStatus.CREATED, (
        'Если POST-запрос авторизованного пользователя к `/api/scores/` '
        'содержит корректные данные - должен вернуться ответ со статусом 201.'
    )
    data['id'] = response.json()['id']
    result.append(data)
    data = {
        'cat': cats[1]['id'],
        'score': 1
    }
    response = user_superuser_client.post('/api/scores/', data=data)
    data['id'] = response.json()['id']
    result.append(data)
    return result, cats, breeds
