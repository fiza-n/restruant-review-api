from datetime import datetime, UTC
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Integer, String , Text
from sqlalchemy.orm import Mapped,mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from restaurants import Restaurants
    from reviews import Reviews


class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username:Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email:Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    image_file:Mapped[str|None] = mapped_column(String(200), default=False,nullable=True)
    password:Mapped[str] = mapped_column(String(200), nullable=False)

    restaurants:Mapped[list["Restaurants"]] = relationship("Restaurants", back_populates="owner")
    reviews:Mapped[list["Reviews"]] = relationship("Reviews", back_populates="user")

    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.png"