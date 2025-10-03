from django import forms

from .models import MoneyMovement
from dal import autocomplete


class MoneyMovementForm(forms.ModelForm):
    class Meta:
        model = MoneyMovement
        fields = '__all__'
        widgets = {
            'category': autocomplete.ModelSelect2(
                url='category-autocomplete',
                forward=['operation_type'],
                attrs={
                    'data-placeholder': 'Сначала выберите тип операции...',
                    'data-minimum-input-length': 0,
                    'style': 'min-width: 400px;',
                    'required': 'required',
                }
            ),
            'subcategory': autocomplete.ModelSelect2(
                url='subcategory-autocomplete',
                forward=['category'],
                attrs={
                    'data-placeholder': 'Сначала выберите категорию...',
                    'data-minimum-input-length': 0,
                    'style': 'min-width: 400px;',
                    'required': 'required',
                }
            ),
            'amount': forms.NumberInput(attrs={
                'required': 'required',
                'min': '0.01',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'operation_type': forms.Select(attrs={
                'required': 'required',
            }),
            'status': forms.Select(attrs={
                'required': 'required',
            }),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Необязательный комментарий...'
            }),
        }

