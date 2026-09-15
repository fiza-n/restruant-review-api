from datetime import datetime, UTC
from sqlalchemy import DateTime, ForeignKey, Integer, String , Text, Float
from sqlalchemy.orm import Mapped,mapped_column, relationship
from db.base import Base


class Reviews(Base):
    __tablename__ = "reviews"
        
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title:Mapped[str] = mapped_column(String(50), nullable=False )
    body:Mapped[str] = mapped_column(String(200), nullable=False)
    rating:Mapped[int] = mapped_column(Integer,nullable=False)
    sentiment_label:Mapped[str] = mapped_column(String(200) ,nullable=False)
    sentiment_score:Mapped[float] = mapped_column(Float,nullable=False )
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    restaurants_id:Mapped[int] = mapped_column(Integer, ForeignKey("restaurants.id"), index=True)
        
    restaurant:Mapped["Restaurants"] = relationship("Restaurants", back_populates="reviews")
    user:Mapped["User"] = relationship("User", back_populates="reviews")

    review_posted:Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(UTC))
     