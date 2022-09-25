import pytest
from rest_framework.reverse import reverse


# =================RATE=========================================
def test_rates_get(api_client_auth):
    response = api_client_auth.get(reverse('api-v1:rates'))
    assert response.status_code == 200
    assert response.json()['count']
    assert response.json()['results']


def test_rates_post_empty(api_client_auth):
    response = api_client_auth.post(reverse('api-v1:rates'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'currency_type': ['This field is required.'],
        'buy': ['This field is required.'],
        'sale': ['This field is required.'],
        'source': ['This field is required.'],
    }


# ==================CONTACT US==================================
def test_contactus_api_get(api_client_auth):
    response = api_client_auth.get(reverse('api-v1:contactus-list'))
    assert response.status_code == 200
    assert response.json()


def test_contactus_api_post_empty(api_client_auth):
    response = api_client_auth.post(reverse('api-v1:contactus-list'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.'],
    }


def test_contactus_api_post_valid(api_client_auth, mailoutbox):
    data = {
        'email_from': 'example@mail.com',
        'subject': 'Subject example',
        'message': 'Message example'
    }
    response = api_client_auth.post(reverse('api-v1:contactus-list'), data=data)
    assert response.status_code == 200
    assert len(mailoutbox) == 1


@pytest.mark.parametrize('email_from', ['examplemail.com', '12365.com', 'GHGDHGHD'])
def test_contactus_api_post_invalid_email(api_client_auth, email_from):
    data = {
        'email_from': email_from,
        'subject': 'Subject example',
        'message': 'Message example'
    }
    response = api_client_auth.post(reverse('api-v1:contactus-list'), data=data)
    assert response.status_code == 400
    assert response.json() == {
        'email_from': ['Enter a valid email address.'],
    }
