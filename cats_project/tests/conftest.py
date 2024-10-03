import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def user_superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        username='TestSuperuser',
        email='testsuperuser@cats_project.fake',
        password='1234567'
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser',
        email='testuser@cats_project.fake',
        password='1234567'
    )


@pytest.fixture
def token_user_superuser(user_superuser):
    token = AccessToken.for_user(user_superuser)
    return {
        'access': str(token),
    }


@pytest.fixture
def user_superuser_client(token_user_superuser):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {token_user_superuser["access"]}'
    )
    return client


@pytest.fixture
def token_user(user):
    token = AccessToken.for_user(user)
    return {
        'access': str(token),
    }


@pytest.fixture
def user_client(token_user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_user["access"]}')
    return client
