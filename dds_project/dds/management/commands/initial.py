from django.core.management.base import BaseCommand
from dds.models import Status, OperationType, Category, Subcategory


class Command(BaseCommand):
    help = 'Загрузка начальных данных для системы ДДС'

    def handle(self, *args, **kwargs):
        self.stdout.write('Загрузка начальных данных...')

        statuses = [
            {'name': 'Бизнес', 'description': 'Бизнес операции'},
            {'name': 'Личное', 'description': 'Личные финансы'},
            {'name': 'Налог', 'description': 'Налоговые операции'},
        ]

        for status_data in statuses:
            status, created = Status.objects.get_or_create(**status_data)
            if created:
                self.stdout.write(f'Создан статус: {status.name}')

        operation_types = [
            {'name': 'Пополнение', 'description': 'Поступление денежных средств'},
            {'name': 'Списание', 'description': 'Расход денежных средств'},
        ]

        for op_type_data in operation_types:
            op_type, created = OperationType.objects.get_or_create(**op_type_data)
            if created:
                self.stdout.write(f'Создан тип операции: {op_type.name}')

        categories_data = [
            {
                'name': 'Маркетинг',
                'operation_type': 'Списание',
                'subcategories': ['Avito', 'Farpost', 'Яндекс.Директ']
            },
            {
                'name': 'Инфраструктура',
                'operation_type': 'Списание',
                'subcategories': ['VPS', 'Proxy', 'Домены']
            },
            {
                'name': 'Зарплата',
                'operation_type': 'Пополнение',
                'subcategories': ['Аванс', 'Основная зарплата', 'Премия']
            },
        ]

        for cat_data in categories_data:
            op_type = OperationType.objects.get(name=cat_data['operation_type'])
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                operation_type=op_type
            )
            if created:
                self.stdout.write(f'Создана категория: {category.name}')

            for subcat_name in cat_data['subcategories']:
                subcategory, created = Subcategory.objects.get_or_create(
                    name=subcat_name,
                    category=category
                )
                if created:
                    self.stdout.write(f'Создана подкатегория: {subcategory.name}')

        self.stdout.write(
            self.style.SUCCESS('✅ Начальные данные успешно загружены!')
        )