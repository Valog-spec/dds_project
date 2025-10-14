from dal import autocomplete
from .models import Category, Subcategory


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    """Autocomplete view для категорий с фильтрацией по типу операции"""

    def get_queryset(self):
        """Основной метод для фильтрации категорий"""
        # Начинаем с полного queryset всех категорий
        qs = Category.objects.all()

        # Получаем ID выбранного типа операции из forwarded параметров
        operation_type = self.forwarded.get('operation_type', None)

        if operation_type:
            # Если тип операции выбран - фильтруем категории по этому типу
            qs = qs.filter(operation_type_id=operation_type)
        else:
            # Если тип операции не выбран - возвращаем пустой queryset
            return Category.objects.none()

        if self.q:
            # Дополнительная фильтрация по поисковому запросу (если пользователь что-то ввел)
            qs = qs.filter(name__icontains=self.q)
        return qs


class SubcategoryAutocomplete(autocomplete.Select2QuerySetView):
    """Основной метод для фильтрации подкатегорий"""
    def get_queryset(self):
        # Начинаем с полного queryset всех подкатегорий
        qs = Subcategory.objects.all()

        # Получаем ID выбранной категории из forwarded параметров
        category = self.forwarded.get('category', None)

        if category:
            # Если категория выбрана - фильтруем подкатегории по этой категории
            qs = qs.filter(category_id=category)
        else:
            # Если категория не выбрана - возвращаем пустой queryset
            return Subcategory.objects.none()

        # Дополнительная фильтрация по поисковому запросу (если пользователь что-то ввел)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
