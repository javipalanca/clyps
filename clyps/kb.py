from .agenda import Agenda
from .fact import Fact
from .rule import Rule


class KnowledgeBase:
    def __init__(self):
        self.facts = set()
        self.rules = []
        self.agenda = Agenda(kb=self)

    def add_fact(self, fact):
        """Añade un hecho a la base de conocimientos."""
        self.facts.add(fact)

    def remove_fact(self, fact):
        """Elimina un hecho de la base de conocimientos."""
        self.facts.discard(fact)

    def add_rule(self, rule):
        """Añade una regla a la lista de reglas."""
        self.rules.append(rule)

    def evaluate_rule(self, rule):
        """Evalúa una regla y añade las acciones resultantes a la agenda."""
        actions = rule.evaluate(self.facts)
        self.agenda.add_actions(actions)

    def execute_agenda(self):
        """Ejecuta las acciones en la agenda."""
        self.agenda.execute()

    def clear_agenda(self):
        """Limpia la agenda."""
        self.agenda.actions.clear()

    def run(self, max_iterations=1000):
        """Ejecuta todas las reglas aplicables hasta que no haya más reglas que se puedan activar o se alcance el límite de iteraciones."""
        iterations = 0

        while iterations < max_iterations:
            new_actions_added = False

            # Evaluar todas las reglas y añadir acciones a la agenda
            for rule in self.rules:
                actions = rule.evaluate(self.facts)
                if actions:
                    new_actions_added = True
                    self.agenda.add_actions(actions)

            # Si no se añadieron nuevas acciones a la agenda, terminar
            if not new_actions_added:
                break

            # Ejecutar las acciones en la agenda
            self.execute_agenda()

            # Limpiar la agenda para el siguiente ciclo
            self.clear_agenda()

            iterations += 1

        if iterations == max_iterations:
            print(f"Advertencia: Se alcanzó el límite máximo de iteraciones ({max_iterations}).")


# Example:
if __name__ == "__main__":
    kb = KnowledgeBase()

    # Adding facts
    fact_str1 = "(dog has hair)"
    fact1 = Fact.from_string(fact_str1)
    kb.add_fact(fact1)

    fact_str2 = "(cat has hair)"
    fact2 = Fact.from_string(fact_str2)
    kb.add_fact(fact2)

    # Adding rules
    rule_str = "(defrule mammalRule (?animal has hair) => (assert (?animal is mammal)))"
    rule = Rule.from_string(rule_str)
    kb.add_rule(rule)

    # Before inference
    print("Before inference:")
    print(kb.facts)
    print(kb.rules)

    kb.run()

    # After inference
    print("\nAfter inference:")
    print(kb.facts)
