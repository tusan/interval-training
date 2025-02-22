from __future__ import annotations

from interval_training.triad import Triad, TriadAnswer, TriadQuestionBuilder
from interval_training.interval import Interval


def test_triad_question_builder():
    assert TriadQuestionBuilder().build_question()


def test_triad_answer():
    c_maj = Triad(Interval("C", 3), Interval("C", 5))

    assert TriadAnswer(c_maj, "C,E,G").is_correct()
    assert not TriadAnswer(c_maj, "D,E,G").is_correct()

    assert (
        str(TriadAnswer(c_maj, "C,E,G"))
        == "question C, user answer C,E,G correct answer C,E,G"
    )


def test_triad():
    root = "C"
    base_chord = Triad.from_root(root)

    assert str(base_chord) == "C,E,G"
    assert base_chord == Triad(Interval(root, 3), Interval(root, 5))
    assert base_chord != Triad(Interval("D", 3), Interval("D", 5))
