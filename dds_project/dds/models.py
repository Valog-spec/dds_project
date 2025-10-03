from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название статуса")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class OperationType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Тип операции")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    operation_type = models.ForeignKey(OperationType, on_delete=models.CASCADE, verbose_name="Тип операции",
                                       related_name="category")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ['name', 'operation_type']

    def __str__(self):
        return f"{self.name} ({self.operation_type})"


class Subcategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название подкатегории")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория",
                                 related_name="subcategory")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        unique_together = ['name', 'category']

    def __str__(self):
        return f"{self.name} ({self.category})"


class MoneyMovement(models.Model):
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата создания",
                                        null=False,
                                        blank=False
                                        )
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус",
                               null=False,
                               blank=False
                               )
    operation_type = models.ForeignKey(OperationType, on_delete=models.PROTECT, verbose_name="Тип операции",
                                       null=False,
                                       blank=False
                                       )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория",
                                 null=False,
                                 blank=False
                                 )
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, verbose_name="Подкатегория",
                                    null=False,
                                    blank=False
                                    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Сумма",
        null=False,
        blank=False
    )
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Движение денежных средств"
        verbose_name_plural = "Движения денежных средств"
        ordering = ['-created_date']

    def clean(self):

        if hasattr(self, 'category') and self.category and hasattr(self, 'operation_type') and self.operation_type:
            if self.category.operation_type != self.operation_type:
                raise ValidationError({
                    'category': 'Категория должна принадлежать выбранному типу операции.'
                })

        if hasattr(self, 'subcategory') and self.subcategory and hasattr(self, 'category') and self.category:
            if self.subcategory.category != self.category:
                raise ValidationError({
                    'subcategory': 'Подкатегория должна принадлежать выбранной категории.'
                })

    def save(self, *args, **kwargs):

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.created_date.strftime('%d.%m.%Y')} - {self.amount} руб. - {self.status}"
