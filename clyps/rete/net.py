from .nodes import AlphaNode, MemoryNode, BetaNode, JoinNode


class ReteNetwork:
    def __init__(self):
        self.alpha_nodes = {}
        self.beta_nodes = {}
        self.memory_nodes = {}

    def add_alpha_node(self, condition):
        if condition not in self.alpha_nodes:
            alpha_node = AlphaNode(condition)
            memory_node = MemoryNode()
            alpha_node.add_child(memory_node)
            self.alpha_nodes[condition] = alpha_node
            self.memory_nodes[condition] = memory_node
        return self.alpha_nodes[condition], self.memory_nodes[condition]

    def add_beta_node(self, condition):
        if condition not in self.beta_nodes:
            beta_node = BetaNode(condition)
            join_node = JoinNode(beta_node, self.memory_nodes[condition[0]], self.memory_nodes[condition[1]])
            memory_node = MemoryNode()
            join_node.add_child(memory_node)
            self.beta_nodes[condition] = beta_node
            self.memory_nodes[condition] = memory_node
        return self.beta_nodes[condition], self.memory_nodes[condition]

    def build(self, rules):
        for rule in rules:
            for condition in rule.conditions:
                if isinstance(condition, tuple) and len(condition) == 2:  # Condición Beta
                    self.add_beta_node(condition)
                else:  # Condición Alfa
                    self.add_alpha_node(condition)
