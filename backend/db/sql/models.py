from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, Numeric, String, ForeignKey, BigInteger, Text, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional

class Base(DeclarativeBase):
    pass

class Roles(Base): # КАРПЕЧИН
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    role: Mapped["Users"] = relationship(back_populates="user", cascade="all, delete-orphan")

class Users(Base): # КАРПЕЧИН
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    father_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=False)
    hash_password: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    is_acive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=False)

    role: Mapped["Roles"] = relationship(back_populates="role", cascade="all, delete-orphan")
    passport_data: Mapped["PassportsData"] = relationship(back_populates="user", 
                                                         cascade="all, delete-orphan")
    log_user: Mapped["Logs"] = relationship(back_populates="user", cascade="all, delete-orphan")
    transaction_user: Mapped["Transactions"] = relationship(back_populates="user", 
                                                            cascade="all, delete-orphan")

class PassportsData(Base): # ТЕРИХОВ
    __tablename__ = "passportsdata"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    father_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    place_birth: Mapped[str] = mapped_column(String(255), nullable=False)
    number_passport: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    passport_issue_date: Mapped[str] = mapped_column(String(255), nullable=False)
    issued_by: Mapped[str] = mapped_column(String(255), nullable=False)
    code_issued_by: Mapped[str] = mapped_column(String(255), nullable=False)
    registration: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["Users"] = relationship(back_populates="passport_data", 
                                         cascade="all, delete-orphan")
    
class Logs(Base): # ТЕРИХОВ
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    lead_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    system: Mapped[str] = mapped_column(String(255), nullable=False)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["Users"] = relationship(back_populates="log_user", cascade="all, delete-orphan") 

class Blueprints(Base): # МОТРЯ
    __tablename__ = "blueprints"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(400), nullable=False)

class Products(Base): # МОТРЯ
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Numeric, nullable=False)
    
    quantity_product: Mapped["QuantityProducts"] = relationship(back_populates="product", cascade="all, delete-orphan")

class QuantityProducts(Base): 
    __tablename__ = "quantity_products"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, unique=True)

    product: Mapped["Products"] = relationship(back_populates="quantity_product", cascade="all, delete-orphan")

class Transactions(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sum: Mapped[float] = mapped_column(Numeric, nullable=False)
    card_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["Users"] = relationship(back_populates="transaction_user", 
                                         cascade="all, delete-orphan")

class ConfirmPasspotrData(Base):
    __tablename__ = "confirm_passport_data"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    passport_data_id: Mapped[int] = mapped_column(ForeignKey("passportsdata.id"), nullable=False)
    is_confirm: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)