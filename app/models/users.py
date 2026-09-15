from datetime import datetime, UTC
from sqlalchemy import DateTime, ForeignKey, Integer, String , Text
from sqlalchemy.orm import Mapped,mapped_column, relationship


from db.base import Base


class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)