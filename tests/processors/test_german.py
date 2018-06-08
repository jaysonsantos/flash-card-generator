from learning.processors.german import GermanProcessor


def test_separable_verbs():
    processor = GermanProcessor("Ich steige hier aus")
    sentences = list(processor.iterate_sentences())
    words = list(processor.iterate_words(sentences[0]))
    assert words == ["Ich", "aussteigen", "hier"]
