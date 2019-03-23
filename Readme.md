Django state machine.
=====================
A simple decorator to get a state machine handler function for Django Models.
 

Overview
---------
State machines are very useful to track the lifecycle of an object. 
In Django `Models` are the main objects which holds all the data and are at the core of the business logic.

This small decorator will provide an simple state transition.
Since an object can have multiple states in its lifecycle. The state here will hold a list of states. 
These states are nothing but a Comma Seperated Integer field. 

Installation
------------
Download this repository / copy the required code. 

Add `django_state_machine` in settings file, section INSTALLAED_APPS.

In any models add a field which is a comma seperated field.

```
state = models.CharField(max_length=100, null=False, default=str(START),
                             validators=[validate_comma_separated_integer_list])
                             
``` 

To add a transition use the decorator above the function.

```
@state_transition(source=[START, FIRST_STATE, SECOND_STATE], target=THIRD_STATE)
```

state transition accepts following params

```
source: list of source states which is acceptable for transition
target: Target state which has to be moved
field_name: name of the model field which holds the state. By default it's set to state.
custom_validator: Any custom validation before doing tansition.
extra_log: Extra log information to be logged
```

Refer to the implementation for more details. 

Note:- state transition decorator will save the model after successful transition.

Unit test
-----------
./manage.py test => Will run few test cases. 

```
$ ./manage.py test
Loading : /Users/sesh/repos/offonlabs/state_machine/.env
The .env file has been loaded. See base.py for more information
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.......
----------------------------------------------------------------------
Ran 7 tests in 0.321s

OK
``` 
