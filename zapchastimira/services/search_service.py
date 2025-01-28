from zapchastimira.repositories.part import PartDTO, part_repository
from zapchastimira.repositories.product import ProductDTO, product_repository


def search_by_products(query: str, user_id: str) -> list[PartDTO | ProductDTO]:
    result_by_parts, _ = part_repository.get_all(query)
    result_by_products, _ = product_repository.get_all(query)

    return result_by_parts + result_by_products

