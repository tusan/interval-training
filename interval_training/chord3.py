from interval_training.interval import Interval
from interval_training.lib import (
    QuestionBuilder,
    Answer,
    Question,
    TrainingApp,
    random_scale,
)


class Chord3(Question):
    def __init__(self, third: Interval, fifth: Interval):
        self._third = third
        self._fifth = fifth

    @classmethod
    def from_root(cls, root: str):
        return cls(Interval(root, 3), Interval(root, 5))

    @property
    def root(self) -> str:
        return self._third.root

    def prompt_msg(self) -> str:
        return f"{self.root} maj"

    def __repr__(self) -> str:
        return f"{self.root},{self._third},{self._fifth}"

    def __eq__(self, other) -> bool:
        return (
            self._third == other._third and self._fifth == other._fifth
            if other and isinstance(other, Chord3)
            else False
        )


class Chord3Answer(Answer):
    def __init__(self, chord3: Chord3, user_answer: str):
        self._chord3 = chord3
        self._user_answer = user_answer

    def is_correct(self):
        return str(self._chord3) == self._user_answer

    def __repr__(self) -> str:
        return f"question {self._chord3.root}, user answer {self._user_answer} correct answer {self._chord3}"


class Chord3QuestionBuilder(QuestionBuilder):
    def build_question(self) -> Chord3:
        return Chord3.from_root(random_scale())


class Chord3TrainingApp(TrainingApp):
    def _question_builder(self) -> QuestionBuilder:
        return Chord3QuestionBuilder()

    def _answer(self, question: Chord3, answer: str) -> Answer:
        return Chord3Answer(question, answer)
