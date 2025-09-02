# tools.py
from app.models.pagination import Pagination
from typing import List, Any

def paginator(
    items: List[Any] = None,
    page: int = 1,
    page_size: int = 10,
    total: int = 0
) -> Pagination:
   
    if items is None:
        items = []
    
    if total < 0:
        total = 0
    
    if page < 1:
        page = 1
    
    if page_size < 1:
        page_size = 10
    
   
    if total == 0 or page_size == 0:
        pages = 0
    else:
        pages = (total + page_size - 1) // page_size
    
    
    current_size = len(items)
    
    return Pagination(
        items=items,
        page=page,
        size=current_size,  
        pages=pages,        
        total=total         
    )