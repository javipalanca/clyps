from clyps.fact import Fact


def test_fact_init():
    fact = Fact("dog", "has", "hair")
    assert fact.entity == "dog"
    assert fact.attribute == "has"
    assert fact.value == "hair"


def test_fact_from_string():
    fact_string = "(dog has hair)"
    fact = Fact.from_string(fact_string)
    assert fact.entity == "dog"
    assert fact.attribute == "has"
    assert fact.value == "hair"


def test_fact_from_string_invalid():
    fact_string = "dog has hair"
    try:
        Fact.from_string(fact_string)
    except ValueError as e:
        assert str(e) == "Invalid fact string: dog has hair"


def test_fact_repr():
    fact = Fact("dog", "has", "hair")
    assert repr(fact) == "(dog has hair)"


def test_fact_eq():
    fact1 = Fact("dog", "has", "hair")
    fact2 = Fact("dog", "has", "hair")
    fact3 = Fact("cat", "has", "hair")
    assert fact1 == fact2
    assert fact1 != fact3


def test_fact_from_string_with_spaces():
    fact_string = "(  dog  has  hair  )"
    fact = Fact.from_string(fact_string)
    assert fact.entity == "dog"
    assert fact.attribute == "has"
    assert fact.value == "hair"


def test_fact_from_string_with_capital_letters():
    fact_string = "(Dog Has Hair)"
    fact = Fact.from_string(fact_string)
    assert fact.entity == "Dog"
    assert fact.attribute == "Has"
    assert fact.value == "Hair"


def test_fact_from_string_with_special_characters():
    fact_string = "(dog has $hair!)"
    fact = Fact.from_string(fact_string)
    assert fact.entity == "dog"
    assert fact.attribute == "has"
    assert fact.value == "$hair!"


def test_fact_from_string_with_numbers():
    try:
        fact_string = "(dog has 4 legs)"
        fact = Fact.from_string(fact_string)
    except ValueError as e:
        assert str(e) == f"Invalid fact string: {fact_string}"


def test_fact_from_string_with_no_spaces():
    fact_string = "(dog_has_hair)"
    try:
        Fact.from_string(fact_string)
    except ValueError as e:
        assert str(e) == f"Invalid fact string: {fact_string}"


def test_fact_from_string_with_missing_parenthesis():
    fact_string = "dog has hair"
    try:
        Fact.from_string(fact_string)
    except ValueError as e:
        assert str(e) == f"Invalid fact string: {fact_string}"


def test_fact_from_string_with_extra_parenthesis():
    fact_string = "((dog has hair))"
    try:
        Fact.from_string(fact_string)
    except ValueError as e:
        assert str(e) == f"Invalid fact string: {fact_string}"
