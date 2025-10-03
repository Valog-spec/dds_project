from django.contrib import admin

from .forms import MoneyMovementForm
from .models import Status, OperationType, Category, Subcategory, MoneyMovement


class SubcategoryInline(admin.TabularInline):
    """
    Inline для отображения подкатегорий внутри категории
    Позволяет управлять подкатегориями прямо из формы категории
    """
    model = Subcategory
    extra = 1
    fields = ["name", "description"]


class CategoryInline(admin.TabularInline):
    """
    Inline для отображения категорий внутри типа операции
    Позволяет управлять категориями прямо из формы типа операции
    """
    model = Category
    extra = 1
    fields = ["name", "description"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("operation_type")


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """
    Админка для управления статусами операций
    """
    list_display = ["name", "description"]
    search_fields = ["name"]


@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    """
    Админка для управления типами операций
    """
    list_display = ["name", "description", "category_count"]
    search_fields = ["name"]

    inlines = [CategoryInline]  # Inline для управления категориями

    def category_count(self, obj):
        return obj.category.count()

    category_count.short_description = "Количество категорий"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админка для управления категориями
    """
    list_display = ["name", "operation_type", "description", "subcategory_count"]
    list_filter = ["operation_type"]
    search_fields = ["name"]
    inlines = [SubcategoryInline]  # Inline для управления подкатегориями

    def get_queryset(self, request):
        """Оптимизация запроса с select_related"""
        return super().get_queryset(request).select_related("operation_type")

    def subcategory_count(self, obj):
        """Отображение количества подкатегорий для категории"""
        return obj.subcategory.count()

    subcategory_count.short_description = 'Количество подкатегорий'


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """
    Админка для управления подкатегориями
    """
    list_display = ["name", "category", "operation_type", "description"]
    list_filter = ["category__operation_type", "category"]
    search_fields = ['name']

    def get_queryset(self, request):
        """Оптимизация запроса с select_related"""
        return super().get_queryset(request).select_related("category", "category__operation_type")

    def operation_type(self, obj):
        """Отображение типа операции через категорию"""
        return obj.category.operation_type

    operation_type.short_description = "Тип операции"


@admin.register(MoneyMovement)
class MoneyMovementAdmin(admin.ModelAdmin):
    """
    Админка для управления движениями денежных средств
    """
    form = MoneyMovementForm  # Кастомная форма с autocomplete
    list_display = [
        "created_date",
        "status",
        "operation_type",
        "category",
        "subcategory",
        "amount",
        "comment_short"
    ]
    list_filter = [
        "created_date",
        "status",
        "operation_type",
        "category",
        "subcategory"
    ]
    search_fields = ["comment", "subcategory__name", "category__name"]
    date_hierarchy = "created_date" # Иерархическая навигация по датам
    list_per_page = 20 # Пагинация

    def comment_short(self, obj):
        """Сокращенное отображение комментария в списке"""
        return obj.comment[:48] + "..." if len(obj.comment) > 48 else obj.comment

    comment_short.short_description = "Комментарий"

    def get_queryset(self, request):
        """Оптимизация запроса с select_related"""
        return super().get_queryset(request).select_related(
            "status",
            "operation_type",
            "category",
            "subcategory",
        )

    def get_changelist_form(self, request, **kwargs):
        """ Переопределение метода для использования кастомной формы в changelist"""
        kwargs["form"] = MoneyMovementForm
        return super().get_changelist_form(request, **kwargs)
