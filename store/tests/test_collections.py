import pytest
from rest_framework import status
from model_bakery import baker
from store.models import Collection
from django.contrib.auth import get_user_model
User = get_user_model()
# --------------------
# FIXED FIXTURES
# --------------------
@pytest.fixture
def payload():
    return {
        "title": "Test Collection",
    }

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(data):
        return api_client.post("/store/collections/", data, format="json")
    return do_create_collection

@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        user = baker.make(User, is_staff=is_staff)
        api_client.force_authenticate(user=user)
        return user
    return do_authenticate

# --------------------
# CREATE COLLECTION TESTS
# --------------------
@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection, payload):
        response = create_collection(payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_collection, payload):
        authenticate(is_staff=False)
        response = create_collection(payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_collection):
        authenticate(is_staff=True)
        response = create_collection({"title": ""})  # invalid title
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

    def test_if_data_is_valid_returns_201(self, authenticate, create_collection, payload):
        authenticate(is_staff=True)
        response = create_collection(payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

# --------------------
# RETRIEVE COLLECTION TESTS
# --------------------
@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        collection = baker.make(Collection)
        response = api_client.get(f"/store/collections/{collection.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": collection.id,
            "title": collection.title,
            "products_count": 0,
        }
