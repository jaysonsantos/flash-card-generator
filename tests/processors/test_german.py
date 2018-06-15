import pytest

from learning.processors.german import GermanProcessor


def process(text):
    processor = GermanProcessor(text)
    sentences = list(processor.iterate_sentences())
    words = list(processor.iterate_words(sentences[0]))
    return words, sentences


def test_separable_verbs():
    words, _ = process("Ich steige hier aus")
    assert words == ["Ich", "aussteigen", "hier"]

    # TODO: Fix separable verbs in questions?
    # words = process("Steigst du um?")
    # assert words == ["umsteigen", "du"]


def test_wrong_separable_verbs():
    # Make sure we don't think that particles that are not separable verbs create things like "nichtkönnen"
    words, _ = process("Das kann nicht sein.")
    assert words == ["Das", "können", "nicht", "sein"]


def test_possessive_pronouns():
    # TODO: Decide if possessive pronouns should be used with lemma like ihr/dein all become mein
    words, _ = process("Das ist nicht ihr Vater.")
    assert words == ["Das", "sein", "nicht", "mein", "Vater"]


@pytest.mark.skip()
def test_definitive_article():
    # TODO: If we remove lemma for articles the indefinitive articles that are "declensed"
    words, _ = process("Er hat die Tür zugemacht.")
    assert words == ["Er", "haben", "die", "Tür", "zumachen"]
