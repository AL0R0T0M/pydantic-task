from pydantic import BaseModel, validate_call, EmailStr, ValidationError

class User(BaseModel):
    login: str
    name: str
    age: int
    email: EmailStr

@validate_call
def valid_call(value: User):
    return f'Аккаунт пользователя {value.name} проверку прошёл успешно'
