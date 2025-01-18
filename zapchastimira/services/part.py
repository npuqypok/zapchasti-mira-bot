from sqlalchemy.orm import Session
from zapchastimira.repositories.part import (
    part_repository,
    PartDTO,
)  # Импортируем репозиторий и DTO
from zapchastimira.common import (
    tables,
)  # Импортируем таблицы для использования в запросах


def search_parts_service(session: Session, query: str):
    """
    Ищет запасные части по заданному запросу.

    :param session: Сессия базы данных.
    :param query: Строка запроса для поиска.
    :return: Список найденных запасных частей.
    """
    return (
        session.query(tables.Part)
        .filter(  # Используем tables.Part вместо Part
            tables.Part.name.ilike(f"%{query}%")
            | tables.Part.part_number.ilike(f"%{query}%")
            | tables.Part.brand.ilike(f"%{query}%")
        )
        .all()
    )


def search_parts(query: str, session: Session) -> list[PartDTO]:
    """
    Ищет запасные части по заданному запросу.

    :param query: Строка запроса для поиска.
    :param session: Сессия базы данных.
    :return: Список найденных запасных частей в формате PartDTO.
    """
    parts = search_parts_service(
        session, query
    )  # Используем локальную функцию для поиска
    return [
        PartDTO(
            part_id=part.part_id,
            name=part.name,
            brand=part.brand,
            description=part.description,
            compatibility=part.compatibility,
            price=part.price,
            stock_quantity=part.stock_quantity,
            image_url=part.image_url,
        )
        for part in parts
    ]  # Преобразуем в DTO


# Пример использования функции
if __name__ == "__main__":
    from zapchastimira.common.db_utils import (
        get_db,
    )  # Импортируем функцию для получения сессии

    # Получаем сессию базы данных
    with get_db() as session:
        result = search_parts("пример запроса", session)
        for part in result:
            print(
                part.to_dict()
            )  # Используем метод to_dict() для вывода информации о запчасти
