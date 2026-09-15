from datetime import datetime, UTC
from sqlalchemy import DateTime, ForeignKey, Integer, String , Text
from sqlalchemy.orm import Mapped,mapped_column, relationship



from db.base import Base


class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username:Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email:Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    image_file:Mapped[str|None] = mapped_column(String(200), default=False,nullable=True)

    restaurants:Mapped[list["Restaurants"]] = relationship("Restaurants", back_populates="owner")
    review:Mapped[list["Reviews"]] = relationship("Review", back_populates="user")