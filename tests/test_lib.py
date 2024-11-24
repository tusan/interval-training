from __future__ import annotations

import pytest

from interval_training.lib import Interval, QuestionStats, QuestionBuilder, Answer


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


def test_answer():
    assert Answer(Interval("C", 1), "C").is_correct()
    assert not Answer(Interval("C", 1), "C#").is_correct()


def test_question_stats():
    sut = QuestionStats()
    assert not sut.correct_answers
    assert not sut.wrong_answers

    correct_answer = Answer(Interval("C", 1), "C")
    sut.register(correct_answer)
    assert sut.correct_answers == [correct_answer]
    assert not sut.wrong_answers

    wrong_answer = Answer(Interval("C", 1), "C#")
    sut.register(wrong_answer)
    assert sut.correct_answers == [correct_answer]
    assert sut.wrong_answers == [wrong_answer]

    assert str(sut) == (
        "\n"
        "RESULT:\n"
        "1 correct answers\n"
        "\n"
        "Wrong answers:\n"
        "question 1 th, answer C# but was C"
    )


def test_question_builder():
    sut = QuestionBuilder("C", exclude_alterations=False)
    assert not sut.stats().correct_answers
    assert not sut.stats().wrong_answers

    correct_answer = Answer(Interval("C", 4), "F")
    sut.register_answer(correct_answer)
    assert sut.stats().correct_answers == [correct_answer]
    assert not sut.stats().wrong_answers

    wrong_answer = Answer(Interval("C", 4), "G")
    sut.register_answer(wrong_answer)
    assert sut.stats().correct_answers == [correct_answer]
    assert sut.stats().wrong_answers == [wrong_answer]
