"""
Django State machine :-
Provides a simple decorator to track state transition.
Check Readme file for more information.
"""
import logging

from functools import wraps
from .exception import StateMachineException

logger = logging.getLogger('StateMachine')


def state_transition(source, target, field_name='state', custom_validator=None, extra_log=None):
    """
    Decorator to perform state transition.
    Field name is expected to be ',' seperated integer field.

    :param source: list of source states which is acceptable for transition
    :param target: Target state which has to be moved
    :param field_name: name of the model field which holds the state. By default it's set to state.
    :param custom_validator: Any custom validation before doing tansition.
    :param extra_log: Extra log information to be logged

    :return: None
    """
    def true_decorator(f):
        @wraps(f)
        def wrapped(self, *args, **kwargs):
            current_state = getattr(self, field_name)
            valid = custom_validator(current_state, source) if custom_validator else _validate(current_state, source)

            if not valid:
                raise StateMachineException(f'State Transition failed current = {current_state} , source = {source}. {extra_log}')

            r = f(self, *args, **kwargs)
            logger.info(f'Transition [{source}] - [{target}]. {extra_log} ')

            new_value = _append_state(current_state, target)
            setattr(self, field_name, new_value)
            self.save()
            return r
        return wrapped
    return true_decorator

#####################################################################
# util functions
#####################################################################


def get_state(curr):
    """
    convert , separated states to integer
    :param curr: , seperated current states
    :return:
    """
    return [state for state in map(int, str(curr).split(','))] if curr else []


#####################################################################
# Local functions
#####################################################################


def _append_state(curr, value):
    """
    :param curr: current list of states
    :param value: new value to be added into states
    :return: New value of state variable in ',' seperated formatted
    """
    current_states = get_state(curr)
    current_states.append(value)
    return ",".join(map(str, current_states))


def _validate(curr, source):
    """
    Ensure current state has the source state in the list.
    If the source state is not found then this state transition is not possible
    :param curr:- current list of states which model has passed.
    :param source:- source list which has to be validated against current states.

    :return: None
    """
    current_states = get_state(curr)
    for state in source:
        if state in current_states:
            return True
    return False
