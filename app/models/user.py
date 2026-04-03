from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserLogin(BaseModel):
    email: EmailStr
    password: str  = Field(min_length=6, max_length=100)


# user
class UserBase(BaseModel):
    user_id: int
    user_name: str  = Field(min_length=1, max_length=80)
    model_config = ConfigDict(str_strip_whitespace=True)


class UserPrivate(UserBase):
    email: EmailStr
# class UserInDB(UserPrivate):
#     hashed_password: str


class CreateUser(UserPrivate):
    password: str = Field(min_length=6, max_length=100)


class UserUpdate(CreateUser):
    pass
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    user_name: str = Field(min_length=1, max_length=80)
    email: EmailStr
class DelUser(BaseModel):
    user_id: int    


