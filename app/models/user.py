from sqlalchemy import  String, Integer
from app.db.database import Base
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class User(Base):

    __tablename__ = "users"
    __table_args__ = {'schema': 'public', 'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(String(50), nullable=False,  default=datetime.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(String(50), nullable=False,  default=datetime.now())
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True, nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=False)
    city: Mapped[Optional[str]] = mapped_column(String(50), nullable=False)
    is_deleted: Mapped[Optional[bool]] = mapped_column(nullable=False, default=False)

