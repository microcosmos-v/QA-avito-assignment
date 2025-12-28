import requests
import pytest
import uuid
ENDPOINT = 'https://qa-internship.avito.com'


@pytest.fixture
def def_payload():
    return {"sellerID": 131313, "name": "2018 Jaguar E-Pace P300", "price": 2000, "statistics": {"likes": 12, "viewCount": 13, "contacts": 3}}


def test_create_ad_with_unique_seller_id(def_payload):
    """Создание объявления с уникальным sellerID"""
    payload = def_payload
    response = create_ad(payload)
    assert response.status_code == 200  # Проверка успешного ответа от сервера
    response = response.json()['status'].split(' - ')
    # Проверка существует ли объявление по его идентификатору
    assert get_ad(response[1]).status_code == 200


def test_create_ad_with_negative_seller_id(def_payload):  # тест не проходит
    """Создание объявления с отрицательным sellerID"""
    payload = def_payload
    payload['sellerID'] = -131313
    # Сколько объявлений было у продавца до создания объявления
    ad_count = len(get_seller_ads(payload['sellerID']).json())
    response = create_ad(payload)
    assert response.status_code == 400  # Проверка возвращается ли ошибка
    # Проверка что новых объявлений создано не было
    assert ad_count == len(get_seller_ads(payload['sellerID']).json())


def test_create_ad_with_negative_price(def_payload):  # тест не проходит
    """Создание объявления с отрицательным price"""
    payload = def_payload
    payload["price"] = -2000
    # Сколько объявлений было у продавца до создания объявления
    ad_count = len(get_seller_ads(payload['sellerID']).json())
    response = create_ad(payload)
    assert response.status_code == 400  # Проверка возвращается ли ошибка
    # Проверка что новых объявлений создано не было
    assert ad_count == len(get_seller_ads(payload['sellerID']).json())


def test_create_ad_with_negative_likes(def_payload):  # тест не проходит
    """Создание объявления с отрицательным likes"""
    payload = def_payload
    payload["likes"] = -12
    # Сколько объявлений было у продавца до создания объявления
    ad_count = len(get_seller_ads(payload['sellerID']).json())
    response = create_ad(payload)
    assert response.status_code == 400  # Проверка возвращается ли ошибка
    # Проверка что новых объявлений создано не было
    assert ad_count == len(get_seller_ads(payload['sellerID']).json())


def test_create_ad_with_negative_view_count(def_payload):  # тест не проходит
    """Создание объявления с отрицательным viewCount"""
    payload = def_payload
    payload["viewCount"] = -13
    # Сколько объявлений было у продавца до создания объявления
    ad_count = len(get_seller_ads(payload['sellerID']).json())
    response = create_ad(payload)
    assert response.status_code == 400  # Проверка возвращается ли ошибка
    # Проверка что новых объявлений создано не было
    assert ad_count == len(get_seller_ads(payload['sellerID']).json())


def test_create_ad_with_negative_contacts(def_payload):
    """Создание объявления с отрицательным contacts"""
    payload = def_payload
    payload["contacts"] = -3
    # Сколько объявлений было у продавца до создания объявления
    ad_count = len(get_seller_ads(payload['sellerID']).json())
    response = create_ad(payload)
    assert response.status_code == 400  # Проверка возвращается ли ошибка
    # Проверка что новых объявлений создано не было
    assert ad_count == len(get_seller_ads(payload['sellerID']).json())


def test_get_ad_by_existing_id(def_payload):
    """Получение объявления по существующему ID"""
    payload = def_payload
    id = create_ad(payload).json()['status'].split(' - ')[1]
    response = get_ad(id)
    assert response.status_code == 200  # Объявление существует


def test_get_ad_by_non_existent_id():
    """Получение объявления по несущесвующему ID"""
    response = get_ad(uuid.uuid4())
    assert response.status_code == 404  # Объявление не существует


def test_get_ads_by_seller_id(def_payload):
    """Получение всех объявлений по seller ID"""
    payload = def_payload
    create_ad(payload)
    payload['name'] = 'second'
    create_ad(payload)
    response = get_seller_ads(payload['sellerID'])
    assert response.status_code == 200  # Успешный ответ
    assert len(response.json()) >= 2  # Все объявления отображаются


def test_get_stats_by_item_id(def_payload):
    """Получение статистики по item id"""
    payload = def_payload
    ad_id = create_ad(payload).json()['status'].split(' - ')[1]
    response = get_stat(ad_id)
    response_data = response.json()[0]
    assert response.status_code == 200  # Успешный ответ
    # Проверка существуют ли поля в запросе
    assert 'likes' in response_data and 'contacts' in response_data and 'viewCount' in response_data


def test_get_stats_by_non_existent_item_id():
    """Получение статистики по несущесвующему item id"""
    response = get_stat(uuid.uuid4())
    assert response.status_code == 404  # Успешный ответ


def get_ad(ad_id: str) -> requests.Response:
    """Получения объявления по его идентификатору
    :param ad_id: идентификатор объявления"""
    return requests.get(ENDPOINT + f'/api/1/item/{ad_id}')


def get_seller_ads(seller_id: int) -> requests.Response:
    """Получение всех объявлений продавца
    :param seller_id: идентификатор продавца"""
    return requests.get(ENDPOINT + f'/api/1/{seller_id}/item')


def create_ad(payload: dict) -> requests.Response:
    """Создание объявления
    :param payload: передаваемые данные (body)"""
    return requests.post(ENDPOINT + '/api/1/item', json=payload)


def get_stat(ad_id: str):
    """Получение статистики объявления
    :param ad_id: идентификатор объявления"""
    return requests.get(ENDPOINT + f'/api/1/statistic/{ad_id}')
