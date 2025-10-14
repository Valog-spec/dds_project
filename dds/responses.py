from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, OpenApiExample


# Общие ответы для ошибок API
BAD_REQUEST_RESPONSE = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    description="Некорректный запрос - ошибки валидации",
    examples=[
        OpenApiExample(
            "Пример ошибки валидации",
            value={
                "amount": ["Сумма должна быть больше нуля."],
                "category": ["Это поле обязательно."]
            },
            status_codes=['400']
        )
    ]
)

NOT_FOUND_RESPONSE = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    description="Объект не найден",
    examples=[
        OpenApiExample(
            "Объект не найден",
            value={
                "detail": "Страница не найдена."
            },
            status_codes=['404']
        )
    ]
)

MONEY_MOVEMENT_BAD_REQUEST = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    description="Некорректный запрос - ошибки валидации бизнес-правил",
    examples=[
        OpenApiExample(
            "Ошибка обязательных полей",
            value={
                "status": ["Это поле обязательно."],
                "amount": ["Это поле обязательно."]
            },
            status_codes=['400']
        ),
        OpenApiExample(
            "Ошибка бизнес-правил",
            value={
                "amount": ["Сумма должна быть больше нуля."],
                "category": ["Категория не принадлежит выбранному типу операции."],
                "subcategory": ["Подкатегория не принадлежит выбранной категории."]
            },
            status_codes=['400']
        )
    ]
)
