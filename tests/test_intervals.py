from __future__ import annotations

import pytest

from interval_training.interval import Interval, IntervalAnswer


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
        ("Cb", 4, "x", "F#"),
    ],
)
def test_get_interval(tune, interval, alteration, expected):
    assert str(Interval(tune, interval, alteration)) == expected


@pytest.mark.parametrize(
    "tune,interval,alteration,expected",
    [
        (
            "C",
            22,
            "",
            "Invalid interval provided 22, accepted [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13]",
        ),
        (
            "G#",
            2,
            "",
            "Provide only tunes from circle of fifth: dict_keys(["
            "'C', 'G', 'F', 'D', 'Bb', 'A', 'Eb', 'E', 'Ab', 'B', 'Db', 'F#', 'Gb', 'Cb', 'C#'"
            "])",
        ),
        ("A", 6, "x", "Invalid interval F#x"),
        (
            "A",
            6,
            "##",
            "Invalid alteration provided ##, accepted ['', 'b', '#', 'bb', 'x']",
        ),
    ],
)
def test_get_interval_errors(tune, interval, alteration, expected):
    with pytest.raises(ValueError) as e:
        Interval(tune, interval, alteration)
    assert str(e.value) == expected


def test_interval_answer():
    assert IntervalAnswer(Interval("C", 1), "C").is_correct()
    assert not IntervalAnswer(Interval("C", 1), "C#").is_correct()

    assert (
        str(IntervalAnswer(Interval("C", 1), "C"))
        == "question 1 th, user answer C - correct answer C"
    )
