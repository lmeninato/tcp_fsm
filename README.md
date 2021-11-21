TCP Connection Finite State Machine

Depends on the transitions python library.

Examples for running the FSM:

(Borrowed the test.txt sample test file from Alex Lee)

```
cat test.txt | python3 fsm.py 
```

Or interactively:

```
python3 fsm.py
```

Unit tests can be ran with the following:

```
pytest test_fsm.py
```