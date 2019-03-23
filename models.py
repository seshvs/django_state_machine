import logging

from django.core.validators import validate_comma_separated_integer_list
from django.db import models

from apps.django_state_machine import state_transition, get_state

logger = logging.getLogger('StateMachine')


def ensure_start_state(current_state, source):
    """
        Sample validator. This can be any check according to business logic
    """
    valid_source = False
    for item in source:
        if item in get_state(current_state):
            valid_source = True
            break

    return Test.FIRST_STATE in get_state(current_state) and valid_source


# Create your models here.
class Test(models.Model):
    START = 0
    FIRST_STATE = 1
    SECOND_STATE = 2
    THIRD_STATE = 3
    FOURTH_STATE = 4
    END = 5

    state = models.CharField(max_length=100, null=False, default=str(START),
                             validators=[validate_comma_separated_integer_list])

    @state_transition(source=[START, FIRST_STATE, SECOND_STATE], target=THIRD_STATE)
    def move_to_third_state(self):
        logger.info('move to third state')
        return True

    @state_transition(source=[THIRD_STATE], target=FOURTH_STATE)
    def move_to_fourth_state(self):
        logger.info('move to fourth state')
        return True

    @state_transition(source=[FOURTH_STATE], target=END, custom_validator=ensure_start_state)
    def move_to_end(self):
        logger.info('move to end')
        return True

