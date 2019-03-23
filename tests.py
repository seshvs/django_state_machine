import logging

from django.test import TestCase

from apps.django_state_machine import StateMachineException, get_state
from apps.django_state_machine.models import Test

logger = logging.getLogger('StateMachine')


class StateMachineTest(TestCase):
    """
       Validate State machine transitions.
    """
    def setUp(self):
        """
        Create a sample object to work
        """
        self.obj = Test()

    def tearDown(self):
        """
            Destruct the object which was created
        """
        if self.obj and self.obj.id:
            # This can happen when object is not created.
            self.obj.delete()

    def test_state_transition_to_third_state(self):
        """
            Test if state transition is completed to third state
        """
        result = self.obj.move_to_third_state()
        self.assertTrue(result)
        self.assertIn(Test.THIRD_STATE, get_state(self.obj.state))

    def test_failed_state_transition_to_fourth_state(self):
        """
            Test if moving to fourth state will cause an error
        """
        with self.assertRaises(StateMachineException):
            result = self.obj.move_to_fourth_state()
            self.assertFalse(result)
            self.assertNotIn(Test.FOURTH_STATE, get_state(self.obj.state))

    def test_success_state_transition_to_fourth_state(self):
        """
            Test if moving to fourth state will cause an error
        """
        result = self.obj.move_to_third_state()
        self.assertTrue(result)
        self.assertIn(Test.THIRD_STATE, get_state(self.obj.state))

        result = self.obj.move_to_fourth_state()
        self.assertTrue(result)
        self.assertIn(Test.FOURTH_STATE, get_state(self.obj.state))

    def test_custom_validator(self):
        """
        Test custom validator. move to end state uses custom validator.
        if we try to transit the state to end custom validator will be used and hence we should have an error
        :return:
        """
        with self.assertRaises(StateMachineException):
            result = self.obj.move_to_end()
            self.assertFalse(result)
            self.assertNotIn(Test.FOURTH_STATE, get_state(self.obj.state))
