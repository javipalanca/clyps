import re


class Fact:
    """Represents a fact with entity, attribute, and value.
    Example: (dog has hair)"""

    def __init__(self, entity: str, attribute: str, value: str):
        self.entity = entity
        self.attribute = attribute
        self.value = value

    @classmethod
    def from_string(cls, fact_string: str):
        """Parses a fact from a string."""
        parts = re.findall(r"\(([^)]+)", fact_string)
        if not parts:
            raise ValueError(f"Invalid fact string: {fact_string}")
        # check if the fact length is valid
        parts = parts[0].split()
        if len(parts) != 3:
            raise ValueError(f"Invalid fact string: {fact_string}")
        return cls(*parts)

    def __repr__(self) -> str:
        return f"({self.entity} {self.attribute} {self.value})"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Fact):
            return (
                self.entity == __value.entity
                and self.attribute == __value.attribute
                and self.value == __value.value
            )
        return False
