import pytest
from rest_framework import status
from model_bakery import baker
from store.models import Customer, Product, ProductImage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
import uuid
@pytest.fixture
def data():
    file = BytesIO()
    image = Image.new("RGB", (100, 100))  # small valid image
    image.save(file, "jpeg")
    file.seek(0)
    return SimpleUploadedFile("test.jpg", file.read(), content_type="image/jpeg")

User = get_user_model()
@pytest.fixture
def unique_user(db):
    username = f"user_{uuid.uuid4().hex}"  # truly unique
    return User.objects.create_user(username=username, password="pass")
@pytest.fixture
def unique_customer(unique_user, db):
    # Explicitly tie the customer to the unique user
    customer, _ = Customer.objects.get_or_create(user=unique_user)
    return customer

PRODUCTS_URL = "/store/products/"
# COMMON FIXTURES
@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        user = baker.make(User, is_staff=is_staff)
        api_client.force_authenticate(user=user)
        return user
    return do_authenticate

@pytest.fixture
def product():
    return baker.make(Product)

@pytest.fixture
def product_image(product):
    return baker.make(ProductImage, product=product)

@pytest.fixture
def payload():
    collection = baker.make("store.Collection")
    return {"title": "Test Product",
    "slug": "testproduct",
    "inventory": 10,
    "unit_price": "100.00",
    "collection": collection.id }
# ---------------------------
# PRODUCT CRUD TESTS
# ---------------------------
@pytest.mark.django_db
class TestGetProducts:
    def test_get_product_list_returns_200(self, api_client):
        products = baker.make(Product, _quantity=3)

        response = api_client.get(PRODUCTS_URL)

        # Extract actual list of product objects
        items = response.data['results']
        ids_returned = [item['id'] for item in items]

        for p in products:
            assert p.id in ids_returned

        assert response.status_code == status.HTTP_200_OK
        assert len(items) == 3



    def test_get_product_detail_returns_200(self, api_client, product):
        response = api_client.get(f"{PRODUCTS_URL}{product.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == product.id

    def test_get_nonexistent_product_returns_404(self, api_client):
        response = api_client.get(f"{PRODUCTS_URL}9999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
@pytest.mark.django_db
class TestPostProducts:
    def test_post_product_returns_201(self, authenticate, api_client, payload):
        authenticate(is_staff=True)

        response = api_client.post(PRODUCTS_URL, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

    def test_post_product_with_invalid_data_returns_400(self, authenticate, api_client):
        authenticate(is_staff=True)

        response = api_client.post(PRODUCTS_URL, {"title": ""}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data
@pytest.mark.django_db
class TestPatchProducts:
    def test_patch_product_returns_200(self, authenticate, api_client, product):
        authenticate(is_staff=True)

        response = api_client.patch(
            f"{PRODUCTS_URL}{product.id}/",
            {"title": "Updated"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated"

    def test_patch_product_with_invalid_data_returns_400(self, authenticate, api_client, product):
        authenticate(is_staff=True)

        response = api_client.patch(
            f"{PRODUCTS_URL}{product.id}/",
            {"title": ""},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_nonexistent_product_returns_404(self, authenticate, api_client):
        authenticate(is_staff=True)

        response = api_client.patch(f"{PRODUCTS_URL}9999/", {"title": "Updated"}, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
@pytest.mark.django_db
class TestDeleteProducts:
    def test_delete_product_without_orderitems_returns_204(self, authenticate, api_client, product):
        authenticate(is_staff=True)

        response = api_client.delete(f"{PRODUCTS_URL}{product.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data in (None, {})
    @pytest.mark.django_db(transaction=True)
    def test_delete_product_with_orderitems_returns_400(self, authenticate, api_client, product, unique_customer):
        authenticate(is_staff=True)

        # Create an order linked to this customer
        order = baker.make("store.Order", customer=unique_customer)

        # Create an order item
        baker.make("store.OrderItem", product=product, order=order)

        # Attempt to delete the product
        response = api_client.delete(f"{PRODUCTS_URL}{product.id}/")

        assert response.status_code == 400
        assert response.data is not None



    def test_delete_nonexistent_product_returns_404(self, authenticate, api_client):
        authenticate(is_staff=True)

        response = api_client.delete(f"{PRODUCTS_URL}9999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

# ---------------------------
# PRODUCT IMAGES TESTS
# ---------------------------
@pytest.mark.django_db
class TestProductImages:
    def test_get_image_list_returns_200(self, api_client, product):
        baker.make(ProductImage, product=product, _quantity=2)

        response = api_client.get(f"{PRODUCTS_URL}{product.id}/images/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_get_images_for_nonexistent_product_returns_404(self, api_client):
        response = api_client.get(f"{PRODUCTS_URL}9999/images/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_image_returns_201(self, authenticate, api_client, product,data):
        authenticate(is_staff=True)

        response = api_client.post(
            f"{PRODUCTS_URL}{product.id}/images/",
            {"images": data},
            format="multipart",
        )
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "images" in response.data
        


    def test_post_image_with_invalid_data_returns_400(self, authenticate, api_client, product):
        authenticate(is_staff=True)

        response = api_client.post(
            f"{PRODUCTS_URL}{product.id}/images/",
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_image_for_nonexistent_product_returns_404(self, authenticate, api_client, data):
        authenticate(is_staff=True)

        nonexistent_product_id = 9999  # choose an ID that does not exist

        response = api_client.post(
            f"{PRODUCTS_URL}{nonexistent_product_id}/images/",
            {"images": data},
            format="multipart"
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_image_returns_204(self, authenticate, api_client, product_image):
        authenticate(is_staff=True)

        response = api_client.delete(
            f"{PRODUCTS_URL}{product_image.product.id}/images/{product_image.id}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_nonexistent_image_returns_404(self, authenticate, api_client, product):
        authenticate(is_staff=True)

        response = api_client.delete(f"{PRODUCTS_URL}{product.id}/images/9999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

# ---------------------------
# PERMISSION TESTS (PARAMETRIZED)
# ---------------------------
@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_staff, expected_status",
    [
        (True, status.HTTP_201_CREATED),
        (False, status.HTTP_403_FORBIDDEN),
        (None, status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_post_product_permissions(is_staff, expected_status, authenticate, api_client, payload):
    if is_staff is None:
        pass
    else:
        authenticate(is_staff=is_staff)

    response = api_client.post(PRODUCTS_URL, payload, format="json")
    assert response.status_code == expected_status
@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_staff, expected_status",
    [
        (True, status.HTTP_200_OK),
        (False, status.HTTP_403_FORBIDDEN),
        (None, status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_patch_product_permissions(is_staff, expected_status, authenticate, api_client, product):
    if is_staff is None:
        pass
    else:
        authenticate(is_staff=is_staff)

    response = api_client.patch(
        f"{PRODUCTS_URL}{product.id}/",
        {"title": "Updated"},
        format="json",
    )

    assert response.status_code == expected_status


@pytest.mark.django_db  
class TestDeleteProductPermissions:
    def test_admin_user_can_delete_product_returns_204(self, authenticate, api_client):
        authenticate(is_staff=True)
        product = baker.make('store.Product')

        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_non_admin_user_cannot_delete_product_returns_403(self, authenticate, api_client):
        authenticate()
        product = baker.make('store.Product')

        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_user_cannot_delete_product_returns_401(self, api_client):
        product = baker.make('store.Product')

        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

