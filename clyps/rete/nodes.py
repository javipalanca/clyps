class Node:
    def __init__(self):
        self.children = []

    def add_child(self, child):
        self.children.append(child)


class AlphaNode(Node):
    def __init__(self, condition):
        super().__init__()
        self.condition = condition

    def evaluate(self, fact):
        if self.condition(fact):
            for child in self.children:
                child.add_fact(fact)


class MemoryNode(Node):
    def __init__(self):
        super().__init__()
        self.facts = []

    def add_fact(self, fact):
        self.facts.append(fact)
        for child in self.children:
            child.evaluate(fact)


class BetaNode(Node):
    def __init__(self, condition):
        super().__init__()
        self.condition = condition

    def unify(self, pattern1, pattern2):
        """Unifica dos patrones y devuelve un mapeo de variables a valores si la unificación es exitosa."""
        bindings = {}
        for var, value in zip(pattern1, pattern2):
            if var.startswith("?"):
                if var not in bindings:
                    bindings[var] = value
                elif bindings[var] != value:
                    return None  # Fallo en la unificación
            elif var != value:
                return None  # Fallo en la unificación
        return bindings

    def evaluate(self, fact1, fact2):
        bindings = self.unify(self.condition[0], fact1)
        if bindings is None:
            return False

        bindings2 = self.unify(self.condition[1], fact2)
        if bindings2 is None:
            return False

        # Comprobar si las unificaciones son consistentes
        for var, value in bindings2.items():
            if var in bindings and bindings[var] != value:
                return False
            bindings[var] = value

        return True


class JoinNode(Node):
    def __init__(self, beta_node, left_memory, right_memory):
        super().__init__()
        self.beta_node = beta_node
        self.left_memory = left_memory
        self.right_memory = right_memory

    def evaluate(self, fact):
        for other_fact in (self.left_memory.facts if fact in self.right_memory.facts else self.right_memory.facts):
            if self.beta_node.evaluate(fact, other_fact):
                combined_fact = (fact, other_fact)
                for child in self.children:
                    child.add_fact(combined_fact)
