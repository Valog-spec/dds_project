from django import forms

from .models import MoneyMovement
from dal import autocomplete


class MoneyMovementForm(forms.ModelForm):
    """
    Кастомная форма для MoneyMovement с autocomplete полями
    Обеспечивает динамическую фильтрацию категорий и подкатегорий
    """
    class Meta:
        model = MoneyMovement
        fields = '__all__'
        widgets = {
            # Autocomplete для категории с фильтрацией по типу операции
            'category': autocomplete.ModelSelect2(
                url='category-autocomplete',
                forward=['operation_type'],  # Передача типа операции для фильтрации
                attrs={
                    'data-placeholder': 'Сначала выберите тип операции...',
                    'data-minimum-input-length': 0, # Показывать варианты сразу без ввода
                    'style': 'min-width: 400px;', # Единообразная ширина полей
                    'required': 'required',  # HTML валидация - обязательное поле
                }
            ),
            # Autocomplete для подкатегории с фильтрацией по категории
            'subcategory': autocomplete.ModelSelect2(
                url='subcategory-autocomplete',
                forward=['category'],  # Передача категории для фильтрации
                attrs={
                    'data-placeholder': 'Сначала выберите категорию...',
                    'data-minimum-input-length': 0,
                    'style': 'min-width: 400px;',
                    'required': 'required',
                }
            ),
            'amount': forms.NumberInput(attrs={
                'required': 'required',
                'min': '0.01',  # HTML валидация - минимальное значение
                'step': '0.01',  # Шаг изменения значения
                'placeholder': '0.00'  # Подсказка в поле
            }),
            'operation_type': forms.Select(attrs={
                'required': 'required',
            }),
            'status': forms.Select(attrs={
                'required': 'required',
            }),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Необязательный комментарий...' # Указываем что поле необязательное
            }),
        }

