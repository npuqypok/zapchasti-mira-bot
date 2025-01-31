from zapchastimira.repositories.user import user_repository, UserDTO
from typing import Optional


def create_user(tg_uid: str, phone: str) -> UserDTO:
    """
    Создает нового пользователя или возвращает существующего.

    Эта функция проверяет, существует ли пользователь с указанным номером телефона.
    Если пользователь не существует, функция создает нового пользователя с указанным
    Telegram ID и номером телефона. Если пользователь существует, функция возвращает
    существующего пользователя.

    Args:
        tg_uid (str): Telegram ID пользователя.
        phone (str): Номер телефона пользователя.

    Returns:
        UserDTO: Объект DTO пользователя.
    """
    user = user_repository.get_user_by_phone(phone)
    if user is None:
        tmp = UserDTO(tg_uid=tg_uid, phone=phone)
        user_repository.create(tmp)
        user = user_repository.get_user_by_phone(phone)
    return user


def update_user(
    user_id: str, phone: Optional[str] = None, tg_uid: Optional[str] = None
) -> None:
    """
    Обновляет данные пользователя.

    Эта функция обновляет данные пользователя с указанным ID. Можно обновить
    номер телефона и/или Telegram ID.

    Args:
        user_id (str): ID пользователя для обновления.
        phone (Optional[str]): Новый номер телефона пользователя (необязательно).
        tg_uid (Optional[str]): Новый Telegram ID пользователя (необязательно).
    """
    user_dto = UserDTO(phone=phone, tg_uid=tg_uid)
    user_repository.update(user_id, user_dto)


def delete_user(user_id: str) -> None:
    """
    Удаляет пользователя по ID.

    Args:
        user_id (str): ID пользователя для удаления.
    """
    user_repository.delete(user_id)


def get_user_by_id(user_id: str) -> Optional[UserDTO]:
    """
    Получает информацию о пользователе по ID.

    Args:
        user_id (str): ID пользователя.

    Returns:
        Optional[UserDTO]: Объект DTO пользователя, если найден, иначе None.
    """
    return user_repository.get_by_id(user_id)
