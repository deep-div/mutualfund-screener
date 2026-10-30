from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base

TABLE_NAME_4 = "users"
TABLE_NAME_6 = "user_screens"
TABLE_NAME_7 = "user_watchlist"
SCREEN_TYPE_SCREEN = "screen"
SCREEN_TYPE_WATCHLIST = "watchlist"

"""Stores user profile information"""
class UserORM(Base):
    __tablename__ = TABLE_NAME_4

    uid = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    email_verified = Column(Boolean)
    name = Column(String)
    provider = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


"""Stores applied screen JSON per user"""
class UserScreenORM(Base):
    __tablename__ = TABLE_NAME_6

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(
        String,
        ForeignKey(f"{TABLE_NAME_4}.uid", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    external_id = Column(String(32), index=True, nullable=False, unique=True)
    name = Column(String)
    description = Column(String)
    screen_type = Column(String(16), nullable=False, server_default=SCREEN_TYPE_SCREEN, index=True)
    screens = Column(JSONB, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


"""Stores selected mutual fund external IDs linked to a saved screen"""
class UserWatchlistORM(Base):
    __tablename__ = TABLE_NAME_7
    __table_args__ = (
        UniqueConstraint("user_screen_id", "scheme_external_id", name="uq_user_watchlist_scheme_external_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_screen_id = Column(
        Integer,
        ForeignKey(f"{TABLE_NAME_6}.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    scheme_external_id = Column(String(32), index=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
