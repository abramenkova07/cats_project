from http import HTTPStatus
import pytest

from .utils import check_permissions, create_breeds


@pytest.mark.django_db(transaction=True)
class Test01BreedAPI:

    BREED_URL = '/api/breeds/'
    BREED_SLUG_TEMPLATE_URL = '/api/breeds/{slug}/'

    def test_01_breed_not_auth(self, client):
        response = client.get(self.BREED_URL)
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.BREED_URL}` не найден. Проверьте настройки в '
            '*urls.py*.'
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос неавторизованного пользователя к '
            f'`{self.BREED_URL}` возвращает ответ со статусом 200.'
        )

    def test_02_breed_post_superuser(self, user_superuser_client):
        breeds_count = 0

        data = {}
        response = user_superuser_client.post(self.BREED_URL, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Если POST-запрос суперюзера, отправленный к '
            f'`{self.BREED_URL}`, содержит некорректные данные - должен '
            'вернуться ответ со статусом 400.'
        )

        data = {
            'name': 'Порода',
            'slug': 'breed'
        }
        response = user_superuser_client.post(self.BREED_URL, data=data)
        assert response.status_code == HTTPStatus.CREATED, (
            'Если POST-запрос суперюзера, отправленный к '
            f'`{self.BREED_URL}`, содержит корректные данные - должен '
            'вернуться ответ со статусом 201.'
        )
        breeds_count += 1

        data = {
            'name': 'Новая порода',
            'slug': 'breed'
        }
        response = user_superuser_client.post(self.BREED_URL, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если в POST-запросе суперюзера к `{self.BREED_URL}` '
            'передан уже существующий `slug` - должен вернуться ответ со '
            'статусом 400.'
        )

        post_data = {
            'name': 'Новая порода',
            'slug': 'new_breed'
        }
        response = user_superuser_client.post(self.BREED_URL, data=post_data)
        assert response.status_code == HTTPStatus.CREATED, (
            f'Если POST-запрос суперюзера к `{self.BREED_URL}` '
            'содержит корректные данные - должен вернуться ответ со статусом '
            '201.'
        )
        breeds_count += 1

        response = user_superuser_client.get(self.BREED_URL)
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что при GET-запросе к `{self.BREED_URL}` '
            'возвращается статус 200.'
        )

    def test_03_breed_delete_patch_superuser(self, user_superuser_client):
        breed_1, breed_2 = create_breeds(user_superuser_client)
        response = user_superuser_client.delete(
            self.BREED_SLUG_TEMPLATE_URL.format(
                slug=breed_1['slug']
            )
        )
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'Проверьте, что DELETE-запрос суперюзера к '
            f'`{self.BREED_SLUG_TEMPLATE_URL}` возвращает ответ со '
            'статусом 204.'
        )
        response = user_superuser_client.get(self.BREED_URL)
        test_data = response.json()
        assert len(test_data) == 1, (
            'Проверьте, что DELETE-запрос суперюзера к '
            f'`{self.BREED_SLUG_TEMPLATE_URL}` удаляет категорию.'
        )
        response = user_superuser_client.get(
            self.BREED_SLUG_TEMPLATE_URL.format(
                slug=breed_2['slug']
            )
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запросы к '
            f'`{self.BREED_SLUG_TEMPLATE_URL}` разрешены и возвращают '
            'ответ со статусом 200.'
        )
        response = user_superuser_client.patch(
            self.BREED_SLUG_TEMPLATE_URL.format(
                slug=breed_2['slug']
            )
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что PATCH-запросы к '
            f'`{self.BREED_SLUG_TEMPLATE_URL}` разрешены и возвращают '
            'ответ со статусом 200.'
        )

    def test_04_breed_check_permission(self, client,
                                       user_client,
                                       user_superuser_client):
        breeds = create_breeds(user_superuser_client)
        data = {
            'name': 'Обновленная порода',
            'slug': 'updated_breed'
        }
        check_permissions(client, self.BREED_URL, data,
                          'неавторизованного пользователя',
                          breeds, HTTPStatus.UNAUTHORIZED)
        check_permissions(user_client, self.BREED_URL, data,
                          'пользователя с ролью `user`', breeds,
                          HTTPStatus.FORBIDDEN)
