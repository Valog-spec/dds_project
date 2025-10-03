from django.contrib import admin

from .forms import MoneyMovementForm
from .models import Status, OperationType, Category, Subcategory, MoneyMovement

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1
    fields = ["name", "description"]


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    fields = ["name", "description"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("operation_type")


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]


@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "category_count"]
    search_fields = ["name"]

    inlines = [CategoryInline]

    def category_count(self, obj):
        return obj.category.count()

    category_count.short_description = "Количество категорий"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "operation_type", "description", "subcategory_count"]
    list_filter = ["operation_type"]
    search_fields = ["name"]
    inlines = [SubcategoryInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("operation_type")

    def subcategory_count(self, obj):
        return obj.subcategory.count()

    subcategory_count.short_description = 'Количество подкатегорий'


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "operation_type", "description"]
    list_filter = ["category__operation_type", "category"]
    search_fields = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category", "category__operation_type")

    def operation_type(self, obj):
        return obj.category.operation_type

    operation_type.short_description = "Тип операции"


@admin.register(MoneyMovement)
class MoneyMovementAdmin(admin.ModelAdmin):
    form = MoneyMovementForm
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
    date_hierarchy = "created_date"
    list_per_page = 20

    def comment_short(self, obj):
        return obj.comment[:48] + "..." if len(obj.comment) > 48 else obj.comment

    comment_short.short_description = "Комментарий"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "status",
            "operation_type",
            "category",
            "subcategory",
        )

    def get_changelist_form(self, request, **kwargs):
        kwargs["form"] = MoneyMovementForm
        return super().get_changelist_form(request, **kwargs)
