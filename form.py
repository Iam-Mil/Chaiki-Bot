import re
from aiogram.fsm.state import State, StatesGroup


class BasicForm(StatesGroup):
    check_summary = State()


class Field:
    def __init__(self, name, message, validators=None, state=None):
        self.name = name
        self.validators = validators
        self.message = message
        self.state = state

    def set_state(self, state):
        self.state = state


class Form:
    def __init__(self, name, fields: list[Field]):
        self.name = name
        self.fields = []

        states_attrs = {f'set_{field.name}': State() for field in fields}
        states_class = type(f'{name.capitalize()}InputStates', (StatesGroup,), states_attrs)

        self.states = states_class()

        for i, field in enumerate(fields):
            field.set_state(self.states.__states__[i])
            self.fields.append(field)

        Forms.forms.append(self)

    def get_next_field(self, field):
        if field not in self.fields:
            raise KeyError
        if self.fields.index(field) == len(self.fields) - 1:
            return None
        else:
            return self.fields[self.fields.index(field) + 1]
        
    def get_prev_field(self, field):
        if field not in self.fields:
            raise KeyError
        if self.fields.index(field) == 0:
            return None
        else:
            return self.fields[self.fields.index(field) - 1]

    def get_field_by_state(self, state):
        for field in self.fields:
            if field.state == state:
                return field

        return None


class Forms:
    forms = []

    @classmethod
    def get_by_name(cls, form_name) -> Form:
        for form in cls.forms:
            if form.name == form_name:
                return form

        return None

    @classmethod
    def get_all_states(cls):
        states = []

        for form in cls.forms:
            for state in form.states.__states__:
                states.append(state)

        print(states)

        return states


adidas_form = Form(
    'adidas',
    [
        Field('name',
              'Введите имя покупателя: ',
              validators=[
                  lambda x: {'status': True} if len(x) > 1 else {'status': False, 'error': 'Слишком короткое имя'}
              ]),
        Field('surname',
              'Введите фамилию покупателя: ',
              validators=[
                  lambda x: {'status': True} if len(x) > 1 else {'status': False, 'error': 'Слишком короткое имя'}
              ])
        ]
    )


def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None
