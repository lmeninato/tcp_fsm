import sys
from transitions import Machine, MachineError

class Event:
    events = {"PASSIVE", "ACTIVE", "SYN", "SYNACK",
              "ACK", "RDATA", "SDATA", "FIN",
              "CLOSE", "TIMEOUT"}

    def __init__(self, event):
        if not isinstance(event, str):
            raise FSMException(f"not a valid string input: {event}")
        if event not in self.events:
            raise FSMException(event)

        self.event = event

    def _apply_to_fsm(self, fsm):
        transition = getattr(fsm, self.event)
        transition()
        state = fsm.state
        if self.event == "RDATA":
            n = fsm.rdata_events
            msg = f"DATA received {n}"
        elif self.event == "SDATA":
            n = fsm.sdata_events
            msg = f"DATA sent {n}"
        else:
            msg = f"Event {self.event} received, current state is {state}"

        print(msg)
        return msg

    def apply_to_fsm(self, fsm):
        try:
            msg = self._apply_to_fsm(fsm)
        except MachineError:
            msg = "Error: Invalid state transition"
            print(msg)
        return msg

class FSMException(Exception):
    def __init__(self, event):
        self.event = event
        self.message = f"Error: unexpected Event: {self.event}"
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

class FSM(object):

    states = ["CLOSED", "SYN_SENT", "LISTEN", "SYN_RCVD",
              "ESTABLISHED", "CLOSE_WAIT", "FIN_WAIT_1", "FIN_WAIT_2",
              "TIME_WAIT", "CLOSING", "LAST_ACK"]

    def __init__(self):
        self.rdata_events = 0
        self.sdata_events = 0
        self.machine = Machine(model = self, states = FSM.states, initial = "CLOSED")

        self.add_closed_transitions()
        self.add_listen_transitions()
        self.add_syn_sent_transitions()
        self.add_syn_rcvd_transitions()
        self.add_fin_wait_1_transitions()
        self.add_fin_wait_2_transitions()
        self.add_closing_transitions()
        self.add_time_wait_transitions()
        self.add_established_transitions()
        self.add_close_wait_transitions()
        self.add_last_ack_transitions()

    def add_closed_transitions(self):
        self.machine.add_transition("ACTIVE", "CLOSED", "SYN_SENT")
        self.machine.add_transition("PASSIVE", "CLOSED", "LISTEN")

    def add_listen_transitions(self):
        # excluded according to note 2
        # self.machine.add_transition("SEND", "LISTEN", "SYN_SENT")

        self.machine.add_transition("CLOSE", "LISTEN", "CLOSED")
        self.machine.add_transition("SYN", "LISTEN", "SYN_RCVD")

    def add_syn_sent_transitions(self):
        self.machine.add_transition("CLOSE", "SYN_SENT", "CLOSED")
        self.machine.add_transition("SYN", "SYN_SENT", "SYN_RCVD")
        self.machine.add_transition("SYNACK", "SYN_SENT", "ESTABLISHED")

    def add_syn_rcvd_transitions(self):
        self.machine.add_transition("ACK", "SYN_RCVD", "ESTABLISHED")
        self.machine.add_transition("CLOSE", "SYN_RCVD", "FIN_WAIT_1")

    def add_fin_wait_1_transitions(self):
        self.machine.add_transition("ACK", "FIN_WAIT_1", "FIN_WAIT_2")
        self.machine.add_transition("FIN", "FIN_WAIT_1", "CLOSING")

    def add_fin_wait_2_transitions(self):
        self.machine.add_transition("FIN", "FIN_WAIT_2", "TIME_WAIT")

    def add_closing_transitions(self):
        self.machine.add_transition("ACK", "CLOSING", "TIME_WAIT")

    def add_time_wait_transitions(self):
        self.machine.add_transition("TIMEOUT", "TIME_WAIT", "CLOSED")

    def add_established_transitions(self):
        self.machine.add_transition("CLOSE", "ESTABLISHED", "FIN_WAIT_1")
        self.machine.add_transition("RDATA", "ESTABLISHED", "ESTABLISHED", after='increment_rdata')
        self.machine.add_transition("SDATA", "ESTABLISHED", "ESTABLISHED", after='increment_sdata')
        self.machine.add_transition("FIN", "ESTABLISHED", "CLOSE_WAIT")

    def add_close_wait_transitions(self):
        self.machine.add_transition("CLOSE", "CLOSE_WAIT", "LAST_ACK")

    def add_last_ack_transitions(self):
        self.machine.add_transition("ACK", "LAST_ACK", "CLOSED")

    def increment_rdata(self):
        self.rdata_events += 1

    def increment_sdata(self):
        self.sdata_events += 1

if __name__ == "__main__":
    print("Starting up TCP finite state machine")

    fsm = FSM()

    while True:
        try:
            data = input()
            data = data.split()
            for evt in data:
                try:
                    event = Event(evt)
                    event.apply_to_fsm(fsm)
                except FSMException as err:
                    print(err)

        except EOFError:
            break