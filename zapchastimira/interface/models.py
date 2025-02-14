from pydantic import BaseModel


class OutputSearchDataProduct(BaseModel):
    name: str
    price: float
    stock_quantity: int
    description: str
    url: str

    def __str__(self):
        return f"""
Название товара: {self.name}
цена: {self.price}
количество {self.stock_quantity}
описание: {self.description}
ссылка: {self.url}
"""


class OutputSearchDataPart(BaseModel):
    name: str
    brand: str
    part_number: str
    price: float
    stock_quantity: int
    description: str
    url: str
    compatibility: str

    def __str__(self):
        return f"""
Название товара: {self.name}
цена: {self.price}
номер запчасти: {self.part_number}
бренд: {self.brand}
совместимость: {self.compatibility}
количество {self.stock_quantity}
описание: {self.description}
ссылка: {self.url}
"""
