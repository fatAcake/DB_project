from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, Numeric, String, ForeignKey, BigInteger, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional


class Base(DeclarativeBase):
    pass