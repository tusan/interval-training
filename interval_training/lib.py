import logging
import random
from collections import deque
from dataclasses import dataclass

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


class Interval:
    _intervals = [*range(1, 9), 9, 11, 13]
    _alterations = ["", "b", "#", "bb", "x"]
    _alterations_weight = [100, 50, 50, 10, 10]

    def __init__(self, root: str, interval: int, alteration: str = ""):
        self._root = root
        self._interval = interval
        self._alteration = alteration

        self._validate_interval()

    def _validate_interval(self):
        if self.root not in MAJOR_SCALES:
            raise ValueError(
                f"Provide only tunes from circle of fifth:" f" {MAJOR_SCALES.keys()}",
            )

        if self.interval not in self._intervals:
            raise ValueError(
                f"Invalid interval provided {self.interval}, "
                f"accepted {self._intervals}"
            )

        if self.alteration not in self._alterations:
            raise ValueError(
                f"Invalid alteration provided {self.alteration}, "
                f"accepted {self._alterations}"
            )

        if self.alteration in ["bb", "x"]:
            check = f"{self._get_major_interval()}{self.alteration}"
            if check.count("b") > 2 or check.replace("x", "##").count("#") > 2:
                raise ValueError(f"Invalid interval {check}")

    @classmethod
    def random(cls, root: str, exclude_alterations: bool = False):
        return cls(
            root,
            random.choices(cls._intervals)[0],
            (
                ""
                if exclude_alterations
                else random.choices(cls._alterations, weights=cls._alterations_weight)[
                    0
                ]
            ),
        )

    @property
    def root(self):
        return self._root

    @property
    def interval(self):
        return self._interval

    @property
    def alteration(self):
        return self._alteration

    def _get_major_interval(self):
        return MAJOR_SCALES[self.root][self.interval % 7 - 1]

    def __eq__(self, other) -> bool:
        return (
            self.interval == other.interval and self.alteration == other.alteration
            if other and isinstance(other, Interval)
            else False
        )

    def __repr__(self) -> str:
        return (
            f"{self._get_major_interval()}{self._alteration}".replace("##", "x")
            .replace("#b", "")
            .replace("b#", "")
            .replace("bx", "#")
            .replace("xb", "#")
        )


@dataclass(frozen=True)
class Answer:
    interval: Interval
    user_answer: str

    def is_correct(self):
        return str(self.interval) == self.user_answer.replace("##", "x")


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
        result = f"\nRESULT:\n{len(self.correct_answers)} correct answers\n\n"
        wrong_answers_recap = "\n".join(
            [
                f"question {answer.interval.interval}{answer.interval.alteration} th, "
                f"answer {answer.user_answer} but was {answer.interval}"
                for answer in self.wrong_answers
            ]
        )

        return (
            f"{result}Wrong answers:\n{wrong_answers_recap}"
            if self.wrong_answers
            else result
        )


class QuestionBuilder:
    def __init__(self, root: str, exclude_alterations: bool):
        self._exclude_alterations = exclude_alterations
        self._root = root

        self._question_stats = QuestionStats()
        self._already_seen: deque[Interval] = deque(maxlen=7)

    def build_question(self) -> Interval:
        for _ in range(50, 0, -1):
            try:
                interval = Interval.random(
                    self._root, exclude_alterations=self._exclude_alterations
                )
                if interval not in self._already_seen:
                    self._already_seen.append(interval)
                    return interval
            except ValueError as e:
                logger.debug(f"Error while generating question: {e}")
                pass

        raise ValueError("Error in building questions, too many attempt")

    def register_answer(self, answer: Answer) -> None:
        self._question_stats.register(answer)

    def stats(self) -> QuestionStats:
        return self._question_stats
