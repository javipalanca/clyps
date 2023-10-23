from .actions import printout, PRINTOUT, ASSERT
from .fact import Fact


class Agenda:
    def __init__(self, kb):
        self.kb = kb
        self.actions = []

    def add_actions(self, actions):
        self.actions.extend(actions)

    def execute(self):
        while self.actions:
            action_type, action_args = self.actions.pop(0)  # Obtiene y elimina la primera acción
            if action_type == PRINTOUT:
                printout(action_args, action_args)
            elif action_type == ASSERT:
                fact = Fact(*action_args)
                self.kb.add_fact(fact)
            # ... manejar otros tipos de acciones ...
