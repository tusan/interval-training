import pytest

from interval_training.main import get_interval


@pytest.mark.parametrize(
    "tune,interval,alteration,expected",
    [
        ("C", 2, "", "D"),
        ("C", 2, "", "D"),
        ("C", 2, "#", "D#"),
        ("C", 2, "b", "Db"),
        ("C", 2, "bb", "Dbb"),
        ("C", 2, "x", "Dx"),
        ("Db", 5, "b", "Abb"),
        ("D", 3, "#", "Fx"),
        ("D", 3, "b", "F"),
        ("C", 9, "", "D"),
        ("C", 11, "", "F"),
        ("C", 13, "", "A"),
        ("A", 6, "x", "Fx#"),
    ],
)
def test_get_interval(tune, interval, alteration, expected):
    assert get_interval(tune, interval, alteration) == expected


@pytest.mark.parametrize(
    "tune,interval,alteration,expected",
    [
        ("C", 22, "", "Accepted intervals: [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13]"),
        (
            "G#",
            2,
            "",
            "Provide only tunes from circle of fifth: dict_keys(['C', 'G', 'D', 'A', "
            "'E', 'B', 'Cb', 'F#', 'Gb', 'Db', 'C#', 'Ab', 'Eb', 'Bb', 'F'])",
        ),
    ],
)
def test_get_interval_errors(tune, interval, alteration, expected):
    with pytest.raises(ValueError) as e:
        get_interval(tune, interval, alteration)
    assert str(e.value) == expected
