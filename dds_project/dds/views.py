from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Status, OperationType, Category, Subcategory, MoneyMovement
from .responses import BAD_REQUEST_RESPONSE, MONEY_MOVEMENT_BAD_REQUEST, NOT_FOUND_RESPONSE
from .serializers import (
    StatusSerializer,
    OperationTypeSerializer,
    CategorySerializer,
    SubcategorySerializer,
    MoneyMovementSerializer
)
from .filters import MoneyMovementFilter


@extend_schema_view(
    list=extend_schema(
        summary="Получить список статусов",
        description="Возвращает список всех доступных статусов операций",
        responses={
            200: StatusSerializer(many=True),
        },
        tags=['statuses']
    ),
    create=extend_schema(
        summary="Создать новый статус",
        description="Создает новый статус для операций",
        responses={
            201: StatusSerializer,
            400: BAD_REQUEST_RESPONSE,
        },
        tags=['statuses']
    ),
    retrieve=extend_schema(
        summary="Получить статус по ID",
        description="Возвращает детальную информацию о статусе",
        responses={
            200: StatusSerializer,
            404: NOT_FOUND_RESPONSE,
        },
        tags=['statuses']
    ),
    update=extend_schema(
        summary="Обновить статус",
        description="Полностью обновляет информацию о статусе",
        responses={
            200: StatusSerializer,
            400: BAD_REQUEST_RESPONSE,
            404: NOT_FOUND_RESPONSE,
        },
        tags=['statuses']
    ),
    partial_update=extend_schema(
        summary="Частично обновить статус",
        description="Частично обновляет информацию о статусе",
        responses={
            200: StatusSerializer,
            400: BAD_REQUEST_RESPONSE,
            404: NOT_FOUND_RESPONSE,
        },
        tags=['statuses']
    ),
    destroy=extend_schema(
        summary="Удалить статус",
        description="Удаляет статус из системы",
        responses={
            204: OpenApiResponse(description="Удалено успешно"),
            404: NOT_FOUND_RESPONSE,
        },
        tags=['statuses']
    ),
)
class StatusViewSet(viewsets.ModelViewSet):
    """CRUD API для управления статусами операций"""
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


@extend_schema_view(
    list=extend_schema(
        summary="Получить список типов операций",
        description="Возвращает список всех типов операций (Пополнение, Списание)",
        responses={
            200: OperationTypeSerializer(many=True),
        },
        tags=['operation_types']
    ),
    create=extend_schema(
        summary="Создать новый тип операции",
        description="Создает новый тип операции",
        responses={
            201: OperationTypeSerializer,
            400: BAD_REQUEST_RESPONSE,
        },
        tags=['operation_types']
    ),
    retrieve=extend_schema(
        summary="Получить тип операции по ID",
        description="Возвращает детальную информацию о типе операции",
        responses={
            200: OperationTypeSerializer,
            404: NOT_FOUND_RESPONSE,
        },
        tags=['operation_types']
    ),
    update=extend_schema(
        summary="Обновить тип операции",
        description="Полностью обновляет информацию о типе операции",
        responses={
            200: OperationTypeSerializer,
            400: BAD_REQUEST_RESPONSE,
            404: NOT_FOUND_RESPONSE,
        },
        tags=['operation_types']
    ),
    destroy=extend_schema(
        summary="Удалить тип операции",
        description="Удаляет тип операции из системы",
        responses={
            204: OpenApiResponse(description="Удалено успешно"),
            404: NOT_FOUND_RESPONSE,
        },
        tags=['operation_types']
    ),
)
class OperationTypeViewSet(viewsets.ModelViewSet):
    """CRUD API для управления типами операций"""
    queryset = OperationType.objects.all()
    serializer_class = OperationTypeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    http_method_names = ['get', 'post', 'put', 'delete', ]


@extend_schema_view(
    list=extend_schema(
        summary="Получить список категорий",
        description="Возвращает список категорий с фильтрацией по типу операции",
        parameters=[
            OpenApiParameter(
                name='operation_type',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Фильтр по типу операции'
            ),
        ],
        responses={
            200: CategorySerializer(many=True),
        },
        tags=['categories']
    ),
    create=extend_schema(
        summary="Создать новую категорию",
        description="Создает новую категорию, привязанную к типу операции",
        responses={
            201: CategorySerializer,
            400: BAD_REQUEST_RESPONSE,
        },
        examples=[
            OpenApiExample(
                "Пример успешного запроса",
                value={
                    "name": "Новая категория",
                    "operation_type": 1,
                    "description": "Описание категории"
                },
                status_codes=['201']
            ),
            OpenApiExample(
                "Пример ошибки",
                value={
                    "name": ["category с такими name и operation_type уже существует."],
                    "operation_type": ["Обязательное поле."]
                },
                status_codes=['400']
            )
        ],
        tags=['categories']
    ),
    retrieve=extend_schema(
        summary="Получить категорию по ID",
        description="Возвращает детальную информацию о категории",
        responses={
            200: CategorySerializer,
            404: NOT_FOUND_RESPONSE,
        },
        tags=['categories']
    ),
    update=extend_schema(
        summary="Обновить категорию",
        description="Полностью обновляет информацию о категории",
        responses={
            200: CategorySerializer,
            400: BAD_REQUEST_RESPONSE,
            404: NOT_FOUND_RESPONSE,
        },
        tags=['categories']
    ),
    destroy=extend_schema(
        summary="Удалить категорию",
        description="Удаляет категорию из системы",
        responses={
            204: OpenApiResponse(description="Удалено успешно"),
            404: NOT_FOUND_RESPONSE,
        },
        tags=['categories']
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD API для управления категориями операций"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['operation_type']
    search_fields = ['name']
    http_method_names = ['get', 'post', 'put', 'delete', ]


@extend_schema_view(
    list=extend_schema(
        summary="Получить список подкатегорий",
        description="Возвращает список подкатегорий с фильтрацией по категории и типу операции",
        parameters=[
            OpenApiParameter(
                name='category',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Фильтр по категории'
            ),
            OpenApiParameter(
                name='category__operation_type',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Фильтр по типу операции через категорию'
            )
        ],
        responses={
            200: SubcategorySerializer(many=True),
        },
        tags=['sybcategories']
    ),
    create=extend_schema(
        summary="Создать новую подкатегорию",
        description="Создает новую подкатегорию, привязанную к категории",
        responses={
            201: SubcategorySerializer,
            400: BAD_REQUEST_RESPONSE,
        },
        tags=['sybcategories']
    ),
    retrieve=extend_schema(
        summary="Получить подкатегорию по ID",
        description="Возвращает детальную информацию о подкатегории",
        responses={
            200: SubcategorySerializer,
            404: NOT_FOUND_RESPONSE,
        },
        tags=['sybcategories']
    ),
    update=extend_schema(
        summary="Обновить подкатегорию",
        description="Полностью обновляет информацию о подкатегории",
        responses={
            200: SubcategorySerializer,
            400: BAD_REQUEST_RESPONSE,
            404: NOT_FOUND_RESPONSE,
        },
        tags=['sybcategories']
    ),
    destroy=extend_schema(
        summary="Удалить подкатегорию",
        description="Удаляет подкатегорию из системы",
        responses={
            204: OpenApiResponse(description="Удалено успешно"),
            404: NOT_FOUND_RESPONSE,
        },
        tags=['sybcategories']
    ),
)
class SubcategoryViewSet(viewsets.ModelViewSet):
    """CRUD API для управления подкатегориями операций"""
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'category__operation_type']
    search_fields = ['name']
    http_method_names = ['get', 'post', 'put', 'delete', ]


@extend_schema_view(
    list=extend_schema(
        summary="Получить список операций ДДС",
        description="Возвращает список операций движения денежных средств с поддержкой фильтрации, поиска и сортировки",
        parameters=[
            OpenApiParameter(
                name='created_date_after',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Фильтр по дате начала периода (YYYY-MM-DD)'
            ),
            OpenApiParameter(
                name='created_date_before',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Фильтр по дате окончания периода (YYYY-MM-DD)'
            ),
            OpenApiParameter(
                name='status',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Фильтр по статусу'
            ),
            OpenApiParameter(
                name='operation_type',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Фильтр по типу операции'
            ),
            OpenApiParameter(
                name='category',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Фильтр по категории'
            ),
            OpenApiParameter(
                name='subcategory',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Фильтр по подкатегории'
            ),
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Поиск по комментарию и названиям категорий/подкатегорий'
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Сортировка (-created_date, created_date, amount, -amount)'
            ),
        ],
        responses={
            200: MoneyMovementSerializer(many=True),
            400: BAD_REQUEST_RESPONSE,
        },
        examples=[
            OpenApiExample(
                'Пример успешного ответа',
                value={
                    "count": 150,
                    "next": "http://localhost:8000/api/money-movements/?page=2",
                    "previous": None,
                    "results": [
                        {
                            "id": 1,
                            "created_date": "2024-01-15T10:30:00Z",
                            "status": 1,
                            "status_name": "Бизнес",
                            "operation_type": 2,
                            "operation_type_name": "Списание",
                            "category": 3,
                            "category_name": "Маркетинг",
                            "subcategory": 5,
                            "subcategory_name": "Avito",
                            "amount": "1500.00",
                            "comment": "Оплата рекламы"
                        }
                    ]
                },
                status_codes=['200']
            )
        ],
        tags=['money-movements']
    ),
    create=extend_schema(
        summary="Создать новую операцию ДДС",
        description="Создает новую запись о движении денежных средств с проверкой бизнес-правил",
        responses={
            201: MoneyMovementSerializer,
            400: MONEY_MOVEMENT_BAD_REQUEST,
        },
        examples=[
            OpenApiExample(
                "Пример успешного запроса",
                value={
                    "status": 1,
                    "operation_type": 2,
                    "category": 3,
                    "subcategory": 5,
                    "amount": "1500.00",
                    "comment": "Оплата рекламы в Avito"
                },
                status_codes=['201']
            ),
            OpenApiExample(
                "Пример ошибки валидации",
                value={
                    "amount": ["Сумма должна быть больше нуля."],
                    "category": ["Это поле обязательно."],
                    "subcategory": ["Подкатегория не принадлежит выбранной категории."]
                },
                status_codes=['400']
            )
        ],
        tags=['money-movements']
    ),
    retrieve=extend_schema(
        summary="Получить операцию ДДС по ID",
        description="Возвращает детальную информацию об операции движения денежных средств",
        responses={
            200: MoneyMovementSerializer,
            404: NOT_FOUND_RESPONSE,
        },
        tags=['money-movements']
    ),
    update=extend_schema(
        summary="Обновить операцию ДДС",
        description="Полностью обновляет информацию об операции движения денежных средств",
        responses={
            200: MoneyMovementSerializer,
            400: MONEY_MOVEMENT_BAD_REQUEST,
            404: NOT_FOUND_RESPONSE,
        },
        tags=['money-movements']
    ),
    partial_update=extend_schema(
        summary="Частично обновить операцию ДДС",
        description="Частично обновляет информацию об операции движения денежных средств",
        responses={
            200: MoneyMovementSerializer,
            400: MONEY_MOVEMENT_BAD_REQUEST,
            404: NOT_FOUND_RESPONSE,
        },
        tags=['money-movements']
    ),
    destroy=extend_schema(
        summary="Удалить операцию ДДС",
        description="Удаляет запись о движении денежных средств",
        responses={
            204: OpenApiResponse(description="Удалено успешно"),
            404: NOT_FOUND_RESPONSE,
        },
        tags=['money-movements']
    ),
)
class MoneyMovementViewSet(viewsets.ModelViewSet):
    """
    API для управления операциями движения денежных средств (ДДС)

    Позволяет вести учет всех денежных операций с учетом бизнес-правил.
    """
    queryset = MoneyMovement.objects.all()
    serializer_class = MoneyMovementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MoneyMovementFilter
    search_fields = ['comment', 'subcategory__name', 'category__name']
    ordering_fields = ['created_date', 'amount']
    ordering = ['-created_date']
