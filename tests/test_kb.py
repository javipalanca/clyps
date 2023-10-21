from clyps.fact import Fact
from clyps.rule import Rule
from clyps.kb import KnowledgeBase


def test_add_fact():
    kb = KnowledgeBase()
    fact = Fact("animal", "has", "fur")
    kb.add_fact(fact)
    assert fact in kb.facts


def test_remove_fact():
    kb = KnowledgeBase()
    fact = Fact("animal", "has", "fur")
    kb.add_fact(fact)
    kb.remove_fact(fact)
    assert fact not in kb.facts


def test_add_rule():
    kb = KnowledgeBase()
    rule = Rule(
        "mammalRule", [Fact("animal", "has", "hair")], [Fact("animal", "is", "mammal")]
    )
    kb.add_rule(rule)
    assert rule in kb.rules


def test_infer():
    kb = KnowledgeBase()
    kb.add_fact(Fact("animal", "has", "hair"))
    kb.add_fact(Fact("animal", "is", "vertebrate"))
    rule = Rule(
        "mammalRule",
        [Fact("?x", "has", "hair"), Fact("?x", "is", "vertebrate")],
        [Fact("?x", "is", "mammal")],
    )
    kb.add_rule(rule)
    kb.infer()
    assert Fact("animal", "is", "mammal") in kb.facts


def test_add_fact_from_string():
    kb = KnowledgeBase()
    fact_str = "(dog has hair)"
    fact = Fact.from_string(fact_str)
    kb.add_fact(fact)
    assert fact in kb.facts


def test_add_rule_from_string():
    kb = KnowledgeBase()
    rule_str = "(defrule mammalRule (?animal has hair) => (?animal is mammal))"
    rule = Rule.from_string(rule_str)
    kb.add_rule(rule)
    assert rule in kb.rules


def test_remove_fact_not_in_kb():
    kb = KnowledgeBase()
    fact = Fact("animal", "has", "fur")
    kb.remove_fact(fact)
    assert fact not in kb.facts


def test_remove_rule_not_in_kb():
    kb = KnowledgeBase()
    rule = Rule(
        "mammalRule", [Fact("animal", "has", "hair")], [Fact("animal", "is", "mammal")]
    )
    kb.remove_rule(rule)
    assert rule not in kb.rules


def test_infer_no_rules():
    kb = KnowledgeBase()
    kb.add_fact(Fact("animal", "has", "hair"))
    kb.add_fact(Fact("animal", "is", "vertebrate"))
    kb.infer()
    assert len(kb.facts) == 2


def test_infer_no_facts():
    kb = KnowledgeBase()
    rule = Rule(
        "mammalRule",
        [Fact("?x", "has", "hair"), Fact("?x", "is", "vertebrate")],
        [Fact("?x", "is", "mammal")],
    )
    kb.add_rule(rule)
    kb.infer()
    assert len(kb.facts) == 0


def test_infer_multiple_rules():
    kb = KnowledgeBase()
    kb.add_fact(Fact("dog", "has", "hair"))
    kb.add_fact(Fact("dog", "is", "vertebrate"))
    rule1 = Rule(
        "mammalRule",
        [Fact("?x", "has", "hair"),
         Fact("?x", "is", "vertebrate")],
        [Fact("?x", "is", "mammal")],
    )
    rule2 = Rule("dogRule",
                 [Fact("dog", "is", "mammal")],
                 [Fact("dog", "has", "fur")])
    kb.add_rule(rule1)
    kb.add_rule(rule2)
    kb.infer()
    assert Fact("dog", "has", "fur") in kb.facts


def test_apply_bindings():
    kb = KnowledgeBase()
    fact1 = Fact("dog", "has", "hair")
    fact2 = Fact("dog", "is", "vertebrate")
    rule = Rule(
        "mammalRule",
        [Fact("?x", "has", "hair"),
         Fact("?x", "is", "vertebrate")],
        [Fact("?x", "is", "mammal")],
    )
    bindings = [{"?x": "dog"}]
    new_facts = kb._apply_bindings(rule.actions[0], bindings)
    assert Fact("dog", "is", "mammal") in new_facts
