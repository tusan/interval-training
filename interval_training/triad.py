from interval_training.interval import Interval
from interval_training.lib import (
    QuestionBuilder,
    Answer,
    Question,
    TrainingApp,
    random_scale,
)


class Triad(Question):
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
            if other and isinstance(other, Triad)
            else False
        )


class TriadAnswer(Answer):
    def __init__(self, triad: Triad, user_answer: str):
        self._triad = triad
        self._user_answer = user_answer

    def is_correct(self):
        return str(self._triad) == self._user_answer

    def __repr__(self) -> str:
        return f"question {self._triad.root}, user answer {self._user_answer} correct answer {self._triad}"


class TriadQuestionBuilder(QuestionBuilder):
    def build_question(self) -> Triad:
        return Triad.from_root(random_scale())


class TriadTrainingApp(TrainingApp):
    def _question_builder(self) -> QuestionBuilder:
        return TriadQuestionBuilder()

    def _answer(self, question: Triad, answer: str) -> Answer:
        return TriadAnswer(question, answer)
