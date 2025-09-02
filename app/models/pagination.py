from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar('T')  

class Pagination(BaseModel, Generic[T]):
    """Apresentação Objeto Paginado"""
    items: List[T] = None
    page: int = 0
    size: int = 0
    pages: int = 0
    total: int = 0
