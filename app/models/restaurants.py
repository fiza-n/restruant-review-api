from datetime import datetime, UTC
from sqlalchemy import DateTime, ForeignKey, Integer, String , Text, Float
from sqlalchemy.orm import Mapped,mapped_column, relationship
from db.base import Base


class Restaurants(Base):
    __tablename__ = "restaurants"
            
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title:Mapped[str] = mapped_column(String(50), nullable=False)
    location:Mapped[str] = mapped_column(String(200), nullable=False )
    avg_rating:Mapped[float] = mapped_column(Float,default=0.0)
    cuisine:Mapped[str] = mapped_column(String(200) ,nullable=False)
    contact_number:Mapped[str] = mapped_column(String(15),nullable=False )
    owner_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
            
    reviews:Mapped[list["Reviews"]] = relationship("Review", back_populates="restaurant")
    owner:Mapped["User"] = relationship("User", back_populates="restaurants")