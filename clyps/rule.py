import re

from .fact import Fact


class Rule:
    def __init__(self, name, conditions, action_type, action_args):
        self.name = name
        self.conditions = conditions  # Lista de condiciones con posibles variables
        self.action_type = action_type
        self.action_args = action_args

    def evaluate(self, facts):
        all_bindings = self.match_conditions(facts)
        actions = []
        for bindings in all_bindings:
            action = (self.action_type, [bindings.get(arg, arg) for arg in self.action_args])
            actions.append(action)
        return actions

    def match_conditions(self, facts):
        all_bindings = [{}]

        for condition in self.conditions:
            new_bindings_list = []
            for bindings in all_bindings:
                for fact in facts:
                    local_bindings = self.match_fact(condition, fact)
                    if local_bindings is not None:
                        merged_bindings = bindings.copy()
                        merged_bindings.update(local_bindings)
                        new_bindings_list.append(merged_bindings)
            all_bindings = new_bindings_list

        return all_bindings

    def match_fact(self, condition, fact):
        bindings = {}
        for c_attr, f_attr in zip(condition.attributes, fact.attributes):
            if c_attr.startswith("?"):
                if c_attr in bindings and bindings[c_attr] != f_attr:
                    return None
                bindings[c_attr] = f_attr
            elif c_attr != f_attr:
                return None
        return bindings

    @classmethod
    def from_string(cls, rule_str):
        # Extrae el nombre, las condiciones y la acción de la definición de la regla
        match = re.match(r"\(defrule (\w+)\s+(.*?)\s+=>\s+\((.*?)\)\)", rule_str, re.DOTALL)
        if not match:
            raise ValueError("Invalid rule definition")

        name = match.group(1)
        conditions = [Fact.from_string(cond) for cond in match.group(2).split(")(")]
        action_parts = match.group(3).split()
        action_type = action_parts[0]
        action_args = action_parts[1:]

        return cls(name, conditions, action_type, action_args)

    def __repr__(self):
        return f"(defrule {self.name} {' '.join([str(cond) for cond in self.conditions])} => ({self.action_type} {' '.join(self.action_args)}))"

