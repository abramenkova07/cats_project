from http import HTTPStatus
import pytest

from .utils import check_permissions, create_breeds, create_cats


@pytest.mark.django_db(transaction=True)
class Test02CatAPI:

    CAT_URL = '/api/cats/'
    CAT_ID_TEMPLATE_URL = '/api/cats/{cat_id}/'

    def test_01_cat_not_auth(self, client):
        response = client.get(self.CAT_URL)
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.CAT_URL}` не найден. Проверьте настройки в '
            '*urls.py*.'
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос неавторизованного пользователя к '
            f'`{self.CAT_URL}` возвращает ответ со статусом 200.'
        )

    def test_02_cat_post_user(self, user_client, user_superuser_client):
        breed_1, breed_2 = create_breeds(user_superuser_client)
        cats_count = 0
        data = {}
        response = user_client.post(self.CAT_URL, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Если POST-запрос авторизованного пользователя, отправленный к '
            f'`{self.CAT_URL}`, содержит некорректные данные - должен '
            'вернуться ответ со статусом 400.'
        )
        data = {
            'name': 'Котенок',
            'color': 'Белый',
            'age': 12,
            'breed': breed_1['name'],
            'description': 'Описание'
        }
        response = user_client.post(self.CAT_URL, data=data)
        assert response.status_code == HTTPStatus.CREATED, (
            'Если POST-запрос авторизованного пользователя, отправленный к '
            f'`{self.CAT_URL}`, содержит корректные данные - должен '
            'вернуться ответ со статусом 201.'
        )
        cats_count += 1
        response = user_client.post(self.CAT_URL, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Если в POST-запросе авторизованного пользователя к '
            f'`{self.CAT_URL}` передан уже существующий `name` - должен '
            'вернуться ответ со статусом 400.'
        )
        data = {
            'name': 'Новый Котенок',
            'color': 'Белый',
            'age': 1,
            'breed': breed_1['name'],
            'description': 'Описание'
        }
        response = user_client.post(self.CAT_URL, data=data)
        assert response.status_code == HTTPStatus.CREATED, (
            'Если POST-запрос авторизованного пользователя к '
            f'`{self.CAT_URL}` содержит корректные данные - должен вернуться '
            'ответ со статусом 201.'
        )
        cats_count += 1
        response = user_client.get(self.CAT_URL)
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что при GET-запросе к `{self.CAT_URL}` '
            'возвращается статус 200.'
        )
        post_data = {
            'name': 'Котик',
            'color': 'Черный',
            'age': 2,
            'breed': breed_2['name'],
            'description': 'Описание'
        }
        user_client.post(self.CAT_URL, data=post_data)

        response = user_client.get(
            f'{self.CAT_URL}?breed={breed_2["slug"]}'
        )
        data = response.json()
        assert len(data) == 1, (
            f'Проверьте, что для эндпоинта `{self.CAT_URL}` реализована '
            'возможность фильтрации по полю `breed` с использованием '
            'параметра `slug` породы.'
        )

    def test_03_cat_detail(self, client, user_client, user_superuser_client):
        cats, breeds = create_cats(user_client, user_superuser_client)
        response = client.get(
            self.CAT_ID_TEMPLATE_URL.format(cat_id=cats[0]['id'])
        )
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.CAT_ID_TEMPLATE_URL}` не найден, '
            'проверьте настройки в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос неавторизованного пользователя к '
            f'`{self.CAT_ID_TEMPLATE_URL}` возвращает ответ со '
            'статусом 200.'
        )
        data = response.json()
        assert isinstance(data.get('id'), int), (
            'Поле `id` отсутствует или содержит некорректное значение '
            'в ответе на GET-запрос неавторизованного пользователя к '
            f'`{self.CAT_ID_TEMPLATE_URL}`.'
        )
        assert data.get('breed') == breeds[0]['name'], (
            'Поле `breed` отсутствует или содержит некорректное значение '
            'в ответе на GET-запрос неавторизованного пользователя к '
            f'`{self.CAT_ID_TEMPLATE_URL}`.'
        )
        assert data.get('name') == cats[0]['name'], (
            'Поле `name` отсутствует или содержит некорректное значение '
            'в ответе на GET-запрос неавторизованного пользователя к '
            f'`{self.CAT_ID_TEMPLATE_URL}`.'
        )
        update_data = {
            'name': 'Милый',
            'breed': breeds[1]['name']
        }
        response = user_client.patch(
            self.CAT_ID_TEMPLATE_URL.format(cat_id=cats[0]['id']),
            data=update_data
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что PATCH-запрос авторизованного пользователя к '
            f'`{self.CAT_ID_TEMPLATE_URL}` возвращает ответ со '
            'статусом 200.'
        )
        data = response.json()
        assert data.get('name') == update_data['name'], (
            'Проверьте, что PATCH-запрос авторизованного пользователя к '
            f'`{self.CAT_ID_TEMPLATE_URL}` возвращает изменённые '
            'данные котика. Сейчас поле `name` отсутствует в ответе или '
            'содержит некорректное значение.'
        )
        assert data.get('breed') == update_data['breed'], (
            'Проверьте, что PATCH-запрос авторизованного пользователя к '
            f'`{self.CAT_ID_TEMPLATE_URL}` может изменять значение '
            'поля `breed` котенка.'
        )
        response = user_client.delete(
            self.CAT_ID_TEMPLATE_URL.format(cat_id=cats[0]['id']),
        )
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'Проверьте, что DELETE-запрос авторизованного пользователя к '
            f'`{self.CAT_ID_TEMPLATE_URL}` возвращает ответ со '
            'статусом 204.'
        )
        response = client.get(self.CAT_URL)
        test_data = response.json()
        assert len(test_data) == len(cats) - 1, (
            'Проверьте, что DELETE-запрос авторизованного пользователя к '
            f'`{self.CAT_ID_TEMPLATE_URL}` удаляет котика из '
            'базы данных.'
        )
        response = user_superuser_client.delete(
            self.CAT_ID_TEMPLATE_URL.format(cat_id=cats[0]['id']),
        )
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            'Проверьте, что DELETE-запрос другого пользователя к '
            f'`{self.CAT_ID_TEMPLATE_URL}` возвращает ответ со '
            'статусом 404.'
        )
        response = client.get(self.CAT_URL)
        test_data = response.json()
        assert len(test_data) == len(cats) - 1, (
            'Проверьте, что DELETE-запрос другого пользователя к '
            f'`{self.CAT_ID_TEMPLATE_URL}` не удаляет котика из '
            'базы данных.'
        )

    def test_04_cat_check_permission(self, client, user_client,
                                     user_superuser_client):
        cats, breeds = create_cats(user_client, user_superuser_client)
        data = {
            'name': 'Котенок',
            'color': 'Белый',
            'age': 19,
            'breed': breeds[0]['name'],
            'description': 'Милый котик'
        }
        check_permissions(client, self.CAT_URL, data,
                          'неавторизованного пользователя', cats,
                          HTTPStatus.UNAUTHORIZED)
