import django_filters

from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    created_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Transaction
        fields = {
            "status": ["exact"],
            "operation_type": ["exact"],
            "category": ["exact"],
            "subcategory": ["exact"],
        }
