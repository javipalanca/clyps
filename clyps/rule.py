import itertools
import re
from typing import Any, Dict, List, Optional

from .fact import Fact


class Rule:
    """Represents a rule with conditions and actions."""

    def __init__(self, name, conditions, actions):
        self.name = name
        self.conditions = conditions
        self.actions = actions

    @staticmethod
    def extract_parts(s):
        parts = []
        stack = []
        start_idx = None
        for idx, char in enumerate(s):
            if char == "(":
                if not stack:  # Si es el primer paréntesis abierto
                    start_idx = idx + 1
                stack.append("(")
            elif char == ")":
                if stack:  # Verificar que haya paréntesis abiertos antes de hacer pop
                    stack.pop()
                    if not stack:  # Si todos los paréntesis están cerrados
                        parts.append("(" + s[start_idx:idx].strip() + ")")
        return parts

    @staticmethod
    def parse_rule_parts(rule_string):
        # Extracts the rule name, conditions, and actions from a rule string.
        rule_name_match = re.search(r"defrule (\w+)", rule_string)
        if not rule_name_match:
            raise ValueError("Rule name not found!")
        rule_name = rule_name_match.group(1)

        # Splits the rule string into conditions and actions.
        _, body_str = re.split(r"defrule " + rule_name, rule_string[:-1])
        conditions_str, actions_str = re.split(r" => ", body_str)

        return rule_name, conditions_str, actions_str

    @staticmethod
    def parse_rule_conditions_and_actions(conditions_str, actions_str):
        conditions = [Fact.from_string(r) for r in Rule.extract_parts(conditions_str)]
        actions = [Fact.from_string(r) for r in Rule.extract_parts(actions_str)]
        return conditions, actions

    @classmethod
    def from_string(cls, rule_string):
        """Parses a rule from a string.
        Example: (defrule mammalRule (animal has hair) => (animal is mammal))"""
        rule_name, conditions_str, actions_str = Rule.parse_rule_parts(rule_string)
        conditions, actions = Rule.parse_rule_conditions_and_actions(
            conditions_str, actions_str
        )

        return cls(rule_name, conditions, actions)

    def __eq__(self, other):
        if not isinstance(other, Rule):
            return False
        return (
            self.name == other.name
            and self.conditions == other.conditions
            and self.actions == other.actions
        )

    def __repr__(self):
        conditions_str = " AND ".join(map(str, self.conditions))
        actions_str = ", ".join(map(str, self.actions))
        return f"({conditions_str} => {actions_str})"

    def match(self, facts: List[Fact]) -> List[Dict[str, Any]]:
        all_bindings = []  # Lista para almacenar todos los sets de bindings encontrados

        # Generar todas las combinaciones posibles de hechos (para manejar múltiples coincidencias)
        for fact_combination in itertools.combinations(facts, len(self.conditions)):
            bindings = {}
            matched_conditions = 0  # Contador de condiciones coincidentes

            # Para cada condición en la regla:
            for condition, fact in zip(self.conditions, fact_combination):
                local_bindings = self._match_condition(fact, condition)

                # Si el hecho coincide con la condición
                if local_bindings is not None:
                    # Verificar que no se estén sobrescribiendo los bindings existentes
                    conflicting_bindings = any(
                        k in bindings and bindings[k] != v
                        for k, v in local_bindings.items()
                    )
                    if not conflicting_bindings:
                        bindings.update(local_bindings)
                        matched_conditions += 1
                    else:
                        break  # Rompe el bucle si hay conflictos, y no considerar esta combinación

            # Si todas las condiciones coinciden, añadir los bindings a la lista
            if matched_conditions == len(self.conditions) and bindings:
                all_bindings.append(bindings)

        return all_bindings

    def _match_condition(self, fact: Fact, condition: Fact) -> Optional[Dict[str, str]]:
        """
        Checks if a fact matches a condition.
        Example: (dog has hair) matches (?animal has hair)
        If condition starts with ? it is a variable and will be bound to the fact value.
        """
        bindings = {}  # Make a dictionary to store variable bindings
        if condition.entity.startswith("?"):  # If the condition entity is a variable
            if fact.entity.startswith("?"):  # If the fact entity is also a variable
                return None  # We can't match two variables
            # Bind the condition variable to the fact entity
            bindings[condition.entity] = fact.entity
        # If the condition entity is not a variable, it must match the fact entity
        elif condition.entity != fact.entity:
            return None  # If they don't match, the fact doesn't match the condition
        # If the condition attribute doesn't match the fact attribute
        if condition.attribute != fact.attribute:
            return None  # The fact doesn't match the condition

        if condition.value.startswith("?"):  # If the condition value is a variable
            if fact.value.startswith("?"):  # If the fact value is also a variable
                return None  # We can't match two variables
            # Bind the condition variable to the fact value
            bindings[condition.value] = fact.value
        # If the condition value is not a variable, it must match the fact value
        elif condition.value != fact.value:
            return None  # If they don't match, the fact doesn't match the condition

        return bindings  # If we get here, the fact matches the condition, so return the variable bindings
