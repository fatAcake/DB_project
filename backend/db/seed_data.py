"""
Сид тестовых данных для PostgreSQL.
Заполняет все таблицы (кроме ролей и пользователей — только минимум 1 роль и 1 пользователь для связей)
минимум 5 записями. Вызывается при старте приложения, если данных ещё нет.
"""
import logging
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.sql.crud.roles_crud import get_role_by_name
from db.session import AsyncSessionLocalPostgres
from db.sql.models import (
    Roles,
    Users,
    Products,
    QuantityProducts,
    Blueprints,
    PassportsData,
    Logs,
    Transactions,
    ConfirmPassportData,
    Feedback,
)

logger = logging.getLogger("uvicorn")

# Минимум записей для проверки «уже заполнено»
SEED_MIN_COUNT = 5

# Один пользователь и одна роль для внешних ключей (не заполняем роли/пользователей по заданию)
SEED_ROLE = {"name": "user"}
SEED_USER = {
    "first_name": "Сид",
    "last_name": "Тестовый",
    "father_name": "",
    "email": "seed@test.local",
    "hash_password": "seed",
    "is_acive": True,
    "role_id": 1,
}

PRODUCTS_DATA = [
    {"description": "Антистресс кубик с вращающимися элементами", "price": 599},
    {"description": "Спиннер-звезда для концентрации", "price": 799},
    {"description": "Мяч-антистресс, приятная текстура", "price": 499},
    {"description": "Поп-ит фиджет с пузырьками", "price": 699},
    {"description": "Трансформер-куб многофункциональный", "price": 899},
]

BLUEPRINTS_DATA = [
    {"name": "Кубик антистресс", "description": "STL для 3D-печати, ~2 MB"},
    {"name": "Спиннер-звезда", "description": "STL для 3D-печати, ~1.5 MB"},
    {"name": "Поп-ит фиджет", "description": "STL для 3D-печати, ~3 MB"},
    {"name": "Мяч-антистресс", "description": "STL для 3D-печати, ~1 MB"},
    {"name": "Трансформер-куб", "description": "STL для 3D-печати, ~2.5 MB"},
]

PASSPORTS_DATA = [
    {
        "first_name": "Иван",
        "last_name": "Иванов",
        "father_name": "Иванович",
        "birth_date": datetime(1990, 5, 15),
        "place_birth": "г. Москва",
        "number_passport": "1000 100001",
        "passport_issue_date": "2015-06-20",
        "issued_by": "ОВД Москвы",
        "code_issued_by": "770-001",
        "registration": "г. Москва, ул. Ленина, 1",
        "user_id": 1,
    },
    {
        "first_name": "Мария",
        "last_name": "Петрова",
        "father_name": "Сергеевна",
        "birth_date": datetime(1988, 3, 10),
        "place_birth": "г. Санкт-Петербург",
        "number_passport": "1000 100002",
        "passport_issue_date": "2014-04-12",
        "issued_by": "ОВД СПб",
        "code_issued_by": "780-002",
        "registration": "г. Санкт-Петербург, Невский пр., 10",
        "user_id": 1,
    },
    {
        "first_name": "Алексей",
        "last_name": "Сидоров",
        "father_name": "Андреевич",
        "birth_date": datetime(1995, 11, 22),
        "place_birth": "г. Новосибирск",
        "number_passport": "1000 100003",
        "passport_issue_date": "2018-09-01",
        "issued_by": "ОВД Новосибирска",
        "code_issued_by": "540-003",
        "registration": "г. Новосибирск, ул. Красная, 5",
        "user_id": 1,
    },
    {
        "first_name": "Елена",
        "last_name": "Козлова",
        "father_name": "Дмитриевна",
        "birth_date": datetime(1992, 7, 8),
        "place_birth": "г. Казань",
        "number_passport": "1000 100004",
        "passport_issue_date": "2016-02-14",
        "issued_by": "ОВД Казани",
        "code_issued_by": "920-004",
        "registration": "г. Казань, ул. Баумана, 20",
        "user_id": 1,
    },
    {
        "first_name": "Дмитрий",
        "last_name": "Новиков",
        "father_name": "Павлович",
        "birth_date": datetime(1987, 1, 30),
        "place_birth": "г. Екатеринбург",
        "number_passport": "1000 100005",
        "passport_issue_date": "2013-11-05",
        "issued_by": "ОВД Екатеринбурга",
        "code_issued_by": "660-005",
        "registration": "г. Екатеринбург, ул. Малышева, 15",
        "user_id": 1,
    },
]

LOGS_DATA = [
    {"system": "api", "action": "GET /products", "response": "200", "user_id": 1},
    {"system": "api", "action": "POST /feedback", "response": "201", "user_id": 1},
    {"system": "api", "action": "GET /blueprints", "response": "200", "user_id": 1},
    {"system": "auth", "action": "login", "response": "200", "user_id": 1},
    {"system": "api", "action": "GET /catalog", "response": "200", "user_id": 1},
]

TRANSACTIONS_DATA = [
    {"sum": 599.0, "card_data": {"masked": "****1234", "type": "test"}, "user_id": 1},
    {"sum": 799.0, "card_data": {"masked": "****1234", "type": "test"}, "user_id": 1},
    {"sum": 499.0, "card_data": {"masked": "****5678", "type": "test"}, "user_id": 1},
    {"sum": 1298.0, "card_data": {"masked": "****5678", "type": "test"}, "user_id": 1},
    {"sum": 899.0, "card_data": {"masked": "****9012", "type": "test"}, "user_id": 1},
]

FEEDBACK_DATA = [
    {"message": "Отличные игрушки, заказ пришёл быстро!", "user_id": 1},
    {"message": "Спиннер очень понравился ребёнку.", "user_id": 1},
    {"message": "Хочу ещё кубик в другом цвете.", "user_id": 1},
    {"message": "Качество печати на высоте.", "user_id": 1},
    {"message": "Рекомендую магазин друзьям.", "user_id": 1},
]


async def _ensure_role_and_user(session: AsyncSession) -> None:
    """Создаёт роли (user, admin) и одного пользователя, если их ещё нет (для FK)."""
    role_count = await session.execute(select(Roles))
    if len(list(role_count.scalars().all())) == 0:
        session.add(Roles(**SEED_ROLE))
        await session.flush()
    # Роль admin для доступа в админ-панель (проверка по role.name == "admin")
    if await get_role_by_name(session, "admin") is None:
        session.add(Roles(name="admin"))
        await session.flush()
    user_count = await session.execute(select(Users).limit(1))
    if user_count.scalar_one_or_none() is None:
        user_data = {**SEED_USER, "role_id": 1}
        session.add(Users(**user_data))
        await session.flush()


async def _need_seed(session: AsyncSession) -> bool:
    """Проверяет, нужно ли заполнять данные (мало продуктов)."""
    r = await session.execute(select(Products).limit(SEED_MIN_COUNT))
    products = list(r.scalars().all())
    return len(products) < SEED_MIN_COUNT


async def _seed_products(session: AsyncSession) -> list[int]:
    """Добавляет продукты и quantity_products, возвращает id продуктов."""
    ids = []
    for row in PRODUCTS_DATA:
        p = Products(**row)
        session.add(p)
        await session.flush()
        ids.append(p.id)
    for i, pid in enumerate(ids):
        session.add(QuantityProducts(count=5 + i, product_id=pid))
    await session.flush()
    return ids


async def _seed_blueprints(session: AsyncSession) -> None:
    for row in BLUEPRINTS_DATA:
        session.add(Blueprints(**row))
    await session.flush()


async def _seed_passports(session: AsyncSession) -> list[int]:
    ids = []
    for row in PASSPORTS_DATA:
        pd = PassportsData(**row)
        session.add(pd)
        await session.flush()
        ids.append(pd.id)
    return ids


async def _seed_confirm_passports(session: AsyncSession, passport_ids: list[int]) -> None:
    for i, pid in enumerate(passport_ids):
        session.add(
            ConfirmPassportData(passport_data_id=pid, is_confirm=(i % 2 == 0))
        )
    await session.flush()


async def _seed_logs(session: AsyncSession) -> None:
    for row in LOGS_DATA:
        session.add(Logs(**row))
    await session.flush()


async def _seed_transactions(session: AsyncSession) -> None:
    for row in TRANSACTIONS_DATA:
        session.add(
            Transactions(
                sum=row["sum"],
                card_data=row["card_data"],
                user_id=row["user_id"],
            )
        )
    await session.flush()


async def _seed_feedback(session: AsyncSession) -> None:
    for row in FEEDBACK_DATA:
        session.add(Feedback(**row))
    await session.flush()


async def seed_db() -> None:
    """Главная точка входа: заполняет БД тестовыми данными при необходимости."""
    async with AsyncSessionLocalPostgres() as session:
        try:
            if not await _need_seed(session):
                logger.info("Сид: данные уже есть, пропуск")
                return
            await _ensure_role_and_user(session)
            await _seed_products(session)
            await _seed_blueprints(session)
            passport_ids = await _seed_passports(session)
            await _seed_confirm_passports(session, passport_ids)
            await _seed_logs(session)
            await _seed_transactions(session)
            await _seed_feedback(session)
            await session.commit()
            logger.info("Сид: тестовые данные успешно добавлены")
        except Exception as e:
            await session.rollback()
            logger.exception("Сид: ошибка заполнения данных: %s", e)
            raise
