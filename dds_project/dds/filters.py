import django_filters
from .models import MoneyMovement


class MoneyMovementFilter(django_filters.FilterSet):
    created_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = MoneyMovement
        fields = {
            'status': ['exact'],
            'operation_type': ['exact'],
            'category': ['exact'],
            'subcategory': ['exact'],
        }
