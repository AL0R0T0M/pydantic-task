from settings.settings import Settings
from files.task_2.test_validate_call import test_validate_call
from files.task_3.schemas import DealsRepository, UserScheme, Deal
from pydantic import ValidationError

from const import data, data2, data3, data4

task1 = Settings()
print(f'Task 1{'-'*30}\n    URL: {task1.URL}\n{'-'*36}')

#task2
temp, temp2 = test_validate_call()
print(f'\nTask 2{'-'*30}\n\n    - First: {temp}\n\n    - Second: {temp2}\n{'-'*36}')

#task3
task3 = DealsRepository()
try:
    task3.create_deal(**data)
    task3.get_deals()
    task3.get_deals_dicts()
    task3.get_deal(0)
    task3.update_deal(deal_id=0, data=UserScheme(**data2))
    task3.update_deal(deal_id=0, data=Deal(**data3))
    task3.delete_deal(0)
    task3.create_deal(**data4)
except ValidationError as e:
    print(f'\nTask 3{'-'*30}\n\n    - Ошибка валидации Pydantic:')
    print(str(e))
    print(f'{'-'*36}')
