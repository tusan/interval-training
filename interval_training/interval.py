import logging
import random

from interval_training.lib import (
    MAJOR_SCALES,
    Answer,
    QuestionBuilder,
    Question,
    TrainingApp,
)

logger = logging.getLogger(__file__)


class Interval(Question):
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

    def prompt_msg(self) -> str:
        return f"{self.interval}{self.alteration} th"

    def _get_major_interval(self):
        return MAJOR_SCALES[self.root][self.interval % 7 - 1]

    def __eq__(self, other) -> bool:
        return (
            self.root == other.root
            and self.interval == other.interval
            and self.alteration == other.alteration
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


class IntervalAnswer(Answer):
    def __init__(self, interval: Interval, user_answer: str):
        self._interval = interval
        self._user_answer = user_answer

    def is_correct(self):
        return str(self._interval) == self._user_answer.replace("##", "x")

    def __repr__(self) -> str:
        return (
            f"question {self._interval.interval}{self._interval.alteration} th, "
            f"user answer {self._user_answer} - correct answer {self._interval}"
        )


class IntervalQuestionBuilder(QuestionBuilder):
    def __init__(self, root: str, exclude_alterations: bool):
        self._root = root
        self._exclude_alterations = exclude_alterations

    def build_question(self) -> Interval:
        return Interval.random(self._root, self._exclude_alterations)


class IntervalTrainingApp(TrainingApp):
    def __init__(self, question_size: int, tune: str, exclude_alterations: bool):
        super().__init__(question_size)
        self._root = tune
        self._exclude_alterations = exclude_alterations

        print(f"Tune {tune}")

    def _question_builder(self) -> QuestionBuilder:
        return IntervalQuestionBuilder(self._root, self._exclude_alterations)

    def _answer(self, question: Interval, answer: str) -> Answer:
        return IntervalAnswer(question, answer)
