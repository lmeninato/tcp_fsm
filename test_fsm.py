from fsm import *

def apply_event(fsm, event):
    evt = Event(event)
    evt.apply_to_fsm(fsm)

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