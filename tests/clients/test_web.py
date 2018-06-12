from flask import url_for


def test_wrong_language(test_client):
    response = test_client.post(url_for("main.generate_flash_card", language="abc"))
    assert response.status_code == 404
    assert response.json == {"error": "abc is not a supported language, choose between one of these en, de, fr."}


def test_invalid_payload(test_client):
    response = test_client.post(url_for("main.generate_flash_card", language="de"))
    assert response.status_code == 400
    assert response.json == {"error": "Invalid payload sent."}

    response = test_client.post(url_for("main.generate_flash_card", language="de"), json={})
    assert response.status_code == 400
    assert response.json == {"error": "Invalid payload sent."}

    response = test_client.post(url_for("main.generate_flash_card", language="de"), json={"a": "b"})
    assert response.status_code == 400
    assert response.json == {
        "errors": {"known_words": ["Missing data for required field."], "text": ["Missing data for required field."]}
    }


def test_flash_card_generated(test_client):
    response = test_client.post(
        url_for("main.generate_flash_card", language="de"),
        json={"text": "Er hat mir nein gesagt", "known_words": ["sagen"], "unknown_words": ["nein"]},
    )
    assert response.status_code == 200, response.json
    assert response.json == {
        "text": "nein<br />Er hat mir nein gesagt\tNo<br />He told me no\n"
    }, response.data.decode()


def test_word_tree_generated(test_client):
    response = test_client.post(url_for("main.build_word_tree", language="de"), json={"text": "Er hat mir nein gesagt"})
    assert response.status_code == 200, response.json
    assert response.json == {
        "word_tree": {
            "er": ["Er hat mir nein gesagt"],
            "haben": ["Er hat mir nein gesagt"],
            "nein": ["Er hat mir nein gesagt"],
            "sagen": ["Er hat mir nein gesagt"],
            "sich": ["Er hat mir nein gesagt"],
        }
    }, response.data.decode()
