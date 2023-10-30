def test_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, "The phrase is longer than 15 symbol"