from settings.settings import Settings
from files.task_2.test_validate_call import test_validate_call
from files.task_3.schemas import DealsRepository, UserScheme, Deal
from pydantic import ValidationError

task1 = Settings()
print(f'Task 1{'-'*30}\n    URL: {task1.URL}\n{'-'*36}')

#task2
temp, temp2 = test_validate_call()
print(f'\nTask 2{'-'*30}\n\n    - First: {temp}\n\n    - Second: {temp2}\n{'-'*36}')

#task3
data = {
    'id': 0,
    'title': 'Тестовая Сделка',
    'comment': 'Тестовая сделка',
    'created_at': '2025-11-16T12:00:00',
    'persons_in_charge': [{
        'id': 0,
        'name': 'Igor',
        'age': 18,
        'is_supervisor': True,
        'email': 'test@mail.ru',
        'phone_number': '+7 (996) 918-57-51'
    }],
    'deal_type': {
        'buy': 'test_buy_value',
        'sell': 'test_sell_value'
    }
}

data2 = {
    'id': 0,
    'name': 'Sergey',
    'age': 23,
    'is_supervisor': False,
    'email': 'test2222@mail.ru',
    'phone_number': '+7 (800) 555-35-35'
}

data3 = {
    'id': 0,
    'title': 'Тестовая Сделка (обновлено)',
    'comment': 'Изменённая тестовая сделка',
    'created_at': '2025-12-16T12:30:00',
    'persons_in_charge': [{
        'id': 1,
        'name': 'Maxim',
        'age': 44,
        'is_supervisor': True,
        'email': 'MAXIM@mail.ru',
        'phone_number': '+7 (900) 963-58-61'
    }],
    'deal_type': {
        'buy': 'test_buy_value',
        'sell': 'test_sell_value'
    }
}

task3 = DealsRepository()
try:
    task3.create_deal(**data)
    task3.get_deals()
    task3.get_deals_dicts()
    task3.get_deal(0)
    task3.update_deal(deal_id=0, data=UserScheme(**data2))
    task3.get_deals()
    task3.update_deal(deal_id=0, data=Deal(**data3))
    task3.get_deals()
    task3.delete_deal(0)
except ValidationError as e:
    print(f'\nTask 3{'-'*30}\n\n    - Ошибка валидации Pydantic:')
    print(e)
    print(f'{'-'*36}')