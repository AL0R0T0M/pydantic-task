from .validate_call import valid_call, User
from pydantic import ValidationError

def test_validate_call():

    data = {
        'login': 'Igor_Karpov',
        'name': 'Igor',
        'age': 23,
        'email': 'igorkarpov@mail.ru'
    }

    result = valid_call(User(**data))
    result2 = ''

    try:
        valid_call('hello')
        result2 = 'Успех!'
    except ValidationError as e:
        error = f'not valid, error: {e}'
        result2 = 'Неудача!'
    finally:
        result2 = result2 + '\n\nError: \n    ' + error
    return result, result2
