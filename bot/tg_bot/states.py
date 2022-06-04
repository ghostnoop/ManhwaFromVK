from aiogram.dispatcher.filters.state import StatesGroup, State


class EventStates(StatesGroup):
    event_add_new_group = State()
