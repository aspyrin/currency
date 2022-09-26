import pytest
from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from accounts.models import User


@pytest.fixture(autouse=True, scope="function")
def enable_db_access_for_all_tests(db):
    """
    give access to database for all tests
    """


@pytest.fixture(autouse=True, scope="session")
def load_fixtures(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        fixtures = (
            'source.json',
            'rate.json',
            'contactus.json',
        )
        for fixture in fixtures:
            call_command('loaddata', f'app/tests/fixtures/{fixture}')


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def api_client_auth(api_client):
    # create user
    password = 'password'
    email = 'example@mail.com'
    user = User(email=email)
    user.set_password(password)
    user.save()

    # obtain access_token
    r = api_client.post(
        reverse('api-v1:token_obtain_pair'),
        data={'email': email, 'password': password},
    )
    assert r.status_code == 200, r.content
    assert "access" in r.json(), r.content
    token = r.json()['access']

    # set Authorization header for all requests
    api_client.credentials(
        HTTP_AUTHORIZATION=f'JWT {token}'
    )

    return api_client
