import pytest

from dds.models import Transaction


@pytest.mark.django_db
class TestModels:
    """Тесты моделей"""

    def test_status_creation(self, status):
        """Тест создания статуса"""
        assert status.name == "Бизнес"
        assert str(status) == "Бизнес"

    def test_operation_type_creation(self, operation_type_expense):
        """Тест создания типа операции"""
        assert operation_type_expense.name == "Списание"
        assert str(operation_type_expense) == "Списание"

    def test_category_creation(self, category_marketing):
        """Тест создания категории"""
        assert category_marketing.name == "Маркетинг"
        assert category_marketing.operation_type.name == "Списание"
        assert str(category_marketing) == "Маркетинг"

    def test_subcategory_creation(self, subcategory_avito):
        """Тест создания подкатегории"""
        assert subcategory_avito.name == "Avito"
        assert subcategory_avito.category.name == "Маркетинг"
        assert str(subcategory_avito) == "Avito"

    def test_transaction_creation(self, transaction_record):
        """Тест создания записи ДДС"""
        assert transaction_record.amount == 1000.00
        assert transaction_record.status.name == "Бизнес"
        assert transaction_record.operation_type.name == "Списание"
        assert transaction_record.category.name == "Маркетинг"
        assert transaction_record.subcategory.name == "Avito"
        assert transaction_record.comment == "Рекламная кампания"

    def test_transaction_required_fields(self):
        """Тест обязательных полей Транзакции"""
        with pytest.raises(Exception):
            Transaction.objects.create(
                # Пропущены обязательные поля
                amount=1000.00
            )
