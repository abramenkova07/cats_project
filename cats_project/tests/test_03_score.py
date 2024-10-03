from http import HTTPStatus
import pytest

from .utils import check_permissions, create_cats, create_scores


@pytest.mark.django_db(transaction=True)
class Test03ScoreAPI:

    SCORE_URL = '/api/scores/'
    SCORE_ID_TEMPLATE_URL = '/api/scores/{score_id}/'

    def test_01_score_not_auth(self, client):
        response = client.get(self.SCORE_URL)
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.SCORE_URL}` не найден. Проверьте настройки в '
            '*urls.py*.'
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос неавторизованного пользователя к '
            f'`{self.SCORE_URL}` возвращает ответ со статусом 200.'
        )

    def test_02_score_post_user(self, user_client, user_superuser_client):
        cats, _ = create_cats(user_client, user_superuser_client)
        scores_count = 0
        data = {}
        response = user_superuser_client.post(self.SCORE_URL, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Если POST-запрос авторизованного пользователя, отправленный к '
            f'`{self.SCORE_URL}`, содержит некорректные данные - должен '
            'вернуться ответ со статусом 400.'
        )
        data = {
            'cat': cats[0]['id'],
            'score': 1
        }
        response = user_superuser_client.post(self.SCORE_URL, data=data)
        assert response.status_code == HTTPStatus.CREATED, (
            'Если POST-запрос авторизованного пользователя, отправленный к '
            f'`{self.SCORE_URL}`, содержит корректные данные - должен '
            'вернуться ответ со статусом 201.'
        )
        scores_count += 1
        response = user_superuser_client.post(self.SCORE_URL, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Если в POST-запросе авторизованного пользователя к '
            f'`{self.SCORE_URL}` передан уже существующий `cat` - должен '
            'вернуться ответ со статусом 400.'
        )

    def test_03_score_detail(self, client, user_client, user_superuser_client):
        scores, cats, _ = create_scores(user_client,
                                        user_superuser_client)
        response = client.get(
            self.SCORE_ID_TEMPLATE_URL.format(score_id=scores[0]['id'])
        )
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.SCORE_ID_TEMPLATE_URL}` не найден, '
            'проверьте настройки в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос неавторизованного пользователя к '
            f'`{self.SCORE_ID_TEMPLATE_URL}` возвращает ответ со '
            'статусом 200.'
        )
        data = response.json()
        assert isinstance(data.get('score'), int), (
            'Поле `score` отсутствует или содержит некорректное значение '
            'в ответе на GET-запрос неавторизованного пользователя к '
            f'`{self.SCORE_ID_TEMPLATE_URL}`.'
        )
        data = data.get('cat')
        del data['owner']
        assert data == cats[0], (
            'Поле `cat` отсутствует или содержит некорректное значение '
            'в ответе на GET-запрос неавторизованного пользователя к '
            f'`{self.SCORE_ID_TEMPLATE_URL}`.'
        )
        update_data = {
            'cat': cats[0]['id'],
            'score': 2
        }
        response = user_superuser_client.patch(
            self.SCORE_ID_TEMPLATE_URL.format(score_id=scores[0]['id']),
            data=update_data
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что PATCH-запрос авторизованного пользователя к '
            f'`{self.SCORE_ID_TEMPLATE_URL}` возвращает ответ со '
            'статусом 200.'
        )
        data = response.json()
        assert data.get('score') == update_data['score'], (
            'Проверьте, что PATCH-запрос авторизованного пользователя к '
            f'`{self.SCORE_ID_TEMPLATE_URL}` возвращает изменённые '
            'данные оценки. Сейчас поле `score` отсутствует в ответе или '
            'содержит некорректное значение.'
        )
        response = user_superuser_client.delete(
            self.SCORE_ID_TEMPLATE_URL.format(score_id=scores[0]['id']),
        )
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'Проверьте, что DELETE-запрос авторизованного пользователя к '
            f'`{self.SCORE_ID_TEMPLATE_URL}` возвращает ответ со '
            'статусом 204.'
        )
        response = client.get(self.SCORE_ID_TEMPLATE_URL)
        test_data = response.json()
        assert len(test_data) == len(cats) - 1, (
            'Проверьте, что DELETE-запрос авторизованного пользователя к '
            f'`{self.SCORE_ID_TEMPLATE_URL}` удаляет оценку из '
            'базы данных.'
        )
        response = user_client.delete(
            self.SCORE_ID_TEMPLATE_URL.format(score_id=scores[0]['id']),
        )
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            'Проверьте, что DELETE-запрос другого пользователя к '
            f'`{self.SCORE_ID_TEMPLATE_URL}` возвращает ответ со '
            'статусом 404.'
        )
        response = client.get(self.SCORE_URL)
        test_data = response.json()
        assert len(test_data) == len(cats) - 1, (
            'Проверьте, что DELETE-запрос другого пользователя к '
            f'`{self.SCORE_ID_TEMPLATE_URL}` не удаляет оценку из '
            'базы данных.'
        )

    def test_04_score_check_permission(self, client, user_client,
                                       user_superuser_client):
        scores, cats, breeds = create_scores(
            user_client, user_superuser_client)
        data = {
            'cat': cats[0]['id'],
            'score': 1
        }
        check_permissions(client, self.SCORE_URL, data,
                          'неавторизованного пользователя', cats,
                          HTTPStatus.UNAUTHORIZED)
