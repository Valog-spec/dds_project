from dal import autocomplete

from .models import Category, Subcategory


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    """Autocomplete view для категорий с фильтрацией по типу операции"""

    def get_queryset(self):
        """Основной метод для фильтрации категорий"""
        qs = Category.objects.all()

        # Получаем ID выбранного типа операции из forwarded параметров
        operation_type = self.forwarded.get("operation_type", None)

        if operation_type:
            qs = qs.filter(operation_type_id=operation_type)
        else:
            return Category.objects.none()

        if self.q:
            # Дополнительная фильтрация по поисковому запросу (если пользователь что-то ввел)
            qs = qs.filter(name__icontains=self.q)
        return qs


class SubcategoryAutocomplete(autocomplete.Select2QuerySetView):
    """Основной метод для фильтрации подкатегорий"""

    def get_queryset(self):
        qs = Subcategory.objects.all()

        # Получаем ID выбранной категории из forwarded параметров
        category = self.forwarded.get("category", None)

        if category:
            qs = qs.filter(category_id=category)
        else:
            return Subcategory.objects.none()

        # Дополнительная фильтрация по поисковому запросу (если пользователь что-то ввел)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
