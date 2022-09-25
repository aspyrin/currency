import json
from unittest.mock import MagicMock

from currency.models import Rate
from currency.tasks import parse_privatbank, parse_monobank, parse_vkurse


def test_parse_privatbank(mocker):
    # expected rates from this source
    # 1 USD (UAH), 1 EUR (UAH), 1 BTC (USD)
    expected_rate_count = 3

    with open('app/tests/mocks/privatbank.txt', 'r') as file:
        text = file.read()
        text_cleened = text.replace("\n", "").replace(" ", "")
        response_json = json.loads(text_cleened)

    initial_rate_count = Rate.objects.count()
    requests_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    parse_privatbank()
    assert Rate.objects.count() == initial_rate_count + expected_rate_count


def test_parse_monobank(mocker):
    # expected rates from this source
    # 1 USD (UAH), 1 EUR (UAH), 1 EUR (USD)
    expected_rate_count = 3

    with open('app/tests/mocks/monobank.txt', 'r') as file:
        text = file.read()
        text_cleened = text.replace("\n", "").replace(" ", "")
        response_json = json.loads(text_cleened)

    initial_rate_count = Rate.objects.count()
    requests_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    parse_monobank()
    assert Rate.objects.count() == initial_rate_count + expected_rate_count


def test_parse_vkurse(mocker):
    # expected rates from this source
    # 1 USD (UAH), 1 EUR (UAH)
    expected_rate_count = 2

    with open('app/tests/mocks/vkurse.txt', 'r') as file:
        text = file.read()
        text_cleened = text.replace("\n", "").replace(" ", "")
        response_json = json.loads(text_cleened)

    initial_rate_count = Rate.objects.count()
    requests_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    parse_vkurse()
    assert Rate.objects.count() == initial_rate_count + expected_rate_count
