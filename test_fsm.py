from fsm import *
from transitions import MachineError
import pytest

def apply_event(fsm, event):
    evt = Event(event)
    evt.apply_to_fsm(fsm)

def test_event_constructor():
    with pytest.raises(FSMException) as excinfo:
        Event("bad event")
    assert "Error: unexpected Event:" in str(excinfo.value)

    evt = Event("PASSIVE")
    assert evt.event == "PASSIVE"

def test_invalid_transition():
    machine = FSM()

    with pytest.raises(MachineError) as excinfo:
        evt = Event("ACK") # no transition from CLOSED involving ACK event
        evt._apply_to_fsm(machine)

    assert "Can't trigger event ACK from state CLOSED!" in str(excinfo.value)

def test_fsm_constructor():
    machine = FSM()

    assert machine.rdata_events == 0
    assert machine.sdata_events == 0

def test_transitions():
    machine = FSM()

    apply_event(machine, "PASSIVE")
    assert machine.state == "LISTEN"

    apply_event(machine, "CLOSE")
    assert machine.state == "CLOSED"

    apply_event(machine, "ACTIVE")
    assert machine.state == "SYN_SENT"

    apply_event(machine, "SYN")
    assert machine.state == "SYN_RCVD"

    apply_event(machine, "ACK")
    assert machine.state == "ESTABLISHED"

    apply_event(machine, "SDATA")
    assert machine.state == "ESTABLISHED"
    assert machine.sdata_events == 1

    apply_event(machine, "SDATA")
    assert machine.state == "ESTABLISHED"
    assert machine.sdata_events == 2

    apply_event(machine, "RDATA")
    assert machine.state == "ESTABLISHED"
    assert machine.rdata_events == 1

    apply_event(machine, "FIN")
    assert machine.state == "CLOSE_WAIT"

    apply_event(machine, "CLOSE")
    assert machine.state == "LAST_ACK"

    apply_event(machine, "ACK")
    assert machine.state == "CLOSED"