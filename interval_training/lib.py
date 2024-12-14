import logging
import random
from abc import ABC, abstractmethod
from collections import deque
from typing import Protocol

import click

MAJOR_SCALES = {
    "C": ["C", "D", "E", "F", "G", "A", "B"],
    "G": ["G", "A", "B", "C", "D", "E", "F#"],
    "F": ["F", "G", "A", "Bb", "C", "D", "E"],
    "D": ["D", "E", "F#", "G", "A", "B", "C#"],
    "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
    "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
    "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
    "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
    "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
    "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
    "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
    "Gb": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
    "Cb": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],
    "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
}

logger = logging.getLogger(__file__)


def random_scale() -> str:
    return random.choice(list(MAJOR_SCALES))


class Answer(Protocol):
    def is_correct(self) -> bool: ...


class QuestionStats:
    def __init__(self):
        self._correct_answers: list[Answer] = []
        self._wrong_answers: list[Answer] = []

    def register(self, answer: Answer) -> None:
        if answer.is_correct():
            self._correct_answers.append(answer)
        else:
            self._wrong_answers.append(answer)

    @property
    def correct_answers(self) -> list[Answer]:
        return self._correct_answers

    @property
    def wrong_answers(self) -> list[Answer]:
        return self._wrong_answers

    def __repr__(self):
        result = f"\nRESULT:\n{len(self.correct_answers)} correct answers\n"
        wrong_answers_recap = "\n".join([str(answer) for answer in self.wrong_answers])

        return (
            f"{result}Wrong answers:\n{wrong_answers_recap}"
            if self.wrong_answers
            else result
        )


class Question(Protocol):
    def prompt_msg(self) -> str: ...


class QuestionBuilder(Protocol):
    def build_question(self) -> Question: ...


class Questionnaire[T]:
    def __init__(self, question_builder: QuestionBuilder):
        self._question_builder = question_builder

        self._question_stats = QuestionStats()
        self._already_seen: deque[T] = deque(maxlen=7)

    def build_question(self) -> T:
        for _ in range(50, 0, -1):
            try:
                question = self._question_builder.build_question()
                if question not in self._already_seen:
                    self._already_seen.append(question)
                    return question
            except ValueError as e:
                logger.debug(f"Error while generating question: {e}")
                pass

        raise ValueError("Error in building questions, too many attempt")

    def register_answer(self, answer: Answer) -> None:
        self._question_stats.register(answer)

    def stats(self) -> QuestionStats:
        return self._question_stats


class TrainingApp(ABC):
    def __init__(self, question_size: int):
        if question_size > 1:
            self._question_size = question_size
        else:
            raise ValueError("At least 2 questions should be used")

    @abstractmethod
    def _question_builder(self) -> QuestionBuilder: ...

    @abstractmethod
    def _answer(self, question: Question, answer: str) -> Answer: ...

    def run(self):
        questionnaire = Questionnaire(self._question_builder())

        try:
            for _ in range(1, self._question_size + 1):
                question = questionnaire.build_question()
                answer = click.prompt(question.prompt_msg())
                questionnaire.register_answer(self._answer(question, answer))
        finally:
            return str(questionnaire.stats())
