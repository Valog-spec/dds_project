from rest_framework import serializers
from .models import Status, OperationType, Category, Subcategory, MoneyMovement


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class OperationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationType
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    operation_type_name = serializers.CharField(source='operation_type.name', read_only=True, )

    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    operation_type_name = serializers.CharField(source='category.operation_type.name', read_only=True)

    class Meta:
        model = Subcategory
        fields = '__all__'


class MoneyMovementSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True)
    operation_type_name = serializers.CharField(source='operation_type.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)

    class Meta:
        model = MoneyMovement
        fields = '__all__'

    def validate(self, data):

        required_fields = ['status', 'operation_type', 'category', 'subcategory', 'amount']
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError({
                    field: "Это поле обязательно."
                })
        if 'amount' in data and data['amount'] <= 0:
            raise serializers.ValidationError({
                "amount": "Сумма должна быть больше нуля."
            })

        if 'category' in data and 'subcategory' in data:
            if data['subcategory'].category != data['category']:
                raise serializers.ValidationError({
                    "subcategory": "Выбранная подкатегория не принадлежит выбранной категории."
                })

        if 'operation_type' in data and 'category' in data:
            if data['category'].operation_type != data['operation_type']:
                raise serializers.ValidationError({
                    "category": "Выбранная категория не принадлежит выбранному типу операции."
                })

        return data
