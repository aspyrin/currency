from django.urls import reverse
import pytest


def test_contactus_get(client):
    response = client.get(reverse('currency:contactus_create'))
    assert response.status_code == 200


def test_contactus_post_empty(client):
    response = client.post(reverse('currency:contactus_create'), data={})
    assert response.status_code == 200
    assert response.context_data['form'].errors == {'email_from': ['This field is required.'],
                                                    'subject': ['This field is required.'],
                                                    'message': ['This field is required.'],
                                                    }


def test_contactus_post_valid(client, mailoutbox):
    data = {
        'email_from': 'example@mail.com',
        'subject': 'Subject example',
        'message': 'Message example'
    }
    response = client.post(reverse('currency:contactus_create'), data=data)
    # status code with redirect
    assert response.status_code == 302
    # redirect to
    assert response.headers['Location'] == '/currency/'
    # count mails
    assert len(mailoutbox) == 1


@pytest.mark.parametrize('email_from', ['examplemail.com', '12365.com', 'GHGDHGHD'])
def test_contactus_post_invalid_email(client, email_from):
    data = {
        'email_from': email_from,
        'subject': 'Subject example',
        'message': 'Message example'
    }
    response = client.post(reverse('currency:contactus_create'), data=data)
    assert response.status_code == 200
    assert response.context_data['form'].errors == {'email_from': ['Enter a valid email address.']}
