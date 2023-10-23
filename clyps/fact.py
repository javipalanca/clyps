class Fact:
    def __init__(self, *attributes):
        self.attributes = attributes

    @classmethod
    def from_string(cls, fact_str):
        # Suponiendo que los atributos están separados por espacios en la cadena
        attributes = tuple(fact_str.split())
        return cls(*attributes)

    def __str__(self):
        return "(" + " ".join(self.attributes) + ")"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Fact):
            return self.attributes == other.attributes
        return False

    def __hash__(self):
        return hash(self.attributes)
