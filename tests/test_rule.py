from clyps.rule import Rule
from clyps.fact import Fact


def test_rule_init():
    rule = Rule(
        "mammalRule", [Fact("animal", "has", "hair")], [Fact("animal", "is", "mammal")]
    )
    assert rule.name == "mammalRule"
    assert rule.conditions == [Fact("animal", "has", "hair")]
    assert rule.actions == [Fact("animal", "is", "mammal")]


def test_rule_from_string():
    rule_string = "(defrule mammalRule (animal has hair) => (animal is mammal))"
    rule = Rule.from_string(rule_string)
    assert rule.name == "mammalRule"
    assert rule.conditions == [Fact("animal", "has", "hair")]
    assert rule.actions == [Fact("animal", "is", "mammal")]


def test_rule_repr():
    rule = Rule(
        "mammalRule", [Fact("animal", "has", "hair")], [Fact("animal", "is", "mammal")]
    )
    assert repr(rule) == "((animal has hair) => (animal is mammal))"


def test_rule_match():
    rule = Rule(
        "mammalRule", [Fact("animal", "has", "hair")], [Fact("animal", "is", "mammal")]
    )
    facts = [Fact("animal", "has", "hair"), Fact("animal", "is", "mammal")]
    bindings = rule.match(facts)
    assert bindings == []


def test_rule_match_with_variable():
    rule = Rule("mammalRule", [Fact("?x", "has", "hair")], [Fact("?x", "is", "mammal")])
    facts = [Fact("dog", "has", "hair"), Fact("dog", "is", "mammal")]
    bindings = rule.match(facts)
    assert bindings == [{"?x": "dog"}]


def test_rule_match_with_multiple_variables():
    rule = Rule("mammalRule", [Fact("?x", "has", "?y")], [Fact("?x", "is", "mammal")])
    facts = [Fact("dog", "has", "hair"), Fact("dog", "is", "mammal")]
    bindings = rule.match(facts)
    assert bindings == [{"?x": "dog", "?y": "hair"}]


def test_rule_match_with_no_match():
    rule = Rule(
        "mammalRule", [Fact("animal", "has", "hair")], [Fact("animal", "is", "mammal")]
    )
    facts = [Fact("animal", "has", "fur"), Fact("animal", "is", "mammal")]
    bindings = rule.match(facts)
    assert bindings == []


def test_rule_match_with_multiple_conditions():
    rule = Rule(
        "mammalRule",
        [Fact("animal", "has", "hair"), Fact("animal", "is", "vertebrate")],
        [Fact("animal", "is", "mammal")],
    )
    facts = [
        Fact("animal", "has", "hair"),
        Fact("animal", "is", "mammal"),
        Fact("animal", "is", "vertebrate"),
    ]
    bindings = rule.match(facts)
    assert bindings == []


def test_rule_match_with_multiple_facts():
    rule = Rule(
        "mammalRule", [Fact("animal", "has", "hair")], [Fact("animal", "is", "mammal")]
    )
    facts = [
        Fact("animal", "has", "hair"),
        Fact("animal", "has", "fur"),
        Fact("animal", "is", "mammal"),
    ]
    bindings = rule.match(facts)
    assert bindings == []


def test_rule_match_with_multiple_variables_and_facts():
    rule = Rule(
        "mammalRule",
        [Fact("?x", "has", "?y"),
                  Fact("?x", "is", "vertebrate")],
        [Fact("?x", "is", "mammal")],
    )
    facts = [
        Fact("dog", "has", "hair"),
        Fact("dog", "is", "mammal"),
        Fact("dog", "is", "vertebrate"),
    ]
    bindings = rule.match(facts)
    assert bindings == [{"?x": "dog", "?y": "hair"}]


def test_rule_match_with_multiple_variables_and_facts_no_match():
    rule = Rule(
        "mammalRule",
        [Fact("?x", "has", "?y"), Fact("?x", "is", "vertebrate")],
        [Fact("?x", "is", "mammal")],
    )
    facts = [
        Fact("dog", "have", "hair"),
        Fact("dog", "is", "reptile"),
    ]
    bindings = rule.match(facts)
    assert bindings == []


def test_rule_match_with_multiple_variables_and_facts_multiple_matches():
    rule = Rule(
        "mammalRule",
        [Fact("?x", "has", "?y"),
                  Fact("?x", "is", "vertebrate")],
        [Fact("?x", "is", "mammal")],
    )
    facts = [
        Fact("dog", "has", "hair"),
        Fact("dog", "is", "vertebrate"),
        Fact("cat", "has", "fur"),
        Fact("cat", "is", "vertebrate"),
    ]
    bindings = rule.match(facts)
    assert bindings == [{"?x": "dog", "?y": "hair"}, {"?x": "cat", "?y": "fur"}]


def test_rule_match_with_variable_and_multiple_match():
    rule = Rule(
        "mammalRule",
        [Fact("?x", "has", "hair"),
                  Fact("?x", "is", "vertebrate")],
        [Fact("?x", "is", "mammal")],
    )
    facts = [
        Fact("dog", "has", "hair"),
        Fact("cat", "has", "hair"),
        Fact("dog", "is", "vertebrate"),
        Fact("cat", "is", "vertebrate"),
    ]
    bindings = rule.match(facts)
    assert bindings == [{"?x": "dog"}, {"?x": "cat"}]
