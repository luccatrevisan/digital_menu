import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import CustomUser, Address


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
    )

    return client


@pytest.mark.django_db
def test_list_addresses_returns_only_authenticated_user_addresses(authenticated_client, user):
    Address.objects.create(
        user=user,
        cep="24220-000",
        street="Rua A",
        number="10",
        complement="",
        neighborhood="Centro",
        city="Niterói",
        state="RJ",
        label="Casa"
    )

    other_user = CustomUser.objects.create_user(
        username="other_user",
        password="123456"
    )

    Address.objects.create(
        user=other_user,
        cep="20000-000",
        street="Rua B",
        number="20",
        complement="",
        neighborhood="Copacabana",
        city="Rio de Janeiro",
        state="RJ",
        label="Trabalho"
    )

    response = authenticated_client.get("/api/address/")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["street"] == "Rua A"


@pytest.mark.django_db
def test_list_addresses_returns_empty_list_when_user_has_no_addresses(authenticated_client):
    response = authenticated_client.get("/api/address/")

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_list_addresses_requires_authentication():
    client = APIClient()

    response = client.get("/api/address/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_create_address_success(authenticated_client):
    payload = {
        "cep": "24220-000",
        "street": "Rua A",
        "number": "10",
        "complement": "",
        "neighborhood": "Centro",
        "city": "Niterói",
        "state": "RJ",
        "label": "CASA"
    }

    response = authenticated_client.post(
        "/api/address/",
        payload,
        format="json"
    )

    assert response.status_code == 201, response.data
    assert Address.objects.count() == 1

    address = Address.objects.first()

    assert address.street == payload["street"]
    assert address.city == payload["city"]


@pytest.mark.django_db
def test_create_address_requires_authentication():
    client = APIClient()

    payload = {
        "cep": "24220-000",
        "street": "Rua A",
        "number": "10",
        "complement": "",
        "neighborhood": "Centro",
        "city": "Niterói",
        "state": "RJ",
        "label": "Casa"
    }

    response = client.post(
        "/api/address/",
        payload,
        format="json"
    )

    assert response.status_code == 401