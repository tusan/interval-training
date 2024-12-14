from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import patch

from interval_training.lib import (
    QuestionStats,
    Questionnaire,
    Answer,
    QuestionBuilder,
    Question,
    TrainingApp,
)


@dataclass(frozen=True)
class DummyAnswer(Answer):
    _is_correct: bool

    def is_correct(self) -> bool:
        return self._is_correct

    def __repr__(self):
        return "string repr of the answer"


class DummyQuestion(Question):
    def prompt_msg(self) -> str:
        return "question?"


class DummyQuestionBuilder(QuestionBuilder):
    def build_question(self) -> Question:
        return DummyQuestion()


class DummyTrainingApp(TrainingApp):
    def _question_builder(self) -> QuestionBuilder:
        return DummyQuestionBuilder()

    def _answer(self, question: Question, answer: str) -> Answer:
        return DummyAnswer(answer == "result")


def test_question_stats():
    sut = QuestionStats()
    assert not sut.correct_answers
    assert not sut.wrong_answers

    correct_answer = DummyAnswer(True)
    sut.register(correct_answer)
    assert sut.correct_answers == [correct_answer]
    assert not sut.wrong_answers

    wrong_answer = DummyAnswer(False)
    sut.register(wrong_answer)
    assert sut.correct_answers == [correct_answer]
    assert sut.wrong_answers == [wrong_answer]

    assert str(sut) == (
        "\n"
        "RESULT:\n"
        "1 correct answers\n"
        "Wrong answers:\n"
        "string repr of the answer"
    )


def test_question_builder():
    sut = Questionnaire(DummyQuestionBuilder())
    assert not sut.stats().correct_answers
    assert not sut.stats().wrong_answers

    sut.register_answer(DummyAnswer(True))
    assert sut.stats().correct_answers == [DummyAnswer(True)]
    assert not sut.stats().wrong_answers

    sut.register_answer(DummyAnswer(False))
    assert sut.stats().correct_answers == [DummyAnswer(True)]
    assert sut.stats().wrong_answers == [DummyAnswer(False)]


@patch("interval_training.lib.click")
def test_app(click_mock):
    click_mock.prompt.return_value = "result"
    app = DummyTrainingApp(5)
    assert app.run() == "\nRESULT:\n5 correct answers\n"
