from __future__ import annotations

from interval_training.chord3 import Chord3, Chord3Answer, Chord3QuestionBuilder
from interval_training.interval import Interval


def test_chord3_question_builder():
    sut = Chord3QuestionBuilder()
    assert sut.build_question()


def test_chord3_answer():
    c_maj = Chord3(Interval("C", 3), Interval("C", 5))

    assert Chord3Answer(c_maj, "C,E,G").is_correct()
    assert not Chord3Answer(c_maj, "D,E,G").is_correct()

    assert (
        str(Chord3Answer(c_maj, "C,E,G"))
        == "question C, user answer C,E,G correct answer C,E,G"
    )


def test_chord3():
    root = "C"
    base_chord = Chord3.from_root(root)

    assert str(base_chord) == "C,E,G"
    assert base_chord == Chord3(Interval(root, 3), Interval(root, 5))
    assert base_chord != Chord3(Interval("D", 3), Interval("D", 5))
