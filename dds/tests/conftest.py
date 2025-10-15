import pytest
from django.contrib.auth.models import User
from faker import Faker

from dds.models import Category, OperationType, Status, Subcategory, Transaction


@pytest.fixture
def admin_user():
    """Создает суперпользователя для тестов админки"""
    return User.objects.create_superuser(
        username="admin", password="adminpassword", email="admin@example.com"
    )


@pytest.fixture
def admin_client(admin_user):
    """Клиент для тестирования админки"""
    from django.test import Client

    client = Client()
    client.force_login(admin_user)
    return client


@pytest.fixture
def status():
    return Status.objects.create(name="Бизнес")


@pytest.fixture
def operation_type_expense():
    return OperationType.objects.create(name="Списание")


@pytest.fixture
def operation_type_income():
    return OperationType.objects.create(name="Пополнение")


@pytest.fixture
def category_marketing(operation_type_expense):
    return Category.objects.create(
        name="Маркетинг", operation_type=operation_type_expense
    )


@pytest.fixture
def subcategory_avito(category_marketing):
    return Subcategory.objects.create(name="Avito", category=category_marketing)


@pytest.fixture
def transaction_record(
    status, operation_type_expense, category_marketing, subcategory_avito
):
    return Transaction.objects.create(
        created_date="2024-01-15",
        status=status,
        operation_type=operation_type_expense,
        category=category_marketing,
        subcategory=subcategory_avito,
        amount=1000.00,
        comment="Рекламная кампания",
    )
