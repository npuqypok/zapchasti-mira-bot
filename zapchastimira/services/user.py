from zapchastimira.repositories.user import user_repository, UserDTO


def create_user(tg_uid: str, phone: str) -> UserDTO:
    user = user_repository.get_user_by_phone(phone)
    if user is None:
        tmp = UserDTO(tg_uid=tg_uid, phone=phone)
        user_repository.create(tmp)
        user = user_repository.get_user_by_phone(phone)
    return user


def update_user(
    user_id: str, phone: str | None = None, tg_uid: str | None = None
) -> None:
    """Обновление данных пользователя."""
    user_dto = UserDTO(phone=phone, tg_uid=tg_uid)
    user_repository.update(user_id, user_dto)


def delete_user(user_id: str) -> None:
    """Удаление пользователя."""
    user_repository.delete(user_id)


def get_user_by_id(user_id: str) -> UserDTO | None:
    """Получение информации о пользователе по ID."""
    return user_repository.get_by_id(user_id)
