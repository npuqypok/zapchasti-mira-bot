from zapchastimira.repositories.part import PartDTO, part_repository
from zapchastimira.repositories.product import ProductDTO, product_repository
from typing import List, Union


def search_by_products(query: str, user_id: str) -> List[Union[PartDTO, ProductDTO]]:
    """
    Ищет товары и запчасти, соответствующие запросу пользователя.

    Эта функция выполняет поиск как по запчастям, так и по товарам, используя
    соответствующие репозитории, и возвращает объединенный список результатов.

    Args:
        query (str): Запрос для поиска (например, часть названия или артикул).
        user_id (str): Идентификатор пользователя (может использоваться в будущем для
                       персонализации результатов или логгирования).

    Returns:
        List[Union[PartDTO, ProductDTO]]: Список DTO (Data Transfer Object)
        запчастей и товаров, соответствующих поисковому запросу.
    """
    result_by_parts, _ = part_repository.get_all(query)
    result_by_products, _ = product_repository.get_all(query)

    return result_by_parts + result_by_products
