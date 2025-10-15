import pytest
from django.urls import reverse

from dds.models import Transaction


@pytest.mark.django_db
class TestAdminPanel:
    """Тесты для Django Admin панели"""

    def test_admin_login(self, admin_client):
        """Тест доступа к админке"""
        url = reverse("admin:index")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_transaction_admin_list(self, admin_client, transaction_record):
        """Тест списка Transaction в админке"""
        url = reverse("admin:dds_transaction_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200
        assert "1000.00" in str(response.content)

    def test_transaction_admin_add(
        self,
        admin_client,
        status,
        operation_type_expense,
        category_marketing,
        subcategory_avito,
    ):
        """Тест добавления Transaction через админку"""
        url = reverse("admin:dds_transaction_add")

        # Получаем страницу добавления
        response = admin_client.get(url)
        assert response.status_code == 200

        # Данные для создания записи
        data = {
            "status": status.id,
            "operation_type": operation_type_expense.id,
            "category": category_marketing.id,
            "subcategory": subcategory_avito.id,
            "amount": 1500.00,
            "comment": "Новая рекламная кампания",
        }

        # Отправляем форму
        response = admin_client.post(url, data)
        assert response.status_code == 200

    def test_transaction_admin_change(self, admin_client, transaction_record):
        """Тест редактирования Transaction через админку"""
        url = reverse("admin:dds_transaction_change", args=[transaction_record.id])

        response = admin_client.get(url)
        assert response.status_code == 200
        assert "1000.00" in str(response.content)

    def test_transaction_admin_delete(self, admin_client, transaction_record):
        """Тест удаления Transaction через админку"""
        url = reverse("admin:dds_transaction_delete", args=[transaction_record.id])

        response = admin_client.get(url)
        assert response.status_code == 200

        # Подтверждаем удаление
        data = {"post": "yes"}
        response = admin_client.post(url, data)
        assert response.status_code == 302  # Редирект после удаления
        assert not Transaction.objects.filter(id=transaction_record.id).exists()
