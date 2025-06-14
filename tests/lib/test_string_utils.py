from src.lib.string_utils import *


def test_clean_string():
    test_names = [
        ("Injustice\u2122 2", "Injustice 2"),
        ("Marvel\u2019s Spider-Man Remastered", "Marvels Spider-Man Remastered"),
        ("LEGO\u00ae Harry Potter: Years 1-4", "LEGO Harry Potter: Years 1-4"),
    ]
    for test_name, expected in test_names:
        clean_string = clean_name(test_name)
        assert clean_string == expected
