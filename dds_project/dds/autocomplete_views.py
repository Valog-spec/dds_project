from dal import autocomplete
from .models import Category, Subcategory


class CategoryAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Category.objects.all()

        operation_type = self.forwarded.get('operation_type', None)

        if operation_type:
            qs = qs.filter(operation_type_id=operation_type)
        else:
            return Category.objects.none()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class SubcategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Subcategory.objects.all()

        category = self.forwarded.get('category', None)

        if category:
            qs = qs.filter(category_id=category)
        else:
            return Subcategory.objects.none()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
