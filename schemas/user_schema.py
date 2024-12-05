from pydantic import BaseModel, Field
from typing import Optional


class UserBase(BaseModel):
    """Base schema with shared fields for User."""
    firstname: str = Field(..., example="John")
    lastname: str = Field(..., example="Doe")
    username: str = Field(..., example="johndoe")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, example="securepassword")


class UserRead(UserBase):
    """Schema for reading user data (excluding sensitive fields)."""
    id: int
    pass


class UserUpdate(BaseModel):
    """Schema for updating user data."""
    username: Optional[str] = Field(None, example="newusername")
    firstname: Optional[str] = Field(None, example="NewFirstName")
    lastname: Optional[str] = Field(None, example="NewLastName")
    password: Optional[str] = Field(None, min_length=8, example="newsecurepassword")


class UserLogin(BaseModel):
    username: str = Field(..., example="johndoe")
    password: str = Field(..., example="securepassword")
