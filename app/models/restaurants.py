from datetime import datetime, UTC
from sqlalchemy import DateTime, ForeignKey, Integer, String , Text, Float
from sqlalchemy.orm import Mapped,mapped_column, relationship
from db.base import Base


class Restaurants(Base):
    __tablename__ = "restaurants"
            
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title:Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    location:Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    avg_rating:Mapped[float] = mapped_column(Float,nullable=False)
    cuisine:Mapped[str] = mapped_column(String(200) ,nullable=False)
    contact_number:Mapped[str] = mapped_column(String(15),nullable=False )
    owner_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
            
    review:Mapped[list["Reviews"]] = relationship("Review", back_populates="restaurants")
    owner:Mapped[list["User"]] = relationship("User", back_populates="restaurants")