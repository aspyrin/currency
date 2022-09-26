from django.urls import reverse


def test_rates_get_non_authorization(client):
    """
    without authorization redirect to SignIn
    :param client:
    :return: true if status_code == 302
    """
    response = client.get(reverse('currency:rate_list'))
    assert response.status_code == 302
