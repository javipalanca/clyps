from typing import List

from .fact import Fact
from .rule import Rule


class KnowledgeBase:
    """Represents a knowledge base with facts and rules."""

    def __init__(self):
        self.facts = []
        self.rules = []

    def add_fact(self, _fact):
        """Adds a fact to the knowledge base."""
        self.facts.append(_fact)

    def remove_fact(self, _fact):
        """Removes a fact from the knowledge base."""
        if _fact in self.facts:
            self.facts.remove(_fact)

    def add_rule(self, _rule):
        """Adds a rule to the knowledge base."""
        self.rules.append(_rule)

    def remove_rule(self, _rule):
        """Removes a rule from the knowledge base."""
        if _rule in self.rules:
            self.rules.remove(_rule)

    def infer(self) -> None:
        """Infers new facts using the current facts and rules."""
        new_facts_added: bool = True
        while new_facts_added:
            # Assume that no new facts will be added in this iteration
            new_facts_added = False

            # Go through all the rules
            for _rule in self.rules:
                # Check if the rule contains variables
                contains_variables = any(
                    fact.entity.startswith("?") or fact.value.startswith("?")
                    for fact in _rule.conditions
                )

                if contains_variables:
                    # Try to find a match for the rule
                    bindings = _rule.match(self.facts)
                    if bindings:
                        for action in _rule.actions:
                            try:
                                # Apply the bindings to the action
                                new_facts: List[Fact] = self._apply_bindings(action, bindings)

                                # Add the new fact to the list of facts if it isn't already there
                                for new_fact in new_facts:
                                    if new_fact not in self.facts:
                                        self.facts.append(new_fact)
                                        new_facts_added = True

                            # If there was an error applying the bindings, just move on to the next action
                            except Exception as e:
                                print(e)
                else:
                    # If rule does not contain variables, check if all conditions are present in the facts
                    if all(condition in self.facts for condition in _rule.conditions):
                        # If all conditions are met, add the actions to the facts
                        for action in _rule.actions:
                            if action not in self.facts:
                                self.facts.append(action)
                                new_facts_added = True

    def _apply_bindings(self, action, bindings) -> List[Fact]:
        facts = []
        for binding in bindings:
            if action.entity in binding:
                entity = binding.get(action.entity, action.entity)
                value = binding.get(action.value, action.value)
                facts.append(Fact(entity, action.attribute, value))
        return facts


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
    rule_str = "(defrule mammalRule (?animal has hair) => (?animal is mammal))"
    rule = Rule.from_string(rule_str)
    kb.add_rule(rule)

    # Before inference
    print("Before inference:")
    print(kb.facts)
    print(kb.rules)

    kb.infer()

    # After inference
    print("\nAfter inference:")
    print(kb.facts)
