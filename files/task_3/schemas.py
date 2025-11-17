from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError, ConfigDict, validate_call
from pydantic.alias_generators import to_camel
from datetime import datetime
from time import time

from settings.settings import Settings

class MyBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

class UserScheme(MyBaseModel):
    id: int
    name: str = Field(min_length=1)
    username: str = f'User_{int(time())}'
    age: int = Field(ge=0)
    is_supervisor: bool
    email: EmailStr
    phone_number: str

    @field_validator('phone_number')
    def check_number(phone_number):
        default = '+ () --'
        check_list = []
        for i in phone_number:
            if i in default:
                check_list.append(i)
        check_list = ''.join(check_list)
        if check_list != default or phone_number[1] != '7':
            raise ValidationError('Неверный формат номера телефона, пример записи: +7 (XXX) XXX-XX-XX')
        return phone_number

class TypeDeal(MyBaseModel):
    buy: str
    sell: str

class Deal(MyBaseModel):
    id: int = Field(title='Индентификатор сделки', description='Уникальный индентификатор')
    title: str = Field(title='Название сделки', description='Поле для названия сделки')
    comment: str = Field(title='Текстовый комментарий', description='Комментарий к сделке')
    created_at: datetime = Field(title='Время сделки', description='Дата когда была создана сделка')
    persons_in_charge: list[UserScheme] = Field(title='Список пользователей', description='Список пользователей участвующих в сделке')
    deal_type: TypeDeal = Field(title='Тип', description='Тип созданной сделки')

class Descriptor:
    def __get__(self, instance, owner):
        with ContextManager() as store:
            return store


class DealsStore:
    _store = []

    def __new__(cls):
        if not hasattr(cls, 'isinstance'):
            cls.instance = super(DealsStore, cls).__new__(cls)
        return cls.instance

    def get_store(self):
        return self._store
    
    def set_store_data(self, value):
        self._store.append(value)
    
    def del_store_data(self, value):
        del self._store[value]

class ContextManager():
    task1 = Settings()

    def __enter__(self):
        print(f'\n\n\n{'-'*36}\n    URL: {self.task1.URL}')
        Store = DealsStore()
        print(f'\n    DataBase is connected!\n')
        print(Store.get_store())
        return Store
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'\n    URL: {self.task1.URL}')
        print(f'\n    DataBase is disconnected!\n')


class DealsRepository:
    store = Descriptor()

    @validate_call
    def create_deal(self, **data) -> Deal:
        data = Deal(**data)
        self.store.set_store_data(data)
        print(f'Создана новая сделка!')
    
    def get_deals(self):
        deals = self.store.get_store()
        return deals
    
    def get_deals_dicts(self):
        result = []
        deals = self.store.get_store()
        for deal in deals:
            result.append(deal.model_dump_json())
            print(result)
        return result

    def get_deal(self, deal_id: int) -> Deal | None:
        deals = self.store.get_store()
        for deal in deals:
            if deal.id == deal_id:
                return deal
        print(f'Сделка под ключом: "{deal_id}" не найдена!')
        return None

    def delete_deal(self, deal_id: int):
        deals = self.store.get_store()
        for i, deal in enumerate(deals):
            if deal.id == deal_id:
                print(f'сделка под ID:"{deal.id}" была успешно удалена!')
                del deals[i]
                return f'сделка под ID:"{deal_id}" была успешно удалена!'
        print(f'Сделка под ключом: "{deal_id}" не найдена!')
    
    def update_deal(self, deal_id: int, data: Deal | UserScheme, user_id: int = 0):
        deals = self.store.get_store()
        for i, deal in enumerate(deals):
            if deal.id == deal_id:
                if isinstance(data, Deal):
                    deals[i] = data
                    print(f"Сделка с ID {deal_id} обновлена.")
                    return
                elif isinstance(data, UserScheme):
                    deals[i].persons_in_charge[user_id] = data
                    print(f"Обновление пользователя в сделке {deal_id}...")
                    return
        print(f'Сделка с ID {deal_id} не найдена!')
